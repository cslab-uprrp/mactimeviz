#!/usr/bin/python

import cgi
import cgitb
import datetime

cgitb.enable()  # for troubleshooting

print "Content-type: text/html"
print

# ----------------- Classes ----------------
class Universe:
	def __init__(self):
		self.type = "universe"
		self.name = "Universe"
		self.years = []

	def addYear(self, year):
		self.years.append(year)

	def createDataset(self):
		lables = '"'+ self.years[0].name + '"'
		data = str(self.years[0].counter)
		for i in range(1, len(self.years)):
			lables = lables + ', "'+self.years[i].name+'"'
			data = data + ', '+str(self.years[i].counter)

		dataset = """ data = {
		    labels: [""" + lables + """],
		    datasets: [
		        {
		            label: "Universe Dataset",
		            fillColor: "rgba(151,187,205,0.2)",
		            strokeColor: "rgba(151,187,205,1)",
		            pointColor: "rgba(151,187,205,1)",
		            pointStrokeColor: "#fff",
		            pointHighlightFill: "#fff",
		            pointHighlightStroke: "rgba(151,187,205,1)",
		            data: [""" + data + """]
		        }
		    ]
		};"""
		self.dataset = dataset

class Year:
	def __init__(self, name):
		self.counter = 0
		self.name = str(name)
		self.type = "year"
		self.months = []

	def countFiles(self):
		self.counter = 0
		for month in self.months:
			self.counter = month.counter + self.counter

	def addMonth(self, month):
		self.months.append(month)

	def createDataset(self):
		lables = '"'+ self.months[0].name + '"'
		data = str(self.months[0].counter)
		for i in range(1, len(self.months)):
			lables = lables + ', "'+self.months[i].name+'"'
			data = data + ', '+str(self.months[i].counter)

		dataset = """ data = {
		    labels: [""" + lables + """],
		    datasets: [
		        {
		            label: "Year Dataset",
		            fillColor: "rgba(151,187,205,0.2)",
		            strokeColor: "rgba(151,187,205,1)",
		            pointColor: "rgba(151,187,205,1)",
		            pointStrokeColor: "#fff",
		            pointHighlightFill: "#fff",
		            pointHighlightStroke: "rgba(151,187,205,1)",
		            data: [""" + data + """]
		        }
		    ]
		};"""
		self.dataset = dataset

class Month:
	def __init__(self, name):
		self.counter = 0
		self.name = str(name)
		self.type = "month"
		self.days = []

	def countFiles(self):
		self.counter = 0
		for day in self.days:
			self.counter = day.counter + self.counter

	def addDay(self, day):
		self.days.append(day)

	def createDataset(self):
		lables = '"'+ self.days[0].name + '"'
		data = str(self.days[0].counter)
		for i in range(1, len(self.days)):
			lables = lables + ', "'+self.days[i].name+'"'
			data = data + ', '+str(self.days[i].counter)

		dataset = """ data = {
		    labels: [""" + lables + """],
		    datasets: [
		        {
		            label: "Files Dataset",
		            fillColor: "rgba(151,187,205,0.2)",
		            strokeColor: "rgba(151,187,205,1)",
		            pointColor: "rgba(151,187,205,1)",
		            pointStrokeColor: "#fff",
		            pointHighlightFill: "#fff",
		            pointHighlightStroke: "rgba(151,187,205,1)",
		            data: [""" + data + """]
		        }
		    ]
		};"""
		self.dataset = dataset

