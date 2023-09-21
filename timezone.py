from datetime import datetime
import datetime as dt
import pytz
defaultFmt = "%Y-%m-%d %H:%M:%S %Z%z"
tzList = pytz.all_timezones
timezones ={'London':'UTC','Los Angeles':'US/Pacific','Berlin':'Europe/Berlin','New Delhi':'Asia/Kolkata'}
def convertTo(time,zone=None,fmt=defaultFmt,place=None,SysTZ="UTC"):
		if zone==None:
				zone=timezones[place]
		if type(zone)==str:
			zone=pytz.timezone(zone)
			time = time.replace(tzinfo=pytz.timezone(SysTZ)).astimezone(zone)
		else:
			time = time.replace(tzinfo=pytz.timezone(SysTZ)).astimezone(zone)
		if fmt==None:
			return(time)
		else:
			time = zone.normalize(time).strftime(fmt)
			return time
def searchTZ(keyword=None):
		tzs=pytz.all_timezones
		if keyword==None:
			return tzs
		else:
			r=[]
			for i in tzs:
				if keyword in i:
					r+=[i]
			return r
def timeIn(zone,fmt=defaultFmt,SysTZ="UTC"):
		zone=pytz.timezone(zone)
		time=datetime.now()
		time = time.replace(tzinfo=pytz.timezone(SysTZ)).astimezone(zone)
		if fmt==None:
			return time
		time = zone.normalize(time).strftime(fmt)
		return time
def WeekName(date=None,zone="UTC"):
	if date==None:
		date=timeIn(zone,None)
	fday=date
	lday=date
	while (fday.weekday()>0):
		fday=fday-dt.timedelta(days=1)
	while (lday.weekday()<6):
		lday=lday+dt.timedelta(days=1)
	return("%s - %s"%(fday.strftime('%d %B %y'),lday.strftime('%d %B %y')))
