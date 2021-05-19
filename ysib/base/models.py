from django.db import models
import datetime
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

birim = models.CharField(max_length=20,default="")
birim.contribute_to_class(User, 'birim')
grup = models.CharField(max_length=20,default="kalite-kontrol")
grup.contribute_to_class(User, 'grup')

#pdf_dir = FileSystemStorage(location='/pdfs')


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Emir(models.Model):
    is_emri = models.CharField(max_length=100,unique=True)
    tup_sayisi = models.CharField(max_length=100)
    urun_kodu = models.CharField(max_length=100)
    başlangıç = models.DateField(default=timezone.now)
    bitiş = models.DateField(default=timezone.now)
    emri_veren = models.CharField(max_length=100)
    grup = models.CharField(max_length=100,null=True,blank=True)
    emir_zamani = models.DateTimeField(default=timezone.now)
    tup_govde_turu = models.CharField(max_length=100,null=True)
    valf_turu = models.CharField(max_length=100,null=True)
    renk = models.CharField(max_length=100,null=True)
    sodyum_bikarbonat_miktari = models.CharField(max_length=100,null=True)
    fm200_miktari = models.CharField(max_length=100,null=True)
    bos_agirlik_miktari = models.CharField(max_length=100,null=True)
    emniyet_ventil_turu = models.CharField(max_length=100,null=True)
    oncelik = models.PositiveIntegerField(default=1)
    durum = models.CharField(default="Başlanmamış",max_length=20)
    musteri = models.CharField(max_length=100,null=True,blank=True)
    bolum = models.CharField(max_length=100,null=True,blank=True)
    siparis = models.CharField(max_length=100,null=True,blank=True) #müşteri sipariş numarası
    ağırlık_alt_limit = models.PositiveIntegerField(default=1)
    ağırlık_üst_limit = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.is_emri

class Test(models.Model):
    tur = models.CharField(max_length=30)
    seri_no = models.CharField(max_length=20,blank=True, null=True)
    baslangic_seri_no = models.CharField(max_length=20,blank=True, null=True)
    bitis_seri_no = models.CharField(max_length=20,blank=True, null=True)
    lot_no = models.PositiveIntegerField( blank=True, null=True)
    #lot_no = models.CharField(max_length=20, blank=True, null=True)
    acma = models.CharField(max_length=20,blank=True, null=True)
    kapatma = models.CharField(max_length=20,blank=True, null=True)
    testi_yapan = models.CharField(max_length=20)
    okunan_deger = models.CharField(max_length=20,blank=True, null=True)
    kabul_durumu = models.CharField(max_length=20,blank=True, null=True)
    is_emri = models.CharField(max_length=20,blank=True, null=True)
    pdf_ismi = models.CharField(max_length=100)
    test_basinci = models.CharField(max_length=10,blank=True, null=True)
    patlama_basinci = models.CharField(max_length=10,blank=True, null=True)
    pdf_dosyasi = models.TextField(max_length=10000000000,null=True,blank=True)
    test_tarihi = models.DateTimeField(default=timezone.now,blank=True, null=True)

    def __str__(self):
        return str(self.baslangic_seri_no)



class Bildirim(models.Model):
    zaman = models.CharField(default=timezone.now,blank=True, null=True,max_length=100)#().strftime('%Y%m%d-%H-%M%S')
    tur = models.CharField(max_length=30)
    emri_veren_grup = models.CharField(max_length=30)
    is_emri = models.CharField(max_length=30)
    emri_veren = models.CharField(max_length=30)
    kisi = models.CharField(max_length=30)
    def __str__(self):
        return "bildirim"

class Uretim(models.Model):
    tur = models.CharField(max_length=30)
    vsn = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(default=timezone.now,blank=True, null=True)
    okunan_deger = models.CharField(max_length=10,null=False)
    personel = models.CharField(max_length=40,null=False)
    is_emri = models.CharField(max_length=40,blank=True,null=True)#Valf
    alt_nipel_no = models.CharField(max_length=40,null=True,blank=True)#Valf
    bakir_membran_no = models.CharField(max_length=40,null=True,blank=True)#Valf
    ust_nipel_no = models.CharField(max_length=40,null=True,blank=True)#Valf
    manometre_no = models.CharField(max_length=40,null=True,blank=True)#Valf
    basincanahtari_no = models.CharField(max_length=40,null=True,blank=True)#Valf
    uygunluk = models.CharField(max_length=40,null=True,blank=True)
    acma = models.CharField(max_length=40,null=True,blank=True)#Valf_test
    kapatma = models.CharField(max_length=40,null=True,blank=True)#Valf_test
    sebep = models.CharField(max_length=100,null=True,blank=True)#Valf_test
    tork_degeri = models.CharField(max_length=20,null=True,blank=True)
    tsn = models.CharField(max_length=30,null=True,blank=True)
    bos_agirlik = models.CharField(max_length=30,null=True,blank=True)
    rekorlu_agirlik = models.CharField(max_length=30,null=True,blank=True)
    fm200 = models.CharField(max_length=30,null=True,blank=True)
    azot = models.CharField(max_length=30,null=True,blank=True)
    etiket_seri_no = models.CharField(max_length=30,null=True,blank=True)
    fsn = models.CharField(max_length=30,null=True,blank=True)
    funye_seri_omaj = models.CharField(max_length=30,null=True,blank=True)
    basinc_anahtari_omaj = models.CharField(max_length=30,null=True,blank=True)
    montaj_kurlenme_zamani = models.DateTimeField( blank=True, null=True)
    fm200_kurlenme_zamani = models.DateTimeField( blank=True, null=True)
    govde_kurlenme_zamani = models.DateTimeField( blank=True, null=True)

    def __str__(self):
        return str(self.vsn)


