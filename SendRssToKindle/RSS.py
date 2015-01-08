from SendRssToKindle.models import *
import time, datetime, feedparser, calendar
from django.utils.timezone import utc

def verifyfeed(url):
    d = feedparser.parse(url)
    try:
        title = d['feed']['title']
    except KeyError:
        return False
    else:
        return title

def parsecontent(url, datetime=None, etag=None):
    if etag:
        d = feedparser.parse(url, etag=etag, modified=datetime)
    else:
        d = feedparser.parse(url)
        if d.status == 200:
            rss = RSSList.objects.get(url = url)
            for i in range(len(d.entries)):
                p = RSSContent(content = d.entries[i].content,
                    updatetime = datetime.datetime.utcfromtimestamp(calendar.timegm(d.entries[i].updated_parsed)).replace(tzinfo=utc),
                    RSS = rss,
                    title= d.entries[i].title)
                p.save()
            RSSList.objects.filter(url = url).update(updatetime = datetime.datetime.utcnow().replace(tzinfo=utc), etag = d.etag)
        
#Parse all feed's content and store it in DB
def parseallcontent( ):
    urllist = RSSList.objects.all().values('url','updatetime','etag')
    for url in urllist:
        if url['etag']:
            parsecontent(url['url'], url['etag'], (url['updatetime']).timetuple())
        else:
            parsecontent(url['url'])

if __name__ == '__main__':
    parseallcontent( )

#End       
    