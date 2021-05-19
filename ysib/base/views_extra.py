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
from .models import Emir , Test, Bildirim, Uretim, Valf
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
from base.signals import ping_signal
from django.utils import six 
import itertools
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
        is_emir_valfleri =  Valf_montaj.objects.filter(is_emri=emir)
    except Exception as err:
        is_emir_valfleri =  Valf.objects.filter(is_emri=emir).values_list('valf_montaj',flat=True)
    for is_id in is_emir_valfleri:
        veri={}
        veri['id'] = is_id
        veri['parti_no'] = Valf_montaj.objects.filter(id=is_id).first().kurlenme_parti_no
        temp.append(veri)
        print(temp)
    # temp = []
    # for valf in is_emir_valfleri.values():
    #     temp.append(valf)
    # veri = list(temp)
    print("veriiiiiii",list(temp)) 
    return JsonResponse(list(temp),safe=False)

data_list = []
@csrf_exempt
def valf_test_kayıt(request):
    print("içerde-----< kayıt")
    try:
        
        counter = 0
        for key,value in  dict(request.POST.dict()).items():
            data_list.append(value)
            counter += 1
            if counter % 5 == 0:
                value_list=list_function(counter-5,counter)
                cleandata = control_save_function(value_list)
                control_duplicate = control_duplicate_test(cleandata)
                if isinstance(control_duplicate,list):
                    save_function(control_duplicate,request.user.id) 
                    return JsonResponse({'status':200})   
    except Exception as err:
        print("err")
        return JsonResponse({'status':500})
        #return True



def list_function(first,second):

    #print(list(itertools.islice(data_list, first,second)))
    return list(itertools.islice(data_list, first,second))

def control_save_function(list):
    if list[0]:
        return list

def control_duplicate_test(clean_list):
    valf_test_id = Valf.objects.filter(id=clean_list[0]).first().valf_test_id
    if valf_test_id:
        ''' Mevcut Ama Durum Kontrolü '''
        status = Valf_test.objects.filter(id=valf_test_id).first().uygun
        if status == False:
            ''' Düzeltme İçin Gönderim '''
            return clean_list
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
    print(cleanlist)
    print("save function")
    print("---------------------->",is_not_blank(cleanlist[1]))
    valf_test =Valf_test(acma=cleanlist[2],kapama=cleanlist[3],sebep=cleanlist[4],uygun=is_not_blank(cleanlist[1]),test_tarihi=timezone.now(),test_personel_id=user_id)
    valf_test.save()
    print("----------------")
    print(valf_test)
    valf = Valf.objects.get(id=cleanlist[0])
    valf.valf_test_id = valf_test.id
    valf.save()
    return True
    #print(cleanlist)
    #personel_id= Valf_montaj.objects.filter(id=cleanlist[0]).first().montaj_personel_id
    #obj = list(Valf_test.objects.filter(personel_id=personel_id))