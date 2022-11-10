from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
)

from datetime import datetime
from .forms import ItemModelForm, CommentModelForm
from django.db.models import Q
from database.models import Item, user_directory_path, Comment, CustomerVote


def itemCreateView(request):
    """
    View used to create an item
    """
    if request.user.is_authenticated == False:
        # Redirect to login if user is not authenticated
        return redirect('accounts:login')
    else:
        # Create empty form
        form = ItemModelForm()
        # POST request
        if request.method == 'POST':
            form = ItemModelForm(request.POST, request.FILES)
            if form.is_valid():
                # Saving item to database
                new_item = Item(
                    owner=request.user.customer,
                    price=form.cleaned_data.get('price'),
                    item_name=form.cleaned_data.get('item_name'),
                    description=form.cleaned_data.get('description'),
                    image=form.cleaned_data.get('image'),
                )
                new_item.save()

    # Returning to form if it was invalid
    context = {'form': form}
    return render(request, 'item_management/item_create.html', context)


def itemUpdateView(request, **kwargs):
    """
    View used to update an item
    """
    if request.user.is_authenticated == False:
        # Redirect to login if user is not authenticated
        return redirect('accounts:login')
    else:
        # Retrieving item, can throw 404 if object doens't belong to customer
        item = get_object_or_404(Item, id=kwargs.get(
            "id"), owner=request.user.customer)
        form = ItemModelForm(instance=item)
        # POST request
        if request.method == 'POST':
            form = ItemModelForm(request.POST, request.FILES, instance=item)
            if form.is_valid():
                # Updating item
                form.save()

                # Updating image if a new one was provided and it's not the old one
                new_image = form.cleaned_data.get('new_image'),
                if new_image is not None and new_image[0] != item.image:
                    item.image = new_image[0]
                    item.save()

    # Returning to form if it was invalid
    context = {'form': form}
    return render(request, 'item_management/item_update.html', context)


class ItemDeleteView(DeleteView):
    """
    View used to delete an item
    """
    template_name = 'item_management/item_delete.html'

    def get_object(self):
        """
        Retrieves the item to delete
        """
        if self.request.user.is_authenticated:
            id = self.kwargs.get("id")
            # Returning object, 404 if it doesn't exist or doesn't belong to customer
            return get_object_or_404(Item, id=id, owner__user=self.request.user)
        return None

    def get_success_url(self):
        """
        Redirects user to home page when deletion is finished
        """
        return reverse("home")


class ItemDetailView(DetailView):
    """
    Detail view used to show an item's iformation
    """
    template_name = 'item_management/item_detail.html'

    def get_object(self):
        """
        Retrieves the item to diplsay
        """
        return get_object_or_404(Item, pk=self.kwargs.get("id"))

    def get_context_data(self, *args, **kwargs):
        """
        Provides context data to template
        """
        # Retrieving the item's commments
        context = super(ItemDetailView, self).get_context_data(*args, **kwargs)
        context['comments'] = Comment.objects.filter(
            item__pk=self.kwargs.get("id"))

        # Retrieving the user's vote on this item, empty if he never like it
        context['customervote'] = CustomerVote.objects.filter(
            item__pk=self.kwargs.get("id"))
        return context


class ItemListView(ListView):
    """
    List view of items
    """
    template_name = 'item_management/item_list.html'

    def get_queryset(self):
        """
        Retrieves the list of items to display
        """
        # Retrieving url query if there is one to search for items with a certain
        # substring in its title or the owner's username
        if self.request.method == 'GET' and 'search' in self.request.GET:
            return Item.objects.filter(Q(item_name__icontains=self.request.GET['search']) | Q(owner__user__username__icontains=self.request.GET['search']))
        else:
            return Item.objects.all()


class ItemBuyView(DeleteView):
    """
    View used to buy an item
    """
    template_name = 'item_management/item_buy.html'

    def get_object(self):
        """
        Retrieves the item to buy
        """
        if self.request.user.is_authenticated:
            id = self.kwargs.get("id")
            item = get_object_or_404(
                Item, ~Q(owner=self.request.user.customer), id=id)
            return item
        return None

    def get_success_url(self):
        """
        Returns to home page when user has bought item
        """
        id = self.kwargs.get("id")
        item = Item.objects.get(id=id)
        self.request.user.customer.account_cost -= item.price
        self.request.user.customer.save()

        return reverse("home")


def upvote(request, id):
    """
    View used to upvote an item
    """
    # Retrieving item
    item = get_object_or_404(Item, pk=id)
    # Making sure user is authenticated
    if request.user.is_authenticated:
        # Retrieving the user's vote on this item, empty if he never like it
        customer_vote = CustomerVote.objects.filter(
            customer=request.user.customer).filter(item=item)
        if customer_vote.exists():
            # If user had already voted, we remove his vote
            item.votes -= 1
            customer_vote.delete()
        else:
            # Adding vote
            item.votes += 1
            new_vote = CustomerVote(customer=request.user.customer, item=item)
            new_vote.save()
        item.save()
        # Going back to the item detail view
        return redirect('../')
    else:
        return redirect('accounts:login')


def comment(request, **kwargs):
    """
    View used to comment on an item
    """
    if request.user.is_authenticated == False:
        return redirect('home')
    else:
        form = CommentModelForm()
        if request.method == 'POST':
            form = CommentModelForm(request.POST, request.FILES)
            if form.is_valid():
                new_comment = Comment(
                    item=get_object_or_404(Item, pk=kwargs.get("id")),
                    comment_text=form.cleaned_data.get('comment_text'),
                    author=request.user.customer,
                    comment_date=datetime.today()
                )
                new_comment.save()
                return redirect('../')

    context = {'form': form}
    return render(request, 'item_management/item_comment.html', context)


def flag(request, id):
    """
    View used to flag an item
    """
    item = get_object_or_404(Item, pk=id)
    if request.user.is_authenticated:
        item.flags += 1

        item.save()
        return redirect('../')
    else:
        return redirect('accounts:login')
