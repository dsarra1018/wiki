from django import forms
from django.shortcuts import render
from markdown import markdown
from . import util

# Create class forms with textarea
class NewTaskForm(forms.Form):
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)

# index function – homepage of the wiki
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# entry function – displays the contents of the encyclopedia entry
def entry(request, title):

    html = markdown(util.get_entry(title))
    print(html)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": html
    })


# new function – creates a new encyclopedia entry
def new(request):
    return render(request, "encyclopedia/new.html", {
        "form": NewTaskForm()
    })