"""ocrHtml URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]


from django.conf.urls import url

from aiapp.views import index as ocr_index, show as ocr_show, download as ocr_download
from phm.views import index as phm_index, show as phm_show

urlpatterns = [
    url('^index/', ocr_index),
    url('^show/(?P<task_id>.+)/', ocr_show),
    url('^download/(?P<task_id>.+)/', ocr_download),


    url('^phm_index/', phm_index),
    url('^phm_show/', phm_show),
]
