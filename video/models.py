from django.db import models
import os
import requests
from urllib.parse import urlparse


# Create your models here.

class Section(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    thumbnail = models.ImageField(upload_to='static/thumbnails/', blank=True)

    def __str__(self):
        return self.name

class Difficulty(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name
        
DIFFICULTY_CHOICES = (("beginner", "Beginner"),
                      ("intermediate", "Intermediate"), ("advanced", "Advanced"))
SECTION_CHOICES = (("guard", "Guard"), ("passing", "Passing"),
                   ("submissions", "Submissions"), ("defense", "Defense"))


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=50)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE, db_constraint=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, db_constraint=False)

    @property
    def thumbnail(self):
        parsed = urlparse(self.url)

        id = parsed.path.split('/')[-1]

        endpoint = "https://vimeo.com/api/v2/video/{}.json".format(id)

        res = requests.get(endpoint)
        thumbnail = res.json()[0]['thumbnail_large']
        return thumbnail

    def __str__(self):
        return self.title

class TechniqueOfTheWeek(models.Model):
    video = models.ManyToManyField(Video)
    date = models.DateField(null=True)