from django.urls import path
from django.conf import settings

from .views import SectionListView, VideoDetailView, VideoListView

app_name="videos"

urlpatterns = [
    path('', VideoListView.as_view(), name="video_list_view"),
    path('<difficulty>/<section>/', SectionListView.as_view(), name="section"),
    path('<difficulty>/<section>/<category>/<pk>/', VideoDetailView.as_view(), name="lesson"),
]