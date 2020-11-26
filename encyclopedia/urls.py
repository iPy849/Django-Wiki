from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:entry_name>', views.entry, name='entry'),
    path('new', views.newEntry, name='new'),
    path('new/<str:entry_name>', views.newEntry, name='edit'),
    path('randompage', views.randomPage, name='random_page'),
    path('promedio', views.average, name='average')
]
