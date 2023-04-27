from django import forms

from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    """Class to build a simple form to add a new topic"""
    class Meta:
        model = Topic
        fields = ["text"]
        labels = {"text": ""}


class EntryForm(forms.ModelForm):
    """Class to build a simnple form to add new entries for a topic"""
    class Meta:
        model = Entry
        fields = ["text"]
        labels = {"text": ""}
        widgets = {"text": forms.Textarea(attrs={"cols": 80})}
