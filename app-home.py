import json
import requests
from flask import Flask, render_template, request, jsonify, send_file
import dbHandler as dbh
import timezone as tz

import arraylizer as arr
import dbHandler as dbh
import os
import requests
import timezone as tz
import ssl,socket
application = app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
	if request.method == "GET":
		return(render_template("load.html"))
	else:
		dId=request.form['dId']
		con=dbh.Connect()
		print(dId)
		info=con.getTable("user", ["enabled"],{"id": dId})
		if dId=="" or len(info)==0:
			dId=con.insertIntoTable("user",{"ip":request.remote_addr,"enabled":1},returnId=True)
		else:
			if not info[0]["enabled"]:
				con.close()
				return("<h1>Forbidden</h1>",403)
		cities=con.getTable("cities",["id","name"],ext="order by name")
		resource= con.getTable("resource", ["id", "name"], ext="order by name")
		con.close()
		return (render_template("home.html",dId=dId,cities=cities,resource=resource))
@app.route('/search', methods=['POST'])
def search():
	data = request.json
	print(data)
	con=dbh.Connect()
	city=con.getTable("cities",["name"],{"id":data["city"]})[0]["name"]
	resource = con.getTable("resource", ["name"], {"id": data["resource"]})[0]["name"]
	posts=con.getTable("review,post,user",["post.id","post.time","phone","name"],where={"city":int(data["city"]),"resource":int(data["resource"]),"post.enabled":True,"user.enabled":True},join={"post.id":"post","post.user":"user.id"},ext="group by post order by sum(mark) DESC",columnNames=["id","time","phone","name"])
	print(posts)
	for i in posts:
		i["time"]=tz.convertTo(i["time"],"Asia/Kolkata",fmt="%-d %b, %-I:%M %p")
	return jsonify({"reply": {"auth": 1, "reply": {"html":render_template("searchRes.html",city=city,resource=resource,posts=posts)}}})

@app.route('/getPost', methods=['POST'])
def getPost():
	data = request.json
	con=dbh.Connect()
	post=con.getTable("post",["id","time","phone","info","name","user"],{"id":data["id"]})[0]
	post["time"] = tz.convertTo(post["time"], "Asia/Kolkata", fmt="%-d %b, %-I:%M %p")
	positives=con.getTable("review",["sum(mark)"],where=con.appendQuery("post=%0 and mark>-1",[data["id"]]))
	verified=con.getTable("review",["time"],where=con.appendQuery("post=%0 and mark>-1",[data["id"]]),ext="order by time DESC LIMIT 1")[0]["time"]
	verified=tz.convertTo(verified, "Asia/Kolkata", fmt="%-d %b, %-I:%M %p")
	post["info"]=post["info"].replace("\n","<br>")
	if len(positives)==0:
		positives=""
	else:
		positives="%s users found this helpful."%(positives[0]["sum(mark)"])
	return jsonify({"reply": {"auth": 1, "reply": {"exe":[{"method": "displayPost", "arg": {"id":data["id"],"html":render_template("postTemp.html",post=post,dId=data["dId"],verified=verified,positives=positives)}}]}}})
def isPhoneNo(num):
	if num[0]=="+":
		num=num[1:]
	return num.isnumeric()
def makePhoneN0(num):
	return("<a href='tel:%s' rel ='nofollow'>%s</a>"%(num,num))
def isLink(link):
	return "." in link
def makeLink(link):
	if "@" in link:
		return("<a href ='mailto:%s'>%s</a>"%(link,link))
	else:
		if link[:4]!="http":
			link="https://"+link
		return ("<a href='%s' target='_blank'>%s</a> "%(link,link))
def formatInfo(a):
	a=a.replace("\n"," <br> ")
	a=a.replace('\t'," ")
	info = a.replace(",", " ")
	info=" "+info
	info=info.split(" ")
	for i in info:
		if len(i)>0:
			if isPhoneNo(i):
				a=a.replace(" %s"%(i)," %s"%(makePhoneN0(i)))
			elif isLink(i):
				a=a.replace(" %s"%(i)," %s"%(makeLink(i)))
	return(a)
@app.route('/link', methods=['GET'])
def shared():
	data = request.args.to_dict()
	con=dbh.Connect()
	if "post" in data:
		post = con.getTable("post", ["id", "time", "phone", "info", "name", "user","city","resource"], {"id": data["post"]})[0]
		post["time"] = tz.convertTo(post["time"], "Asia/Kolkata", fmt="%-d %b, %-I:%M %p")
		positives = con.getTable("review", ["sum(mark)"], where=con.appendQuery("post=%0 and mark>-1", [data["post"]]))
		verified = con.getTable("review", ["time"], where=con.appendQuery("post=%0 and mark>-1", [data["post"]]), ext="order by time DESC LIMIT 1")[0]["time"]
		verified = tz.convertTo(verified, "Asia/Kolkata", fmt="%-d %b, %-I:%M %p")
		post["info"] = post["info"].replace("\n", "<br>")
		if len(positives) == 0:
			positives = ""
		else:
			positives = "%s users found this helpful." % (positives[0]["sum(mark)"])
		html=render_template("postTemp.html",post=post,dId=0,verified=verified,positives=positives)
		resource=con.getTable("resource",["name"],{"id":post["resource"]})
		city=con.getTable("cities",["name"],{"id":post["city"]})

	con.close()
