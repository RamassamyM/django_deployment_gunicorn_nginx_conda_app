from django.urls import path
from .views import ArticleList, ArticleDetail, NewContact, ContactList
from django.views.generic import TemplateView, ListView
from .models import Article
from . import views

urlpatterns = [
    path('articles', views.ListerArticles.as_view(), name='root'),
    path('category/<int:category_pk>', views.ListerArticlesParCategorie.as_view(), name='articles_by_category'),
    path('', ArticleList.as_view(), name='article_list'),
    # path('articles/<int:pk>', ArticleDetail.as_view(), name='article_detail'),
    path('articles/<int:pk>', views.ShowArticle.as_view(), name='show_article'),
    path('newcontact', NewContact.as_view(), name='new_contact'),
    path('contacts', ContactList.as_view(), name='contact_list'),
    path('contact', TemplateView.as_view(template_name='blog/contact.html'), name='contact'),
]