class Day:
	def __init__(self, name):
		self.counter = 0
		self.name = str(name)
		self.type = "day"
		self.minutes = []

	def countFiles(self):
		self.counter = 0
		for time in self.minutes:
			self.counter = time.counter + self.counter

	def addInterval(self, minute):
		self.minutes.append(minute)

	def createDataset(self):
		lables = '"'+ self.minutes[0].name + '"'
		data = str(self.minutes[0].counter)
		for i in range(1, len(self.minutes)):
			if self.minutes[i].counter > 0:
				lables = lables + ', "'+self.minutes[i].name+'"'
				data = data + ', '+str(self.minutes[i].counter)

		dataset = """ data = {
		    labels: [""" + lables + """],
		    datasets: [
		        {
		            label: "Files Dataset",
		            fillColor: "rgba(151,187,205,0.2)",
		            strokeColor: "rgba(151,187,205,1)",
		            pointColor: "rgba(151,187,205,1)",
		            pointStrokeColor: "#fff",
		            pointHighlightFill: "#fff",
		            pointHighlightStroke: "rgba(151,187,205,1)",
		            data: [""" + data + """]
		        }
		    ]
		};"""
		self.dataset = dataset

class TimeInterval:
	def __init__(self, name):
		self.counter = 0
		self.name = name
		self.type = "time"
		self.files = []

	def addFile(self, file):
		self.files.append(file)
		self.counter = len(self.files)

# ----------------- End Classes ----------------

# ----------------- Fucntions ----------------
def getTime(currentL):
	less = currentL.split(',')
	date = less[0].replace(' ', ':')
	date = date.split(':')
	theTime = datetime.datetime(1,1,1,int(date[4]), int(date[5]), int(date[6]))
	return theTime

def getDate(currentL):
    less = currentL.split(',')
    date = less[0].replace(' ', ':')
    date = date.split(':')
    monthNum = date[1]
    if monthNum in monthDict:
    	monthNum = monthNum.replace(monthNum, monthDict[monthNum])
    date[1] = monthNum
    date = datetime.datetime(int(date[3]), int(date[1]), int(date[2]))
    return date

def createInterval(fileLine, currentT, maxT): 
	objTimef = TimeInterval(str(currentT.time())+"-"+str(maxT.time())) 
	objTimef.addFile(fileLine)
	return objTimef

def buildDataset(currentO):
	if currentO.type == "time":
		return
	else:
		if currentO.type == "universe":
			for year in currentO.years:
				buildDataset(year)
				year.createDataset()
			currentO.createDataset()
		elif currentO.type == "year":
			for month in currentO.months:
				buildDataset(month)
				month.createDataset()
		elif currentO.type == "month":
			for day in currentO.days:
				buildDataset(day)
				day.createDataset()
		elif currentO == "day":
			for time in currentO.minutes:
				buildDataset(time)

def printAll(currentO):
	if currentO.type == "time":
		for filee in currentO.files:
			print """<p>"""+ filee+"""</p>"""
	else:
		if currentO.type == "universe":
			for year in currentO.years:
				print """<p>"""+ year.name+"""</p>"""
				printAll(year)
		elif currentO.type == "year":
			for month in currentO.months:
				print """<p>"""+ month.name+"""</p>"""
				printAll(month)
		elif currentO.type == "month":
			for day in currentO.days:
				print """<p>"""+ day.name+"""</p>"""
				printAll(day)
		elif currentO.type == "day":
			for minute in currentO.minutes:
				print """<p>"""+ minute.name+"""</p>"""
				printAll(minute)

def getCurrentYear(yearTag, uni):
	if yearTag != 'empty':
		for year in uni.years:
			if year.name == yearTag:
				return year
	else:
		return uni

def getCurrentMonth(monthTag, theYear):
	if monthTag != 'empty':
		for month in theYear.months:
			if month.name == monthTag:
				return month
	else:
		return theYear

def getCurrentDay(dayTag, theMonth):
	if dayTag != 'empty':
		for day in theMonth.days:
			if day.name == dayTag:
				return day
	else:
		return theMonth

def getCurrentTime(timeTag, theDay):
	if timeTag != 'empty':
		for minute in theDay.minutes:
			if minute.name == timeTag:
				return minute
	else:
		return theDay

# ----------------- End Fucntions ----------------

# ----------------- Main ----------------

form = cgi.FieldStorage()

monthDict = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05",
			"Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10",
			"Nov": "11", "Dec": "12"}

