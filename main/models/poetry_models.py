# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Ci(models.Model):
    rhythmic = models.CharField(max_length=150)
    dynasty = models.CharField(max_length=10)
    author = models.CharField(max_length=50)
    complete = models.BooleanField(default=True,blank=True, null=True)
    content = models.TextField()
    three_hundred = models.BooleanField(default=False,blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ci'


class Fly(models.Model):
    kind = models.IntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    dynasty = models.CharField(max_length=10, blank=True, null=True)
    author = models.CharField(max_length=50, blank=True, null=True)
    content = models.CharField(max_length=100, blank=True, null=True)
    fly_number = models.BooleanField()
    fly_season = models.BooleanField()
    fly_position = models.BooleanField()
    fly_weather = models.BooleanField()
    fly_color = models.BooleanField()
    fly_wine_vessel = models.BooleanField()
    fly_reduplicate = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'fly'


class Shi(models.Model):
    title = models.CharField(max_length=255)
    dynasty = models.CharField(max_length=10)
    author = models.CharField(max_length=50)
    content = models.TextField()
    yan = models.IntegerField(blank=True, null=True)
    rhyme_type = models.IntegerField()
    rhyme = models.CharField(max_length=20, blank=True, null=True)
    metric = models.BooleanField(default=False, blank=True, null=True)
    jue = models.IntegerField(default=3,blank=True, null=True)
    qi = models.BooleanField(default=True,blank=True, null=True)
    ru = models.BooleanField(default=False,blank=True, null=True)
    three_hundred = models.BooleanField(default=False,blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'shi'


class WordFrequency(models.Model):
    dynasty = models.IntegerField()
    word = models.CharField(max_length=20)
    word_len = models.IntegerField()
    phrase = models.CharField(max_length=5)
    num = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'word_frequency'

class Shijing(models.Model):
    title = models.CharField(max_length=5)
    section = models.CharField(max_length=6)
    chapter = models.CharField(max_length=4)
    content = models.TextField()

    class Meta:
        managed = True
        db_table = 'shijing'
