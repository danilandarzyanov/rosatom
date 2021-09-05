from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('update_rts', UpdateRTSView.as_view(), name='update_rts'),
    path('update_sbis', UpdateOrgSBISView.as_view(), name='update_sbis'),
    path('suppliers/<int:pk>', SuppliersView.as_view(), name='suppliers'),
    path('suppliers_detail/<int:pk>', SuppliersDetailView.as_view(), name='suppliers_detail'),
    path('send_email/<int:id_query>/<int:id_org>', SendEmailView.as_view(), name='send_email'),
    path('org_list', OrgView.as_view(), name='org_list'),
    path('404', Error404.as_view(), name='404'),
    path('step0/<int:pk>', Step0View.as_view(), name='step0'),
    path('step1/<int:pk>', Step1View.as_view(), name='step1'),
    path('step2/<int:pk>', Step2View.as_view(), name='step2'),
    path('step3/<int:pk>', Step3View.as_view(), name='step3'),
    path('print', PrintView.as_view(), name='print'),
]
