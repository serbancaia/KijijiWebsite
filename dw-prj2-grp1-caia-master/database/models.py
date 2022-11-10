from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Custom user for the website
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_picture = models.ImageField(default = 'images/avatar.png', upload_to = 'profile_pics')
    account_cost = models.DecimalField(max_digits = 10, decimal_places = 2, default = 1000)

    def __str__(self):
        return self.user.get_username()


def user_directory_path(instance, filename):
    #file will be uploaded to items_images/user_<id>/<filename>
    return 'items_images/user_{0}/{1}'.format(instance.owner.id, filename)


"""
Items that will be listed to a website.
Belongs to a customer, creating a one to many relationship
"""
class Item(models.Model):
    owner = models.ForeignKey(Customer, on_delete = models.CASCADE)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    item_name = models.CharField(max_length = 200)
    description = models.TextField()
    image = models.ImageField(default=None, upload_to = user_directory_path)
    votes = models.IntegerField(default = 0)
    flags = models.IntegerField(default = 0)

    def __str__(self):
        return "{0} - ${1}".format(self.item_name, self.price)

    def get_owner_username(self):
        return self.owner

    def get_absolute_url(self):
        return "/item/%i/" % self.id

"""
A comment on a seller's item. This creates a one to many relationship
An item can have many comments. An entered comment can only belong to
one item
"""
class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    comment_text = models.TextField(max_length = 1000)
    author = models.ForeignKey(Customer, on_delete = models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "{0}: {1}".format(self.author, self.comment_text)

#A blog contains the list of comments (Entry) on a user' profile page
class Blog(models.Model):
    owner = models.OneToOneField(Customer, on_delete = models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add = True)
    last_modification_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "{0}'s blog".format(self.owner)

"""
A comment on a user's blog (kind of like a chat). One blog can have
many entries and an entry belongs to one blog
"""
class Entry(models.Model):
    author = models.ForeignKey(Customer, on_delete = models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    entry_text = models.TextField(max_length = 1000)
    entry_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "{0}: {1}".format(self.author, self.entry_text)

"""
A bridging table between a customer and an item they have liked.
"""
class CustomerVote(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
