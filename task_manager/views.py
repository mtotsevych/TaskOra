from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import WorkerCreationForm
from task_manager.models import Worker, Task


def index(request: HttpRequest) -> HttpResponse:
    num_of_workers = Worker.objects.filter(is_active=True).count()
    num_of_completed_tasks = Task.objects.filter(is_completed=True).count()
    num_of_not_completed_tasks = Task.objects.filter(is_completed=False).count()
    num_of_unassigned_tasks = Task.objects.filter(assignees__isnull=True).count()
    num_of_all_tasks = Task.objects.count()
    percentage_of_low_priority_tasks = round(
            Task.objects.filter(priority="Low").count() * 100 / num_of_all_tasks, 1
    )
    percentage_of_medium_priority_tasks = round(
            Task.objects.filter(priority="Medium").count() * 100 / num_of_all_tasks, 1
    )
    percentage_of_high_priority_tasks = round(
            Task.objects.filter(priority="High").count() * 100 / num_of_all_tasks, 1
    )
    percentage_of_urgent_priority_tasks = round(
            Task.objects.filter(priority="Urgent").count() * 100 / num_of_all_tasks, 1
    )

    worker_task_list = (
        Task.objects.filter(assignees__id=request.user.id)
        .select_related("task_type")
        .prefetch_related("tags")
    )
    if request.GET.get("completed") == "Yes":
        worker_task_list = worker_task_list.filter(is_completed=True)
    elif request.GET.get("completed") == "No":
        worker_task_list = worker_task_list.filter(is_completed=False)

    context = {
        "num_of_workers": num_of_workers,
        "num_of_completed_tasks": num_of_completed_tasks,
        "num_of_not_completed_tasks": num_of_not_completed_tasks,
        "num_of_unassigned_tasks": num_of_unassigned_tasks,
        "percentage_of_low_priority_tasks": percentage_of_low_priority_tasks,
        "percentage_of_medium_priority_tasks": percentage_of_medium_priority_tasks,
        "percentage_of_high_priority_tasks": percentage_of_high_priority_tasks,
        "percentage_of_urgent_priority_tasks": percentage_of_urgent_priority_tasks,
        "worker_task_list": worker_task_list,
    }
    return render(request, "task_manager/index.html", context=context)

class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "task_manager/register.html"
    success_url = reverse_lazy("task_manager:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
