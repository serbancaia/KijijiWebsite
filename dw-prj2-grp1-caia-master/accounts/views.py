from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm, AccountForm
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from database.models import Customer, Item, Blog

from django.views.generic import ListView


def signUpPage(request):
    """
    View of a visitor's signup
    """
    if request.user.is_authenticated:
        # redirecting customer to home if he's already logged in
        return redirect('home')
    else:
        # Create empty form
        form = SignUpForm()
        # POST request
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                # Adding User to database
                form.save()

                # Retrieving created user
                username = form.cleaned_data.get('username')
                created_user = User.objects.get(username=username)
                # messages.success(
                #     request, 'Account was created for ' + username)

                # Creating customer
                new_customer = Customer(user=created_user)
                new_customer.save()

                # autenticating user
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)

                # creating new customer's associated blog
                new_blog = Blog(owner=new_customer)
                new_blog.save()

                # Returning to home page
                return redirect('home')

        # Returning to form if it was invalid
        context = {'form': form}
        return render(request, 'accounts/sign_up.html', context)


def loginPage(request):
    """
    View of a visitor's login
    """
    if request.user.is_authenticated:
        # redirecting customer to home if he's already logged in
        return redirect('home')
    else:
        # Create empty form
        form = LoginForm()
        # POST request
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                # Retrieving form fields
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                # Trying to authenticate
                user = authenticate(
                    request, username=username, password=password)

                # If authentication succeeded, go to home
                if user is not None:
                    login(request, user)
                    return redirect('home')
                # else display what went wrong
                else:
                    messages.info(request, 'Username OR password is incorrect')

    # Return to form if we couldn't log visitor in
    context = {'form': form}
    return render(request, 'accounts/login.html', context)  # , context)


def logoutUser(request):
    """
    Logs a customer out
    """
    logout(request)
    # Redirecting to
    return redirect('accounts:login')


def accountManagementPage(request):
    """
    View that allows a customer to update his profile
    """
    if request.user.is_authenticated == False:
        # redirecting customer to login if he's not logged in
        return redirect('accoutns:login')

    # Retrieving current user
    user = request.user
    # Creating udpate form
    form = AccountForm(instance=user)
    # POST request
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # Saving the form/updating customer
            form.save()
            # Checking if a new picture was added
            new_picture = form.cleaned_data.get('profile_picture')
            if new_picture is not None and new_picture != user.customer.profile_picture:
                # If a new picture was added and it's not the same one, we add it to the database
                customer = user.customer
                customer.profile_picture = new_picture
                customer.save()

    # Returning to form if it was invalid
    context = {'form': form}
    return render(request, 'accounts/account.html', context)


def changePassword(request):
    """
    View that allows a customer to change his password
    """
    if request.user.is_authenticated == False:
        # redirecting customer to login if he's not logged in
        return redirect('accounts:login')

    # Creating password change form
    form = PasswordChangeForm(user=request.user)
    # POST request
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            # Saving new password
            form.save()
            # Keeping customer logged in
            update_session_auth_hash(request, form.user)
            # Redirecting him to his account
            return redirect("accounts:account")

    # Returning to form if it was invalid
    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)


class AccountItemListView(ListView):
    """
    View to display a customer's items
    """
    template_name = 'accounts/item_list.html'

    def get_queryset(self):
        """
        Retrieves the customer's items
        """
        return Item.objects.filter(owner=self.request.user.customer)

    def get(self, *args, **kwargs):
        """
        Main purpose is to validate that the user is authenticated
        """
        # Making sure user is authenticated, if he's not, he's going to login
        if self.request.user.is_authenticated == False:
            return redirect('accounts:login')
        return super(AccountItemListView, self).get(*args, **kwargs)
