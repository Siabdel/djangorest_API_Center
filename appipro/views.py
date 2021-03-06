# -*- coding: utf-8 -*-
"""This file
This program is appli todo for manage incidents and action
"""
import os, sys, time
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import  redirect as  redirect_to, render, reverse, redirect

from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView, BaseListView

from django.template import RequestContext
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import FormMixin

from  appipro.models import StaffDirectory
from  appipro import models as api_models
from  appipro.serializes import StaffDirectorySerializer, TodoSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.http import Http404
from rest_framework.views import APIView

from django import template
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your views here.

def import_json():
    ## lecture fichier data json
    #data = json.load(open("appipro/data/data.json"))
    #data = json.load(open("appipro/data/directory.json"))
    data = json.load(open("appipro/data/directories2.json"))

    # passe en data panda
    dd = data['results']

    cc = models.StaffDirectory.objects.all()
    #
    for elem in dd :
     print(elem )
     cc.create(user_id=1,
         category_id=2,
         title = elem['gender'],
         nom = elem['name']['last'],
         prenom = elem['name']['first'],
         adresse = str(elem['location']['street']['number']) + " " + elem['location']['street']['name'] ,
         ville = elem['location']['city'],
         codepostal = elem['location']['postcode'],
         pays = elem['location']['country'],
         latitude = elem['location']['coordinates']['latitude'],
         longitude = elem['location']['coordinates']['longitude'],
         email = elem['email'],
         telephone = elem['phone'],
         )



#@method_decorator(login_required, 'dispatch')
class DirectoryList(APIView):
    """
    List all StaffDirectorys, or create a new StaffDirectory
    """
    def get(self, request, format=None):
        directorys = StaffDirectory.objects.all()
        serializer = StaffDirectorySerializer(directorys, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StaffDirectorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, 'dispatch')
class MemberList(APIView):
    """
    List all members
    """
    def get(self, request, StaffDirectory_id, format=None):
        members = StaffDirectory.objects.get(pk=StaffDirectory_id).list_members()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#@method_decorator(login_required, 'dispatch')
class TodoList(APIView):
    """
    List all tasks todo
    """
    def get(self, request, format=None):
        todos = api_models.Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
