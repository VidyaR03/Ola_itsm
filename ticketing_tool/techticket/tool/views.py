from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from tool.models import cl_Location, cl_Service, cl_Software
from django.contrib.auth import authenticate, login, logout
import random
import datetime
import time
from django.http import JsonResponse
from tool.models import cl_New_organization
from django.db.models import Q
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.template.loader import get_template
# from django.views import View
from django.core.exceptions import BadRequest
from django.http import FileResponse
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import send_mail
from xhtml2pdf import pisa
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

from django.utils import timezone
from datetime import *
from django.contrib.auth.decorators import login_required
from tool.modules.configurationmanagement.ConfigurationManagement import *
from tool.modules.user_logs.user_activity_log import *



@login_required(login_url='/login_render/')
def home(request):
    # print(request.COOKIES['sessionid'])
    return render(request, 'tool/dashboard.html')

@login_required(login_url='/login_render/')
def dashboard(request):
    # print(request.COOKIES['sessionid'])
    return render(request, 'tool/dashboard.html')


def login_render(request):
    return render(request, 'tool/login.html')


def servicenav(request):
    return render(request, 'tool/servicenav.html')

def systemnav(request):
    return render(request, 'tool/systemnav.html')


def sysconfienav(request):
    return render(request, 'tool/sysconfinav.html')


def sysconfiauth(request):
    return render(request, 'tool/sysconfiauth.html')


def admuser(request):
    return render(request, 'tool/admuser.html')


def integrationav(request):
    return render(request, 'tool/integrationav.html')