@app.route('/getDid', methods=['POST'])
def getDid():
	dId = dbh.insertIntoTable("user", {"ip": request.remote_addr, "enabled": 1}, returnId=True)
	return jsonify({"reply": {"auth": 1, "reply": {"exe": [{"method": "setDid","arg":{"dId":dId}}]}}})
@app.route('/new', methods=['POST'])
def new():
	data = request.json
	if "data" in data:
		con=dbh.Connect()
		dId=con.getTable("user",["id","enabled"],{"id":data["dId"]})
		if len(dId)==0 or not dId[0]["enabled"]:
			con.close()
			return jsonify({"reply": {"auth": 1, "reply": {"html":"<h1>Forbidden</h1>"}}})
		else:
			formId=data["formId"]
			data=data["data"]
			if not isPhoneNo(data["phone"]):
				con.close()
				return jsonify({"reply": {"auth": 1, "reply": {"exe": [{"method": "displayError","arg":{"msg":"Invalid Phone No."}}]}}})
			data["city"]=data["city"].capitalize()
			data["resource"] = data["resource"].capitalize()
			if data["name"]=="":
				data["name"]="Unnamed"
			data["name"] = data["name"].capitalize()
			info=con.getTable("cities",["id"],{"name":data["city"]})
			if len(info)==1:
				data["city"]=info[0]["id"]
			else:
				data["city"] = con.insertIntoTable("cities",{"name":data["city"]},returnId=True)
			info = con.getTable("resource", ["id"], {"name": data["resource"]})
			if len(info) == 1:
				data["resource"] = info[0]["id"]
			else:
				data["resource"] = con.insertIntoTable("resource", {"name": data["resource"]}, returnId=True)
			data["user"]=dId[0]["id"]
			data["enabled"]=True
			info=con.getTable("forms",["id"],{"id":formId,"received":0})
			data["info"]=formatInfo(data["info"])
			if len(info)==1:
				postId=con.insertIntoTable("post",data,returnId=True)
				con.insertIntoTable("review",{"post":postId,"user":dId[0]["id"],"mark":0})
				con.updateTable("forms",{"received":1},{"id":formId})
			con.close()
			return (jsonify({"reply": {"auth": 1, "reply": {"html":"<h3>Resource Posted!<h3> <b>Thank you for your assistance.</b>"}}}))
	else:
		con=dbh.Connect()
		cities = con.getTable("cities", ["id", "name"], ext="order by name")
		resources = con.getTable("resource", ["id", "name"], ext="order by name")
		formId = con.insertIntoTable("forms",{"type":"newPost"},returnId=True)
		con.close()
		return(jsonify({"reply": {"auth": 1, "reply": {"html":render_template("new.html",cities=cities,resources=resources,formId=formId),"exe":[{"method": "focusOn", "arg": {"div": "new_city"}}]}}}))
@app.route('/vote', methods=['POST'])
def vote():
	data = request.json
	con = dbh.Connect()
	dId = con.getTable("user", ["id", "enabled"], {"id": data["dId"]})
	if len(dId) == 0 or not dId[0]["enabled"]:
		con.close()
		return jsonify({"reply": {"auth": 1, "reply": {"html": "<h1>Forbidden</h1>"}}})
	else:
		info=con.getTable("post",["user"],{"id":data["post"]})
		if len(info)==0:
			con.close()
			return (jsonify({"reply": {"auth": 1, "reply": {"html": "<h3>Vote Submitted!<h3> <b>Thank you for your assistance.</b>"}}}))
		else:
			if info[0]["user"]==dId[0]["id"]:
				return jsonify({"reply": {"auth": 1, "reply": {"exe": [{"method": "displayError", "arg": {"msg": "You can not vote on your own post"}}]}}})
			else:
				info=con.getTable("review",["id"],{"user":dId[0]["id"],"post":data["post"]})
				if len(info)==1:
					con.updateTable("review",{"mark":data["mark"]},{"id":info[0]["id"]})
				else:
					con.insertIntoTable("review",{"user":dId[0]["id"],"post":data["post"],"mark":data["mark"]})
				if data["mark"]==-1:
					info=con.getTable("review",["sum(mark)"],{"post":data["post"]},ext="group by post")[0]["sum(mark)"]
					if info==-3:
						con.updateTable("post",{"enabled":0},{"id":data["post"]})
				con.close()
				return (jsonify({"reply": {"auth": 1, "reply": {"html": "<h3>Vote Submitted!<h3> <b>Thank you for your assistance.</b>"}}}))
if __name__ == '__main__':
    app.secret_key = 'password'
    app.debug = True
    app.run(host='0.0.0.0',port=80,threaded=True)