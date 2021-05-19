from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from base.models import Emir , User, Bildirim, Valf_montaj
from django.contrib.auth.models import User
from django.dispatch import Signal,receiver
import asyncio
from datetime import datetime
now = datetime.now()

ping_signal = Signal(providing_args=["context"])

@receiver(post_save, sender=Emir)
def announce_new_job(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifiy", {"type": "send.notifiy",
                       "event": "is emri",
                       "kisi": instance.emri_veren,
                       "emir": instance.is_emri,
                       "grupp": instance.grup})


#Üretim kontrol bitince
#Üretim kontrol başlayınca
#Öncelik sırası değişince
@receiver(post_save, sender=Bildirim)
def announce_starting(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifiy", {"type": "send.notifiy",
                       "event": instance.tur,
                       "grup" : instance.emri_veren_grup})

@receiver(ping_signal)
def pong(**kwargs):
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)	
    if kwargs['PING']:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            async_result = loop.run_until_complete(yazdır())
            loop.close()
        except Exception as err:
            print(err)

        


async def yazdır():
    await asyncio.sleep(20)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)	
    print('PONG')


