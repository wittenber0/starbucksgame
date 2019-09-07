import urllib2
import json
import datetime
import threading
import os


#REQUEST DETAILS
url = 'https://www.starbuckssummergame.com/api/game/11e9cfeaa7b11cd095d325ae508ca846/prizes'
cookie= '__utma=188328938.878183557.1567694176.1567694176.1567694176.1; __utmb=188328938; __utmc=188328938; __utmz=188328938.1567694176.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none); __utmz_FT=utmcsr=(direct)|utmcmd=(none)|utmccn=|utmctr=|utmcct=; _fbp=fb.1.1567694176880.1663583260; _ga=GA1.2.878183557.1567694176; _gid=GA1.2.1402003165.1567694177; __utmv=188328938.r%3D1%3Bc%3Ddef%3Bd%3Ddef%3Ba%3D; viewedCookieDisclaimer=true; @rocd/starbucks_summer19_mystery=1; @rocd/starbucks_summer19_rainbow_game=1; @rocd/starbucks_summer19_floatie_game=1; _gat_mpgaTracker1=1; _gat_mpgaTracker2=1'
dnt=1
token= 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1Njc2OTQyMzUsImV4cCI6MTU3MDgwNDYzNSwiYXVkIjoiQHJvY2Qvc3RhcmJ1Y2tzX3N1bW1lcjE5IiwiaXNzIjoiQHJvY2Qvc3RhcmJ1Y2tzX3N1bW1lcjE5Iiwic3ViIjoiMTFlOWNmZWFhN2IxMWNkMDk1ZDMyNWFlNTA4Y2E4NDYifQ.w16PORt7JUFJlYhCMPXAuI0ZvbFovLYPyF6WKq29GG8'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.172 Safari/537.36 Vivaldi/2.5.1525.48'
headers = {'cookie' : cookie,'dnt' : dnt,'x-hw-profile-token': token, 'User-Agent': user_agent}

#RESPONSE PARSING
tier3US = 'collect_tier3_US'
starBig = '8f8340d6-548c-11e9-88aa-ef67360373e4'
tier4US = 'collect_tier4_US'
starMedium = '8f4cdaa0-548c-11e9-88aa-ef67360373e4'
tier5US = 'collect_tier5_US'
starSmall = '8efa5a14-548c-11e9-88aa-ef67360373e4'

#METRICS
PrizeCounts = {'tier3' : {'count':0, 'last':'2019-09-07 12:01:56.655216'}, 'tier4' : {'count':0, 'last':'2019-09-07 12:01:56.655216'}, 'tier5' : {'count':0, 'last':'2019-09-07 12:01:56.655216'}}
t3Factor = 1769
t4Factor = 1060
t5Factor = 150


#LOGGING
countFileName = 'starbuckscounts.json'
logFileName = 'log.txt'

def main():
    threading.Timer(10.0, main).start()
    run()
    printStatus()

def run():
    logRun(checkAndUpdateCounts(getPrizeCounts()))

def printStatus():
    n = datetime.datetime.now()
    os.system('clear')
    print("STARBUCKS GAME PRIZE TRACKER\n\n")
    print("Tier 3:\t%d\t\tTime since last win:\t%s\t\tRatio of average win:\t%f" % (gpc(3)[0], str(n-gpc(3)[1]), (n-gpc(3)[1]).total_seconds()/t3Factor))
    print("Tier 4:\t%d\t\tTime since last win:\t%s\t\tRatio of average win:\t%f" % (gpc(4)[0], str(n-gpc(4)[1]), (n-gpc(4)[1]).total_seconds()/t4Factor))
    print("Tier 5:\t%d\t\tTime since last win:\t%s\t\tRatio of average win:\t%f" % (gpc(5)[0], str(n-gpc(5)[1]), (n-gpc(5)[1]).total_seconds()/t5Factor))

def loadCounts():
    countfile = open(countFileName)
    counts = json.load(countfile)
    countfile.close()
    return counts

def dumpCounts():
    countfile = open(countFileName, 'w')
    json.dump(PrizeCounts, countfile, default=str)
    countfile.close()

def logRun(params):
    dirty = params[0]
    t = params[1]

    if dirty:
        s = str(t)+'\t2500 Stars:'+str(gpc(3)[0])+'\t1000 Stars:'+str(gpc(4)[0])+'\t500 Stars:'+str(gpc(5)[0])+'\n'
        f = open(logFileName, 'a')
        f.write(s)
        f.close()

def getPrizeCounts():
    req = urllib2.Request(url=url, headers=headers)
    res = urllib2.urlopen(req)
    data = json.load(res)['result']['prizeCounts']
    t = datetime.datetime.now()

    return [int(data[tier3US][starBig]), int(data[tier4US][starMedium]), int(data[tier5US][starSmall]), t]

def logTime(fname, time):
    f = open(fname, 'a')
    l = str(time) + "\n"
    f.write(l)
    f.close()

def checkAndUpdateCounts(countList):
    dirty = False

    if countList[0] > gpc(3)[0]:
        dirty = True
        upc(3, countList[0], countList[3])
        logTime("t3.txt", countList[3])

    if countList[1] > gpc(4)[0]:
        dirty = True
        upc(4, countList[1], countList[3])
        logTime("t4.txt", countList[3])

    if countList[2] > gpc(5)[0]:
        dirty = True
        upc(5, countList[2], countList[3])
        logTime("t5.txt", countList[3])

    if dirty:
        dumpCounts()

    return [dirty, countList[3]]

#update PrizeCounts
def upc(tier, count, last):
    if count != None:
        PrizeCounts['tier'+str(tier)]['count'] = int(count)

    if last != None:
        PrizeCounts['tier'+str(tier)]['last'] = str(last)

#get PrizeCounts
def gpc(tier):
    return [int(PrizeCounts['tier'+str(tier)]['count']), datetime.datetime.strptime(PrizeCounts['tier'+str(tier)]['last'], '%Y-%m-%d %H:%M:%S.%f')]

PrizeCounts = loadCounts()
main()
