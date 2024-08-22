from django import forms
from .models import Test, Question, Answer, Comment


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["title", "description"]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["text", "is_correct"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text"]

    answer_formset = forms.inlineformset_factory(
        Question, Answer, form=AnswerForm, extra=4
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
