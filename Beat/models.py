from django.db import models
from django.urls import reverse


class Beat(models.Model):
    """Биты"""
    name = models.CharField("Названиие", max_length=100)
    file = models.FileField("Файл", upload_to="Beats/")
    price = models.DecimalField("Цена в долларах", max_digits=10, decimal_places=2, default=0)
    bpm = models.CharField("BPM", max_length=5, default="", blank=True, null=True)
    url = models.SlugField(max_length=160, unique=True)
    url_to_cloud = models.URLField("Ссылка на ФАЙЛ в облаке", max_length=200, default="")

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("beat_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Бит"
        verbose_name_plural = "Биты"
        ordering = ("name",)
        index_together = (("id", "url"),)