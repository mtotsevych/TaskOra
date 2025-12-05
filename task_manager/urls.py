from django.urls import path

from task_manager.views import (
    index,
    WorkerCreateView,
    WorkerDetailView,
    WorkerDeleteView,
    WorkerUpdateView,
    WorkerListView,
)

app_name = "task_manager"

urlpatterns = [
    path("", index, name="index"),
    path("register/", WorkerCreateView.as_view(), name="register"),
    path("profiles/", WorkerListView.as_view(), name="profile-list"),
    path("profile/<int:pk>/", WorkerDetailView.as_view(), name="profile-detail"),
    path("profile/<int:pk>/update/", WorkerUpdateView.as_view(), name="profile-update"),
    path("profile/<int:pk>/delete/", WorkerDeleteView.as_view(), name="profile-delete"),

]
