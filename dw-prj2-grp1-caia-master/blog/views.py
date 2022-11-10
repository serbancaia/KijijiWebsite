from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

from database.models import Blog, Entry
from .forms import EntryModelForm

# Create your views here.

#DetailView showing a user's blog
class BlogView(generic.DetailView):
    model = Blog
    template_name = 'blog/blog.html'

#Function based view to add an entry to a user's blog
def AddEntryView(request, blog_id):
    #Only signed in users can add an entry
    if request.user.is_authenticated:
        blog = get_object_or_404(Blog, id=blog_id)
        form = EntryModelForm()

        if request.method == 'POST':
            form = EntryModelForm(request.POST)
            if form.is_valid():
                new_entry = Entry (
                    author = request.user.customer,
                    blog = blog,
                    entry_text= form.cleaned_data.get('entry_text')
                )
                new_entry.save()
                #Return to the blog that was commented on after it's done
                return HttpResponseRedirect(reverse('blog:blog', args=(blog_id,)))
    else:
        return redirect('../')

    #Return the form view if the request isn't a POST
    context = {'form': form}
    return render(request, 'blog/add_entry.html', context)
