from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from .models import Article, Contact, Category
from .forms import NewContactForm
from datetime import datetime, timedelta

class ArticleList(View):
    def get(self, request):
        articles = Article.objects.all()
        categories = Category.objects.all()
        """ test de variables dates pour tester naturalday from humanize"""
        date_avant_hier = datetime(2018, 9, 25)
        date_hier = datetime(2018, 9, 26)
        date_auj = datetime(2018, 9, 27)
        date_demain = datetime(2018, 9, 28)
        date1 = datetime(2018, 9, 27, 16, 20, 0)
        date2 = datetime(2018, 9, 27, 14, 19, 30)
        date3 = datetime(2018, 9, 27, 13, 15, 25)
        date4 = datetime(2018, 9, 27, 12, 20, 0)
        date5 = datetime(2018, 9, 27, 13, 10, 0)
        date6 = datetime(2018, 9, 27, 18, 20, 0)
        return render(request, 'blog/article_list.html', locals())

class ListerArticles(ListView):
    model = Article
    context_object_name = "articles"
    # template_name = 'blog/article_list.html'
    paginate_by = 2

class ListerArticlesParCategorie(ListView):
    model = Article
    context_object_name = "articles"
    # template_name = 'blog/article_list.html'
    paginate_by = 2
    def get_queryset(self):
        return Article.objects.filter(category_id=self.kwargs['category_pk'])

    def get_context_data(self, **kwargs):
        context = super(ListerArticlesParCategorie, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ArticleDetail(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        return render(request, 'blog/article_detail.html', {'article': article})

class ShowArticle(DetailView):
    model = Article
    context_object_name = "article"
    # template_name = 'blog/article_detail'
    def get_object(self):
        # Nous récupérons l'objet, via la super-classe
        article = super(ShowArticle, self).get_object()
        article.view_nb = article.view_nb or 0
        article.view_nb += 1  # Imaginons un attribut « Nombre de vues »
        article.save()

        return article  # Et nous retournons l'objet à afficher
        # remarque attribut self.request est aussi dispo

class NewContact(View):
    def get(self, request):
        return render(request, 'blog/newcontact.html', {'form': NewContactForm(), 'saved': False})

    def post(self, request):
        saved = False
        form = NewContactForm(request.POST or None, request.FILES)
        if form.is_valid():
            contact = Contact()
            contact.name = form.cleaned_data["name"]
            contact.adress = form.cleaned_data["adress"]
            contact.photo = form.cleaned_data["photo"]
            contact.save()
            saved = True
        return render(request, 'blog/newcontact.html', {'form': form, 'saved': saved})

class ContactList(View):
    def get(self, request):
        return render(request, 'blog/contact_list.html', {'contacts': Contact.objects.all()})