dictMonth = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul",
			8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

yTag = form["yTag"].value
print yTag
mTag = form["mTag"].value
print mTag
dTag = form["dTag"].value
print dTag
tTag = form["tTag"].value
print tTag
universe = Universe()
interval = datetime.timedelta(0, 300) # 5 minutes
startTime = datetime.datetime(1,1,1,0,0,0)

theFile = open(form["fileName"].value, 'r')

if theFile:
    # It's an uploaded file; count lines
    line = theFile.readline()
    dateInfo = getDate(line)

    # The next few lines get the time of the line, set a time interval
    # and creates a timeInterval object and adds the file
    cTime = getTime(line)
    cDay = dateInfo.day
    cMonth = dateInfo.month
    cYear = dateInfo.year
    maxTime = startTime + interval
    minTime = startTime

    objDay = Day(str(cDay))

    while maxTime < datetime.datetime(1,1,2,0,0,1):
    	objTime = TimeInterval(str(minTime.time())+"-"+str(maxTime.time()))
    	if cTime.time() >= minTime.time() and cTime.time() <= maxTime.time():
    		objTime.addFile(line)
    	objDay.addInterval(objTime)
    	minTime = minTime + interval
    	maxTime = maxTime + interval
    	del objTime

    objMonth = Month(dictMonth[cMonth])
    objYear = Year(str(cYear))

    objMonth.addDay(objDay)
    objYear.addMonth(objMonth)
    universe.addYear(objYear)

    objDay.countFiles()
    objMonth.countFiles()
    objYear.countFiles()

    while 1:
    	line = theFile.readline()
    	if not line: break
    	dateInfo = getDate(line)
    	nYear = dateInfo.year
    	nMonth = dateInfo.month
    	nDay = dateInfo.day
    	nTime = getTime(line)

    	if nYear == cYear:
    		#print str(nYear) + " == " + objYear.name
    		if nMonth == cMonth:
    			#print dictMonth[nMonth]+ " == "+ objMonth.name
    			if nDay == cDay:
    				#print str(nDay) + " == " + objDay.name
    				for inter in objDay.minutes:
    					times = inter.name.split("-")
    					theMin = times[0].split(":")
    					theMax = times[1].split(":")
    					times0 = datetime.datetime(1,1,1,int(theMin[0]), int(theMin[1]), int(theMin[2]))
    					times1 = datetime.datetime(1,1,1,int(theMax[0]), int(theMax[1]), int(theMax[2]))
    					if nTime.time() >= times0.time() and nTime.time() <= times1.time():
    						#print line
    						inter.addFile(line)

    			else:
    				maxTime = startTime + interval
    				minTime = startTime
    				objDay = Day(str(nDay))
    				while maxTime.day == 1:
    					if cTime.time() >= minTime.time() and cTime.time() <= maxTime.time():
    						objTime = createInterval(line, minTime, maxTime)
    						objDay.addInterval(objTime)
    					else:
    						objTime = TimeInterval(str(minTime.time())+"-"+str(maxTime.time()))
    						objDay.addInterval(objTime)
    					minTime = minTime + interval
    					maxTime = maxTime + interval

    				objMonth.addDay(objDay)
    				cDay = nDay

    		else:
    			maxTime = startTime + interval
    			minTime = startTime
    			objDay = Day(str(nDay))
    			while maxTime.day == 1:
    				if cTime.time() >= minTime.time() and cTime.time() <= maxTime.time():
    					objTime = createInterval(line, minTime, maxTime)
    					objDay.addInterval(objTime)
    				else:
    					objTime = TimeInterval(str(minTime.time())+"-"+str(maxTime.time()))
    					objDay.addInterval(objTime)
    				minTime = minTime + interval
    				maxTime = maxTime + interval

	    		objMonth = Month(dictMonth[nMonth])
	    		objMonth.addDay(objDay)
	    		objYear.addMonth(objMonth)
	    		cDay = nDay
	    		cMonth = nMonth

    	else:
    		maxTime = startTime + interval
    		minTime = startTime
    		objDay = Day(str(nDay))
    		while maxTime.day == 1:
    			if cTime.time() >= minTime.time() and cTime.time() <= maxTime.time():
    				objTime = createInterval(line, minTime, maxTime)
    				objDay.addInterval(objTime)
    			else:
    				objTime = TimeInterval(str(minTime.time())+"-"+str(maxTime.time()))
    				objDay.addInterval(objTime)
    			minTime = minTime + interval
    			maxTime = maxTime + interval

    		objMonth = Month(dictMonth[nMonth])
    		objYear = Year(nYear)
    		objMonth.addDay(objDay)
    		objYear.addMonth(objMonth)
    		universe.addYear(objYear)
    		cDay = nDay
    		cMonth = nMonth
    		cYear = nYear

    	objDay.countFiles()
    	objMonth.countFiles()
    	objYear.countFiles()

    #printAll(universe)
    buildDataset(universe)

    currentOb = getCurrentYear(yTag, universe)
    currentOb = getCurrentMonth(mTag, currentOb)
    currentOb = getCurrentDay(dTag, currentOb)
    currentOb = getCurrentTime(tTag, currentOb)

    if currentOb.type == "time":
    	for minute in currentOb.files:
			print """<p>""",minute,"""</p>"""
    else:
    	print """<p>""",currentOb.name,"""</p>"""
    	print """<html>
		  <head>
		  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/1.0.2/Chart.js"></script>
		  </head>

		  <body>
		  	<div id = "roomForChart">

			    <script>
			    	htmlForGraph = "<canvas id='myChart' width ='500' height='400'>";
			    	holder = document.getElementById('roomForChart');
					holder.innerHTML += htmlForGraph;
			    	

			    var"""+currentOb.dataset+"""

					var ctx = document.getElementById("myChart").getContext("2d");
					var myLineChart = new Chart(ctx).Line(data);

					holder.onclick = function(evt){
		    			var activePoints = myLineChart.getPointsAtEvent(evt);
						if (activePoints[0].x != "undefined"){
							var form = document.createElement("form");
							var theName = document.createElement("input"); 
						    var yTag = document.createElement("input");
						    var mTag = document.createElement("input");
						    var dTag = document.createElement("input");
						    var tTag = document.createElement("input");

							form.method = "POST";
						    form.action = "dataMaker.cgi";

						    theName.value = "practiceFile.txt";
						   	theName.name = "fileName";

						   	if('"""+yTag+"""' == 'empty'){
						   		yTag.value = activePoints[0].label;
						    	mTag.value = 'empty';
						    	dTag.value = 'empty';
						    	tTag.value = 'empty';
						   	}
						   	else if('"""+mTag+"""' == 'empty'){
						   		yTag.value = '"""+yTag+"""';
						    	mTag.value = activePoints[0].label;
						    	dTag.value = 'empty';
						    	tTag.value = 'empty';
						   	}
						   	else if('"""+dTag+"""' == 'empty'){
						   		yTag.value = '"""+yTag+"""';
						    	mTag.value = '"""+mTag+"""';
						    	dTag.value = activePoints[0].label;
						    	tTag.value = 'empty';
						   	}
						   	else{
						   		yTag.value = '"""+yTag+"""';
						    	mTag.value = '"""+mTag+"""';
						    	dTag.value = '"""+dTag+"""';
						    	tTag.value = activePoints[0].label;
						   	}

						   	yTag.name = "yTag";
						   	mTag.name = "mTag";
						   	dTag.name = "dTag";
						   	tTag.name = "tTag";

						    form.appendChild(theName);
						    form.appendChild(yTag);
						    form.appendChild(mTag);
						    form.appendChild(dTag);
						    form.appendChild(tTag);

						    document.body.appendChild(form);

    						form.submit();

						}
					};

			    </script>
		    </div>
		  </body>

		</html>
	    """

else:
	print "Not a file."