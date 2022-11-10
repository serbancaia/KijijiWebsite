from django.test import TestCase
from django.contrib.auth.models import User
from database.models import (
    Customer,
    Item,
    Comment,
    Blog,
    Entry,
    CustomerVote,
)

# Create your tests here.

"""
Creating a sample user
"""
def create_user():
    return User.objects.create_user(username="testuser",
                                        email="testuser@email.com",
                                        password="testpassword1@")

"""
Testing the customer model
"""
class CustomerModelTests(TestCase):
    """
    Creating a customer test
    """
    def test_create_customer(self):
        user = create_user()
        customer = Customer(user=user)
        self.assertIs(customer.user.username, user.username)

"""
Creating a sample item
"""
def create_item(customer):
    return Item(owner=customer, price=100, item_name="Test Item",
                    description="Test description", votes=0, flags=0)

"""
Testing the item model
"""
class ItemModelTests(TestCase):
    """
    Creating an item test
    """
    def test_create_item(self):
        user = create_user()
        customer = Customer(user=user)

        item = create_item(customer)
        self.assertIs(item.item_name, "Test Item")

"""
Testing the comment model
"""
class CommentModelTests(TestCase):
    """
    Creating a comment test
    """
    def test_create_comment(self):
        user = create_user()
        customer = Customer(user=user)
        item = create_item(customer)

        comment = Comment(item=item, comment_text="Comment", author=customer)
        self.assertIs(comment.comment_text, "Comment")

"""
Testing the blog model
"""
class BlogModelTests(TestCase):
    """
    Creating a blog test. Check if it belongs to the right user
    """
    def test_create_blog(self):
        user = create_user()
        customer = Customer(user=user)

        blog = Blog(owner=customer)
        self.assertIs(blog.owner.user.username, "testuser")

"""
Testing the entry model
"""
class EntryModelTests(TestCase):
    """
    Creating an entry test
    """
    def test_create_entry(self):
        user = create_user()
        customer = Customer(user=user)
        blog = Blog(owner=customer)

        entry = Entry(author=customer, blog=blog, entry_text="Entry text")
        self.assertIs(entry.entry_text, "Entry text")
