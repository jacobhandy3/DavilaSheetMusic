from django.urls import path
from . import views

urlpatterns = [
    path("", views.SheetMusicList.as_view(), name="sheetmusic-list"),
    path("<slug:slug>", views.SheetMusicDetail.as_view(), name="sheetmusic-detail"),
]