from django.db import models
from django.utils import timezone
from datetime import datetime
from .services import file_rename

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    author = models.CharField(max_length=42)
    content = models.TextField(null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now,
                                verbose_name="Date de parution")
    view_nb = models.IntegerField(default=0)

    class Meta:
        verbose_name = "super article"
        ordering = ['-date']

    def est_recent(self):
        """ Retourne True si l'article a été publié dans
            les 30 derniers jours """
        return (datetime.now() - self.date).days < 30 and self.date < datetime.now()

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=255)
    adress = models.TextField()
    photo = models.ImageField(upload_to=file_rename, verbose_name="Photo")

    def __str__(self):
        return self.name
