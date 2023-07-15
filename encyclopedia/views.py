from django.shortcuts import render, redirect
import markdown2
from . import util
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    else:
        # Convert Markdown content to HTML
        html_content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title, "content": html_content
        })

def search(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()

    if query in entries:
        return redirect('encyclopedia:entry_page', title=query)
    else:
        search_results = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, 'encyclopedia/search.html', {
            'query': query, 'search_results': search_results
        })

def create_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        # Check if an entry with the same title already exists
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/create_page.html", {
                "error": "An entry with this title already exists.", "title": title, "content": content
            })
        # Save the new entry
        util.save_entry(title, content)

        # Redirect to the newly created entry page
        return redirect("encyclopedia:entry", title=title)
    else:
        return render(request, "encyclopedia/create_page.html")

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect("encyclopedia:entry", title=title)
    else:
        entry_content = util.get_entry(title)
        if entry_content is None:
            return render(request, "encyclopedia/error.html", {"title": title})
        else:
            return render(request, "encyclopedia/edit_page.html", {"title": title, "content": entry_content})

def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    return redirect("encyclopedia:entry", title=random_title)
