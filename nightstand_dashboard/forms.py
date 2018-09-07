from django.forms import ModelForm
from nightstand_dashboard.models import ChapterComment

class CommentForm(ModelForm):

    class Meta:
        model = ChapterComment
        fields = ["content",]