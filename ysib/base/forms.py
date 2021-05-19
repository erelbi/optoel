from django import forms
#from django.contrib.auth import login , authenticate
from .models import UserProfileInfo
from django.contrib.auth.models import User
from .models import Emir, User ,Test
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

#select optionlar
tup_govde_turleri = [
    ('34lt aluminyum', '3.4 LT Aluminyum'),
    ('45lt aluminyum', '4.5 LT Aluminyum'),
    ('34lt celik', '3.4 LT Çelik'),
    ('45lt celik', '4.5 LT Çelik'),
    ('10lt aluminyum', '10 LT Aluminyum'),
    ('10lt celik', '10 LT Çelik'),
    ('15lt aluminyum', '1.5 LT Aluminyum'),
    ('2lt aluminyum', '2 LT Aluminyum'),
]
valf_turleri = [
    ('Aluminyum', 'Aluminyum'),
    ('Çelik', 'Çelik'),
]
renkler = [
    ('Kırmızı Ral3000 ', 'Kırmızı Ral3000 '),
    ('Yeşil Ral6019', 'Yeşil Ral6019'),
    ('Tan Sarısı', 'Tan Sarısı'),
    ('Haki Yeşili', 'Haki Yeşili'),
]
emniyet_ventil_turleri = [
    ('Rapture Disk', 'Rapture Disk'),
    ('Mekanik', 'Mekanik')
]

kullanici_birim = [
    ('IT','IT'),
    ('Planlama','Planlama'),
    ('Üretim','Üretim'),
    ('Kalite kontrol','Kalite Kontrol'),
]
kullanici_grup = [
    ('Yönetici','Yönetici'),
    ('Mühendis','Mühendis'),
    ('Teknisyen','Teknisyen'),
]
bolum_turleri = [
    ('Motor','Motor'),
    ('Personel','Personel')
]

#kendi alanımız oluşturabiliyoruz:)
class DateInput(forms.DateInput):
    input_type = 'date'

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100, label='Kullanıcı Adı')
    first_name = forms.CharField(max_length=100, label='İsim')
    last_name = forms.CharField(max_length=100, label='Soyisim')
    grup = forms.ChoiceField(
        initial='Planlama',
        label="Yetki Grubu",
        choices=kullanici_grup
    )
    birim = forms.ChoiceField(
        initial='Teknisyen',
        label="Birim",
        choices=kullanici_birim
    )
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1','password2','grup','birim')

class IsEmri(forms.ModelForm):
    is_emri = forms.CharField(max_length=100, label='İş Emri No')
    siparis = forms.CharField(max_length=100, label='Müşteri Siparis No')
    tup_sayisi = forms.CharField(max_length=100, label='Tüp Sayısı')
    urun_kodu = forms.CharField(max_length=100, label='Ürün Kodu')
    agirlik_min = forms.CharField(max_length=100, label='Ağırlık alt limit')
    agirlik_max = forms.CharField(max_length=100, label='Ağırlık üst limit')
    grup = forms.CharField(max_length=100,required = False)
    başlangıç = forms.DateInput()
    bitiş = forms.DateInput()
    emri_veren = forms.CharField(label='Emri Veren')
    emir_zamani = forms.DateTimeField(initial=timezone.now)
    sodyum_bikarbonat_miktari = forms.CharField(label="Sodyum Bikarbonat Miktarı (gram)")
    fm200_miktari = forms.CharField(label="FM200 Miktarı (gram)")
    tup_govde_turu = forms.ChoiceField(
        choices=tup_govde_turleri,
        label="Tüp Gövde Türü",
        required = False,
    )
    valf_turu = forms.ChoiceField(
        widget=forms.Select,
        choices=valf_turleri,
        label="Valf Türü",
    )
    renk = forms.ChoiceField(
        widget=forms.Select,
        choices=renkler,
        label="Renk",
    )
    emniyet_ventil_turu = forms.ChoiceField(
        widget=forms.Select,
        choices=emniyet_ventil_turleri,
        label="Emniyet Ventil Türü",
    )
    oncelik = forms.IntegerField(initial=1,required=False)
    musteri = forms.CharField(max_length=100, label='Müşteri')
    bolum = forms.ChoiceField(
        widget=forms.Select,
        choices=bolum_turleri,
        label="Bölüm",
    )
    class Meta:
        model = Emir
        widgets = {
            'başlangıç': DateInput(),
            'bitiş': DateInput(),
        }
        fields = ('is_emri', 'başlangıç', 'bitiş', 'tup_sayisi','emri_veren','emir_zamani','tup_govde_turu',
                'valf_turu','renk','fm200_miktari','sodyum_bikarbonat_miktari','emniyet_ventil_turu',
                'oncelik','bolum','musteri')


class TestForm(forms.ModelForm):
    tur = forms.CharField(max_length=100)
    seri_no = forms.CharField(max_length=100)
    acma = forms.CharField(max_length=100)
    kapatma = forms.CharField(max_length=100)
    testi_yapan = forms.CharField()
    text_tarihi = forms.DateTimeField(initial=timezone.now)

    class Meta:
        model = Emir
        fields = ('tur', 'seri_no', 'acma', 'kapatma','text_tarihi')
