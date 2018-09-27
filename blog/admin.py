from django.contrib import admin
from .models import Category, Article
from django.utils.text import Truncator

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'content_display', 'slug', 'id')
    # fields = ('title', 'content', 'author', 'category')
    list_filter = ('author', 'category',)
    date_hierarchy = 'date'
    ordering = ('-date',)
    search_fields = ('title', 'content')
    fieldsets = (
        ('General', {
            'classes': ['collapse',],
            'fields': ('title', 'author', 'category', 'slug')
        }),
        ('Contenu de l\'article', {
            'description': 'Le formulaire accepte les balises HTML. Utilisez-les à bon escient !',
            'fields': ('content',),
            'classes': [],
        }),
    )
    prepopulated_fields = {'slug': ('title', ), }

    def content_display(self, article):
        """
        Return the first 40 characters of an article with ...
        """
        return Truncator(article.content).chars(40, truncate='...')

     # En-tête de notre colonne
    content_display.short_description = 'Aperçu du contenu'

from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
