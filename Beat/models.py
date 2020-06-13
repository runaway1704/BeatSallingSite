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
        ordering = ("name",)


class Beat(models.Model):
    """Биты"""
    name = models.CharField("Названиие", max_length=100)
    file = models.FileField("Файл", upload_to="Beats/")
    price = models.DecimalField("Цена в долларах", max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    created = models.DateTimeField("Дата создания", auto_now_add=True)
    updated = models.DateTimeField("Дата обновления", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бит"
        verbose_name_plural = "Биты"
        ordering = ("name",)
        index_together = (("id", "slug"),)