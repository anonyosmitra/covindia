import dbHandler as dbh


def isPhoneNo(num):
	if num[0] == "+":
		num = num[1:]
	return len(num)>=6 and num.isnumeric()


def makePhoneN0(num):
	print("making number: %s" % (num))
	return ("<a href='tel:%s' rel ='nofollow'>%s</a>" % (num, num))


def isLink(link):
	return "." in link and link[-1:]!="."

def formatInfo(a):
	a=a.replace("\n"," <br> ")
	a=a.replace('\t'," ")
	info = a.replace(",", " ")
	info=info.split(" ")
	for i in info:
		if len(i)>0:
			if isPhoneNo(i):
				a=a.replace(" %s"%(i)," %s"%(makePhoneN0(i)))
			elif isLink(i):
				a=a.replace(" %s"%(i)," %s"%(makeLink(i)))
	return(a)

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
		info=formatInfo(j["info"])
		if info!=j["info"]:
			con.updateTable("post",{"info":info},{"id":j["id"]})
	con.close()
fix()