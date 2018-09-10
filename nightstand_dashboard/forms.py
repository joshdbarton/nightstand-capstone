from django import forms
from nightstand_dashboard.models import ChapterComment

class CommentForm(forms.ModelForm):

    class Meta:
        model = ChapterComment
        fields = ["content",]


class SearchForm(forms.Form):


    search_field = forms.ChoiceField(label="Search by:", choices=(
        ("author", "Author"),
        ("title", "Title"),  
    ))
    search_term = forms.CharField(max_length=100)



