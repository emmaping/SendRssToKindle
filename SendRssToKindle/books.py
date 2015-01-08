import makeoeb
import time
from collections import OrderedDict, defaultdict
from calibre.ebooks.conversion.mobioutput import MOBIOutput
from calibre.ebooks.conversion.epuboutput import EPUBOutput
from calibre.utils.bytestringio import byteStringIO
from SendRssToKindle.models import *

def GenerateMobi(request):
    if request.user.is_authenticated():
        messages = []
        kindleuser = KindleUser.objects.get(user=request.user)
        global log    
        opts = oeb = None
        
        # 创建 OEB

        opts = makeoeb.getOpts()
        oeb = makeoeb.CreateOeb(log, None, opts)
        title = "%s %s" % ("KindleEmma", time.time()) 
        
        makeoeb.setMetaData(oeb, title, )
        oeb.container = makeoeb.ServerContainer(log)
                
        itemcnt,imgindex = 0,0
        sections = OrderedDict()
        rsslists = kindleuser.rsslist_set.all() 
        lasttime = kindleuser.lastupdatetime
        for rss in rsslists:
                   
            rss.RSSContent_set.all()
            # 对于html文件，变量名字自文档
            # 对于图片文件，section为图片mime,url为原始链接,title为文件名,content为二进制内容
            for  title, content  in book.Items(opts,user):
                if not sec_or_media or not title or not content:
                    continue
                
                if sec_or_media.startswith(r'image/'):
                    id, href = oeb.manifest.generate(id='img', href=title)
                    item = oeb.manifest.add(id, href, sec_or_media, data=content)
                    imgindex += 1
                else:
                    id, href = oeb.manifest.generate(id='feed', href='feed%d.html'%itemcnt)
                    item = oeb.manifest.add(id, href, 'application/xhtml+xml', data=content)
                    oeb.spine.add(item, True)
                    sections.setdefault(sec_or_media, [])
                    sections[sec_or_media].append((title, item, brief))
                    itemcnt += 1
                    
        if itemcnt > 0: # 建立TOC，杂志模式需要为两层目录结构
            stoc = ['<html><head><title>Table Of Contents</title></head><body><h2>Table Of Contents</h2>']
            for sec in sections.keys():
                stoc.append('<h3><a href="%s">%s</a></h3>'%(sections[sec][0][1].href,sec))
                sectoc = oeb.toc.add(sec, sections[sec][0][1].href)
                for title, a, brief in sections[sec]:
                    stoc.append('&nbsp;&nbsp;&nbsp;&nbsp;<a href="%s">%s</a><br />'%(a.href,title))
                    sectoc.add(title, a.href, description=brief if brief else None)
            stoc.append('</body></html>')
            id, href = oeb.manifest.generate(id='toc', href='toc.html')
            item = oeb.manifest.add(id, href, 'application/xhtml+xml', data=''.join(stoc))
            oeb.guide.add('toc', 'Table of Contents', href)
            oeb.spine.add(item, True)
            
#            oIO = byteStringIO()
            oIO = "c:\\temp.mobi"
            o = MOBIOutput()
            o.convert(oeb, oIO, opts, log)


