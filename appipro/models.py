# -*- coding: utf-8 -*-
"""This file
This program bank of api
"""

__author__ = 'Abdelaziz Sadquaoui'
__copyright__ = 'Copyright (c) 2020 AtlassRDV'
__version__ = '0.9'

from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.template.defaultfilters import slugify
from django.utils.text import slugify
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey


# Create your models here.

class Category(models.Model):
    """Category model.
    """
    #parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete='models.CASCADE')
    title = models.CharField(_('title'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('title',)

    def _occurences(self):
        object_list = []
        related_objects = self._meta.get_all_related_many_to_many_objects()
        for related in related_objects:
            if related.opts.installed:
                model = related.model
                for obj in model.objects.select_related().filter(categories__title=self.title):
                    object_list.append(obj)
        return object_list
    occurences = property(_occurences)

    def __unicode__(self):
        return u'%s' % self.title
    def __str__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return ("category_detail", (), {"slug": self.slug})


ROLE_CHOICES = (
        (1, 'Manager'),
        (2, 'Superviseur'),
        (3, 'Utilisateur'),
    )

class UProfile(models.Model):
    # User profile.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=5, null=True, choices=[(settings.LANGUAGES, settings.LANGUAGES)], default=settings.LANGUAGE_CODE, verbose_name=_("language"))
    timezone = models.CharField(max_length=20, null=True, choices=[(settings.TIME_ZONE, settings.TIME_ZONE)],  default=settings.TIME_ZONE, verbose_name=_("timezone"))
    # calendar = models.OneToOneField('calendar.Calendar', null=True, verbose_name=_("calendar"))
    date_naissance = models.DateField(verbose_name="Date de naissance", null=True, blank=True)
    photo = models.FileField(upload_to='documents/', null=True, blank=True)
    language = models.CharField(max_length=5, null=True, choices=[(1, settings.LANGUAGES)], default=settings.LANGUAGE_CODE, verbose_name=_("language"))
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=3)

    @property
    def full_name(self):
        if self.user.first_name :
            return u"{} {}".format(self.user.first_name, self.user.last_name)
        else :
            return u"{}".format(self.user.username)

    def __unicode__(self): # __unicode__ for Python 2
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def __str__(self): # __unicode__ for Python 2
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def get_language(self):
        return self.language

    def get_timezone(self):
        return self.timezone

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            UProfile.objects.create(user=instance)
        instance.uprofile.save()



class Member(User):
    """A project Member proxy.
    """
    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super(Member, self).__init__(*args, **kwargs)
        self._meta.get_field('is_active').verbose_name = _('active?')
        self._meta.get_field('is_staff').verbose_name = _('staff?')
        self._meta.get_field('is_superuser').verbose_name = _('admin?')

    def __unicode__(self):
        return "%s" % self.username


    def _full_name(self):
        return self.get_full_name()
    _full_name.short_description = _('full name')
    full_name = property(_full_name)

    def get_edit_url(self):
        return ('user_edit', (), {"username": self.username})

    def get_delete_url(self):
        return ('user_delete', (), {"username": self.username})


GENRES = (
        (1, 'Miss'),
        (2, 'Madame'),
        (3, 'Monsieur'),
    )
class StaffDirectory(models.Model):
    created     = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category    = models.ForeignKey('Category',  null=True, blank=True,
                                    verbose_name=_('categories'), related_name='mes_contacte',
                                    on_delete=models.CASCADE)

    title = models.CharField(max_length=10, null=True,
                    choices=GENRES, default=1, verbose_name=_("genre"))

    nom   = models.CharField(max_length=20)
    prenom  = models.CharField(max_length=20)
    adresse = models.CharField(max_length=100, null=True, blank=True,)
    codepostal = models.CharField(max_length=10, null=True, blank=True,)
    ville = models.CharField(max_length=50, null=True, blank=True,)
    pays = models.CharField(max_length=50, null=True, blank=True,)

    latitude = models.DecimalField(decimal_places=2,max_digits=8, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=2,max_digits=8,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True,)




class Todo(models.Model):
    """A todo list
    """
    content = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % self.content

    class Meta:
        verbose_name = _('Todo')
        ordering = ('-created',)
