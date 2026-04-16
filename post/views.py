from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q 
from django.contrib.auth.forms import UserCreationForm
import xml.etree.ElementTree as ET
import requests

from post.models import Article, Category, Tag, Comment


def register(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {
        'form':form,
    }
    return render(request, 'register.html', context)


def currency_view(request):
    url = 'https://www.nbkr.kg/XML/daily.xml'
    response = requests.get(url)
    currencies = []
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        for currency in root.findall('Currency'):
            code = currency.get('ISOCode')
            nominal = int(currency.find('Nominal').text)
            value = float(currency.find('Value').text.replace(',', '.'))
            rate = value/nominal
            currencies.append({
                'code': code,
                'rate': rate,
            })
    # добавляем сом
    currencies.insert(0, {'code':'KGS', 'rate':1})

    #калькулятор
    result = None 
    amount = request.GET.get('amount')
    from_rate = request.GET.get('from')
    to_rate = request.GET.get('to')
    if amount and from_rate and to_rate:
        try:
            amount = float(amount)
            from_rate = float(from_rate)
            to_rate = float(to_rate)
            result = (amount*from_rate)/to_rate
        except:
            pass 
    context = {
        'currencies':currencies,
        'result':result,
    }
    return render(request, 'valuta.html', context)


def search(request):
    query = request.GET.get('q')
    articles = Article.objects.all()
    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    paginator = Paginator(articles, 6) # кол-во постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'query':query,
        'page_obj':page_obj, 
    }
    return render(request, 'search.html', context)



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

    if request.method == 'POST':
        name = request.POST.get('name')
        text = request.POST.get('text')
        if name and text:
            Comment.objects.create(
                article=articles,
                name=name,
                text=text 
            )
            return redirect('post_detail', slug=slug)
    comments = articles.comments.all().order_by('-id')

    context = {
        'tags':tags, 
        'comments':comments, 
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