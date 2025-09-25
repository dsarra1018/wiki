from django.shortcuts import render
from markdown import markdown
from . import util

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
    return render(request, "encyclopedia/new.html")