def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('login')

    context = {'form': form}
    return render(request, 'tool/register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_name = "Mangesh"
            useraction = "Login on Web_page"
            event ="event"
            resultcode = "200"
            user_activity(user_name, useraction, event, resultcode)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect')
    return redirect('home')


def logoutUser(request):
    logout(request)
    return render(request, 'tool/login.html')


def landingPage(request):
    return render(request, 'tool/login.html')


def view_logs(request):
    """
    This function create views of log
    """
    log = user_activity_log.objects.all()
    context = {"log" : log}
    return render(request, 'tool/logs.html', context)

# @login_required(login_url='/login_render/')


def document(request):
    doc = cl_Document.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(doc, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    for entry in doc:
        if entry.disc_Attachment == 'annonymous.pdf':
            entry.disc_Attachment = 'No File'
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            doc = cl_Document.objects.filter(ch_name__icontains=q)        
    context = {
        'doc': doc,
        'users':users
    }
    return render(request, 'tool/document.html', context)


def DocAdd(request):
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=request.POST.get('ch_organization'))
        ch_version = request.POST.get('ch_version')
        txt_description = request.POST.get('txt_description')
        txt_text = request.POST.get('txt_text')
        url_URL = request.POST.get('url_URL')
        try:
            Attachment = request.FILES['disc_Attachment']
        except:
            Attachment = 'annonymous.pdf'
        doc = cl_Document(
            # id=id,
            ch_name=ch_name,
            ch_organization=ch_organization,
            ch_version=ch_version,
            txt_description=txt_description,
            txt_text=txt_text,
            url_URL=url_URL,
            disc_Attachment = Attachment
        )
        doc.save()
        return redirect('document')
    return render(request, 'tool/document.html')


def DocEdit(request,id):
    doc = cl_Document.objects.filter(id=id).first()
    context = {
        'doc': doc,
    }
    return render(request, 'tool/document.html', context)


def DocUpdate(request, id):
    if request.method == "POST":
        discl = cl_Document.objects.filter(id = id).first()
        attachment_name = request.POST.get('disc_Attachment')
        if discl.disc_Attachment == attachment_name:
            # id = request.POST.get('id')
            ch_name = request.POST.get('ch_name')
            ch_organization = cl_New_organization.objects.get(ch_name=request.POST.get('ch_organization'))
            ch_version = request.POST.get('ch_version')
            txt_description = request.POST.get('txt_description')
            txt_text = request.POST.get('txt_text')
            url_URL = request.POST.get('url_URL')
      
            doc = cl_Document(
                id=id,
                ch_name=ch_name,
                ch_organization=ch_organization,
                ch_version=ch_version,
                txt_description=txt_description,
                txt_text=txt_text,
                url_URL=url_URL,
                disc_Attachment = attachment_name,
        
            )
            doc.save()
            return redirect('document')
        # return render(request, 'tool/document.html')

        else:
            ch_name=request.POST.get('ch_name')
            ch_organization = cl_New_organization.objects.get(ch_name=request.POST.get('ch_organization'))
            ch_version=request.POST.get('ch_version')
            txt_description=request.POST.get('txt_description')
            txt_text=request.POST.get('txt_text')
            url_URL=request.POST.get('url_URL')
            try:
                Attachment = request.FILES['disc_Attachment']
            except:
                Attachment = 'annonymous.pdf'
            doc = cl_Document(
                id = id,
                ch_name=ch_name,
                ch_organization=ch_organization,
                ch_version=ch_version,
                txt_description=txt_description,
                txt_text=txt_text,
                url_URL=url_URL,
                disc_Attachment = Attachment,
            )
            doc.save()
            return redirect('document')
    return render(request, 'tool/document.html')


def DocDelete(request,id):
    doc = cl_Document.objects.filter(id=id)
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            doc = cl_Document.objects.filter(id=i).first()
            doc.delete()
    doc.delete()
    context = {
        'doc': doc,
    }
    return redirect('document')


def DeleteAttachedPDF(request,id):
    print('function called')
    id = request.GET['id']
    doc = cl_Document.objects.filter(id = id).first()
    file_to_delete = str(doc.disc_Attachment)
    media_path = settings.MEDIA_ROOT
    file_path = os.path.join(media_path, file_to_delete)
    print(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
        return HttpResponse(request, 'tool/document.html')
    else:
        return HttpResponse(request, 'tool/document.html')



def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None




class ViewAttachedPDF(View):
	def get(self, request, path):
            media_path = settings.MEDIA_ROOT
            file_path = os.path.join(media_path, path)
            print(file_path)
            return FileResponse(open(file_path, 'rb'), content_type='application/')



############## Location ##########

def Location(request):
    loc = cl_Location.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(loc, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            org = cl_New_organization.objects.filter(ch_location_name__icontains=q)

    context = {
        'loc': loc,
        'users':users
    }
    return render(request, 'tool/location.html', context)



@login_required(login_url='/login_render/')

def LADD(request):
    if request.method == "POST":
        ch_location_name = request.POST.get('ch_location_name')
        txt_address = request.POST.get('txt_address')

        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        print('organization :', ch_organization)

        ch_city = request.POST.get('ch_city')
        i_pincode = request.POST.get('i_pincode')
        ch_country = request.POST.get('ch_country')
        ch_status = request.POST.get('ch_status')

        loc = cl_Location(
            ch_location_name=ch_location_name,
            txt_address=txt_address,
            ch_organization=ch_organization,
            ch_city=ch_city,
            i_pincode=i_pincode,
            ch_country=ch_country,
            ch_status=ch_status,
        )
        loc.save()
        return redirect('location')
    return render(request, 'tool/location.html')



@login_required(login_url='/login_render/')

def LEdit(request):
    loc = cl_Location.objects.all()
    context = {
        'loc': loc,
    }
    return render(request, 'tool/location.html', context)



@login_required(login_url='/login_render/')

def LUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_location_name = request.POST.get('ch_location_name')
        txt_address = request.POST.get('txt_address')
        ch_organization = request.POST.get('ch_owner_organization')
        ch_city = request.POST.get('ch_city')
        i_pincode = request.POST.get('i_pincode')
        ch_country = request.POST.get('ch_country')
        ch_status = request.POST.get('ch_status')

        loc = cl_Location(
            id=id,
            ch_location_name=ch_location_name,
            txt_address=txt_address,
            ch_organization=ch_organization,
            ch_city=ch_city,
            i_pincode=i_pincode,
            ch_country=ch_country,
            ch_status=ch_status,
        )
        loc.save()
        return redirect('location')
    return redirect(request, 'tool/location.html')


# @login_required(login_url='/login_render/')
def LDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            loc = cl_Location.objects.filter(id=i).first()
            loc.delete()

    context = {
        'loc': loc,
    }
    return redirect('location')


@login_required(login_url='/login_render/')

def new_organization(request):
    org = cl_New_organization.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(org, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            org = cl_New_organization.objects.filter(ch_name__icontains=q)
    return render(request, 'tool/neworganization.html', {'org': org,'users':users})



@login_required(login_url='/login_render/')

def OrgADD(request):
    if request.method == "POST":
        ch_name = str.capitalize(request.POST.get('ch_name'))
        ch_code = request.POST.get('ch_code')
        ch_status = request.POST.get('ch_status')
        ch_parent = request.POST.get('ch_parent')
        ch_delivery_model = request.POST.get('ch_delivery_model')
        org = cl_New_organization(
            ch_name=ch_name,
            ch_code=ch_code,
            ch_status=ch_status,
            ch_parent=ch_parent,
            ch_delivery_model=ch_delivery_model,
        )
        org.save()
        return redirect('new_organization')
    return render(request, 'tool/neworganization.html')



@login_required(login_url='/login_render/')

def OrgEdit(request):
    org = cl_New_organization.objects.all()
    context = {
        'org': org,
    }
    return render(request, 'tool/neworganization.html', context)



@login_required(login_url='/login_render/')

def OrgUpdate(request):
    if request.method == "POST":
        ch_name = request.POST.get('ch_name')
        ch_code = request.POST.get('ch_code')
        ch_status = request.POST.get('ch_status')
        ch_parent = request.POST.get('ch_parent')
        ch_delivery_model = request.POST.get('ch_delivery_model')

        org = cl_New_organization(
            ch_name=ch_name,
            ch_code=ch_code,
            ch_status=ch_status,
            ch_parent=ch_parent,
            ch_delivery_model=ch_delivery_model,

        )
        org.save()
        return redirect('new_organization')
    return render(request, 'tool/neworganization.html')


@login_required(login_url='/login_render/')

def OrgDelete(request):
    org = cl_New_organization.objects.filter()
    org.delete()
    context = {
        'org': org,
    }
    return redirect('new_organization')


@login_required(login_url='/login_render/')
def client(request):    
    per = cl_Person.objects.all()
    org = cl_New_organization.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(per, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            per = cl_Person.objects.filter(ch_person_firstname__icontains=q)
    return render(request, 'tool/client.html', {'per': per, 'org':org,'users':users})


#     context={
#         'per':per,
#     }
#     return render(request,'tool/client.html',context)


@login_required(login_url='/login_render/')
def ADD(request):
    if request.method == "POST":
        ch_person_firstname = str.capitalize(
            request.POST.get('ch_person_firstname'))
        ch_person_lastname = str.capitalize(
            request.POST.get('ch_person_lastname'))
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        ch_team = cl_Team.objects.get(
            ch_teamname=str.capitalize(request.POST.get('ch_team')))
        ch_person_status = str.capitalize(request.POST.get('ch_person_status'))
        ch_person_location = str.capitalize(
            request.POST.get('ch_person_location'))
        ch_person_function = str.capitalize(
            request.POST.get('ch_person_function'))
        ch_manager = str.capitalize(request.POST.get('ch_manager'))
        ch_employee_number = str.upper(request.POST.get('ch_employee_number'))
        e_person_email = str.lower(request.POST.get('e_person_email'))
        ch_person_phone = request.POST.get('ch_person_phone')
        ch_person_mobilenumber = request.POST.get('ch_person_mobilenumber')

        per = cl_Person(
            ch_person_firstname=ch_person_firstname,
            ch_person_lastname=ch_person_lastname,
            ch_organization=ch_organization,
            ch_team=ch_team,
            ch_person_status=ch_person_status,
            ch_person_location=ch_person_location,
            ch_person_function=ch_person_function,
            ch_manager=ch_manager,
            ch_employee_number=ch_employee_number,
            e_person_email=e_person_email,
            ch_person_phone=ch_person_phone,
            ch_person_mobilenumber=ch_person_mobilenumber,
        )
        per.save()
        return redirect('client')
    return render(request, 'tool/client.html')



@login_required(login_url='/login_render/')

def Edit(request):
    per = cl_Person.objects.all()
    context = {
        'per': per,
    }
    return render(request, 'tool/client.html', context)


# @login_required(login_url='/login_render/')
def Update(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_person_firstname = request.POST.get('ch_person_firstname')
        ch_person_lastname = request.POST.get('ch_person_lastname')
        ch_organization = cl_New_organization.objects.get(ch_name = request.POST.get('ch_organization'))    
        ch_team = cl_Team.objects.get(ch_teamname=str.capitalize(request.POST.get('ch_team')))
        ch_person_status = request.POST.get('ch_person_status')
        ch_person_location = request.POST.get('ch_person_location')
        ch_person_function = request.POST.get('ch_person_function')
        ch_manager = request.POST.get('ch_manager')
        ch_employee_number = request.POST.get('ch_employee_number')
        e_person_email = request.POST.get('e_person_email')
        ch_person_phone = request.POST.get('ch_person_phone')
        ch_person_mobilenumber = request.POST.get('ch_person_mobilenumber')

        per = cl_Person(
            id=id,
            ch_person_firstname=ch_person_firstname,
            ch_person_lastname=ch_person_lastname,
            ch_organization=ch_organization,
            ch_team=ch_team,
            ch_person_status=ch_person_status,
            ch_person_location=ch_person_location,
            ch_person_function=ch_person_function,
            ch_manager=ch_manager,
            ch_employee_number=ch_employee_number,
            e_person_email=e_person_email,
            ch_person_phone=ch_person_phone,
            ch_person_mobilenumber=ch_person_mobilenumber,
        )
        per.save()
        return redirect('client')
    return render(request, 'tool/client.html')


# @login_required(login_url='/login_render/')
def Delete(request):
   if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            per = cl_Person.objects.filter(id=i).first()
            per.delete()
            context = {
                'per': per,
            }
        return redirect('client')

########### Document #####################

def document(request):
    doc = cl_Document.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(doc, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    for entry in doc:
        if entry.disc_Attachment == 'annonymous.pdf':
            entry.disc_Attachment = 'No File'
    
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            doc = cl_Document.objects.filter(ch_name__icontains=q)        

    context = {
        'doc': doc,
        'users':users
    }
    return render(request, 'tool/document.html', context)

def DocAdd(request):
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=request.POST.get('ch_organization'))
        ch_version = request.POST.get('ch_version')
        txt_description = request.POST.get('txt_description')
        txt_text = request.POST.get('txt_text')
        url_URL = request.POST.get('url_URL')
        try:
            Attachment = request.FILES['disc_Attachment']
        except:
            Attachment = 'annonymous.pdf'
        doc = cl_Document(
            # id=id,
            ch_name=ch_name,
            ch_organization=ch_organization,
            ch_version=ch_version,
            txt_description=txt_description,
            txt_text=txt_text,
            url_URL=url_URL,
            disc_Attachment = Attachment
        )
        doc.save()
        return redirect('document')
    return render(request, 'tool/document.html')


def DocEdit(request,id):
    doc = cl_Document.objects.filter(id=id).first()
    context = {
        'doc': doc,
    }
    return render(request, 'tool/document.html', context)

def DocUpdate(request, id):
    if request.method == "POST":
        discl = cl_Document.objects.filter(id = id).first()
        attachment_name = request.POST.get('disc_Attachment')
        if discl.disc_Attachment == attachment_name:
            # id = request.POST.get('id')
            ch_name = request.POST.get('ch_name')
            ch_organization = cl_New_organization.objects.get(ch_name=request.POST.get('ch_organization'))
            ch_version = request.POST.get('ch_version')
            txt_description = request.POST.get('txt_description')
            txt_text = request.POST.get('txt_text')
            url_URL = request.POST.get('url_URL')
      
            doc = cl_Document(
                id=id,
                ch_name=ch_name,
                ch_organization=ch_organization,
                ch_version=ch_version,
                txt_description=txt_description,
                txt_text=txt_text,
                url_URL=url_URL,
                disc_Attachment = attachment_name,
        
            )
            doc.save()
            return redirect('document')
        # return render(request, 'tool/document.html')

        else:
            ch_name=request.POST.get('ch_name')
            ch_organization = cl_New_organization.objects.get(ch_name=request.POST.get('ch_organization'))
            ch_version=request.POST.get('ch_version')
            txt_description=request.POST.get('txt_description')
            txt_text=request.POST.get('txt_text')
            url_URL=request.POST.get('url_URL')
            try:
                Attachment = request.FILES['disc_Attachment']
            except:
                Attachment = 'annonymous.pdf'
            doc = cl_Document(
                id = id,
                ch_name=ch_name,
                ch_organization=ch_organization,
                ch_version=ch_version,
                txt_description=txt_description,
                txt_text=txt_text,
                url_URL=url_URL,
                disc_Attachment = Attachment,
            )
            doc.save()
            return redirect('document')
    return render(request, 'tool/document.html')


def DocDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            doc = cl_Document.objects.filter(id=i)
            doc.delete()
    context = {
        'doc': doc,
    }
    return redirect('document')


def DeleteAttachedPDF(request,id):
    print('function called')
    id = request.GET['id']
    doc = cl_Document.objects.filter(id = id).first()
    file_to_delete = str(doc.disc_Attachment)
    media_path = settings.MEDIA_ROOT
    file_path = os.path.join(media_path, file_to_delete)
    print(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
        return HttpResponse(request, 'tool/document.html')
    else:
        return HttpResponse(request, 'tool/document.html')



def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None



###################  Software #####################


def software(request):
    soft = cl_Software.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(soft, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

   
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            soft = cl_Software.objects.filter(ch_teamname__icontains=q)
        return render(request, 'tool/software.html', {'soft': soft,'users':users})


def softAdd(request):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_sofname = request.POST.get('ch_sofname')
        # ch_organization = cl_New_organization.objects.get(ch_name = request.POST.get('ch_organization'))
        # print('organization :',ch_organization)
        ch_vendor = request.POST.get('ch_vendor')
        chversion = request.POST.get('chversion')
        ch_type = request.POST.get('ch_type')
        soft = cl_Software(
            id=id,
            ch_sofname=ch_sofname,
            ch_vendor=ch_vendor,
            chversion=chversion,
            ch_type=ch_type,
        )
        soft.save()
        return redirect('software')
    return render(request, 'tool/software.html')


def softEdit(request):
    soft = cl_Software.objects.all()
    context = {
        'soft': soft,
    }
    return render(request, 'tool/software.html', context)


def softUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_sofname = request.POST.get('ch_sofname')
        ch_vendor = request.POST.get('ch_vendor')
        chversion = request.POST.get('chversion')
        ch_type = request.POST.get('ch_type')
        soft = cl_Software(
            id=id,
            ch_sofname=ch_sofname,
            ch_vendor=ch_vendor,
            chversion=chversion,
            ch_type=ch_type,
        )
        soft.save()
        return redirect('software')
    return redirect(request, 'tool/software.html')


def softDelete(request):
   if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            soft = cl_Software.objects.filter(id=i).first()
            soft.delete()
            context = {
                'soft': soft,
            }
        return redirect('software')






################### Team ######################


# @login_required(login_url='/login_render/')
def team(request):
    if request.method == "GET":
        tem = cl_Team.objects.all()
        org = cl_New_organization.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(tem, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        q = request.GET.get('searchname')
        if q != None:
            tem = cl_Team.objects.filter(ch_teamname__icontains=q)
    return render(request, 'tool/service.html', {'tem': tem, 'org':org,'users':users})


# @login_required(login_url='/login_render/')
def TADD(request):
    if request.method == "POST":
        # id = request.POST.get('id')
        print('organization :',request.POST.get('ch_organization'))
        ch_teamname = request.POST.get('ch_teamname')
        ch_teamstatus = request.POST.get('ch_teamstatus')
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        e_team_emailfield = str.lower(request.POST.get('e_team_emailfield'))
        i_team_phonenumber = request.POST.get('i_team_phonenumber')
        b_team_notification = request.POST.get('b_team_notification')
        ch_team_function = request.POST.get('ch_team_function')
        tem = cl_Team(

            # id=id,
            ch_teamname=ch_teamname,
            ch_teamstatus=ch_teamstatus,
            ch_organization=ch_organization,
            e_team_emailfield=e_team_emailfield,
            i_team_phonenumber=i_team_phonenumber,
            b_team_notification=b_team_notification,
            ch_team_function=ch_team_function,
        )
        tem.save()
        return redirect('team')
    return render(request, 'tool/service.html')



@login_required(login_url='/login_render/')

def TEdit(request):
    tem = cl_Team.objects.all()
    context = {
        'tem': tem,
    }
    return render(request, 'tool/service.html', context)



@login_required(login_url='/login_render/')

def TUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_teamname = request.POST.get('ch_teamname')
        ch_teamstatus = request.POST.get('ch_teamstatus')
        ch_organization = cl_New_organization.objects.get(ch_name = request.POST.get('ch_organization'))        
        e_team_emailfield = str.lower(request.POST.get('e_team_emailfield'))
        i_team_phonenumber = request.POST.get('i_team_phonenumber')
        b_team_notification = request.POST.get('b_team_notification')
        ch_team_function = request.POST.get('ch_team_function')
        tem = cl_Team(
            id=id,
            ch_teamname=ch_teamname,
            ch_teamstatus=ch_teamstatus,
            ch_organization=ch_organization,
            e_team_emailfield=e_team_emailfield,
            i_team_phonenumber=i_team_phonenumber,
            b_team_notification=b_team_notification,
            ch_team_function=ch_team_function,
        )
        tem.save()
        return redirect('team')
    return render(request, 'tool/service.html')

# @login_required(login_url='/login_render/')
def TDelete(request):
   if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            tem = cl_Team.objects.filter(id=i).first()
            tem.delete()
            context = {
                'tem': tem,
            }
        return redirect('team')



 
################### New channge   #############################

@login_required(login_url='/login_render/')
def newchange(request):
    nchange = cl_New_change.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(nchange, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.method == "GET":
        allteam = cl_Team.objects.all()
        team_person = cl_Person.objects.all()
    q = request.GET.get('searchstatus')
    if q != None:
        nchange = cl_New_change.objects.filter(ch_status__icontains=q)
    return render(request, 'tool/newchange.html', {'nchange': nchange, 'allteam': allteam, 'team_person': team_person,'users':users})


@login_required(login_url='/login_render/')
def CADD(request):
    if request.method == "POST":

        print('organization :', request.POST.get('ch_organization'))
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_caller =cl_Person.objects.get(
            ch_person_firstname=str.capitalize(request.POST.get('ch_caller')))
        ch_status = request.POST.get('ch_status')
        ch_category = request.POST.get('ch_category')
        ch_title = request.POST.get('ch_title')
        dt_start_date = request.POST.get('dt_start_date')
        dt_Updated_date = request.POST.get('dt_Updated_date')
        ch_parent_change = request.POST.get('ch_parent_change')
        txt_fallback_plan = request.POST.get('txt_fallback_plan')
        txt_description = request.POST.get('txt_description')
        nchange = cl_New_change(
            ch_organization=ch_organization,
            ch_caller=ch_caller,
            ch_status=ch_status,
            ch_category=ch_category,
            ch_title=ch_title,
            dt_start_date=dt_start_date,
            dt_Updated_date=dt_Updated_date,
            ch_parent_change=ch_parent_change,
            txt_fallback_plan=txt_fallback_plan,
            txt_description = txt_description,

        )
        nchange.save()
        return redirect('newchange')
    return render(request, 'tool/newchange.html')


@login_required(login_url='/login_render/')
def CEdit(request):
    nchange = cl_New_change.objects.all()
    context = {
        'nchange': nchange,
    }
    return render(request, 'tool/newchange.html', context)


@login_required(login_url='/login_render/')
def CUpdate(request, id):
    """
    Function for update change_information
    """
    if request.method == "POST":
        nchange = cl_New_change.objects.filter(id=id).first()
        id = request.POST.get('id')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_caller =cl_Person.objects.get(
            ch_person_firstname=str.capitalize(request.POST.get('ch_caller')))
        ch_status = request.POST.get('ch_status')
        ch_category = request.POST.get('ch_category')
        ch_title = request.POST.get('ch_title')
        dt_start_date = nchange.dt_start_date
        # dt_start_date = request.POST.get('dt_start_date')
        dt_Updated_date = request.POST.get('dt_Updated_date')
        ch_parent_change = request.POST.get('ch_parent_change')
        txt_fallback_plan = request.POST.get('txt_fallback_plan')
        txt_description = request.POST.get('txt_description')
        nchange = cl_New_change(
            id=id,
            ch_organization=ch_organization,
            ch_caller=ch_caller,
            ch_status=ch_status,
            ch_category=ch_category,
            ch_title=ch_title,
            dt_start_date=dt_start_date,
            dt_Updated_date=dt_Updated_date,
            ch_parent_change=ch_parent_change,
            txt_fallback_plan=txt_fallback_plan,
            txt_description=txt_description,

        )
        nchange.save()
        return redirect('newchange')
    return render(request, 'tool/newchange.html')


@login_required(login_url='/login_render/')
def CDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            nchange = cl_New_change.objects.filter(id=i).first()
            nchange.delete()
            context = {
                'nchange': nchange,
            }
        return redirect('newchange')


@login_required(login_url='/login_render/')
def assign_changeModal(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        p_Emp_id = request.POST.get('p')
        print(list_id)
        print(p_Emp_id)
        per = cl_Person.objects.filter(ch_employee_number=p_Emp_id).first()
        for i in list_id:
            nchange = cl_New_change.objects.filter(id=i).first()
            nchange.ch_assign_agent = per.ch_person_firstname
            nchange.save()
        try:
            subject = 'Welcome to Olatech Solutions'
            message = 'Hope you are enjoying your Olatech Services'
            sender = settings.EMAIL_HOST_USER
            recepient = per.e_person_email,
            send_mail(subject, message, sender, [
                      recepient], fail_silently=False)
        except:
            print('email not send')

        nchange = cl_New_change.objects.all()
        context = {
            'nchange': nchange,
        }
    return render(request, 'tool/tassign.html', context)


#############################################################

@login_required(login_url='/login_render/')
def user_request(request):
    ur = cl_User_request.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(ur, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        ur = cl_User_request.objects.all()
        q = request.GET.get('searchstatus')
        if q != None:
            ur = cl_User_request.objects.filter(ch_status__icontains=q)
        escalated_ur = escalation(ur)

        context = {
            'ur': ur,
            'escalated_ur': escalated_ur,
            'users':users
            }
        return render(request, 'tool/userrequest.html', context)

def escalation(ur):
    escalated_ur = []
    for req in ur:
        if datetime.date(req.dt_escalation_date) < datetime.date(datetime.now()) and req.ch_agent == 'Deallocate':
            escalated_ur.append(req)
        elif datetime.date(req.dt_escalation_date) == datetime.date(datetime.now()) and datetime.time(req.dt_escalation_date) < datetime.time(datetime.now()):
            escalated_ur.append(req)
    return escalated_ur


@login_required(login_url='/login_render/')
def UADD(request):
    if request.method == "POST":
        id = request.POST.get('id')
        print(id)
        fk_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        fk_caller = cl_Person.objects.get(
            ch_person_firstname=str.capitalize(request.POST.get('ch_Person')))
        # fk_caller = request.POST.get('ch_Person')
        ch_status = request.POST.get('ch_status')
        ch_origin = request.POST.get('ch_origin')
        ch_title = request.POST.get('ch_title')
        ch_request_type = request.POST.get('ch_request_type')
        ch_impact = request.POST.get('ch_impact')
        ch_urgency = request.POST.get('ch_urgency')
        ch_priority = request.POST.get('ch_priority')   
        dt_start_date = request.POST.get('dt_start_date')
        dt_updated_date = request.POST.get('dt_updated_date')
        dt_escalation_date = request.POST.get('dt_escalation_date')
        ch_service = request.POST.get('ch_service')
        ch_service_subcategory = request.POST.get('ch_service_subcategory')
        ch_parent_request = request.POST.get('ch_parent_request')
        ch_parent_change = request.POST.get('ch_parent_change')
        txt_description = request.POST.get('txt_description')
        ur = cl_User_request(
            fk_organization=fk_organization,
            fk_caller=fk_caller,
            ch_status=ch_status,
            ch_origin=ch_origin,
            ch_title=ch_title,
            ch_request_type=ch_request_type,
            ch_impact=ch_impact,
            ch_urgency=ch_urgency,
            ch_priority=ch_priority,

            dt_start_date =dt_start_date,
            dt_updated_date =dt_updated_date,
            dt_escalation_date = dt_escalation_date,
            ch_service =ch_service,
            ch_service_subcategory =ch_service_subcategory,
            ch_parent_request=ch_parent_request,
            ch_parent_change =ch_parent_change,
            txt_description =txt_description,

        )
        ur.save()
        return redirect('userrequest')
    return render(request, 'tool/userrequest.html')


@login_required(login_url='/login_render/')
def UEdit(request):
    ur = cl_User_request.objects.all()
    context = {
        'ur': ur,
    }
    return render(request, 'tool/userrequest.html', context)


@login_required(login_url='/login_render/')
def UUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        fk_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        fk_caller = cl_Person.objects.get(
            ch_person_firstname=str.capitalize(request.POST.get('ch_Person')))
        ch_status = request.POST.get('ch_status')
        ch_origin = request.POST.get('ch_origin')
        ch_title = request.POST.get('ch_title')
        ch_request_type = request.POST.get('ch_request_type')
        ch_impact = request.POST.get('ch_impact')
        ch_urgency = request.POST.get('ch_urgency')
        ch_priority = request.POST.get('ch_priority')
        dt_start_date = request.POST.get('dt_start_date')
        dt_end_date = request.POST.get('dt_end_date')
        ch_service = request.POST.get('ch_service')
        ch_service_subcategory = request.POST.get('ch_service_subcategory')
        ch_parent_request = request.POST.get('ch_parent_request')
        # dt_tto = request.POST.get('ch_tto')
        # dt_ttr=request.POST.get('ch_tto')
        ch_parent_change = request.POST.get('ch_parent_change')
        txt_description = request.POST.get('txt_description')
        ur = cl_User_request(
            id=id,
            fk_organization=fk_organization,
            fk_caller=fk_caller,
            ch_status=ch_status,
            ch_origin=ch_origin,
            ch_title=ch_title,
            ch_request_type=ch_request_type,
            ch_impact=ch_impact,
            ch_urgency=ch_urgency,
            ch_priority=ch_priority,
            dt_start_date=dt_start_date,
            dt_end_date=dt_end_date,
            ch_service=ch_service,
            ch_service_subcategory=ch_service_subcategory,
            ch_parent_request=ch_parent_request,
            # dt_tto=dt_tto,
            # dt_ttr=dt_ttr,
            ch_parent_change =ch_parent_change,
            txt_description =txt_description,
        )
        ur.save()
        # print(ur)

        return redirect('userrequest')
    return render(request, 'tool/userrequest.html')


@login_required(login_url='/login_render/')
def UDelete(request, id):
    ur = cl_User_request.objects.filter(id=id)
    ur.delete()
    context = {
        'ur': ur,
    }
    return redirect('userrequest')


@login_required(login_url='/login_render/')
def escalate_notify(request):
    ur = cl_User_request.objects.all()
    return render(request, 'tool/userrequest.html', {'ur': ur})


#######################################################

@login_required(login_url='/login_render/')
def customer_contract(request):
    cust = cl_Customer_contract.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(cust, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
   
    if request.method == "GET":
        q = request.GET.get('searchstatus')
        if q != None:
            cust = cl_Customer_contract.objects.filter(ch_status__icontains=q)
    return render(request, 'tool/scustomer_contract.html', {'cust': cust,'users':users})


@login_required(login_url='/login_render/')
def SCADD(request):
    if request.method == "POST":
        # org_id = cl_New_organization.objects.get(ch_name = request.POST.get('ch_organization'
        # id = request.POST.get('id')

        ch_cname = request.POST.get('ch_cname')
        ch_ccustomer = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_contract_type = request.POST.get('ch_contract_type')
        ch_pprovider = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        dt_start_date = request.POST.get('dt_start_date')
        dt_end_date = request.POST.get('dt_end_date')
        i_cost_unit = request.POST.get('i_cost_unit')
        i_cost = request.POST.get('i_cost')
        i_cost_currency = request.POST.get('i_cost_currency')
        i_billing_frequency = request.POST.get('i_billing_frequency')
        txt_description = request.POST.get('txt_description')
        cust = cl_Customer_contract(
            # id=id,
            ch_cname=ch_cname,
            ch_ccustomer=ch_ccustomer,
            ch_status=ch_status,
            ch_contract_type=ch_contract_type,
            ch_pprovider=ch_pprovider,
            dt_start_date=dt_start_date,
            dt_end_date=dt_end_date,
            i_cost_unit=i_cost_unit,
            i_cost=i_cost,
            i_cost_currency=i_cost_currency,
            i_billing_frequency=i_billing_frequency,
            txt_description=txt_description,
        )
        cust.save()
        # print(nchange)

        return redirect('customercontract')
    return render(request, 'tool/scustomer_contract.html')


@login_required(login_url='/login_render/')
def SCEdit(request):
    cust = cl_Customer_contract.objects.all()
    context = {
        'cust': cust,
    }
    return render(request, 'tool/scustomer_contract.html', context)


@login_required(login_url='/login_render/')
def SCUpdate(request, id):
    """
    Function for update change_information
    """
    if request.method == "POST":
        id = request.POST.get('id')
        ch_cname = request.POST.get('ch_cname')
        ch_ccustomer = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_contract_type = request.POST.get('ch_contract_type')
        ch_pprovider = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        dt_start_date = request.POST.get('dt_start_date')
        dt_end_date = request.POST.get('dt_end_date')
        i_cost_unit = request.POST.get('i_cost_unit')
        i_cost = request.POST.get('i_cost')
        i_cost_currency = request.POST.get('i_cost_currency')
        i_billing_frequency = request.POST.get('i_billing_frequency')
        txt_description = request.POST.get('txt_description')
        cust = cl_Customer_contract(
            id=id,

            ch_cname=ch_cname,
            ch_ccustomer=ch_ccustomer,
            ch_status=ch_status,
            ch_contract_type=ch_contract_type,
            ch_provider=ch_pprovider,
            dt_start_date=dt_start_date,
            dt_end_date=dt_end_date,
            i_cost_unit=i_cost_unit,
            i_cost=i_cost,
            i_cost_currency=i_cost_currency,
            i_billing_frequency=i_billing_frequency,
            txt_description=txt_description,
        )
        cust.save()

        # print(nchange)
        return redirect('customercontract')

    return render(request, 'tool/scustomer_contract.html')


@login_required(login_url='/login_render/')
def SCDelete(request, id):
    # nchange = cl_New_change.objects.filter(id = id)
    # nchange.delete()
    cust = cl_Customer_contract.objects.filter(id=id)

    cust.delete()

    # return redirect('newchange')

    context = {
        'cust': cust,
    }
    return redirect('customercontract')


@login_required(login_url='/login_render/')
def provider_contract(request):
    pro = cl_Providercontract.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(pro, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
   
    if request.method == "GET":
        q = request.GET.get('searchstatus')
        if q != None:
            pro = cl_Customer_contract.objects.filter(ch_status__icontains=q)
    return render(request, 'tool/sprovidercontract.html', {'pro': pro,'users':users})


@login_required(login_url='/login_render/')
def SPADD(request):
    if request.method == "POST":
        ch_pname = request.POST.get('ch_pname')
        ch_customer = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_contract_type = request.POST.get('ch_contract_type')
        ch_pcprovider = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        dt_start_date = request.POST.get('dt_start_date')
        dt_end_date = request.POST.get('dt_end_date')
        i_cost_unit = request.POST.get('i_cost_unit')
        i_cost = request.POST.get('i_cost')
        i_cost_currency = request.POST.get('i_cost_currency')
        i_billing_frequency = request.POST.get('i_billing_frequency')
        txt_description = request.POST.get('txt_description')
        ch_sla = request.POST.get('ch_sla')

        pro = cl_Providercontract(
            # id=id,
            ch_pname=ch_pname,
            ch_customer=ch_customer,
            ch_status=ch_status,
            ch_contract_type=ch_contract_type,
            ch_pcprovider=ch_pcprovider,
            dt_start_date=dt_start_date,
            dt_end_date=dt_end_date,
            i_cost_unit=i_cost_unit,
            i_cost=i_cost,
            i_cost_currency=i_cost_currency,
            i_billing_frequency=i_billing_frequency,
            txt_description=txt_description,
            ch_sla=ch_sla,
        )
        pro.save()
        # print(nchange)

        return redirect('providercontract')

    return render(request, 'tool/sprovidercontract.html')


@login_required(login_url='/login_render/')
def SPEdit(request):
    pro = cl_Providercontract.objects.all()
    context = {
        'pro': pro,
    }
    return render(request, 'tool/sprovidercontract.html', context)


@login_required(login_url='/login_render/')
def SPUpdate(request, id):
    """
    Function for update change_information
    """
    if request.method == "POST":
        # org_id = cl_New_organization.objects.get(ch_name = request.POST.get('ch_organization'))
        # print('o_id = ',org_id)
        # ch_organization = org_id
        id = request.POST.get('id')

        print('organization :', request.POST.get('ch_organization'))
        ch_pname = request.POST.get('ch_pname')
        ch_customer = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))

        ch_status = request.POST.get('ch_status')
        ch_contract_type = request.POST.get('ch_contract_type')
        ch_pcprovider = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))

        dt_start_date = request.POST.get('dt_start_date')
        dt_end_date = request.POST.get('dt_end_date')
        i_cost_unit = request.POST.get('i_cost_unit')
        i_cost = request.POST.get('i_cost')
        i_cost_currency = request.POST.get('i_cost_currency')
        i_billing_frequency = request.POST.get('i_billing_frequency')
        txt_description = request.POST.get('txt_description')
        ch_sla = request.POST.get('ch_sla')

        pro = cl_Providercontract(
            id=id,
            ch_pname=ch_pname,
            ch_customer=ch_customer,
            ch_status=ch_status,
            ch_contract_type=ch_contract_type,
            ch_pcprovider=ch_pcprovider,
            dt_start_date=dt_start_date,
            dt_end_date=dt_end_date,
            i_cost_unit=i_cost_unit,
            i_cost=i_cost,
            i_cost_currency=i_cost_currency,
            i_billing_frequency=i_billing_frequency,
            txt_description=txt_description,
            ch_sla=ch_sla,
        )
        pro.save()
        # print(nchange)

        return redirect('providercontract')

    return render(request, 'tool/sprovidercontract.html')


@login_required(login_url='/login_render/')
def SPDelete(request, id):
    # nchange = cl_New_change.objects.filter(id = id)
    # nchange.delete()
    pro = cl_Providercontract.objects.filter(id=id)

    pro.delete()

    # return redirect('newchange')

    context = {
        'pro': pro,
    }
    return redirect('providercontract')


@login_required(login_url='/login_render/')
def servicefamilies(request):
    sf = cl_Servicefamilies.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(sf, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            sf = cl_Servicefamilies.objects.filter(ch_sname__icontains=q)

    context = {
        'sf': sf,
        'users':users
    }
    return render(request, 'tool/sservicefamily.html', context)


@login_required(login_url='/login_render/')
def SFADD(request):
    if request.method == "POST":
        id = request.POST.get('id')

        ch_sname = request.POST.get('ch_sname')

        sf = cl_Servicefamilies(
            id=id,
            ch_sname=ch_sname,


        )
        sf.save()
        return redirect('servicefamilies')
    return render(request, 'tool/sservicefamily..html')


@login_required(login_url='/login_render/')
def SFEdit(request):
    sf = cl_Servicefamilies.objects.all()
    context = {
        'sf': sf,
    }
    return render(request, 'tool/sservicefamily.html', context)


@login_required(login_url='/login_render/')
def SFUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_sname = request.POST.get('ch_sname')

        sf = cl_Servicefamilies(
            id=id,
            ch_sname=ch_sname,

        )
        sf.save()
        return redirect('servicefamilies')
    return redirect(request, 'tool/sservicefamily.html')


@login_required(login_url='/login_render/')
def SFDelete(request, id):
    sf = cl_Servicefamilies.objects.filter(id=id)
    sf.delete()
    context = {
        'sf': sf,
    }
    return redirect('servicefamilies')


@login_required(login_url='/login_render/')
def sservice(request):
    ser = cl_Service.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(ser, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.method == "GET":
        q = request.GET.get('searchstatus')
        if q != None:
            ser = cl_Service.objects.filter(ch_status__icontains=q)
    return render(request, 'tool/sservice.html', {'ser': ser,'users':users})


@login_required(login_url='/login_render/')
def SSADD(request):
    if request.method == "POST":
        # org_id = cl_New_organization.objects.get(ch_name = request.POST.get('ch_organization'
        id = request.POST.get('id')

        ch_ssname = request.POST.get('ch_ssname')
        ch_sprovider = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_service_family = cl_Servicefamilies.objects.get(
            ch_sname=request.POST.get('ch_sfamily'))
        ch_status = request.POST.get('ch_status')
        txt_description = request.POST.get('txt_description')

        ser = cl_Service(
            id=id,
            ch_ssname=ch_ssname,
            ch_sprovider=ch_sprovider,
            ch_service_family=ch_service_family,
            ch_status=ch_status,
            txt_description=txt_description,
        )
        ser.save()
        # print(nchange)
        return redirect('service')

    return render(request, 'tool/sservice.html')


@login_required(login_url='/login_render/')
def SSEdit(request):
    ser = cl_Service.objects.all()
    context = {
        'ser': ser,
    }
    return render(request, 'tool/sservice.html', context)


@login_required(login_url='/login_render/')
def SSUpdate(request, id):
    """
    Function for update change_information
    """
    if request.method == "POST":
        id = request.POST.get('id')

        ch_ssname = request.POST.get('ch_ssname')
        ch_sprovider = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_service_family = cl_Servicefamilies.objects.get(
            ch_sname=request.POST.get('ch_sfamily'))
        ch_status = request.POST.get('ch_status')
        txt_description = request.POST.get('txt_description')
        ser = cl_Service(
            id=id,
            ch_ssname=ch_ssname,
            ch_sprovider=ch_sprovider,
            ch_service_family=ch_service_family,
            ch_status=ch_status,
            txt_description=txt_description,

        )
        ser.save()

        # print(nchange)
        return redirect('service')

    return render(request, 'tool/sservice.html')


@login_required(login_url='/login_render/')
def SSDelete(request, id):
    # nchange = cl_New_change.objects.filter(id = id)
    # nchange.delete()
    ser = cl_Service.objects.filter(id=id)

    ser.delete()

    # return redirect('newchange')

    context = {
        'ser': ser,
    }
    return redirect('service')


@login_required(login_url='/login_render/')
def service_subcategory(request):
    sub = cl_Service_subcategory.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(sub, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.method == "GET":
        q = request.GET.get('searchstatus')
        if q != None:
            sub = cl_Service_subcategory.objects.filter(ch_status__icontains=q)
    return render(request, 'tool/service_subcategory.html', {'sub': sub,'users':users})


@login_required(login_url='/login_render/')
def SADD(request):
    if request.method == "POST":
        # org_id = cl_New_organization.objects.get(ch_name = request.POST.get('ch_organization'
        # id = request.POST.get('id')

        ch_subname = request.POST.get('ch_subname')
        ch_sservice = cl_Service.objects.get(
            ch_ssname=request.POST.get('ch_sservice'))
        ch_status = request.POST.get('ch_status')
        ch_request_type = request.POST.get('ch_request_type')
        txt_description = request.POST.get('txt_description')
        sub = cl_Service_subcategory(
            # id=id,
            ch_subname=ch_subname,
            ch_sservice=ch_sservice,
            ch_status=ch_status,
            ch_request_type=ch_request_type,
            txt_description=txt_description,
        )
        sub.save()
        # print(nchange)

        return redirect('service_subcategory')
    return render(request, 'tool/service_subcategory.html')


@login_required(login_url='/login_render/')
def SEdit(request):
    sub = cl_Service_subcategory.objects.all()
    context = {
        'sub': sub,
    }
    return render(request, 'tool/service_subcategory.html', context)


@login_required(login_url='/login_render/')
def SUpdate(request, id):
    """
    Function for update change_information
    """
    if request.method == "POST":
        id = request.POST.get('id')

        ch_subname = request.POST.get('ch_subname')
        ch_sservice = cl_Service.objects.get(
            ch_ssname=request.POST.get('ch_sservice'))
        ch_status = request.POST.get('ch_status')
        ch_request_type = request.POST.get('ch_request_type')
        txt_description = request.POST.get('txt_description')
        sub = cl_Service_subcategory(
            id=id,
            ch_subname=ch_subname,
            ch_sservice=ch_sservice,
            ch_status=ch_status,
            ch_request_type=ch_request_type,
            txt_description=txt_description,
        )
        sub.save()

        # print(nchange)
        return redirect('service_subcategory')

    return render(request, 'tool/service_subcategory.html')


@login_required(login_url='/login_render/')
def SDelete(request, id):
    # nchange = cl_New_change.objects.filter(id = id)
    # nchange.delete()
    sub = cl_Service_subcategory.objects.filter(id=id)

    sub.delete()

    # return redirect('newchange')

    context = {
        'sub': sub,
    }
    return redirect('service_subcategory')


@login_required(login_url='/login_render/')
def sla(request):
    sl = cl_Sla.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(sl, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchstatus')
        if q != None:
            sl = cl_Sla.objects.filter(ch_status__icontains=q)
    return render(request, 'tool/ssla.html', {'sl': sl,'users':users})


@login_required(login_url='/login_render/')
def SLADD(request):
    if request.method == "POST":
        # org_id = cl_New_organization.objects.get(ch_name = request.POST.get('ch_organization'
        # id = request.POST.get('id')

        ch_slname = request.POST.get('ch_slname')
        ch_slaprovider = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        txt_description = request.POST.get('txt_description')

        sl = cl_Sla(
            # id=id,
            ch_slname=ch_slname,
            ch_slaprovider=ch_slaprovider,
            txt_description=txt_description
        )
        sl.save()
        # print(nchange)
        return redirect('sla')
    return render(request, 'tool/ssla.html')


@login_required(login_url='/login_render/')
def SLEdit(request):
    sl = cl_Sla.objects.all()
    context = {
        'sl': sl,
    }
    return render(request, 'tool/ssla.html', context)


@login_required(login_url='/login_render/')
def SLUpdate(request, id):
    """
    Function for update change_information
    """
    if request.method == "POST":
        id = request.POST.get('id')
        ch_slname = request.POST.get('ch_slname')
        ch_slaprovider = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        txt_description = request.POST.get('txt_description')
        sl = cl_Sla(
            id=id,
            ch_slname=ch_slname,
            ch_slaprovider=ch_slaprovider,
            txt_description=txt_description
        )
        sl.save()

        # print(nchange)
        return redirect('sla')

    return render(request, 'tool/ssla.html')


@login_required(login_url='/login_render/')
def SLDelete(request, id):
    # nchange = cl_New_change.objects.filter(id = id)
    # nchange.delete()
    sl = cl_Sla.objects.filter(id=id)

    sl.delete()

    # return redirect('newchange')

    context = {
        'sl': sl,
    }
    return redirect('sla')


@login_required(login_url='/login_render/')
def SLT(request):
    slt = cl_Slt.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(slt, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {
        'slt': slt,
        'users':users
    }
    return render(request, 'tool/sslt.html', context)


@login_required(login_url='/login_render/')
def STADD(request):
    if request.method == "POST":
        # id =  request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_priority = request.POST.get('ch_priority')
        ch_request_type = request.POST.get('ch_request_type')
        ch_metric = request.POST.get('ch_metric')
        ch_value = request.POST.get('ch_value')
        ch_unit = request.POST.get('ch_unit')

        slt = cl_Slt(
            # id = id,
            ch_name=ch_name,
            ch_priority=ch_priority,
            ch_request_type=ch_request_type,
            ch_metric=ch_metric,
            ch_value=ch_value,
            ch_unit=ch_unit,

        )
        slt.save()
        return redirect('slt')
    return render(request, 'tool/slt.html')


@login_required(login_url='/login_render/')
def SLTEdit(request):
    slt = cl_Slt.objects.all()
    context = {
        'slt': slt,
    }
    return render(request, 'tool/slt.html', context)


@login_required(login_url='/login_render/')
def SLTUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_priority = request.POST.get('ch_priority')
        ch_request_type = request.POST.get('ch_request_type')
        ch_metric = request.POST.get('ch_metric')
        ch_value = request.POST.get('ch_value')
        ch_unit = request.POST.get('ch_unit')

        slt = cl_Slt(
            id=id,
            ch_name=ch_name,
            ch_priority=ch_priority,
            ch_request_type=ch_request_type,
            ch_metric=ch_metric,
            ch_value=ch_value,
            ch_unit=ch_unit,
        )
        slt.save()
        return redirect('slt')
    return redirect(request, 'tool/slt.html')


@login_required(login_url='/login_render/')
def SLTDelete(request, id):
    slt = cl_Slt.objects.filter(id=id)
    slt.delete()
    context = {
        'slt': slt,
    }
    return redirect('slt')


@login_required(login_url='/login_render/')
def servicedelivery(request):
    sd = cl_Servicedelivery.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(sd, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            sd = cl_Servicedelivery.objects.filter(ch_name__icontains=q)
    return render(request, 'tool/sdelivery.html', {'sd': sd,'users':users})


@login_required(login_url='/login_render/')
def SDADD(request):
    if request.method == "POST":
        # org_id = cl_New_organization.objects.get(ch_name = request.POST.get('ch_organization'
        # id = request.POST.get('id')

        ch_sdname = request.POST.get('ch_sdname')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        txt_description = request.POST.get('txt_description')

        sd = cl_Servicedelivery(
            # id=id,
            ch_sdname=ch_sdname,
            ch_organization=ch_organization,
            txt_description=txt_description
        )
        sd.save()
        # print(nchange)

        return redirect('servicedelivery')

    return render(request, 'tool/sdelivery.html')


@login_required(login_url='/login_render/')
def SDEdit(request):
    sd = cl_Servicedelivery.objects.all()
    context = {
        'sd': sd,
    }
    return render(request, 'tool/sdelivery.html', context)


@login_required(login_url='/login_render/')
def SDUpdate(request, id):
    """
    Function for update change_information
    """
    if request.method == "POST":
        id = request.POST.get('id')

        ch_sdname = request.POST.get('ch_sdname')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        txt_description = request.POST.get('txt_description')
        sd = cl_Servicedelivery(
            id=id,
            ch_sdname=ch_sdname,
            ch_organization=ch_organization,
            txt_description=txt_description

        )
        sd.save()

        # print(nchange)
        return redirect('servicedelivery')

    return render(request, 'tool/sdelivery.html')


@login_required(login_url='/login_render/')
def SDDelete(request, id):
    # nchange = cl_New_change.objects.filter(id = id)
    # nchange.delete()
    sd = cl_Servicedelivery.objects.filter(id=id)

    sd.delete()

    # return redirect('newchange')

    context = {
        'sd': sd,
    }
    return redirect('servicedelivery')


@login_required(login_url='/login_render/')
def synchro_data_source(request):
    form = SyncrodataForm()
    if request.method == 'POST':
        form = SyncrodataForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Add Successfully")
    context = {'form': form}
    return render(request, 'tool/sysconfisynchro.html', context)


@login_required(login_url='/login_render/')
def oauth_google(request):
    form = OauthgoogleForm()
    if request.method == 'POST':
        form = OauthgoogleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Add Successfully")
    context = {'form': form}
    return render(request, 'tool/authgoogle.html', context)


@login_required(login_url='/login_render/')
def oauth_mazuree(request):
    form = OauthmazureeForm()
    if request.method == 'POST':
        form = OauthmazureeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Add Successfully")
    context = {'form': form}
    return render(request, 'tool/authmazure.html', context)


@login_required(login_url='/login_render/')
def ldapuser(request):
    form = LdapuserForm()
    if request.method == 'POST':
        form = LdapuserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Add Successfully")
    context = {'form': form}
    return render(request, 'tool/ldapuser.html', context)


@login_required(login_url='/login_render/')
def externaluser(request):
    ext = cl_Externaluser.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchstatus')
        if q != None:
            ext = cl_Externaluser.objects.filter(ch_status__icontains=q)
    return render(request, 'tool/externaluser.html', {'ext': ext})


def extADD(request):
    if request.method == "POST":
        ch_person = cl_Person.objects.get(
            ch_person_firstname=request.POST.get('ch_person'))
        ch_person_lastname = request.POST.get('ch_person_lastname')
        e_email = str.lower(request.POST.get('e_email'))
        ch_login = request.POST.get('ch_login')
        ch_language = request.POST.get('ch_language')
        ch_status = request.POST.get('ch_status')
        ext = cl_Externaluser(
            ch_person=ch_person,
            ch_person_lastname=ch_person_lastname,
            e_email=e_email,
            ch_login=ch_login,
            ch_language=ch_language,
            ch_status=ch_status,
        )
        ext.save()
        return redirect('externaluser')
    return render(request, 'tool/externaluser.html')


def extEdit(request):
    ext = cl_Externaluser.objects.all()
    context = {
        'ext': ext,
    }
    return render(request, 'tool/externaluser.html', context)


def extUpdate(request, id):
    """
    Function for update change_information
    """
    if request.method == "POST":
        id = request.POST.get('id')
        ch_person = cl_Person.objects.get(
            ch_person_firstname=request.POST.get('ch_person'))
        ch_person_lastname = request.POST.get('ch_person_lastname')
        e_email = request.POST.get('e_email')
        ch_login = request.POST.get('ch_login')
        ch_language = request.POST.get('ch_language')
        ch_status = request.POST.get('ch_status')
        ext = cl_Externaluser(
            id=id,
            ch_person=ch_person,
            ch_person_lastname=ch_person_lastname,
            e_email=e_email,
            ch_login=ch_login,
            ch_language=ch_language,
            ch_status=ch_status,
        )
        ext.save()
        return redirect('externaluser')
    return render(request, 'tool/externaluser.html')


def extDelete(request, id):
    ext = cl_Externaluser.objects.get(id=id)
    ext.delete()
    context = {
        'ext': ext,
    }
    return redirect('externaluser')


@login_required(login_url='/login_render/')
def itsmuser(request):
    form = ItsmuserForm()
    if request.method == 'POST':
        form = ItsmuserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Add Successfully")
    context = {'form': form}
    return render(request, 'tool/itsmuser.html', context)


@login_required(login_url='/login_render/')
def slacknoti(request):
    form = SlacknotiForm()
    if request.method == 'POST':
        form = SlacknotiForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Add Successfully")
    context = {'form': form}
    return render(request, 'tool/slacknoti.html', context)


@login_required(login_url='/login_render/')
def micronoti(request):
    form = MicronotiForm()
    if request.method == 'POST':
        form = MicronotiForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Add Successfully')
    context = {'form': form}
    return render(request, 'tool/micronoti.html', context)


@login_required(login_url='/login_render/')
def webhook(request):
    form = WebhookForm()
    if request.method == 'POST':
        form = WebhookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Add Successfully')
    context = {'form': form}
    return render(request, 'tool/webhook.html', context)


@login_required(login_url='/login_render/')
def googlechat(request):
    form = GooglechatForm()
    if request.method == 'POST':
        form = GooglechatForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Add Successfully')
    context = {'form': form}
    return render(request, 'tool/googlechat.html', context)


@login_required(login_url='/login_render/')
def rocketchat(request):
    form = RocketchatForm()
    if request.method == 'POST':
        form = RocketchatForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Add Successfully')
    context = {'form': form}
    return render(request, 'tool/rocketchat.html', context)


@login_required(login_url='/login_render/')
def itsmwebhook(request):
    form = ItsmwebhookForm()
    if request.method == 'POST':
        form = ItsmwebhookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Add Successfully')
    context = {'form': form}
    return render(request, 'tool/itsmwebhook.html', context)

 ############ CSV ###############


def csvimport(request):
    """
    It is view function for the additon of new users
    """
    if request.method == "POST":
        # disc_Attachment = request.POST.get('disc_Attachment')
        
        try:
            Attachment = request.FILES['disc_Attachment']
        except:
            Attachment = 'annonymous.pdf'

        csv = CSV_import(
            
            disc_Attachment = Attachment
        )
        csv.save()
        return redirect('csvimport')
    return render(request, 'tool/add_file1.html')






def csv_edit(request, id):
    csv = CSV_import.objects.filter(Id = id).first
    context = {
        'csv': csv,
    }
    return render(request, 'tool/edit_file.html', context)    


   
def csv_update(request, id):
    """
    It is view function for the additon of new users
    """
    if request.method == "POST":
        discl = CSV_import.objects.filter(Id = id).first()
        attachment_name = request.POST.get('disc_Attachment')
        if discl.disc_Attachment == attachment_name:
            

            csv = CSV_import(
                Id=id,
                 disc_Attachment = attachment_name
               
        
            )
            csv.save()
            return redirect('csvimport')
        else:
          
            
            try:
                Attachment = request.FILES['disc_Attachment']
            except:
                Attachment = 'annonymous.pdf'

            csv = CSV_import (
               
                disc_Attachment = Attachment
            )
            csv.save()
            return redirect('csvimport')
    return render(request, 'tool/edit_file.html')




def DeleteCSVAttachedPDF(request):
    id = request.GET['id']
    csv = CSV_import.objects.filter(Id = id).first()
    file_to_delete = str(csv.disc_Attachment)
    media_path = settings.MEDIA_ROOT
    file_path = os.path.join(media_path, file_to_delete)
    print(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
        return HttpResponse(request, 'tool/edit_file.html')
    else:
        return HttpResponse(request, 'tool/edit_file.html')




def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

