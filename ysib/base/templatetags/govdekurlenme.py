from django import template
from  base.models import Emir
register = template.Library()
@register.simple_tag

def find_user_name(id_user):
    try:
        return Emir.objects.filter(id=id_user).values_list('is_emri',flat=True).first()
    except:
        return {}

