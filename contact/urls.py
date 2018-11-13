from django.conf.urls import patterns, url, include
from rest_framework import routers

from contact.views import ContactViewSet, search_particular_contact

router = routers.SimpleRouter()
router.register(r'contact', ContactViewSet, base_name='contact')

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       url(r'^search_contact/$', search_particular_contact),
                       )
