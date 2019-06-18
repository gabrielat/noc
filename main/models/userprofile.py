# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# UserProfile model
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
import datetime
# Third-party modules
import six
from django.db import models
# NOC modules
from noc import settings
from noc.aaa.models.user import User
from noc.core.middleware.tls import get_user
from noc.core.model.decorator import on_delete_check


class UserProfileManager(models.Manager):
    """
    @todo: remove
    User Profile Manager
    Leave only current user's profile
    """
    def get_queryset(self):
        s = super(UserProfileManager, self)
        user = get_user()
        if user:
            # Create profile when necessary
            try:
                s.get_queryset().get(user=user)
            except UserProfile.DoesNotExist:
                UserProfile(user=user).save()
            return s.get_queryset().filter(user=user)
        else:
            return s.get_queryset()


@on_delete_check(check=[
    ("main.UserProfileContact", "user_profile")
])
@six.python_2_unicode_compatible
class UserProfile(models.Model):
    """
    User profile
    """
    class Meta(object):
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        app_label = "main"
        db_table = "main_userprofile"

    user = models.ForeignKey(User, unique=True)
    # User data
    preferred_language = models.CharField(
        "Preferred Language",
        max_length=16,
        null=True, blank=True,
        default=settings.LANGUAGE_CODE,
        choices=settings.LANGUAGES)
    # Heatmap position
    heatmap_lon = models.FloatField("Longitude", blank=True, null=True)
    heatmap_lat = models.FloatField("Latitude", blank=True, null=True)
    heatmap_zoom = models.IntegerField("Zoom", blank=True, null=True)

    objects = UserProfileManager()

    def __str__(self):
        return "%s's Profile" % self.user.username

    def save(self, **kwargs):
        user = get_user()
        if user and self.user != user:
            raise Exception("Invalid user")
        super(UserProfile, self).save(**kwargs)

    @property
    def contacts(self):
        from .userprofilecontact import UserProfileContact

        return [
            (c.time_pattern, c.notification_method, c.params)
            for c in UserProfileContact.objects.filter(user_profile=self)]

    @property
    def active_contacts(self):
        """
        Get list of currently active contacts

        :returns: List of (method, params)
        """
        now = datetime.datetime.now()
        return [
            (c.notification_method, c.params)
            for c in self.contacts if c.time_pattern.match(now)]
