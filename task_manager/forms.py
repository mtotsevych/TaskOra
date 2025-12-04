from django import forms
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Worker


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position",
        )
