from django.contrib import admin
from .models import Test, Question, Answer, TestResult


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class TestAdmin(admin.ModelAdmin):
    list_display = ["title", "creator", "created_at", "num_attempts"]
    search_fields = ["title", "description"]
    inlines = [QuestionInline]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["text", "test"]
    search_fields = ["text", "test__title"]
    inlines = [AnswerInline]


class TestResultAdmin(admin.ModelAdmin):
    list_display = ["user", "test", "score", "date_taken"]
    search_fields = ["user__username", "test__title"]


class TestResultInline(admin.TabularInline):
    model = TestResult
    extra = 0
    readonly_fields = ["test", "score", "date_taken"]


admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(TestResult, TestResultAdmin)
