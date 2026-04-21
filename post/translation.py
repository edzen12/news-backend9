from modeltranslation.translator import register, TranslationOptions
from post.models import Article


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ['title',]