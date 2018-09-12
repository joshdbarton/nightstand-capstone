from django import forms
from nightstand_dashboard.models import ChapterComment

class CommentForm(forms.ModelForm):

    class Meta:
        model = ChapterComment
        fields = ["content",]


class SearchForm(forms.Form):

  
    search_term = forms.CharField(max_length=100)



