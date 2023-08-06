# -*- coding: utf-8 -*-
import json

import celery

from .common import logger
from .constants import TaskStatus
from .models import Task
from .services import TaskService

# pylint: disable=no-member,import-error,too-many-arguments


class TaskHandler(celery.Task):
    def run(self, *args, **kwargs):
        pass

    def before_start(self, task_id, args, kwargs):
        logger.info(
            "Before started: %s with args: %s, kwargs: %s", task_id, args, kwargs
        )
        if not Task.objects.filter(id=task_id).exists():
            data = {
                "identifiers": kwargs.get("identifiers"),
                "id": task_id,
                "status": TaskStatus.RUNNING,
                "args": json.loads(json.dumps(args)),
                "kwargs": kwargs,
            }
            TaskService().create(data=data)

    def on_success(self, retval, task_id, args, kwargs):
        logger.info("On Success: %s with args: %s, kwargs: %s", task_id, args, kwargs)
        TaskService(task_id).update(
            {
                "status": TaskStatus.SUCCESS,
                "return_value": retval,
            }
        )

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info("On Failure: %s with args: %s, kwargs: %s", task_id, args, kwargs)
        TaskService(task_id).update(
            {
                "status": TaskStatus.FAILED,
                "failed_reason": str(exc),
            }
        )

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.info("On Retry: %s with args: %s, kwargs: %s", task_id, args, kwargs)
        task_instance = Task.objects.filter(id=task_id).first()
        TaskService(task_id).update(
            {
                "status": TaskStatus.RETRYING,
                "counter": task_instance.counter + 1,
            }
        )

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        logger.info("After return: %s with args: %s, kwargs: %s", task_id, args, kwargs)
