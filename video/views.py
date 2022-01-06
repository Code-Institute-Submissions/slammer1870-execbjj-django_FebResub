from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Video, Section, Difficulty

# Create your views here.


class VideoListView(ListView):
    model = Video
    template_name = 'videos/videos.html'
    context_object_name = 'videos'
    ordering = ['-created_at']


class VideoDetailView(DetailView):
    model = Video
    template_name = 'videos/video_detail.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        print(self.kwargs)
        context['video_list'] = Video.objects.filter(
            section=self.kwargs['section'] ,category=self.kwargs['category'])
        return context


class SectionListView(ListView):
    model = Video
    template_name = 'videos/section.html'
    context_object_name = 'section'
    ordering = ['-created_at']

    def get_queryset(self):
        return Video.objects.filter(difficulty=self.kwargs['difficulty'], section=self.kwargs['section'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['video'] = Video.objects.filter(
            difficulty=self.kwargs['difficulty'], section=self.kwargs['section']).first()
        context['category'] = self.kwargs['section']
        context['categories'] = Section.objects.all()
        context['difficulties'] = Difficulty.objects.all()
        return context
