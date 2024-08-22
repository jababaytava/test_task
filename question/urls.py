from django.urls import path, re_path
from . import views

urlpatterns = [
    path("create/", views.create_test, name="create_test"),
    path("tests/", views.test_list, name="test_list"),
    path("test/<int:pk>/", views.test_detail, name="test_detail"),
    path("test/<int:pk>/take/", views.take_test, name="take_test"),
    re_path(
        r"^test/(?P<pk>[0-9]+)/result/(?P<score>\d+\.\d+)/$",
        views.test_result,
        name="test_result",
    ),
    path("test/<int:pk>/result/<int:score>/", views.test_result, name="test_result"),
]
