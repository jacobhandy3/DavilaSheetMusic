from django.urls import path
from . import views

urlpatterns = [
    path("original/", views.SheetMusicList.as_view(), name="sheetmusic-list"),
    path("arrangement/", views.ArrangeMusicList.as_view(), name="arrangemusic-list"),
    path("<slug:slug>/", views.SheetMusicDetail.as_view(), name="sheetmusic-detail"),
]