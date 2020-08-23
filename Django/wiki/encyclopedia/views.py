from django.shortcuts import render
from markdown2 import Markdown
# import markdown
from . import util
from django import forms
from django.views.generic import ListView
from .models import Post

from django.core.files import File
from django.conf import settings


class NewCreateForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

class NewEditForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

class BlogListView(ListView):
    model = Post
    template_name = 'post_list.html'

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def search(title):
    title = title.replace('q=', '').lower()
    entries = list(map(str.lower, util.list_entries()))
    if title in entries:
        print('ENTERING EXACT MATCHING')
        matching_idx = entries.index(title)
        return (matching_idx, True)
    matching_idx = [idx for idx, name in enumerate(entries) if title in name]
    print(f'INSIDE MATCHING {matching_idx}')
    return (matching_idx, False)

def entry(request, title= None):

    if title == 'search':
        print(f'SEARCH SECTION: {request.META["QUERY_STRING"] }')
        matching_idx, match_exact = search(request.META["QUERY_STRING"])
        list_entries = util.list_entries()
        if not match_exact:
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

def create(request):
    if request.method == 'POST':
        print('INSIDE CREATE POST')
        form = NewCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            matching_idx, match_exact = search(title)
            if match_exact:
                print('DO EXIST')
                return render(request, "encyclopedia/create.html", {
                    "form": form,  # instead of returning a new form, we return the form the server received
                    "title":title,
                    "entry_error": match_exact,
                })
            # request.session["title"] = [title]
            else:
                print(f'NOT EXIST {settings.MEDIA_ROOT} title: {title}')
                page = form.cleaned_data["text"]
                # print(f'NOT EXIST {page} {os.path.exist(encyclopedia/entries/{title}.md)}')
                with open(f'entries/{title}.md', 'w') as output_file:
                    myfile = File(output_file)
                    myfile.write(page)
                markdowner = Markdown()
                page = markdowner.convert(util.get_entry(title))
                # return HttpResponseRedirect(f"'encyclopedia:entry' {title}")
                return render(request, "encyclopedia/entry.html", {
                    "page": page,
                    "title": title,
                })
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form,  # instead of returning a new form, we return the form the server received
            })
    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewCreateForm  # instead of returning a new form, we return the form the server received
        })

def edit(request, title=None):
    print('INSIDE EDIT POST')
    form = NewEditForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            text = form.cleaned_data["text"]
            # request.session["title"] = [title]

            with open(f'entries/{title}.md', 'w') as output_file:
                myfile = File(output_file)
                myfile.write(text)
            # return HttpResponseRedirect(f"'encyclopedia:entry' {title}")
            markdowner = Markdown()
            page = markdowner.convert(util.get_entry(title))
            return render(request, "encyclopedia/entry.html", {
                "page": page,
                "title": title,
            })
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form,  # instead of returning a new form, we return the form the server received
            })
    else:
        with open(f'entries/{title}.md', 'r') as f:
            myfile = File(f)
            text = myfile.read()
        form = NewEditForm(initial={'text': text})
        print(f'GET ENTRY FORM.TEXT {form}')

        return render(request, "encyclopedia/edit.html", {
            "form": form,  # instead of returning a new form, we return the form the server received
            "title": title,
        })
