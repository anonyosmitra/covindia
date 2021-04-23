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
	resource = con.getTable("cities", ["name"], {"id": data["resource"]})[0]["name"]
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
	if len(positives)==0:
		positives=""
	else:
		positives="%s users found this helpful."%(positives[0]["sum(mark)"])
	return jsonify({"reply": {"auth": 1, "reply": {"exe":[{"method": "displayPost", "arg": {"id":data["id"],"html":render_template("postTemp.html",post=post,dId=data["dId"],verified=verified,positives=positives)}}]}}})


if __name__ == '__main__':
    app.secret_key = 'password'
    app.debug = True
    app.run(host='0.0.0.0',port=80,threaded=True)