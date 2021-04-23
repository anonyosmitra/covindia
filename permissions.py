import socket
endpoint="localhost"
endpoint=socket.gethostbyname(endpoint)
user="worker"
port=3306
passwd="i2iSoftwares"
db="greenChecklist"
def read(session,table,where):
	resp={"session":session,"sessionValid":True,"Authorized":True,"msg":None}
	return(resp)
def insert(session,table,data):
	resp={"session":session,"sessionValid":True,"Authorized":True,"msg":None}
	return(resp)
def update(session,table,where,update):
	resp={"session":session,"sessionValid":True,"Authorized":True,"msg":None}
	return(resp)
def delete(session,table,where):
	resp={"session":session,"sessionValid":True,"Authorized":True,"msg":None}
	return resp