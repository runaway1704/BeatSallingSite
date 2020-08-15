from django import template
from Beat.models import Beat

register = template.Library()


@register.simple_tag()  # inclusion сделаю потом , когда шаблоны будут
def get_last_beats():
    beats = Beat.objects.order_by("-id")[:3]
    return {"last_beats": beats}

