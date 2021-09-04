from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('update_rts', UpdateRTSView.as_view(), name='update_rts'),
    path('step0', Step0View.as_view(), name='step0'),
    path('step1', Step1View.as_view(), name='step1'),
    path('step2', Step2View.as_view(), name='step2'),
    path('step3', Step3View.as_view(), name='step3'),
]
