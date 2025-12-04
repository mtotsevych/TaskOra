from django.urls import path

from task_manager.views import WorkerCreateView, index

app_name = "task_manager"

urlpatterns = [
    path("", index, name="index"),
    path("register/", WorkerCreateView.as_view(), name="register"),
]
