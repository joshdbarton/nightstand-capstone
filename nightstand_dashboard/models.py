from django.db import models
import datetime 
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Reader(models.Model):
    """proxy model for auth user model
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chapters = models.ManyToManyField(
        'Chapter', 
        through="ReaderChapter", 
        through_fields=("reader", "chapter")
    )

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Reader.objects.create(user=instance)
        instance.reader.save()

    def __str__(self):
        return self.user.username

    


class Book(models.Model):
    """Book model representing the books that have been uploaded to the database from the OpenLibrary API. 
    """


    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    OLID = models.CharField(max_length=255)
    pages = models.IntegerField()
    thumbnail = models.CharField(max_length=1023)
    readers = models.ManyToManyField(Reader, blank=True,  related_name="books")

    def __str__(self):
        return self.title


class Chapter(models.Model):
    """Represents a chapter of a book uploaded to the database.
    """


    name = models.CharField(max_length=255)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    readers = models.ManyToManyField(
        Reader, 
        through="ReaderChapter", 
        through_fields=("chapter", "reader")
    )

    def __str__(self):
        return self.name

    
class Group(models.Model):
    """Represents a reading group of users reading the same book.
    """


    name = models.CharField(max_length=255)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    readers = models.ManyToManyField(Reader, related_name="groups")

    def __str__(self):
        return self.name


class ChapterComment(models.Model):
    """Represents the comments from a user on a particular chapter of a book.
    """


    content = models.CharField(max_length=1023)
    datetime = models.DateField(auto_now=True)
    chapter = models.ForeignKey("Chapter", on_delete=models.CASCADE)
    reader = models.ForeignKey("Reader", on_delete=models.CASCADE)
    likes = models.ManyToManyField(Reader, related_name="liked_comments")

    def __str__(self):
        return f'{self.reader}: {self.datetime}'


class ReaderChapter(models.Model):
    """Represents a user's progress in a book's chapters
    """


    reader = models.ForeignKey('Reader', on_delete=models.CASCADE)
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE)
    duedate = models.DateField(null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.reader}: {self.chapter}'
    
    @property
    def is_late(self):
        if self.duedate:
            return self.duedate < datetime.date.today()
        else:
            return False
