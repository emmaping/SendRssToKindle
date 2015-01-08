#!usr/bin/Python
# -*- coding:utf-8 -*-
#transfer News feed to OEB
import os, sys, uuid

import calibre.startup
import calibre.utils.resources

from calibre.ebooks.conversion.mobioutput import MOBIOutput
from calibre.ebooks.conversion.epuboutput import EPUBOutput
from calibre.utils.bytestringio import byteStringIO

def MimeFromFilename(f):
    #Create MIME from file name
    f = f.lower()
    if f.endswith(('.gif','.png')):
        return r"image/"+f[-3:]
    elif f.endswith(('.jpg','.jpeg')):
        return r"image/jpeg"
    else:
        return ''

#传递给Mobi/epub模块的参数设置
class OptionValues(object):
    pass

class ServerContainer(object):
    def __init__(self, log=None):
        self.log = log
    def read(self, path):
        path = path.lower()
        #所有的图片文件都放在images目录下
        if path.endswith((".jpg",".png",".gif",".jpeg")) \
            and r'/' not in path:
            path = os.path.join("images", path)
        d,f  = '',None
        try:
            f = open(path, "rb")
            d = f.read()
        except Exception,e:
            self.log.warn("read file '%s' failed : %s" % (path,str(e)))
        finally:
            if f:
                f.close()
        return d
    def write(self, path):
        return None
    def exists(self, path):
        return False
    def namelist(self):
        return []

def CreateOeb(log, path_or_stream, opts, encoding='utf-8'):
    """ 创建一个空的OEB书籍 """
    from calibre.ebooks.conversion.preprocess import HTMLPreProcessor
    from calibre.ebooks.oeb.base import OEBBook
    html_preprocessor = HTMLPreProcessor(log, opts)
    if not encoding:
        encoding = None
    return OEBBook(log, html_preprocessor, pretty_print=opts.pretty_print, input_encoding=encoding)

def getOpts():
    from calibre.customize.profiles import KindleInput, KindleOutput
    REDUCE_IMAGE_TO = (600,800)
    opts = OptionValues()
    setattr(opts, "pretty_print", False)
    setattr(opts, "prefer_author_sort", True)
    setattr(opts, "share_not_sync", False)
    setattr(opts, "mobi_file_type", 'old')
    setattr(opts, "dont_compress", True)
    setattr(opts, "no_inline_toc", True)
    setattr(opts, "toc_title", "Table of Contents")
    setattr(opts, "mobi_toc_at_start", False)
    setattr(opts, "linearize_tables", True)
    setattr(opts, "source", None)
    setattr(opts, "dest", KindleOutput(None))
    setattr(opts, "output_profile", KindleOutput(None))
    setattr(opts, "mobi_ignore_margins", True)
    setattr(opts, "extract_to", None)
    setattr(opts, "change_justification", "Left")
    setattr(opts, "process_images", True)
    setattr(opts, "mobi_keep_original_images", False)
    setattr(opts, "graying_image", True)
    setattr(opts, "image_png_to_jpg", True)
    setattr(opts, "fix_indents", False)
    setattr(opts, "reduce_image_to", REDUCE_IMAGE_TO)
    
    #epub
    setattr(opts, "dont_split_on_page_breaks", False)
    setattr(opts, "flow_size", 260)
    setattr(opts, "no_default_epub_cover", True)
    setattr(opts, "no_svg_cover", True)
    setattr(opts, "preserve_cover_aspect_ratio", True)
    setattr(opts, "epub_flatten", False)
    setattr(opts, "epub_dont_compress", False)
    
    #extra
    setattr(opts, "process_images_immediately", True)
    
    return opts
    
def setMetaData(oeb, title='Feeds', lang='zh-cn', date=None, creator='KindleEmma',
    pubtype='periodical:magazine:KindleEmma'):
    oeb.metadata.add('language', lang if lang else 'zh-cn')
    oeb.metadata.add('creator', creator)
    oeb.metadata.add('title', title)
    oeb.metadata.add('identifier', str(uuid.uuid4()), id='uuid_id', scheme='uuid')
    oeb.uid = oeb.metadata.identifier[0]
    oeb.metadata.add("publication_type", pubtype)
    if not date:
        import datetime
        date = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")
    oeb.metadata.add("date", date)

