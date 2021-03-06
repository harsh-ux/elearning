from django.conf.urls import url,include
from . import views as user_views

urlpatterns = [
    url(r'^$', user_views.profile, name='profile'),
    url(r'^affiliate/$', user_views.affiliate, name='affiliate'),
    
    url(r'^student/$', user_views.student, name='student'),
    url(r'^professor/$', user_views.professor, name='professor'),
    url(r'^admin/', user_views.admin, name='admin'),
    url(r'^edit/(?P<username>[\w ]+)/$', user_views.update_user, name='update_user'),
    url(r'^delete/(?P<username>[\w ]+)/$', user_views.delete_user, name='delete_user'),
    url(r'^reg/(?P<parent>[\w ]+)/$', user_views.admin)
]
