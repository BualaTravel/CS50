from django.shortcuts import render
from markdown2 import Markdown
# import markdown
from . import util
from django import forms
from django.views.generic import ListView
from .models import Post

class NewGetForm(forms.Form):
    search = forms.CharField(label = "New Search")

class BlogListView(ListView):
    model = Post
    template_name = 'post_list.html'

def index(request):

    # if request.method == "GET":
    #     form = NewGetForm(request.GET)
    #     if form.is_valid():
    #         search = form.cleaned_data["search"]
    #         request.session["search"] = [search]
    #         return HttpResponseRedirect(reverse("encyclopedia:search"))
    #     else:
    #         return render(request, "encyclopedia/index.html", {
    #             "search": form  # instead of returning a new form, we return the form the server received
    #         })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def search(title):
    title = title.replace('q=', '').lower()
    entries = list(map(str.lower, util.list_entries()))
    if title in entries:
        print('ENTERING MATCHING')
        matching_idx = entries.index(title)
        return (matching_idx, True)
    matching_idx = [idx for idx, name in enumerate(entries) if title in name]
    print(f'INSIDE MATCHING {matching_idx}')
    return (matching_idx, False)

def entry(request, title= None):

    if title == 'search':
        print(f'SEARCH SECTION: {request.META["QUERY_STRING"] }')
        matching_idx, match_bool = search(request.META["QUERY_STRING"])
        list_entries = util.list_entries()
        if not match_bool:
            return render(request, "encyclopedia/search.html",{
                "searches": list(map(lambda x: list_entries[x], matching_idx)),
                "title": title,
            })
        else:
            title =  list_entries[matching_idx]
    elif title not in util.list_entries():
        print('NOT IN SEARCH')
        return render(request, "encyclopedia/error.html",{
            "title": title,
        })
    print(f'OUTSIDE OF SEARCH {title}')
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
