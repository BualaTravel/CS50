from django import forms # Now an alternative an easier way to deal with Forms thanks to django
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# tasks = []

class NewTaskForm(forms.Form): #a new class that represents the Form that inherit from forms.Form
    task = forms.CharField(label = "New Task")   #inside of this class, I will define all of the fields I'd like for this form to have, all of the inputs that I would like the user to provide
    # in this case I'd like the user to provide characters as the task
    priority = forms.IntegerField(label="Priority", min_value=1, max_value=10)
# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []

    return render (request, "tasks/index.html", {
        # "tasks": tasks
        "tasks": request.session["tasks"]
    })
def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            #tasks.append(task)
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form  # instead of returning a new form, we return the form the server received
            })
    return render(request, "tasks/add.html", {
        "form":NewTaskForm()
    })
