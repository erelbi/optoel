from django import template
from base.models import Bildirim
import json
#qr kod aktarılırken sıkıntı vardı
register = template.Library()

@register.simple_tag
def bildirim():
	return Bildirim.objects.all().values()