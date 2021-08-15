from django.urls import path

from .views import MessagesApiView, TestApiView

urlpatterns = [
    path("test", TestApiView.as_view()),
    path("messages", MessagesApiView.as_view()),
]
