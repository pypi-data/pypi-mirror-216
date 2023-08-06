# -*- coding: utf-8 -*-
import time

from drf_misc.core.services import BaseService

from .models import Task
from .serializers import TaskSerializer


class TaskService(BaseService):
    serializer = TaskSerializer
    model = Task

    def create(self, data):
        data["created_at"] = int(time.time())
        return super().create(data, request=None)

    def update(self, data, partial=True):
        data["updated_at"] = int(time.time())
        return super().update(data, request=None, partial=partial)
