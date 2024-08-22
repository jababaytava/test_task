from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory, inlineformset_factory
from django.contrib.auth.decorators import login_required
from .models import Test, Question, Answer
from .forms import TestForm, QuestionForm, AnswerForm, CommentForm


def create_test(request):
    QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=3)
    AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=4)

    if request.method == "POST":
        test_form = TestForm(request.POST)
        question_formset = QuestionFormSet(
            request.POST, queryset=Question.objects.none(), prefix="questions"
        )

        if test_form.is_valid() and question_formset.is_valid():
            test = test_form.save(commit=False)
            test.creator = request.user
            test.save()

            for idx, question_form in enumerate(question_formset):
                question = question_form.save(commit=False)
                question.test = test
                question.save()

                answer_formset = AnswerFormSet(
                    request.POST, instance=question, prefix=f"answers_{idx}"
                )

                if answer_formset.is_valid():
                    answer_formset.save()
            return redirect("test_detail", pk=test.pk)
    else:
        test_form = TestForm()
        question_formset = QuestionFormSet(
            queryset=Question.objects.none(), prefix="questions"
        )

        for idx, question_form in enumerate(question_formset):
            question_form.answer_formset = AnswerFormSet(prefix=f"answers_{idx}")

    return render(
        request,
        "question/create_question.html",
        {
            "test_form": test_form,
            "question_formset": question_formset,
        },
    )


def test_list(request):
    search_query = request.GET.get("q", "")
    filter_passed = request.GET.get("filter", "all")

    tests = Test.objects.all()

    if search_query:
        tests = tests.filter(title__icontains=search_query)

    if filter_passed == "passed":
        tests = tests.filter(testresult__user=request.user).distinct()
    elif filter_passed == "not_passed":
        tests = tests.exclude(testresult__user=request.user).distinct()

    tests = tests.order_by("-created_at")

    return render(
        request,
        "question/test_list.html",
        {"tests": tests, "search_query": search_query, "filter_passed": filter_passed},
    )


@login_required
def test_detail(request, pk):
    test = get_object_or_404(Test, pk=pk)
    questions = test.questions.all()

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.test = test
            comment.user = request.user
            comment.save()
            return redirect("test_detail", pk=test.pk)
    else:
        comment_form = CommentForm()

    return render(
        request,
        "question/test_detail.html",
        {
            "test": test,
            "questions": questions,
            "comment_form": comment_form,
        },
    )


@login_required
def take_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    questions = test.questions.all()

    if request.method == "POST":
        total_questions = questions.count()
        correct_answers = 0

        for question in questions:
            selected_answer_id = request.POST.get(f"question_{question.id}")
            if selected_answer_id:
                try:
                    selected_answer = Answer.objects.get(id=selected_answer_id)
                    if selected_answer.is_correct:
                        correct_answers += 1
                except Answer.DoesNotExist:
                    print(f"Answer with id {selected_answer_id} does not exist.")

        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

        return redirect("test_result", pk=pk, score=score)

    return render(
        request, "question/take_test.html", {"test": test, "questions": questions}
    )


@login_required
def test_result(request, pk, score):
    test = get_object_or_404(Test, pk=pk)
    return render(request, "question/test_result.html", {"test": test, "score": score})
