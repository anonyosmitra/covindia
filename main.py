import dbHandler as dbh


def isPhoneNo(num):
	if num[0] == "+":
		num = num[1:]
	return len(num)>=6 and num.isnumeric()


def makePhoneN0(num):
	print("making number: %s" % (num))
	return ("<a href='tel:%s' rel ='nofollow'>%s</a>" % (num, num))


def isLink(link):
	return "." in link


def makeLink(link):
	print("making link: %s"%(link))
	if "@" in link:
		return ("<a href ='mailto:%s'>%s</a>" % (link, link))
	else:
		if link[:4] != "http":
			link = "https://" + link
		return ("<a href='%s' target='_blank'>%s</a> " % (link, link))
def fix():
	con=dbh.Connect()
	infos=con.getTable("post",["id","info"])
	for j in infos:
		j["info"]=j["info"].replace("\n"," <br> ")
		info=j["info"].split(" ")
		for i in info:
			if len(i)>0:
				if isPhoneNo(i):
					j["info"].replace(i, makePhoneN0(i))
				elif isLink(i):
					j["info"].replace(i, makeLink(i))
		con.updateTable("post",{"info":j["info"]},{"id":j["id"]})
	con.close()
fix()
