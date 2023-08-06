# -*- coding: utf-8 -*-


class TaskStatus:
    SUCCESS = "success"
    PENDING = "pending"
    RUNNING = "running"
    FAILED = "failed"
    RETRYING = "retrying"

    choices = (
        (PENDING, "Pending"),
        (RUNNING, "Running"),
        (SUCCESS, "Success"),
        (FAILED, "Failed"),
        (RETRYING, "Retrying"),
    )
