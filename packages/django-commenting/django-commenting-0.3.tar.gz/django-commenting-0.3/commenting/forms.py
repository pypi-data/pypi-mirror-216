from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
    
    # overriding default form setting and adding bootstrap class
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'Enter name','class':'commenter-name'}
        self.fields['email'].widget.attrs = {'placeholder': 'Enter email', 'class':'commenter-email'}
        self.fields['body'].widget.attrs = {'placeholder': 'Comment here...', 'class':'commenter-body', 'rows':'5'}