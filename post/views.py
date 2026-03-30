from django.shortcuts import render
from post.models import Article, Category


def index(request):
    articles = Article.objects.all()
    categories = Category.objects.all()[:6]
    context = {
        'articles':articles,
        'categories':categories,
    }
    return render(request, 'index.html', context)
