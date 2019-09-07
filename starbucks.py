import urllib2
import json
import datetime
import threading

url = 'https://www.starbuckssummergame.com/api/game/11e9cfeaa7b11cd095d325ae508ca846/prizes'

cookie= '__utma=188328938.878183557.1567694176.1567694176.1567694176.1; __utmb=188328938; __utmc=188328938; __utmz=188328938.1567694176.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none); __utmz_FT=utmcsr=(direct)|utmcmd=(none)|utmccn=|utmctr=|utmcct=; _fbp=fb.1.1567694176880.1663583260; _ga=GA1.2.878183557.1567694176; _gid=GA1.2.1402003165.1567694177; __utmv=188328938.r%3D1%3Bc%3Ddef%3Bd%3Ddef%3Ba%3D; viewedCookieDisclaimer=true; @rocd/starbucks_summer19_mystery=1; @rocd/starbucks_summer19_rainbow_game=1; @rocd/starbucks_summer19_floatie_game=1; _gat_mpgaTracker1=1; _gat_mpgaTracker2=1'
dnt=1
token= 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1Njc2OTQyMzUsImV4cCI6MTU3MDgwNDYzNSwiYXVkIjoiQHJvY2Qvc3RhcmJ1Y2tzX3N1bW1lcjE5IiwiaXNzIjoiQHJvY2Qvc3RhcmJ1Y2tzX3N1bW1lcjE5Iiwic3ViIjoiMTFlOWNmZWFhN2IxMWNkMDk1ZDMyNWFlNTA4Y2E4NDYifQ.w16PORt7JUFJlYhCMPXAuI0ZvbFovLYPyF6WKq29GG8'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.172 Safari/537.36 Vivaldi/2.5.1525.48'

headers = {'cookie' : cookie,'dnt' : dnt,'x-hw-profile-token': token, 'User-Agent': user_agent}

tier3US = 'collect_tier3_US'
starBig = '8f8340d6-548c-11e9-88aa-ef67360373e4'

tier4US = 'collect_tier4_US'
starMedium = '8f4cdaa0-548c-11e9-88aa-ef67360373e4'

tier5US = 'collect_tier5_US'
starSmall = '8efa5a14-548c-11e9-88aa-ef67360373e4'

PrizeCounts = {'tier3' : 0, 'tier4' : 0, 'tier5' : 0}

countFileName = 'starbuckscounts.json'

def main():
    threading.Timer(60.0, main).start()
    run()

def run():
    printCounts(checkAndUpdateCounts(getPrizeCounts()))

def loadCounts():
    countfile = open(countFileName)
    counts = json.load(countfile)
    PrizeCounts['tier3'] = counts['tier3']
    PrizeCounts['tier4'] = counts['tier4']
    PrizeCounts['tier5'] = counts['tier5']

def dumpCounts():
    countfile = open(countFileName, 'w')
    json.dump(PrizeCounts, countfile)
    countfile.close()

def printCounts(dirty):
    if dirty:
        print('2500 Stars:%d\t1000 Stars:%d\t500 Stars:%d' % (int(PrizeCounts['tier3']), int(PrizeCounts['tier4']), int(PrizeCounts['tier5'])))
    else:
        print("ran at %s" % (str(datetime.datetime.now())))

def getPrizeCounts():
    req = urllib2.Request(url=url, headers=headers)
    res = urllib2.urlopen(req)
    data = json.load(res)['result']['prizeCounts']

    return [data[tier3US][starBig], data[tier4US][starMedium], data[tier5US][starSmall]]

def saveTime(fname):
    f = open(fname, 'a')
    l = str(datetime.datetime.now()) + "\n"
    f.write(l)
    f.close()

def checkAndUpdateCounts(countList):
    dirty = False

    if int(countList[0]) > int(PrizeCounts['tier3']):
        dirty = True
        PrizeCounts['tier3'] = countList[0]
        saveTime("t3.txt")
        print 'Tier 3 has been updated'

    if int(countList[1]) > int(PrizeCounts['tier4']):
        dirty = True
        PrizeCounts['tier4'] = countList[1]
        saveTime("t4.txt")
        print 'Tier 4 has been updated'

    if int(countList[2]) > int(PrizeCounts['tier5']):
        dirty = True
        PrizeCounts['tier5'] = countList[2]
        saveTime("t5.txt")
        print 'Tier 5 has been updated'

    if dirty:
        dumpCounts()

    return dirty


loadCounts()
main()
