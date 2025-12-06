from django.urls import path

from task_manager.views import (
    index,
    WorkerCreateView,
    WorkerListView,
    WorkerDetailView,
    WorkerUpdateView,
    WorkerDeleteView,
    TaskListView,
    complete_and_incomplete_task,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView
)

app_name = "task_manager"

urlpatterns = [
    path("", index, name="index"),
    path("register/", WorkerCreateView.as_view(), name="register"),
    path("profiles/", WorkerListView.as_view(), name="profile-list"),
    path("profile/<int:pk>/", WorkerDetailView.as_view(), name="profile-detail"),
    path("profile/<int:pk>/update/", WorkerUpdateView.as_view(), name="profile-update"),
    path("profile/<int:pk>/delete/", WorkerDeleteView.as_view(), name="profile-delete"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/complete-incomplete/", complete_and_incomplete_task, name="task-complete-incomplete"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
]
