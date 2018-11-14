from django.conf.urls import patterns, url, include
from rest_framework import routers

from contact.views import ContactViewSet, SearchContactViewSet

router = routers.SimpleRouter()
router.register(r'contact', ContactViewSet, base_name='contact')
router.register(r'search_contact', SearchContactViewSet, base_name='search_contact')

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       )
