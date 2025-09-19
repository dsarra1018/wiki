from django.shortcuts import render
import markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):

    #convert markdown file to html file


    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": util.get_entry(title)
    })