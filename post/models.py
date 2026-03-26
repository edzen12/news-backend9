from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    # картинку добавить
    # дату создания поста

    def __str__(self):
        return self.title