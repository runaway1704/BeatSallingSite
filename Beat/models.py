from django.db import models


class Category(models.Model):
    """Категории битов"""
    name = models.CharField("Имя категории", max_length=100)
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Beat(models.Model):
    """Биты"""
    name = models.CharField("Названиие", max_length=100)
    date = models.DateTimeField("Дата создания", auto_now_add=True)
    file = models.FileField("Файл", upload_to="Beats/")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бит"
        verbose_name_plural = "Биты"