class Valf_govde(models.Model):
 

    tork=models.PositiveIntegerField(null=True)
    tup_seri_no=models.PositiveIntegerField(null=True)
    sodyum_miktari=models.PositiveIntegerField(null=True)
    uygunluk=models.CharField(max_length=30,null=True,blank=True)
    sebep=models.CharField(max_length=30,null=True,blank=True)
    govde_personel=models.ForeignKey(User,related_name='govde_personel', on_delete=models.DO_NOTHING) 
    govde_tarihi = models.DateTimeField( blank=True, null=True)
    
    govde_kurlenme_personel=models.ForeignKey(User,related_name='govde_kurlenme_personel',null=True,on_delete=models.DO_NOTHING) 
    govde_kurlenme_parti_no = models.PositiveIntegerField(null=True)
    govde_kurlenme_baslangic_tarihi = models.DateTimeField( blank=True, null=True)
    govde_kurlenme_bitis_tarihi = models.DateTimeField( blank=True, null=True)

    


  

class Valf_test(models.Model):
    acma=models.PositiveIntegerField(null=True)
    kapama=models.PositiveIntegerField(null=True)
    uygun=models.BooleanField(default=False)
    sebep=models.CharField(max_length=30,null=True,blank=True)
    test_personel=models.ForeignKey(User,related_name='test_personel', on_delete=models.DO_NOTHING) 
    test_tarihi = models.DateTimeField( blank=True, null=True)


class Valf_montaj(models.Model):

    alt_nipel_no = models.PositiveIntegerField(null=True)
    bakir_membran_no = models.PositiveIntegerField(null=True)
    ust_nipel_no = models.PositiveIntegerField(null=True)
    manometre_no = models.PositiveIntegerField(null=True)
    basincanahtari_no = models.PositiveIntegerField(null=True)
    montaj_personel=models.ForeignKey(User,related_name='montaj_personel', on_delete=models.DO_NOTHING) 
    montaj_tarihi = models.DateTimeField( blank=True, null=True)
    kurlenme_personel=models.ForeignKey(User,related_name='kurlenme_personel',null=True,on_delete=models.DO_NOTHING) 
    kurlenme_parti_no = models.PositiveIntegerField(null=True)
    kurlenme_baslangic_tarihi = models.DateTimeField( blank=True, null=True)
    kurlenme_bitis_tarihi = models.DateTimeField( blank=True, null=True)


class Valf(models.Model):
    is_emri = models.ForeignKey(Emir,on_delete=models.DO_NOTHING) 
    valf_montaj = models.ForeignKey(Valf_montaj,on_delete=models.DO_NOTHING)
    valf_test = models.ForeignKey(Valf_test,on_delete=models.DO_NOTHING,null=True)
    valf_govde = models.ForeignKey(Valf_govde,on_delete=models.DO_NOTHING,null=True)

 












 



class Valf_fm200(models.Model):
    valf=models.ForeignKey(Valf,on_delete=models.DO_NOTHING)
    personel=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    kayit_tarihi=models.DateTimeField( blank=True, null=True)
    
    kurlenme_bitis=models.DateTimeField( blank=True, null=True)
    bos_agirlik =models.PositiveIntegerField(null=True)
    rekorlu_agirlik = models.PositiveIntegerField(null=True)
    fm200 = models.PositiveIntegerField(null=True)
    azot = models.PositiveIntegerField(null=True)


class Valf_havuz(models.Model):
    valf=models.ForeignKey(Valf,on_delete=models.DO_NOTHING)
    personel=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    kayit_tarihi=models.DateTimeField( blank=True, null=True)
    
    tup_cidar_sicaklik =models.PositiveIntegerField(null=True)
    tup_basinc = models.PositiveIntegerField(null=True)
    uygunluk=models.CharField(max_length=30,null=True,blank=True)
    sebep=models.CharField(max_length=30,null=True,blank=True)
 


class Valf_final_montaj(models.Model):
    valf=models.ForeignKey(Valf,on_delete=models.DO_NOTHING)
    personel=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    kayit_tarihi=models.DateTimeField( blank=True, null=True)
    
    etiket_seri_no =models.PositiveIntegerField(null=True)
    funye_seri_no = models.PositiveIntegerField(null=True)
    funye_seri_omaj = models.PositiveIntegerField(null=True)
    basinc_anahtari_omaj = models.PositiveIntegerField(null=True)
 