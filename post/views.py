from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.core.paginator import Paginator

from post.models import Article, Category, Tag


def index(request):
    articles = Article.objects.all()

    tags = Tag.objects.annotate(
        articles_count=Count('articles')
    ).filter(articles_count__gt=0)[:10] # ограничение

    paginator = Paginator(articles, 6) # кол-во постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
 
    categories = Category.objects.annotate(
        articles_count=Count('articles')
    ).filter(articles_count__gt=0)[:6]
    context = {
        'tags':tags,
        'page_obj':page_obj,
        'categories':categories,
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    articles = get_object_or_404(Article, slug=slug)

    tags = Tag.objects.annotate(
        articles_count=Count('articles')
    ).filter(articles_count__gt=0)[:10] # ограничение

    categories = Category.objects.annotate(
        articles_count=Count('articles')
    ).filter(articles_count__gt=0)[:6]
    context = {
        'tags':tags, 
        'articles':articles, 
        'categories':categories,
    }
    return render(request, 'post-detail.html', context)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category)

    tags = Tag.objects.annotate(
        articles_count=Count('articles')
    ).filter(articles_count__gt=0)[:10] # ограничение
    
    paginator = Paginator(articles, 2) # кол-во постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.annotate(
        articles_count=Count('articles')
    ).filter(articles_count__gt=0)[:6]
    context = {
        'tags':tags,
        'category':category,
        'page_obj':page_obj,
        'categories':categories,
    }
    return render(request, 'category.html', context)


def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    articles = Article.objects.filter(tags=tag)

    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.annotate(
        articles_count=Count('articles')
    ).filter(articles_count__gt=0)[:6]
    context = {
        'tag':tag,
        'page_obj':page_obj,
        'categories':categories,
    }
    return render(request, 'tags.html', context)