from base.views import index
from django.http.request import QueryDict
from django.shortcuts import render,redirect
from .forms import UserRegisterForm, IsEmri ,TestForm
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.http import HttpResponseRedirect, HttpResponse ,JsonResponse
from django.urls import reverse
from django.db.models import Max, query
from django.contrib.auth.models import User
from .models import Emir , Test, Bildirim, Uretim, Valf,PDF_Rapor
from .models import Valf_montaj,Valf_test,Valf_govde,Valf_fm200,Valf_havuz,Valf_final_montaj
from django.contrib.auth.decorators import login_required
import json, platform, base64, datetime, os
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from base64 import b64decode
import time
from django.utils import six 
import itertools
from .forms import PDFForm
from datetime import datetime
# Create your views here.





@csrf_exempt
def valf_parti_no_ata(request):
    # ping_signal.send(sender="valf", PING=True)


    emir_valuelist = Emir.objects.filter(is_emri=request.POST.dict()['is_emri']).values_list('id', flat=True)
    print(Valf.objects.filter(is_emri_id=emir_valuelist[0]).values_list('valf_montaj_id',flat=True))

    valf_montaj_idleri= Valf.objects.filter(is_emri_id=emir_valuelist[0]).values_list('valf_montaj_id',flat=True)
  

    kurlenme_parti_noları = []
    for valf_montaj_id in valf_montaj_idleri :
        if  Valf_montaj.objects.filter(id=valf_montaj_id).first().kurlenme_parti_no is None:
            kurlenme_parti_noları.append(0)
        else:
            kurlenme_parti_noları.append(Valf_montaj.objects.filter(id=valf_montaj_id).first().kurlenme_parti_no) 
    print(max(kurlenme_parti_noları))
 
 
    #parti_no__max= valfler.aggregate(Max('kurlenme_parti_no'))['kurlenme_parti_no__max']  









    #valfler= Valf_montaj.objects.filter(is_emri= emir)
    #parti_no__max= valfler.aggregate(Max('kurlenme_parti_no'))['kurlenme_parti_no__max']  
    #if parti_no__max is None: 
    #    parti_no__max=0
    next_parti_no= max(kurlenme_parti_noları) + 1
 
    print("next_parti_no",next_parti_no)



    valfler_id=request.POST.dict()['valfler_id'] 
    print("valfler_id",valfler_id)
    valfler_id_array = json.loads(valfler_id)
    print(valfler_id_array)
    for id in valfler_id_array:
        valf  =  Valf_montaj.objects.get(id=id)
        if valf.kurlenme_parti_no is None:
            valf.kurlenme_parti_no=next_parti_no
            valf.kurlenme_baslangic_tarihi = timezone.now()
            valf.kurlenme_bitis_tarihi =  timezone.now()+timezone.timedelta(hours=12)
            valf.kurlenme_personel = User.objects.get(id=request.user.id)
            valf.save()
 
    
    return HttpResponse('OK')


@csrf_exempt
def is_emri_valfleri(request):
    
    temp = []
    emir = Emir.objects.get(is_emri=request.POST.dict()['is_emri_id'])
    try:
        is_emir_valfleri =  Valf.objects.filter(is_emri=emir).values_list('valf_montaj',flat=True)
        # //is_emir_valfleri =  Valf_montaj.objects.filter(is_emri=emir)
    except Exception as err:
        is_emir_valfleri =  Valf.objects.filter(is_emri=emir).values_list('valf_montaj',flat=True)
    for is_id in is_emir_valfleri:
        veri={}
        veri['id'] = is_id
        veri['parti_no'] = Valf_montaj.objects.filter(id=is_id).first().kurlenme_parti_no
        temp.append(veri)
        
    # temp = []
    # for valf in is_emir_valfleri.values():
    #     temp.append(valf)
    # veri = list(temp)
    print("veriiiiiii",list(temp)) 
    return JsonResponse(list(temp),safe=False)

