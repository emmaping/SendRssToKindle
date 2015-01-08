from django.db import models
from django.contrib.auth.models import User

class KindleUser(models.Model):
    user = models.OneToOneField(User)
    kindleemail = models.EmailField()
    scheduletime = models.TimeField()
    lastupdatetime = models.DateTimeField(null=True)
    def __unicode__(self):
        return self.user.username
    
    
class RSSList(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=100)
    user = models.ManyToManyField(KindleUser,blank=True, null=True)
    updatetime = models.DateTimeField(blank=True, null=True)
    etag = models.CharField(max_length=30,blank=True, null=True)
    
    def __unicode__(self):
        #return self.title
        return self.title

class RSSContent(models.Model):
    content = models.TextField()
    updatetime = models.DateTimeField()
    RSS = models.ForeignKey(RSSList, related_name='RSSList')
    title= models.CharField(max_length=100)
    def __unicode__(self):
        #return self.title
        return u'%s %s' % (self.title, self.RSS.url)


