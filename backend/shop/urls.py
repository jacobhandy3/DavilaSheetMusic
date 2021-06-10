from django.urls import path, reverse
from .views import *

urlpatterns = [
    path("", SheetMusicList.as_view(), name="sheetmusic-list"),
    path("<slug:slug>", SheetMusicDetail.as_view(), name="sheetmusic-detail"),
]