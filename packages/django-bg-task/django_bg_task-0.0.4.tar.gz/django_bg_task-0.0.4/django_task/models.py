# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import JSONField
from drf_misc.core.models import AbstractModel

from .constants import TaskStatus


class Task(AbstractModel):
    id = models.CharField(unique=True, primary_key=True, max_length=36)
    identifiers = models.JSONField(null=True, blank=True)
    status = models.CharField(
        max_length=20, default=TaskStatus.PENDING, choices=TaskStatus.choices
    )
    args = JSONField(blank=True, null=True)
    kwargs = JSONField(blank=True, null=True)
    return_value = JSONField(blank=True, null=True)
    failed_reason = JSONField(blank=True, null=True)
    counter = models.IntegerField(default=1)
