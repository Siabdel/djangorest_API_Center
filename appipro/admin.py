# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import csv
from django.contrib import admin
from appipro import models
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.management import get_permission_codename
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _
# from core.profile.models import  ProfileUser as Profile
from django.contrib.auth.admin import UserAdmin, User


# Register your models here.

# export des données en admin de toutes les table
# def make_planified(modeladmin, request, queryset):
def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response

def export_selected_objects(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    #return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
    return HttpResponseRedirect("/export/%s/%s" % (ct.pk, ",".join(selected)))

#-----------------
# Project
# ---------------
class CategoryAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in  models.Category._meta.get_fields()]
    # list_total.remove('stream')
    #list_display = list_total
    list_display = list_total



class  StaffDirectoryAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in  models.StaffDirectory._meta.get_fields()]
    list_display = list_total
    #autocomplete_lookup_fields = { 'Project_ProfileUser': [['project', 'member']], }

    search_fields = ['title'] # moteur de recherche
    #list_filter  = ('category', )
    # action supplementaires
    actions  = [ 'export_as_json',  'export_as_csv',  'make_closed']

    def export_as_json(modeladmin, request, queryset):
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json", queryset, stream=response)
        return response

    def export_as_csv(modeladmin, request, queryset):
        # Create the HttpResponse object with the appropriate CSV header.
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        #
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        # response['Content-Disposition'] = 'attachment; filename="%s"'% os.path.join('export', 'export_of.csv')
        writer = csv.writer(response)
        for obj in queryset:
            writer.writerow([
                smart_str(obj.pk),
                smart_str(obj.created),
                smart_str(obj.title),
            ])
        # return HttpResponseRedirect("/export/csv/%s/%s" % (ct.pk, ",".join(selected)))
        return response


    def export_json_selected_objects(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        #return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
        return HttpResponseRedirect("/export/json/%s/%s" % (ct.pk, ",".join(selected)))


    def export_selected_objects(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        #return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
        return HttpResponseRedirect("/export/%s/%s" % (ct.pk, ",".join(selected)))

    def export_csv_selected_objects(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        #return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
        return HttpResponseRedirect("/export/csv/%s/%s" % (ct.pk, ",".join(selected)))

    def make_planified(self, request, queryset):
        project_updater =  queryset.filter(status='C').update(statut='P')
        #pass
        if project_updater == 1:
            message = "project cloturé"
        else :
            message = "La cloture des projects est réussi "
        self.message_user(request, "%s " % message)




#-----------------
# Todos
# ---------------
class TodoAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in  models.Todo._meta.get_fields()]
    # list_total.remove('stream')
    #list_display = list_total
    list_display = list_total


admin.site.register(models.StaffDirectory,  StaffDirectoryAdmin)
admin.site.register(models.Category    , CategoryAdmin)
admin.site.register(models.UProfile)
admin.site.register(models.Todo, TodoAdmin)
