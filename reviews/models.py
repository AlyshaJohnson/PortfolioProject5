from django.db import models
from library.models import Book, Tags
from django.contrib.auth.models import User


RATING = (
    (1, "*"),
    (2, "**"),
    (3, "***"),
    (4, "****"),
    (5, "*****"),
)
YES_NO = ((0, "No"), (1, "Yes"))


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    title = models.CharField(max_length=75, blank=False)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, default="")
    description = models.TextField(max_length=500, blank=False)
    date_added = models.DateField(blank=True, null=True)
    book_started = models.DateField(blank=True, null=True)
    book_finished = models.DateField(blank=True, null=True)
    rating = models.IntegerField(choices=RATING, default=None)
    tags = models.ManyToManyField(Tags, blank=True)
    visibility = models.IntegerField(choices=YES_NO, default=1)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title}"
