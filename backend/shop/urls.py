from django.urls import path, reverse
from .views import *

urlpatterns = [
    path("original/", SheetMusicList.as_view(), name="sheetmusic-list"),
    path("arrangement/", ArrangeMusicList.as_view(), name="arrangemusic-list"),
    path("<slug:slug>", SheetMusicDetail.as_view(), name="sheetmusic-detail"),
]