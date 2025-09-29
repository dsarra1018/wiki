import random

from django import forms
from django.shortcuts import render, redirect
from markdown2 import Markdown
from . import util

# Create form for new entries with a charfield for title and textarea for the content
class NewTaskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'style':'width: 1000px'
        }))
    body = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'style':'width: 1000px'
    }))

# Create form for updating entries with a textarea for the content
class EditTaskForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'style':'width: 1000px'
    }))

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
        return render(request, "encyclopedia/entry.html", {
            "title": "Does not exist",
            "entry": None,
            "message": f"The requested page was not found. Entry for '{title}' currently does not exist."
        })


# new function – creates a new encyclopedia entry
def new(request):
    # POST method – valid data and save entry
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["body"]

            # check if entry exist for title
            titles = [entry.lower() for entry in util.list_entries()]
            if title.lower() in titles:
                return render(request, "encyclopedia/new.html", {
                    "error": f"An entry for '{title}' already exists."
                })

            # save entry and renders entry page
            util.save_entry(title.capitalize(), content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": content
            })
            
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
        
    # GET method – render an empty form
    return render(request, "encyclopedia/new.html", {
        "form": NewTaskForm()
    })


# edit function - edits existing page
def edit(request, title):

    # load existing content
    content = util.get_entry(title)

    # POST method - save edited entry
    if request.method == "POST":
        form = EditTaskForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data["body"]
            util.save_entry(title, body)
            return redirect("entry", title=title)
        
    # pre-populate textarea
    else:
        form = EditTaskForm(initial={"body":content})
    
    # GET method - render edit form
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": form
    })


# random function – display a random entry from the list of available entries
# completed
def random_page(request):

    # generate random page
    entry = random.choice(util.list_entries())

    # convert markdown to html
    markdowner = Markdown()
    html = markdowner.convert(util.get_entry(entry))

    # display random page from the list
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "entry": html 
    })


# search function - search for an entry
def search(request):

    # GET q value
    query = (request.GET.get("q") or "").strip()
    
    # Empty search redirects to index
    if not query:
        return redirect("index")
    
    # get list of entries
    entries = util.list_entries()

    # Exact match (case-insensitive)
    for title in entries:
        if title.lower() == query.lower():
            return redirect("entry", title=title)
    
    # Substring matches (case-insensitive)
    results = [title for title in entries if query.lower() in title.lower()]

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })