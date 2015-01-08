from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from  django.shortcuts  import  render_to_response, RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from SendRssToKindle.models import *
from SendRssToKindle.forms import UserForm
from SendRssToKindle.RSS import verifyfeed

# Create your views here.
def profile(request):
    if request.user.is_authenticated():
        user = KindleUser.objects.get(user = request.user)
        if request.method == 'POST':
            rsstobedelete = request.POST.getlist('checkedrss')            
            for rsstbd in rsstobedelete:
                user.rsslist_set.get(url = rsstbd).delete()
                
        #get all subscribed RSS lists by the User

        rtk = user.rsslist_set.all().values    
        #rtk = RssToKindle.objects.filter(user = request.user).values('Rssset',flat=True)
    return render_to_response('profile.html', {'subscribedrsses': rtk,}, RequestContext(request))



@csrf_exempt    
def settings(request):
    if request.user.is_authenticated():
        user = KindleUser.objects.get(user=request.user)
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user.kindleemail = cd['kindleemail']
                user.scheduletime = cd['scheduletime']
                user.save()
                return HttpResponseRedirect('/profile/')
        else:
            form = UserForm(
                initial={'username': user.user.username,
                         'kindleemail':user.kindleemail,
                         'scheduletime':user.scheduletime,}
            )
    else:
        return HttpResponseRedirect("/login/", RequestContext(request)) 
    return render_to_response('settings.html', {'form': form},context_instance=RequestContext(request))

def addfeeds(request):
    if request.user.is_authenticated():
        messages = []
        currentuser = KindleUser.objects.get(user=request.user)
        if request.method == 'POST':
            newtitle = request.POST.get('title')
            newurl = request.POST.get('url')
            if verifyfeed(newurl):
                    
                try:
                    #Check if URL in rsslist already
                    rl = currentuser.rsslist_set.get(url = newurl,title = newtitle)
                    
                except RSSList.DoesNotExist:
                    try:
                        rl = RSSList.objects.get(url = newurl,title = newtitle)
                    except RSSList.DoesNotExist:  
                        rl = RSSList.objects.create(url = newurl ,title = newtitle)
                        rl.user.add(currentuser)
                    else:
                        rl.user.add(currentuser)
                    
                    messages.append("Success to add feed , please add continually")
                else:
                    messages.append("This feed already in your subscribe list")
            else:
                messages.append("This URL is not valid")

    return render_to_response('addfeeds.html', {'messages':messages,},context_instance=RequestContext(request))



