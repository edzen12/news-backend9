from django.db import models


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


class Article(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True,
        related_name="articles", verbose_name="Категория"
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='posts', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return f"ID:{self.id}  _Название: {self.title}"

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = "Посты"
        ordering = ['-id']