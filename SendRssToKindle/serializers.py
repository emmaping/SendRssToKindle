from django.contrib.auth.models import User, Group
from rest_framework import serializers
from SendRssToKindle.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username','password', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
        
class KindleUserSerializer(serializers.HyperlinkedModelSerializer):
    kindleemail = serializers.SerializerMethodField('get_kindleemail')
    scheduletime = serializers.SerializerMethodField('get_scheduletime')
    lastupdatetime = serializers.SerializerMethodField('get_lastupdatetime')
    class Meta:
        model = User
        fields = ('url', 'username','password', 'email', 'kindleemail','scheduletime','lastupdatetime')
    
    def get_kindleemail(self,obj):
        return KindleUser.objects.get(user = obj).kindleemail
    
    def get_scheduletime(self,obj):
        return KindleUser.objects.get(user = obj).scheduletime
    
    def get_lastupdatetime(self,obj):
        return KindleUser.objects.get(user = obj).lastupdatetime
    
class RSSListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RSSList
        fields = ('url', 'title')