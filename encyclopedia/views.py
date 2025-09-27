import random

from django import forms
from django.shortcuts import render
from markdown2 import Markdown
from . import util

# Create class forms with textarea
class NewTaskForm(forms.Form):
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)

# index function – list of clickable entries
# completed
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# entry function – displays the contents of the encyclopedia entry
# completed
def entry(request, title):

    # displays entry 
    if title in util.list_entries():
        # convert markdown to HTML
        markdowner = Markdown()
        html = markdowner.convert(util.get_entry(title))

        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": html
        })
    # error message when entry does not exist
    else:
        return render(request, "encyclopedia/errors.html", {
            "title": title
        })


# new function – creates a new encyclopedia entry
def new(request):
    # POST method – valid data and save entry
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["body"]
            util.save_entry(title.capitalize(), content)
            
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
        
    # GET method – render an empty form
    return render(request, "encyclopedia/new.html", {
        "form": NewTaskForm()
    })