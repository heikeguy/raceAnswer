"""responder_backgrounder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from main import views as main_views

urlpatterns = [
	url(r'^$', main_views.front, name='front'),                                         #前端主页
	url(r'^front_next/$', main_views.front_next, name='front_next'),                    #前端分页

    url(r'^comSerial_write/$', main_views.comSerial_write, name='comSerial_write'),     #串口处理分页
    url(r'^comSerial_read/$', main_views.comSerial_read, name='comSerial_read'),        #串口处理分页

    url(r'^background/$', main_views.background, name='background'),                    #后端主页
    url(r'^background_next/$', main_views.background_next, name='background_next'),     #后端分页
    url(r'^admin/', admin.site.urls),                                                   # no use        
]+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
