from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название", unique=True)
    slug = models.SlugField(
        unique=True, verbose_name='путь(ссылка)', 
        help_text='она автоматически заполнится когда вы пишете название'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = "Категории"


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name = 'хештег'
        verbose_name_plural = 'Хештеги'


class Article(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True,
        related_name="articles", verbose_name="Категория"
    )
    tags = models.ManyToManyField(
        Tag, related_name='articles', 
        blank=True
    )
    title = models.CharField(max_length=150)
    description = CKEditor5Field('Описание', config_name='extends')
    image = models.ImageField(upload_to='posts', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return f"ID:{self.id}  _Название: {self.title}"

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = "Посты"
        ordering = ['-id']


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments'
    )
    name = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.article.title}"
    
    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'комментарии'