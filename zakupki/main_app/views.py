from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from .models import *
from datetime import datetime

class IndexView(ListView):
    template_name = 'index.html'
    paginate_by = 4
    model = Query
    context = {'query': Query.objects.all()}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org_count'] = len(Organization.objects.all())
        return context

class OrgView(ListView):
    template_name = 'org_list.html'
    paginate_by = 5
    model = Organization


class UpdateRTSView(View):
    template = 'index.html'
    context = {'object_list': Query.objects.all(),
               'org_count': len(Organization.objects.all())}
    Query.objects.get_from_rts()

    def get(self, requests):
        return render(requests, self.template, self.context)


class UpdateOrgSBISView(View):
    template = 'org_list.html'
    context = {'object_list': Organization.objects.all()}
    Organization.objects.get_from_sbis()
    def get(self, requests):
        return render(requests, self.template, self.context)


class SendEmailView(View):
    template = 'send_email.html'

    def get(self, requests, id_query, id_org ):
        query = Query.objects.get(pk=id_query)
        supplier = Organization.objects.get(pk=id_org)
        qs = QuerySupplier(supplier = supplier, query = query)
        qs.save()
        return render(requests, self.template, {"qs": qs})


class Step0View(View):
    template = 'step0.html'

    def get(self, requests, pk):
        qs = QuerySupplier.objects.get(pk=pk)
        return render(requests, self.template, {'qs':qs})


class Step1View(View):
    template = 'step1.html'

    def get(self, requests, pk):
        qs = QuerySupplier.objects.get(pk=pk)
        return render(requests, self.template, {'qs':qs})

class Step2View(View):
    template = 'step2.html'

    def get(self, requests, pk):
        qs = QuerySupplier.objects.get(pk=pk)
        return render(requests, self.template, {'qs':qs})

class Step3View(View):
    template = 'step3.html'

    def get(self, requests, pk):
        qs = QuerySupplier.objects.get(pk=pk)
        return render(requests, self.template, {'qs':qs})

class PrintView(View):
    template = 'print.html'

    def post(self, requests):
        qs = QuerySupplier.objects.get(pk=requests.POST.get('qs'))
        qRecords = qs.query.query_nomenclature.all()
        records = []
        for i, rec in enumerate(qRecords):
            print(requests.POST)
            print(requests.POST.get('price'+str(i)))
            records.append({
                'nomenclature': rec.nomenclature,
                'ie': rec.ei,
                'count': rec.count,
                'price': requests.POST.get('price'+str(i)),
            })
        return render(requests, self.template, {'qs':qs,
                                                'price': records,
                                                'date_end': requests.POST.get('date_end'),
                                                'ext': requests.POST.get('ext'),
                                                'today': datetime.now(),
                                                })


class SuppliersView(View):
    template='suppliers.html'

    def get(self, requests, pk):
        query = Query.objects.get(pk=pk)
        return render(requests, self.template, {'query': query})

class SuppliersDetailView(View):
    template='suppliers_detail.html'

    def get(self, requests, pk):
        supplier = Organization.objects.get(pk=pk)
        return render(requests, self.template, {'supplier': supplier})

class Error404(View):
    template='404.html'

    def get(self, requests):
        return render(requests, self.template, {})
