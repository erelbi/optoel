from django.urls import path
from . import views,views_extra
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

handler404 = views.handler404
urlpatterns = [
    path('', views.index, name='index'),
    path('arama', views.arama, name='arama'),
    path('giriskalite', views.giriskalite, name='giriskalite'),
    path('uretimkontrol', views.uretimkontrol, name='uretimkontrol'),
    path('isemri', views.isemri, name='isemri'),
    path('yetkilendirme', views.yetkilendirme, name='yetkilendirme'),
    path('performans', views.performans, name='performans'),
    path('yazdir', views.yazdir, name='yazdir'),
    path('login/', views.ulogin, name='ulogin'),
    path('logout/', views.ulogout, name='ulogout'),
    path('pdf/', views.pdf, name='pdf'),
    #hata sayfaları
    path('403', views._403, name='403'),
    #fonksiyonlar
    url(r'^kullanicijson',views.kullanicijson),
    url(r'^kullanicisil',views.kullanicisil),
    url(r'^kullaniciduzelt',views.kullaniciduzelt),
    url(r'^passwordreset',views.passwordreset),
    url(r'^bildirim',views.bildirim),
    url(r'^dashboard',views.dashboard),
    url(r'^uretimdurum',views.uretimdurum),
    url(r'^personeldurum',views.personeldurum),
    url(r'^acikisemirleri',views.acikisemirleri),
    url(r'^tupTuru',views.tupTuru),
    url(r'^kontrolEt',views.kontrolEt),
    url(r'^is_emri_valfleri',views_extra.is_emri_valfleri), 
    url(r'^valf_parti_no_ata',views_extra.valf_parti_no_ata), 
    url(r'^kurlenmeKontrol',views.kurlenmeKontrol),
    url(r'^newVSN',views.newVSN),
    url(r'^getEmirNo',views.getEmirNo),
    url(r'^hardreset',views.hardreset),
     url(r'^valf_test_kayıt',views_extra.valf_test_kayıt),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
