def addSep(st,sep):
	if st[len(st)-1]!=sep:
		st=st+sep
	return(st)
def rmSep(st,sep):
	if st[len(st)-1]==sep:
		st=st[0:len(st)-1]
	return(st)
def countSep(st,sep):
	st=addSep(st,sep)
	i=0
	for a in st:
		if a==sep:
			i=i+1
	return(i)
def dearraylize(lt,sep):
	a=''
	for i in lt:
		a=a+i+sep
	return(rmSep(a,sep))
def arraylize(st,sep):
	st=addSep(st,sep)
	a=[]
	b=''
	for i in st:
		if i==sep:
			a=a+[b]
			b=''
		else:
			b=b+i
	return(a)
def doubleArr(st,sep1,sep2):
	a=arraylize(st,sep1)
	j=0
	for i in a:
		a[j]=arraylize(i,sep2)
		j=j+1
	return(a)
def doubleDearr(lt,sep1,sep2):
	j=0
	for i in lt:
		lt[j]=dearraylize(i,sep2)
		j=j+1
	return(dearraylize(lt,sep1))
def dictOfArr(arr,var,val):
	dc={}
	for i in arr:
		dc[i[var]]=i[val]
	return(dc)
def arrFromDict(dc,var):
	arr=[]
	for i in dc:
		arr+=[i[var]]
	return(arr)