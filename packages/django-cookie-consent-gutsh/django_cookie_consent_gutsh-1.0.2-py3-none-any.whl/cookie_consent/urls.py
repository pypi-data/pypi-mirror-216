from django.urls import path


from . import views

urlpatterns = [
    path('', views.index),
    path('accept', views.Acceptor.as_view()),
    path('template', views.template),
]