@csrf_exempt
def montajKurlenme(request):
    print(request.POST.getlist('parti_no[]'))
    
    montaj_list=[]
    try:
        if  len(request.POST.getlist('parti_no[]')[0]) > 0:
            for parti_no in request.POST.getlist('parti_no[]'):
                clock = Valf_montaj.objects.filter(kurlenme_parti_no=parti_no).first().kurlenme_bitis_tarihi - timezone.now()
                
                montaj={}
                montaj['tarih'] = time_calc(clock)
                montaj['partino'] = parti_no
                valf_no_list=[]
                for valf_no in  Valf_montaj.objects.filter(kurlenme_parti_no=parti_no).values_list('id',flat=True):  
                    valf_no_list.append(valf_no)
                montaj['valfno'] = valf_no_list
                montaj_list.append(montaj)
            return JsonResponse(list(montaj_list),safe=False)
        else:
            return JsonResponse(list(montaj_list),safe=False)
    except Exception as err:
        print(err)
        return JsonResponse(list(montaj_list),safe=False)


def time_calc(data):
    print(data.days)
    if data.days == 0:
        
       return  "{}:{}".format(data.seconds//3600,(data.seconds//60)%60,data.seconds%60)
    else:
        return "Kürleme Bitmiştir"



@csrf_exempt
def valf_test_kayıt(request):
    print("----------------valf-test-kayıt")
    print(request.FILES.getlist('file'))
    print("-----------------------")
    data_list = []
    print("içerde-----< kayıt")
    user_id = request.user.id
    try:
        counter = 0
        #print(request.POST.dict())
        
        for key,value in  dict(request.POST.dict()).items():
            #print(value)
            data_list.append(value)
            counter += 1
           
            if counter % 7 == 0:
         
                value_list=list_function(data_list,counter-7,counter)
                
                if value_list[0]:
                    print("----------------------->", value_list[0])
                    control_duplicate = control_duplicate_test(value_list,user_id)
                    print("----------------------------<",control_duplicate)
                    if isinstance(control_duplicate,list):
                        
                        save_function(control_duplicate,request.user.id) 
                        return JsonResponse({'status':200}) 
                else:
                    print("boş")  
    except Exception as err:
        print(err)
        return JsonResponse({'status':500})
        #return True



def list_function(data_list,first,second):

    #print(list(itertools.islice(data_list, first,second)))
    return list(itertools.islice(data_list, first,second))


def control_duplicate_test(clean_list,uid):
    print(clean_list)
    valf_test_id = Valf.objects.filter(id=clean_list[0]).first().valf_test_id
    print("print_valf_test_id",valf_test_id)
    if valf_test_id:
        ''' Mevcut Ama Durum Kontrolü '''
        status = Valf_test.objects.filter(id=valf_test_id).first().uygun
        if status == False:
            valf_id = Valf.objects.filter(id=clean_list[0]).first().valf_test_id
            Valf_test.objects.filter(id=valf_id).update(test_tarihi=timezone.now(),test_personel_id=uid,acma=clean_list[2],kapama=clean_list[3],uygun=is_not_blank(clean_list[1]))
            return False
        else:
            return False
    elif  valf_test_id is None:
        ''' Duplicate Yok Devam '''
        return clean_list

def is_not_blank(s):
    print("is not blank")
    print(s)
    if s:
        return True
    else:
        return False

def save_function(cleanlist,user_id):
    filename =  cleanlist[4]
   
    print(cleanlist)
    print("---------------------------->")
    valf_test =Valf_test(acma=cleanlist[2],kapama=cleanlist[3],sebep=cleanlist[6],uygun=is_not_blank(cleanlist[1]),test_tarihi=timezone.now(),test_personel_id=user_id)
    valf_test.save()
    valf = Valf.objects.get(id=cleanlist[0])
    valf.valf_test_id = valf_test.id
    valf.save()
    return True
    #print(cleanlist)
    #personel_id= Valf_montaj.objects.filter(id=cleanlist[0]).first().montaj_personel_id
    #obj = list(Valf_test.objects.filter(personel_id=personel_id))



@csrf_exempt
def upload_pdf_rapor(request):
    try:
        if request.method == 'POST':
            if request.FILES and request.POST.dict():
                pdf_response = pdf_save_function(file=request.FILES['file'],filename=request.POST.dict()['pdf_ismi'])
                pdf_remark   = pdf_remark_save(data_pdf=request.POST.dict())
                if pdf_response and pdf_remark:
                    return JsonResponse({'status':200,'message': 'Kayıt Başarılı!'})
                else:
                    return JsonResponse({'status':500,'message': 'Kayıt işlemi baraşız!'})
            else:
                return JsonResponse({'status':400,'message': 'Dosya veya Data Hatası!'})  
    except Exception as err:
        return JsonResponse({'status':400,'message':err }) 


def pdf_save_function(file,filename):
    try:
        fs = FileSystemStorage()
        fs.save(filename,file)
        return True
    except Exception as err:
        print(err)
        return False

def pdf_remark_save(data_pdf):
    print(data_pdf['uygun'])
    try:
        if data_pdf['uygun'] == "true":
            
            valf_id=Valf.objects.filter(valf_montaj_id=data_pdf['vsn']).first().valf_test_id
            Valf_test.objects.filter(id=valf_id).update(uygun=True)
        rapor =  PDF_Rapor(istasyon=data_pdf['istasyon'],valf_seri_no=data_pdf['vsn'],pdf_ismi=data_pdf['pdf_ismi'],aciklama=data_pdf['aciklama'])
        rapor.save()
        return True           
    except Exception as err:
        print(err)
        return False


    

# def control_vsn(vsn):
#     try:
#         Valf_test.objects.filter(id)



###############Valf Govde################################

def duplicate_control_govde(id):
    return Valf.objects.filter(valf_montaj_id=id).values_list('valf_govde_id',flat = True).first()

@csrf_exempt
def valf_govde_save(request):
    print("valf_govde_içerde")
    try:
        valf_govde_veri_list = json.loads(request.POST.dict()['veri'])
        valf_main = Valf.objects.get(id=valf_govde_veri_list[0])
        if  duplicate_control_govde(valf_govde_veri_list[0]) is  None:
            if valf_govde_veri_list[4] == True:
                govde = Valf_govde(tork=valf_govde_veri_list[3],tup_seri_no=valf_govde_veri_list[1] ,sodyum_miktari=valf_govde_veri_list[2],govde_personel_id=request.user.id,uygunluk=True)
                print("govde-----True")
            else:
                print("uygundegil")
                govde = Valf_govde(tork=valf_govde_veri_list[3],tup_seri_no=valf_govde_veri_list[1] ,sodyum_miktari=valf_govde_veri_list[2],uygunluk=False,sebep=valf_govde_veri_list[5],govde_personel_id=request.user.id)
            govde.save()
            valf_main.valf_govde_id = govde.id
            valf_main.save()
        else:
            print("duplike var")
            Valf_govde.objects.filter(id=valf_main.valf_govde_id).update(tork=valf_govde_veri_list[3],tup_seri_no=valf_govde_veri_list[1] ,sodyum_miktari=valf_govde_veri_list[2],uygunluk=valf_govde_veri_list[4],sebep=valf_govde_veri_list[5],govde_personel_id=request.user.id)
           
            return JsonResponse({'status':201,'remark':"Güncelleme İşlemi Başarılı!"})
            
      
        return JsonResponse({'status':200,'remark':"Save"})
    except Exception as err:
        print("valf_govde_hata----->",err)
    



##############Valf Govde Kontrol###############################
@csrf_exempt
def GovdekontrolEt(request):
    if request.method == 'POST':
        try:
            valf_id=Valf.objects.filter(valf_montaj_id=request.POST['veri']).values_list('valf_test_id',flat = True).first()       
            if isinstance(valf_id,int):
                Valf_test.objects.filter(id=valf_id).values_list('uygun',flat = True).first()
                if (Valf_test.objects.filter(id=valf_id).values_list('uygun',flat = True).first()):
                    response = {'status':"OK"}
                else:
                    response = {'status':"NO",'remark':"Bu valfin; valf test adımı başarısız!"}
            else:
                response = {'status':"NO",'remark':"Valf Mevcut Değil!"}
        except:
            response = {'status':"NO",'remark':"Sunucu Fonksiyon Hatası!"}

    return JsonResponse(response)


####################Govde Kurlenme Kontrol##############################

@csrf_exempt
def kurlenme_govde(request):
    list_govde=[]
    is_emri_id = request.POST.dict()['is_emri_id']
    for govde in Valf.objects.filter(is_emri_id=is_emri_id).filter(valf_govde_id__isnull=False).values_list('valf_govde_id',flat=True):
        if uygunluk_kontrol(govde):
            dict_govde = {}
            dict_govde['id'] = Valf.objects.filter(valf_govde_id=govde).values_list('id',flat=True).first()
            dict_govde['parti'] = Valf_govde.objects.filter(id=govde).values_list('govde_kurlenme_parti_no',flat=True).first()
            list_govde.append(dict_govde)
        else:
            print("uygun değil")
            pass
    print(list_govde)
    return JsonResponse(list(list_govde),safe=False)
    


    
    #uygunluk = Valf_govde.objects.filter(id=govde_id).values_list('uygunluk',flat=True)
    #print(uygunluk)


def uygunluk_kontrol(govde):
    try:
       print(type(Valf_govde.objects.filter(id=govde).values_list('uygunluk',flat=True).first()))
       return  Valf_govde.objects.filter(id=govde).values_list('uygunluk',flat=True).first()
    except Exception as err:
        print(err)
        return False


################Govde kurlenme Ata############################
@csrf_exempt
def valf_govde_parti_no_ata(request):
    print(request.POST.dict()['is_emri'])
    print(request.POST.dict()['valfler_id'])
    #valf_govde_idleri = Valf.objects.filter(is_emri_id=request.POST.dict()['is_emri']).values_list('valf_govde_id', flat=True)
    emir_valuelist = Emir.objects.filter(id=request.POST.dict()['is_emri']).values_list('id', flat=True)
    #print(Valf.objects.filter(is_emri_id=emir_valuelist[0]).values_list('valf_govde_id',flat=True))
   
    valf_govde_idleri= Valf.objects.filter(is_emri_id=emir_valuelist[0]).filter(valf_govde_id__isnull=False).values_list('valf_govde_id',flat=True)
    print(valf_govde_idleri)

   
    
    kurlenme_parti_noları = []
    try:
        for valf_id in valf_govde_idleri :
            print("değer",valf_id)
            if  Valf_govde.objects.filter(id=valf_id).first().govde_kurlenme_parti_no is None:
                kurlenme_parti_noları.append(0)
            else:   
               kurlenme_parti_noları.append(Valf_govde.objects.filter(id=valf_id).first().govde_kurlenme_parti_no)
        next_parti_no= max(kurlenme_parti_noları) + 1
    except Exception as err:
        print("error",err)
    print("next_parti_no",next_parti_no)




    valfler_id=request.POST.dict()['valfler_id'] 
    print("valfler_id",valfler_id)
    valfler_id_array = json.loads(valfler_id)
    print(valfler_id_array)
    for id in valfler_id_array:
        valf  =  Valf_govde.objects.get(id=id)
        if valf.govde_kurlenme_parti_no is None:
            valf.govde_kurlenme_parti_no=next_parti_no
            valf.govde_kurlenme_baslangic_tarihi = timezone.now()
            valf.govde_kurlenme_bitis_tarihi =  timezone.now()+timezone.timedelta(hours=12)
            valf.govde_kurlenme_personel = User.objects.get(id=request.user.id)
            valf.save()
 
    
    return HttpResponse('OK')



################Govde kurlenme tarih getir##########
@csrf_exempt
def govdemontajKurlenme(request):
    print(request.POST.getlist('parti_no[]'))
    
    montaj_list=[]
    try:
        if  len(request.POST.getlist('parti_no[]')[0]) > 0:
            for parti_no in request.POST.getlist('parti_no[]'):
                clock = Valf_govde.objects.filter(govde_kurlenme_parti_no=parti_no).first().govde_kurlenme_bitis_tarihi - timezone.now()
                montaj={}
                montaj['tarih'] = time_calc(clock)
                montaj['partino'] = parti_no
                valf_no_list=[]
                for valf_no in  Valf_govde.objects.filter(govde_kurlenme_parti_no=parti_no).values_list('id',flat=True):  
                    valf_no_list.append(valf_no)
                montaj['valfno'] = Valf.objects.filter(valf_govde_id=valf_no).values_list('id',flat=True).first()
                print("------------------>",valf_no_list)
                montaj_list.append(montaj)
            return JsonResponse(list(montaj_list),safe=False)
        else:
            return JsonResponse(list(montaj_list),safe=False)
    except Exception as err:
        print(err)
        return JsonResponse(list(montaj_list),safe=False)


def time_calc(data):
    print(data.days)
    if data.days == 0:
        
       return  "{}:{}".format(data.seconds//3600,(data.seconds//60)%60,data.seconds%60)
    else:
        return "Kürleme Bitmiştir"
    