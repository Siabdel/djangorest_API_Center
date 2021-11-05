# -*- coding:utf-8 -*-
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from collections import OrderedDict
from appipro.models import Category, StaffDirectory
from appipro import models as models_api
from functools import wraps

from django.middleware.csrf import CsrfViewMiddleware, get_token
from django.utils.decorators import available_attrs, decorator_from_middleware

csrf_protect = decorator_from_middleware(CsrfViewMiddleware)
csrf_protect.__name__ = "csrf_protect"
csrf_protect.__doc__ = """
This decorator adds CSRF protection in exactly the same way as
CsrfViewMiddleware, but it can be used on a per view basis.  Using both, or
using the decorator multiple times, is harmless and efficient.
"""


class _EnsureCsrfToken(CsrfViewMiddleware):
    # We need this to behave just like the CsrfViewMiddleware, but not reject
    # requests or log warnings.
    def _reject(self, request, reason):
        return None


requires_csrf_token = decorator_from_middleware(_EnsureCsrfToken)
requires_csrf_token.__name__ = 'requires_csrf_token'
requires_csrf_token.__doc__ = """
Use this decorator on views that need a correct csrf_token available to
RequestContext, but without the CSRF protection that csrf_protect
enforces.
"""


class _EnsureCsrfCookie(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        retval = super(_EnsureCsrfCookie, self).process_view(request, callback, callback_args, callback_kwargs)
        # Forces process_response to send the cookie
        get_token(request)
        return retval


ensure_csrf_cookie = decorator_from_middleware(_EnsureCsrfCookie)
ensure_csrf_cookie.__name__ = 'ensure_csrf_cookie'
ensure_csrf_cookie.__doc__ = """
Use this decorator to ensure that a view sets a CSRF cookie, whether or not it
uses the csrf_token template tag, or the CsrfViewMiddleware is used.
"""

class AsymetricRelatedField(serializers.PrimaryKeyRelatedField):

    # en lecture, je veux l'objet complet, pas juste l'id
    def to_representation(self, value):
        # le self.serializer_class.serializer_class est redondant
        # mais obligatoire
        return self.serializer_class.serializer_class(value).data

    # petite astuce perso et pas obligatoire pour permettre de taper moins
    # de code: lui faire prendre le queryset du model du serializer
    # automatiquement. Je suis lazy
    def get_queryset(self):
        if self.queryset:
            return self.queryset
        return self.serializer_class.serializer_class.Meta.model.objects.all()

    # Get choices est utilisé par l'autodoc DRF et s'attend à ce que
    # to_representation() retourne un ID ce qui fait tout planter. On
    # réécrit le truc pour utiliser item.pk au lieu de to_representation()
    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])

    # DRF saute certaines validations quand il n'y a que l'id, et comme ce
    # n'est pas le cas ici, tout plante. On désactive ça.
    def use_pk_only_optimization(self):
        return False

    # Un petit constructeur pour générer le field depuis un serializer. lazy,
    # lazy, lazy...
    @classmethod
    def from_serializer(cls, serializer, name=None, args=(), kwargs={}):
        if name is None :
            name = "{}AsymetricAutoField".format(serializer.__class__.__name__)

        return type(name, (cls,), {"serializer_class": serializer})(*args, **kwargs)



class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = '__all__'




class StaffDirectorySerializer(serializers.ModelSerializer):
    class Meta :
        model = models_api.StaffDirectory
        fields = '__all__'


class TodoSerializer(serializers.ModelSerializer):
    class Meta :
        model = models_api.Todo
        fields = '__all__'
