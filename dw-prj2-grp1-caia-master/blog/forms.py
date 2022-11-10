from django import forms

from database.models import Entry

class EntryModelForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = [
            "entry_text",
        ]