from django.shortcuts import render, get_object_or_404
from post.models import Article, Category


def index(request):
    articles = Article.objects.all()
    categories = Category.objects.all()[:6]
    context = {
        'articles':articles,
        'categories':categories,
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    articles = get_object_or_404(Article, slug=slug)
    categories = Category.objects.all()[:6]
    context = {
        'articles':articles, 
        'categories':categories,
    }
    return render(request, 'post-detail.html', context)