from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from profiles.models import Profile


def blank_true_false():
    # if series_title is not blank, series_book_no and series_link mandatory  # noqa
    if series_title == "":
        return False
    else:
        return True


class Book(models.Model):
    title = models.CharField(max_length=50, blank=False)
    author = models.CharField(max_length=50, blank=False)
    cover = models.ImageField(
        upload_to='images/', default='../default_cover_qdjgyp'
    )
    ISBN = models.CharField(max_length=50, blank=True)
    publisher = models.CharField(max_length=50, blank=True)
    published = models.DateField(blank=True, null=True)
    blurb = models.TextField(max_length=500, blank=True)
    series_title = models.CharField(max_length=50, blank=True)
    series_book_no = models.IntegerField(blank=blank_true_false, null=True)
    series_links = models.ManyToManyField('self', blank=blank_true_false)  # noqa

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title}"


class Genre(models.Model):
    genre = models.CharField(max_length=50, blank=False)
    tag = models.OneToOneField('Tags', on_delete=models.PROTECT)
    books = models.ForeignKey('Book', on_delete=models.PROTECT)
    profiles = models.ForeignKey(Profile, on_delete=models.PROTECT, default="")

    class Meta:
        ordering = ['genre']


class Tags(models.Model):
    title = models.CharField(max_length=50, blank=False)

    class Meta:
        ordering = ['title']


def create_tag(sender, instance, created, **kwargs):
    if created:
        Tags.objects.create(genre=instance)
