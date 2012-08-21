import csv
import os, popen2
import sys


inputCSV=csv.reader(open(sys.argv[1],'rb'), skipinitialspace=True, dialect = "excel")
#outputCSV=csv.writer(open(sys.argv[2],'wb'), skipinitialspace=True, dialect = "excel")

def convertToSeconds(time,id):
    if len(time)==4:
        minutes=time[0:1]
        seconds=time[2:4]
        hours = "0"
    elif len(time)==5:
        hours = "0"
        seconds=time[3:5]
        minutes=time[0:2]
    elif len(time)==7:
        hours=time[0:1]
        minutes=time[2:4]
        seconds=time[5:7] 
    elif len(time)==8:
        hours=time[0:2]
        minutes=time[3:5]
        seconds=time[6:8]
    else:
        print "ERROR length strange encountered"
        print len(time)
        print id
        return

    try:
        fhours=float(hours)
    except:
        print "ERROR"
        print hours
        print id
        return 0

    try:
        fminutes=float(minutes)
    except:
        print "ERROR"
        print minutes
        print id
        return 0

    try:
        fseconds=float(seconds)
    except:
        print "ERROR"
        print seconds
        print id
        return 0

    converted=int(fhours*60*60+fminutes*60+fseconds)
    return str(converted)

def convertToTimestamp(value, id):
    list = value.split()

    if list[0][0:3] == 'jan':
        #print "found january"
        month = "01"
    elif list[0][0:3] == 'feb':
        #print "found feb"
        month = "02"
    elif list[0][0:3] == 'mar':
        #print "found mar"
        month = "03"
    elif list[0][0:3] == 'apr':
        #print "found apr"
        month = "04"
    elif list[0][0:3] == 'may':
        #print "found may"
        month = "05"
    elif list[0][0:3] == 'jun':
        #print "found jun"
        month = "06"
    elif list[0][0:3] == 'jul':
        #print "found jul"
        month = "07"
    elif list[0][0:3] == 'aug':
        #print "found aug"
        month = "08"
    elif list[0][0:3] == 'sep':
        #print "found sep"
        month = "09"
    elif list[0][0:3] == 'oct':
        #print "found oct"
        month = "10"
    elif list[0][0:3] == 'nov':
        #print "found nov"
        month = "11"
    elif list[0][0:3] == 'dec':
        #print "found dec"
        month = "12"
    else:
        print "found something else (ERROR)"
        print list[0][0:3]
        print id

    if len(list[1]) == 3 and (list[1][2:3] == "," or list[1][2:3] == "."):
        day = list[1][:-1]
        #print date
    elif len(list[1])==2 and (list[1][1:2] == "," or list [1][1:2] == "."):
        day = "0" + list[1][:-1]
        #print date
    elif len(list[1])==2: #no comma
        day = list[1]
    elif len(list[1])==1: #nocomam
        day = "0" + list[1]
    else:
        print "ERROR weird length date?"
        print list[1]
        print id        


    if len(list[2])==5:
        year = list[2][:-1]
    elif len(list[2])==4: #no time, assume morniing assign 6am time
        year = list[2]
        date = year + "-" + month + "-" +  day
        dateTime = date + " 06:00:00"
        return dateTime
    else:
        print "ERROR weird length year"
        print list[2]
        print id
        
    #finished the date part:
    date = year + "-" + month + "-" +  day
    
    #now for time
    try:
        list[4]
    except:
        if list[3] != 'noon':
            list.append('am')
            #print 'no am/pm, assumed morning'
            #print id

    #need to handle annoying "noons"
    if list[3] == 'noon':
        list[3] = '12'
        list.append('pm')
    
    if list[4] == 'n': #set noon to pm
        list[4] = 'pm'

    #weirdness
    if list[4] == 'a.m.' or list[4]=='a.m':
        list[4] ='am'

    if list[4] == 'p.m.' or list[4]=='p.m':
        list[4] = 'pm'

    if list[3] == '8:00/9:00':
        list[3] = "8:00"
    elif list[3] == '9:00/10:00':
        list[3] = '9:00'
    elif list[3] == '8/9:00':
        list[3] = "8:00"
    elif list[3] == '8:30/9:30':
        list[3] = "8:00"
    elif list[3] == '9:30/10:30':
        list[3] = '9:30'

    if list[3] == 'men:':
        list[3] = '8:30'
        list[4] = 'am'

    if list[4] == 'am':
        if list[3][0:2] == '12': #need to deal with 12am issues
            if len(list[3]) == 2:
                time = "00:00:00"
                #print time
            elif len(list[3])==5:
                time = "00" + str(list[3][2:])+":00"
                #print time
            else: 
                print "ERROR weird length of time"
                print list[3]
                print id
        else: #not 12
            if len(list[3]) == 1:
                time = "0"+str(list[3])+":00:00"
                #print time
            elif len(list[3]) == 2:
                time = str(list[3]) + ":00:00"
                #print time
            elif len(list[3])==4:
                time = "0" + str(list[3]) + ":00"
                #print time
            elif len(list[3])==5:
                time = str(list[3])+":00"
                #print time
            else: 
                print "ERROR weird length of time"
                print list[3]
                print id
    elif list[4] and list[4] == 'pm':
        if list[3][0:2] == '12': #don't change 
            if len(list[3]) == 2:
                time = str(list[3]) + ":00:00"
                #print time
            elif len(list[3])==5:
                time = str(list[3])+":00"
                #print time
            else: 
                print "ERROR weird length of time"
                print list[3]
                print id
        else: 
            if len(list[3]) == 1 or len(list[3])==2:
                #print list[3]
                hour = 12+int(list[3])
                time = str(hour) + ":00:00"
                #print time
            elif len(list[3])==4:
                hour = 12+int(list[3][0:1])
                time = str(hour) + str(list[3][1:]) + ":00"
                #print time
            elif len(list[3])==5:
                hour = 12+int(list[3][0:2])
                time = str(hour) + str(list[3][2:])+":00"
                #print time
            else: 
                print "ERROR weird length of time"
                print list[3]
                print id    
    else:
        print "ERROR other am/pm?"
        print list[4]
        print id
    
    dateTime = date + " " + time
    #print dateTime

    return dateTime

