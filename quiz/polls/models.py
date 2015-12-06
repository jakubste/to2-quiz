from datetime import datetime
from django.core.urlresolvers import reverse
from django.db import models


class Quiz(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=datetime.now)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('polls:quiz', args=[self.pk])


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions')
    text = models.TextField()

    def __unicode__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices')
    text = models.CharField(max_length=500, default='')
    correct = models.BooleanField(default=False)

    def __unicode__(self):
        return self.text

class NormalUser(models.Model):
    login = models.CharField(max_length=30, default='')
    password = models.CharField(max_length=30, default='yolo')
    registration_date = models.DateField

    def __unicode__(self):
        return self.text