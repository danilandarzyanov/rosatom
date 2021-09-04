from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.apps import apps
from django.http import JsonResponse
from django.forms import ModelForm, ModelChoiceField
import json
from .tasks import *
from .models import *


class IndexView(View):
    template = 'index.html'
    context = {'query': Query.objects.all()}
    def get(self, requests):
        return render(requests, self.template, self.context)


class UpdateRTSView(View):
    template = 'index.html'
    context = {'query': Query.objects.all()}
    Query.objects.get_from_rts()

    def get(self, requests):
        return render(requests, self.template, self.context)


class Step0View(View):
    template = 'step0.html'
    context = {'query': Query.objects.all()}

    def get(self, requests):
        return render(requests, self.template, self.context)


class Step1View(View):
    template = 'step1.html'
    context = {'query': Query.objects.all()}

    def get(self, requests):
        return render(requests, self.template, self.context)

class Step2View(View):
    template = 'step2.html'
    context = {'query': Query.objects.all()}

    def get(self, requests):
        return render(requests, self.template, self.context)

class Step3View(View):
    template = 'step3.html'
    context = {'query': Query.objects.all()}

    def get(self, requests):
        return render(requests, self.template, self.context)