def convertPercent(value, id):
    length = len(value)
    if value[length-2:length] == ' %':
        return value[:-2]
    elif value[length-1:length]=='%':
        return value[:-1]
    elif len(value) == 0:
        return value
    else:
        print "ERROR weird character at end of humidity"
        print value[length-1:length]
        print value
        print id

def convertRaceName(value,id):
    #some race names have &amp;
    length = len(value)
    if length == 0:
        return value

    newval = ""
    if u'&amp;' in value:
        i = 0
        while i < len(value):
            if value[i:i+1] != '&':
                newval = newval + value[i:i+1]
            else:
                newval = newval + "and"
                i = i + 4 
            i = i + 1
    else:
        newval = value

    return value


fields=inputCSV.next()
id = 0
for row in inputCSV:
    row2 = ""
    header =""
    items = zip(fields,row)
    item = {}
    id = 1+id
    flag= 1
    for (name, value) in items:
        header = header + str(name) + ","
        item[name]=value.strip()
        #convert stuff
        #if name == 'netTime':
        if name == 'netTime':
            if len(value)!=0:
                value = convertToSeconds(value,id)
            else:
                flag = 0
        if name == 'AGTime' and len(value)!=0:
            value = convertToSeconds(value,id)
        if name == 'pacePerMile' and len(value)!=0:
            value = convertToSeconds(value,id)
            ppm = float(value)
        if name == 'date':
            value = convertToTimestamp(value,id)
        if name == 'AGPercent' or name == 'PerfPercent':
            value = convertPercent(value,id)
        if name == 'distMiles':
            dist = float(value)

        if name =='team' or name == 'lastName' or name == 'firstName' or name == 'raceName' or name == 'location' or name == 'city' or name == 'state' or name == 'country':
            row2 = row2 + "\"" + str(value) + "\","
        else:
            row2 = row2 + str(value) + ","

        if name =='raceName':
            value = convertRaceName(value,id)
   
    if (flag == 0): #no total time get from ppm
        for(name,value) in items:
            if name == 'netTime':
                #print id
                #print "converted from ", value
                #print "ppm ", ppm
                #print "dist ", dist
                value = int(ppm*dist)
                #print value

    if id == 1:
        print header[:-1]
    
    print row2[:-1]

    
