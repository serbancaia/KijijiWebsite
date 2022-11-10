from django import forms

from database.models import Item, Comment


class ItemModelForm(forms.ModelForm):
    """
    Form used to create or udpate an item
    """
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    item_name = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={"placeholder": "Your item name"}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "Your description"}))
    image = forms.ImageField(required=False)

    class Meta:
        model = Item
        fields = [
            'price',
            'item_name',
            'description',
            'image',
        ]


class CommentModelForm(forms.ModelForm):
    """
    Form used to add a a comment
    """
    comment_text = forms.CharField(label='', widget=forms.Textarea(
        attrs={"placeholder": "Your comment"}))

    class Meta:
        model = Comment
        fields = [
            'comment_text'
        ]
