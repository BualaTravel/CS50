from django.shortcuts import render
from markdown2 import Markdown
# import markdown
from . import util

from django.views.generic import ListView
from .models import Post



class BlogListView(ListView):
    model = Post
    template_name = 'post_list.html'

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title= None):
    if title not in util.list_entries():
        return render(request, "encyclopedia/error.html",{
            "title": title.upper(),
        })
    markdowner = Markdown()
    page = markdowner.convert(util.get_entry(title))
    # html = markdown.markdown(util.get_entry(title), output_format = "html5")
    # with open("encyclopedia/templates/encyclopedia/css_1.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
    #     output_file.write(html)
    # with open("encyclopedia/templates/encyclopedia/css_1.html", "r", encoding="utf-8") as input_file:
    #     text = input_file.read()
    return render(request, "encyclopedia/entry.html", {
        "page": page,
        "title": title,
    })
