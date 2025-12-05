from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import WorkerCreationForm, WorkerSearchForm
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


class WorkerListView(generic.ListView):
    model = Worker
    template_name = "task_manager/profile_list.html"

    def get_queryset(self):
        queryset = Worker.objects.select_related("position")
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = WorkerSearchForm(self.request.GET)
        context["form"] = form
        return context


class WorkerDetailView(generic.DetailView):
    model = Worker
    template_name = "task_manager/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("completed") == "Yes":
            context["tasks"] = self.object.tasks.filter(is_completed=True)
        elif self.request.GET.get("completed") == "No":
            context["tasks"] = self.object.tasks.filter(is_completed=False)
        else:
            context["tasks"] = self.object.tasks.all()
        return context


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "task_manager/register.html"
    success_url = reverse_lazy("task_manager:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class WorkerUpdateView(generic.UpdateView):
    model = Worker
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "bio",
        "position",
    )
    template_name = "task_manager/profile_update.html"


class WorkerDeleteView(generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("login")
    template_name = "task_manager/profile_confirm_delete.html"
