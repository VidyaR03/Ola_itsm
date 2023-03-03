import json
from django.shortcuts import render, get_object_or_404

from django.urls import reverse
import random
import time
import logging
import datetime
import requests
from datetime import *
from .forms import *
from io import BytesIO
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from tool.models import *
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.template.loader import get_template
# from django.core.exceptions import BadRequest
from django.http import FileResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import send_mail
from xhtml2pdf import pisa
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from tool.modules.configurationmanagement.ConfigurationManagement import *
from tool.modules.user_logs.user_activity_log import *
from django.conf import settings
import requests
from .models import cl_Reopen
from django.shortcuts import render
from django.contrib import messages



###################### DONT DELETE THIS CODEEEEEEE ######################

############################# Telegram ########################


def send_telegram_message(token, chat_id, text):

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, data=data)
    return response.json()

logger = logging.getLogger(__name__)

###############################################################

@login_required(login_url='/login_render/')
def home(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    user = adminuser.objects.filter(email=request.user).first()
    context = {
        'user': user,
        'permission':permission
    }
    return render(request, 'tool/dashboard.html',context)


@login_required(login_url='/login_render/')
def dashboard(request): 
    log = user_activity_log.objects.all()
    permission = roles.objects.filter(id=request.session['user_role']).first()
    User = cl_User_request.objects.all().count()
    service = cl_User_request.objects.all().count()
    change = cl_New_change.objects.all().count() 
    total = User+change
    Assign = cl_User_request.objects.exclude(ch_assign_agent = 'Deallocate').count()    
    newopen= cl_User_request.objects.filter(Q(ch_assign_agent = 'Deallocate') | Q(ch_status = 'Active')).count()
    Assign1 = cl_New_change.objects.filter(ch_status = 'Assigned').count()
    newopen1= cl_New_change.objects.exclude(Q(ch_assign_agent = 'request.session(username)') & Q(ch_status = 'Assigned')).count()
    watch = cl_User_request.objects.filter(Q(ch_assign_agent = 'request.session(username)')).count()
    Customer_Contract_count = cl_Customer_contract.objects.all().count()
    Provider_Contract_count = cl_Providercontract.objects.all().count()
    Delivery_Model_count = cl_Servicedelivery.objects.all().count()
    Services_count = cl_Service.objects.all().count()
    Service_Subcategory_count = cl_Service_subcategory.objects.all().count()
    SLA_count = cl_Sla.objects.all().count()
    SLT_count = cl_Slt.objects.all().count()
    incident_count = cl_User_request.objects.filter(ch_request_type = "Incident").count()
    service_count = cl_User_request.objects.filter(ch_request_type = "Service").count()
    overdue= cl_User_request.objects.filter(Q(ch_status = 'TTO Escalated') | Q(ch_status = 'TTR Escalated')).count()
    team = cl_Team.objects.all().count()
    
 

###################### DONT DELETE THIS CODEEEEEEE ######################

    # try:
    #     # send_telegram_message(token=settings.BOT_TOKEN, chat_id=-1001875732520, text="Hello from Django!")
    # except Exception as exception:
   
    context = {
        'log':log,
        'User': User,
        'permission':permission,
        'service':service,
        'change':change,
        'newopen':newopen,
        'Assign':Assign,
        'Assign1':Assign1,
        'newopen1':newopen1,
        'watch':watch,
        'Customer_Contract_count':Customer_Contract_count,
        'Provider_Contract_count':Provider_Contract_count,
        'Delivery_Model_count':Delivery_Model_count,
        'Services_count':Services_count,
        'SLA_count':SLA_count,
        'SLT_count':SLT_count,
        'Service_Subcategory_count':Service_Subcategory_count,
        'incident_count':incident_count,
        'service_count':service_count,
        'overdue':overdue,
        'total':total,
        'team':team
    }

    return render(request, 'tool/dashboard.html',context)


def login_render(request):
    return render(request, 'tool/login.html')


@login_required(login_url='/login_render/')
def servicenav(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    return render(request, 'tool/servicenav.html',{'permission':permission})


@login_required(login_url='/login_render/')
def systemnav(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    return render(request, 'tool/systemnav.html',{'permission':permission})


@login_required(login_url='/login_render/')
def sysconfienav(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    return render(request, 'tool/sysconfinav.html',{'permission':permission})


@login_required(login_url='/login_render/')
def sysconfiauth(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    return render(request, 'tool/sysconfiauth.html',{'permission':permission})


@login_required(login_url='/login_render/')
def admuser(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    return render(request, 'tool/admuser.html',{'permission':permission})


@login_required(login_url='/login_render/')
def integrationav(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    return render(request, 'tool/integrationav.html',{'permission':permission})


def registerPage(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
    context = {
        'form': form,
        'permission':permission
        }
    return render(request, 'tool/register.html', context)

def adminloginPage(request):
    if request.method == 'POST':
        request.session["username"] = request.POST.get('username')
        password = request.POST.get('password')
        username = request.session["username"]
        admin = authenticate(request, username=username, password=password)
        if admin is not None:
            login(request, admin)
            request.session['user_name'] = admin.email
            role_id = admin.ch_user_role_id
            request.session['user_role'] = role_id
            admin_name = "Mangesh"
            adminaction = "Login on Web_page"
            event ="event"
            resultcode = "200"
            user_activity(admin_name, adminaction, event, resultcode)
            return redirect('home')
        else:
            admin_name = request.session["username"]
            adminaction = "Trying to login"
            event ="fail to login"
            resultcode = "401"
            user_activity(admin_name, adminaction, event, resultcode)
            messages.info(request, 'Username OR Password is incorrect')
    return redirect('home')


@login_required(login_url='/login_render/')
def logoutUser(request):
    logout(request)
    return render(request, 'tool/login.html')


@login_required(login_url='/login_render/')
def landingPage(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    return render(request, 'tool/login.html',{'permission':permission})


@login_required(login_url='/login_render/')
def view_logs(request):
    """
    This function create views of log
    """
    permission = roles.objects.filter(id=request.session['user_role']).first()
    log = user_activity_log.objects.all()
    if request.method == "GET":
            q = request.GET.get('searchname')
            if q != None:
                log = user_activity_log.objects.filter(username__icontains=q) 

    page = request.GET.get('page', 1)
    paginator = Paginator(log, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)


    context = {
        'log': log,
        'users':users,
        'permission':permission,
    }

    
    return render(request, 'tool/logs.html', context)


@login_required(login_url='/login_render/')
def LogsDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            log = user_activity_log.objects.filter(id=i).first()
            log.delete()
    return redirect('logs')

@login_required(login_url='/login_render/')
def document(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    doc = cl_Document.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            doc = cl_Document.objects.filter(ch_name__icontains=q) 
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
    context = {
        'doc': doc,
        'users':users,
        'permission':permission
    }
    return render(request, 'tool/document.html', context)


@login_required(login_url='/login_render/')
def DocAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
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
            ch_name=ch_name,
            ch_organization=ch_organization,
            ch_version=ch_version,
            txt_description=txt_description,
            txt_text=txt_text,
            url_URL=url_URL,
            disc_Attachment = Attachment
        )
        doc.save()
        admin_name = request.session["username"]
        adminaction = "Addition of Documents"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('document')
    return render(request, 'tool/document.html',{'permission':permission})


@login_required(login_url='/login_render/')
def DocEdit(request,id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    doc = cl_Document.objects.filter(id=id).first()
    context = {
        'doc': doc,
        'permission':permission
    }
    return render(request, 'tool/document.html', context)


@login_required(login_url='/login_render/')
def DocUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        discl = cl_Document.objects.filter(id = id).first()
        attachment_name = request.POST.get('disc_Attachment')
        if discl.disc_Attachment == attachment_name:
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
            admin_name = request.session["username"]
            adminaction = "Update Documents"
            event ="event"
            resultcode = "200"
            user_activity(admin_name, adminaction, event, resultcode)
            return redirect('document')
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
    return render(request, 'tool/document.html',{'permission':permission})


@login_required(login_url='/login_render/')
def DocDelete(request,id):
    doc = cl_Document.objects.filter(id=id)
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            doc = cl_Document.objects.filter(id=i).first()
            doc.delete()
    return redirect('document')


@login_required(login_url='/login_render/')
def DeleteAttachedPDF(request,id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    id = request.GET['id']
    doc = cl_Document.objects.filter(id = id).first()
    file_to_delete = str(doc.disc_Attachment)
    media_path = settings.MEDIA_ROOT
    file_path = os.path.join(media_path, file_to_delete)
    if os.path.exists(file_path):
        os.remove(file_path)
        return HttpResponse(request, 'tool/document.html',{'permission':permission})
    else:
        return HttpResponse(request, 'tool/document.html',{'permission':permission})



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
            return FileResponse(open(file_path, 'rb'), content_type='application/')


############## Location ##########

@login_required(login_url='/login_render/')
# def Location(request):
#     loc = []
#     if request.method == 'POST':
#         loc = request.POST.getlist('loc')
#     permission = roles.objects.filter(id=request.session['user_role']).first()
#     loc = cl_Location.objects.all()

    
    
#     if request.method == "GET":
#         q = request.GET.get('searchname')
#         if q != None:
#             loc = cl_Location.objects.filter(ch_location_name__icontains=q)
#     page = request.GET.get('page', 1)
#     org = cl_New_organization.objects.all()


#     paginator = Paginator(loc, 10)
#     try:
#         users = paginator.page(page)
#     except PageNotAnInteger:
#         users = paginator.page(1)
#     except EmptyPage:
#         users = paginator.page(paginator.num_pages)


#     context = {
#         'loc': loc,
#         'users':users,
#         'permission':permission,
#         'org':org,
#     }
#     return render(request, 'tool/location.html', context)



def Location(request):
    users = []
    if request.method == 'POST':
        users = request.POST.getlist('users')
    permission = roles.objects.filter(id=request.session['user_role']).first()
    loc_query = cl_Location.objects.all()

    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            loc_query = loc_query.filter(ch_location_name__icontains=q)

    paginator = Paginator(loc_query, 10)
    page = request.GET.get('page', 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    org = cl_New_organization.objects.all()

    # Add URL for each cl_Location object to the context dictionary
    for i in users:
        i.url = reverse('location_detail', args=[i.pk])

    context = {
        'users': users,
        'permission': permission,
        'org': org,
    }
    return render(request, 'tool/location.html', context)


def location_detail(request, pk):
    location = get_object_or_404(cl_Location, pk=pk)
    context = {
        'location': location,
    }
    return render(request, 'tool/location_detail.html', context)


@login_required(login_url='/login_render/')
def LADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_location_name = request.POST.get('ch_location_name')
        txt_address = request.POST.get('txt_address')

        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        
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
        admin_name = request.session["username"]
        adminaction = "Addition of location"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('location')
    return render(request, 'tool/location.html',{'permission':permission})



@login_required(login_url='/login_render/')
def LEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    loc = cl_Location.objects.all()
    context = {
        'loc': loc,
        'permission':permission
    }
    return render(request, 'tool/location.html', context)


@login_required(login_url='/login_render/')
def LUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_location_name = request.POST.get('ch_location_name')
        txt_address = request.POST.get('txt_address')
        ch_organization = cl_New_organization.objects.get(ch_name=request.POST.get('ch_organization'))
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
        admin_name = request.session["username"]
        adminaction = "Location Updated"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('location')
    return redirect(request, 'tool/location.html',{'permission':permission})


@login_required(login_url='/login_render/')
def LDelete(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            loc = cl_Location.objects.filter(id=i).first()
            loc.delete()
        return redirect('location')
    return redirect(request, 'tool/location.html',{'permission':permission})



@login_required(login_url='/login_render/')
def new_organization(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    org = cl_New_organization.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            org = cl_New_organization.objects.filter(ch_name__icontains=q)

    page = request.GET.get('page', 1)
    paginator = Paginator(org, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'tool/neworganization.html', {'org': org,'users':users,'permission':permission})



@login_required(login_url='/login_render/')
def OrgADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_name = str.capitalize(request.POST.get('ch_name'))
        ch_code = request.POST.get('ch_code')
        ch_status = request.POST.get('ch_status')
        # ch_parent = request.POST.get('ch_parent')
        ch_parent = cl_New_organization.objects.filter(id=request.POST.get('ch_parent_id')).first()

        ch_delivery_model = request.POST.get('ch_delivery_model')
        org = cl_New_organization(
            ch_name=ch_name,
            ch_code=ch_code,
            ch_status=ch_status,
            ch_parent=ch_parent,
            ch_delivery_model=ch_delivery_model,
        )
        org.save()
        admin_name = request.session["username"]
        adminaction = "Addition of organization"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('new_organization')
    return render(request, 'tool/neworganization.html',{'permission':permission})


@login_required(login_url='/login_render/')
def OrgEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    org = cl_New_organization.objects.all()
    context = {
        'org': org,
        'permission':permission
    }
    return render(request, 'tool/neworganization.html', context)



@login_required(login_url='/login_render/')
def OrgUpdate(request,id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_code = request.POST.get('ch_code')
        ch_status = request.POST.get('ch_status')
        ch_parent = request.POST.get('ch_parent')
        ch_delivery_model = request.POST.get('ch_delivery_model')
        org = cl_New_organization(
            id = id,
            ch_name=ch_name,
            ch_code=ch_code,
            ch_status=ch_status,
            ch_parent=ch_parent,
            ch_delivery_model=ch_delivery_model,
        )
        org.save()
        return redirect('new_organization')
    return render(request, 'tool/neworganization.html',{'permission':permission})


@login_required(login_url='/login_render/')
def OrgDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            org = cl_New_organization.objects.filter(id=i).first()
            org.delete()
    return redirect('new_organization')


@login_required(login_url='/login_render/')
def client(request):    
    permission = roles.objects.filter(id=request.session['user_role']).first()
    per = cl_Person.objects.all()
    org = cl_New_organization.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            per = cl_Person.objects.filter(ch_person_firstname__icontains=q)
    page = request.GET.get('page', 1)
    paginator = Paginator(per, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'tool/client.html', {'per': per, 'org':org,'users':users,'permission':permission})

def get_team_by_org(request):
    org_id = request.GET.get('org_id')
    teams = cl_Team.objects.filter(ch_organization=org_id)
    return JsonResponse([{'id': team.id, 'teamname': team.ch_teamname} for team in teams], safe=False)


@login_required(login_url='/login_render/')
def ADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_person_firstname = str.capitalize(
            request.POST.get('ch_person_firstname'))
        ch_person_lastname = str.capitalize(
            request.POST.get('ch_person_lastname'))
        ch_organization = cl_New_organization.objects.filter(id=str.capitalize(request.POST.get('ch_organization'))).first()
        ch_team = cl_Team.objects.filter(id=request.POST.get('ch_team_name')).first()
        ch_person_status = str.capitalize(request.POST.get('ch_person_status'))
        ch_person_location = str.capitalize(
            request.POST.get('ch_person_location')) 
        ch_person_function = str.capitalize(request.POST.get('ch_person_function'))
        ch_employee_number = str.upper(request.POST.get('ch_employee_number'))
        e_person_email = str.lower(request.POST.get('e_person_email'))
        telegram_chatid = request.POST.get('telegram_chatid')
        ch_person_mobilenumber = request.POST.get('ch_person_mobilenumber')
        per = cl_Person(
            ch_person_firstname=ch_person_firstname,
            ch_person_lastname=ch_person_lastname,
            ch_organization=ch_organization,
            ch_team=ch_team,
            ch_person_status=ch_person_status,
            ch_person_location=ch_person_location,
            ch_person_function=ch_person_function,
            ch_employee_number=ch_employee_number,
            e_person_email=e_person_email,
            telegram_chatid=telegram_chatid,
            ch_person_mobilenumber=ch_person_mobilenumber,
        )
        per.save()
        admin_name = request.session["username"]
        adminaction = "addition of persion"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('client')
    return render(request, 'tool/client.html',{'permission':permission})


@login_required(login_url='/login_render/')
def Edit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    per = cl_Person.objects.all()
    context = {
        'per': per,
        'permission':permission
    }
    return render(request, 'tool/client.html', context)


@login_required(login_url='/login_render/')
def Update(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_person_firstname = request.POST.get('ch_person_firstname')
        ch_person_lastname = request.POST.get('ch_person_lastname')
        ch_organization = cl_New_organization.objects.get(id = request.POST.get('ch_organization'))    
        ch_team = cl_Team.objects.filter(id=request.POST.get('ch_team_name')).first()
        ch_person_status = request.POST.get('ch_person_status')
        ch_person_location = request.POST.get('ch_person_location')
        ch_person_function = request.POST.get('ch_person_function')
        ch_employee_number = request.POST.get('ch_employee_number')
        e_person_email = request.POST.get('e_person_email')
        telegram_chatid = request.POST.get('telegram_chatid')
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
            ch_employee_number=ch_employee_number,
            e_person_email=e_person_email,
            telegram_chatid=telegram_chatid,
            ch_person_mobilenumber=ch_person_mobilenumber,
        )
        per.save()
        admin_name = request.session["username"]
        adminaction = "update the persion"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('client')
    return render(request, 'tool/client.html',{'permission':permission})


@login_required(login_url='/login_render/')
def Delete(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            per = cl_Person.objects.filter(id=i).first()
            per.delete()
        return redirect('client')
    return render(request, 'tool/client.html',{'permission':permission})


########### Document #####################

@login_required(login_url='/login_render/')
def document(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    doc = cl_Document.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            doc = cl_Document.objects.filter(ch_name__icontains=q)

    page = request.GET.get('page', 1)
    org = cl_New_organization.objects.all()


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

    context = {
        'doc': doc,
        'users':users,
        'org':org,
        'permission':permission
    }
    return render(request, 'tool/document.html', context)


@login_required(login_url='/login_render/')
def DocAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()

        ch_version = request.POST.get('ch_version')
        txt_description = request.POST.get('txt_description')
        txt_text = request.POST.get('txt_text')
        url_URL = request.POST.get('url_URL')
        try:
            Attachment = request.FILES['disc_Attachment']
        except:
            Attachment = 'annonymous.pdf'
        doc = cl_Document(
            ch_name=ch_name,
            ch_organization=ch_organization,
            ch_version=ch_version,
            txt_description=txt_description,
            txt_text=txt_text,
            url_URL=url_URL,
            disc_Attachment = Attachment
        )
        doc.save()
        admin_name = request.session["username"]
        adminaction = "addition of documents"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('document')
    return render(request, 'tool/document.html',{'permission':permission})


@login_required(login_url='/login_render/')
def DocEdit(request,id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    doc = cl_Document.objects.filter(id=id).first()
    context = {
        'doc': doc,
        'permission':permission
    }
    return render(request, 'tool/document.html', context)


@login_required(login_url='/login_render/')
def DocUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        discl = cl_Document.objects.filter(id = id).first()
        attachment_name = request.POST.get('disc_Attachment')
        if discl.disc_Attachment == attachment_name:
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
            admin_name = request.session["username"]
            adminaction = "update the documents"
            event ="event"
            resultcode = "200"
            user_activity(admin_name, adminaction, event, resultcode)
            return redirect('document')
        
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
            admin_name = request.session["username"]
            adminaction = "update the persion"
            event ="event"
            resultcode = "200"
            user_activity(admin_name, adminaction, event, resultcode)
            return redirect('document')
    return render(request, 'tool/document.html',{'permission':permission})


@login_required(login_url='/login_render/')
def DocDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            doc = cl_Document.objects.filter(id=i)
            doc.delete()
    return redirect('document')


@login_required(login_url='/login_render/')
def DeleteAttachedPDF(request,id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    id = request.GET['id']
    doc = cl_Document.objects.filter(id = id).first()
    file_to_delete = str(doc.disc_Attachment)
    media_path = settings.MEDIA_ROOT
    file_path = os.path.join(media_path, file_to_delete)
    if os.path.exists(file_path):
        os.remove(file_path)
        admin_name = request.session["username"]
        adminaction = "removing the file"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return HttpResponse(request, 'tool/document.html',{'permission':permission})
    else:
        return HttpResponse(request, 'tool/document.html',{'permission':permission})


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


################### Software #####################

@login_required(login_url='/login_render/')
def software(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    soft = cl_Software.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            soft = cl_Software.objects.filter(ch_sofname__icontains=q)
    page = request.GET.get('page', 1)
    paginator = Paginator(soft, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'tool/software.html', {'soft': soft,'users':users,'permission':permission})


@login_required(login_url='/login_render/')
def softAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
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
        admin_name = request.session["username"]
        adminaction = "Add the software"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('software')
    return render(request, 'tool/software.html',{'permission':permission})


@login_required(login_url='/login_render/')
def softEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    soft = cl_Software.objects.all()
    context = {
        'soft': soft,
        'permission':permission
    }
    return render(request, 'tool/software.html', context)


@login_required(login_url='/login_render/')
def softUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
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
        admin_name = request.session["username"]
        adminaction = "update the persion"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('software')
    return redirect(request, 'tool/software.html',{'permission':permission})


@login_required(login_url='/login_render/')
def softDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            soft = cl_Software.objects.filter(id=i).first()
            soft.delete()
        admin_name = request.session["username"]
        adminaction = "Delete the software"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('software')


################### Team ######################


@login_required(login_url='/login_render/')
def team(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "GET":
        tem = cl_Team.objects.all()
        org = cl_New_organization.objects.all()
        team_person = cl_Person.objects.all()
        q = request.GET.get('searchname')
        if q != None:
            tem = cl_Team.objects.filter(ch_teamname__icontains=q)

        page = request.GET.get('page', 1)
 
        paginator = Paginator(tem, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        context={
            'tem': tem, 
            'org':org,
            'team_person':team_person,
            'users':users,
            'permission':permission
        }
    return render(request, 'tool/service.html', context)


@login_required(login_url='/login_render/')
def TADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_teamname = request.POST.get('ch_teamname')
        ch_teamstatus = request.POST.get('ch_teamstatus')
        ch_organization = cl_New_organization.objects.filter(
            id=request.POST.get('ch_organization')).first()
        L1_Manager = cl_Person.objects.filter(id=request.POST.get('L1_Manager')).first()
        L2_Manager = cl_Person.objects.filter(id=request.POST.get('L2_Manager')).first()
        ch_team_function = request.POST.get('ch_team_function')
        tem = cl_Team(
            ch_teamname=ch_teamname,
            ch_teamstatus=ch_teamstatus,
            ch_organization=ch_organization,
            L1_Manager=L1_Manager,
            L2_Manager=L2_Manager,
            ch_team_function=ch_team_function,
        )
        tem.save()
        admin_name = request.session["username"]
        adminaction = "Addition of team"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('team')
    return render(request, 'tool/service.html',{'permission':permission})

def get_people_by_org(request):
    org_id = request.GET.get('org_id')
    people = cl_Person.objects.filter(ch_organization=org_id)
    return JsonResponse([{'id': person.id, 'firstname': person.ch_person_firstname, 'lastname': person.ch_person_lastname} for person in people], safe=False)


@login_required(login_url='/login_render/')
def TEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    tem = cl_Team.objects.all()
    context = {
        'tem': tem,
        'permission':permission
    }
    return render(request, 'tool/service.html', context)



@login_required(login_url='/login_render/')
def TUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_teamname = request.POST.get('ch_teamname')
        ch_teamstatus = request.POST.get('ch_teamstatus')
        ch_organization = cl_New_organization.objects.filter(
            id=request.POST.get('ch_organization')).first()
        L1_Manager = cl_Person.objects.filter(id=request.POST.get('L1_Manager')).first()
        L2_Manager = cl_Person.objects.filter(id=request.POST.get('L2_Manager')).first()
        ch_team_function = request.POST.get('ch_team_function')
        tem = cl_Team(
            id=id,
            ch_teamname=ch_teamname,
            ch_teamstatus=ch_teamstatus,
            ch_organization=ch_organization,
            L1_Manager=L1_Manager,
            L2_Manager=L2_Manager,
            ch_team_function=ch_team_function,
        )
        tem.save()
        admin_name = request.session["username"]
        adminaction = "update the team"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('team')
    return render(request, 'tool/service.html',{'permission':permission})


@login_required(login_url='/login_render/')
def TDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            tem = cl_Team.objects.filter(id=i).first()
            tem.delete()
            admin_name = request.session["username"]
            adminaction = "Delete the team"
            event ="event"
            resultcode = "200"
            user_activity(admin_name, adminaction, event, resultcode)
        return redirect('team')


 
################### New channge   #############################
@login_required(login_url='/login_render/')
def newchange(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    user = adminuser.objects.filter(email=request.user).first()
    if user.ch_organization.ch_name == "Inhouse":
        org = cl_New_organization.objects.all()
        call = cl_Person.objects.all()
        nchange = cl_New_change.objects.all()
        if request.method == "GET":
            allteam = cl_Team.objects.all()
            team_person = cl_Person.objects.all()
            q = request.GET.get('searchstatus')
            if q != None:
                nchange = cl_New_change.objects.filter(ch_status__icontains=q)
    elif user.ch_organization.ch_name != 'Inhouse':
        org = cl_New_organization.objects.filter(ch_name=user.ch_organization)
        # print(org)
        call = cl_Person.objects.filter(ch_organization=user.ch_organization)
        nchange = cl_New_change.objects.filter(ch_organization=user.ch_organization)
        if request.method == "GET":
            allteam = cl_Team.objects.filter(ch_organization=user.ch_organization)
            team_person = cl_Person.objects.filter(ch_organization=user.ch_organization)
            q = request.GET.get('searchstatus')
            if q != None:
                nchange = cl_New_change.objects.filter(ch_status__icontains=q)

    page = request.GET.get('page', 1)
    paginator = Paginator(nchange, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    q = request.GET.get('searchstatus')
    if q != None:
        nchange = cl_New_change.objects.filter(ch_status__icontains=q)
    return render(request, 'tool/newchange.html', {'nchange': nchange, 'allteam': allteam,'users':users,'permission':permission,'org':org,'call':call,'team_person':team_person})

def get_people_by_team(request):
    team_id = request.GET.get('teamId')
    people = cl_Person.objects.filter(ch_team_id=team_id)
    return JsonResponse([{'id': person.id, 'name': person.ch_person_firstname} for person in people], safe=False)

def get_service_sub_by_service(request):
    service_id = request.GET.get('serviceId')
    subcategory = cl_Service_subcategory.objects.filter(ch_sservice_id=service_id)
    return JsonResponse([{'id': cato.id, 'name': cato.ch_subname} for cato in subcategory] ,safe=False)

@login_required(login_url='/login_render/')
def CADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()

        ch_caller =cl_Person.objects.filter(
            ch_person_firstname=str.capitalize(request.POST.get('ch_caller'))).first()
        ch_status = request.POST.get('ch_status')
        # ch_status = nchange.ch_status
        ch_category = request.POST.get('ch_category')
        ch_title = request.POST.get('ch_title')
        dt_start_date = request.POST.get('dt_start_date')
        dt_Updated_date = request.POST.get('dt_Updated_date')
        ch_parent_change = cl_New_change.objects.filter(id=request.POST.get('ch_parent_change_id')).first()
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

        cr_raised = cl_New_change.objects.latest('id')
        subject = 'New Change request raised'
        message = f'New Change request raised by "{cr_raised.ch_organization}", Request ID : "{cr_raised.id}".' 
        helpdesk_L1 = cl_Team.objects.filter(ch_teamname='Helpdesk').first()
        recepient = [helpdesk_L1.L1_Manager.e_person_email]
        telchat_id=helpdesk_L1.L1_Manager.telegram_chatid,

        try:
            mail_sender()
            sender = settings.EMAIL_HOST_USER
            send_mail(subject, message, sender, recepient, fail_silently=False)
        except:
            print('email not send')
        try:
            send_telegram_message(token=settings.BOT_TOKEN, chat_id=telchat_id, text=message)
        except:
            print('Telegram notification not send')
        admin_name = request.session["username"]
        adminaction = "addition of new changes"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('newchange')
    return render(request, 'tool/newchange.html',{'permission':permission})


@login_required(login_url='/login_render/')
def CEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    nchange = cl_New_change.objects.all()
    context = {
        'nchange': nchange,
        'permission':permission
    }
    return render(request, 'tool/newchange.html', context)


@login_required(login_url='/login_render/')
def CUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    """
    Function for update change_information
    """
    if request.method == "POST":
        nchange = cl_New_change.objects.filter(id=id).first()
        # id = request.POST.get('id')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_caller =cl_Person.objects.get(
            ch_person_firstname=str.capitalize(request.POST.get('ch_caller')))
        # ch_status = request.POST.get('ch_status')
        ch_status = nchange.ch_status
        ch_category = request.POST.get('ch_category')
        ch_title = request.POST.get('ch_title')
        dt_start_date = nchange.dt_start_date
        dt_Updated_date = request.POST.get('dt_Updated_date')
        ch_parent_change = cl_New_change.objects.filter(id=request.POST.get('ch_parent_change_id')).first()
        txt_fallback_plan = request.POST.get('txt_fallback_plan')
        txt_description = request.POST.get('txt_description')
        ch_assign_agent = nchange.ch_assign_agent
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
            ch_assign_agent=ch_assign_agent
        )
        nchange.save()
        admin_name = request.session["username"]
        adminaction = "addition of new changes"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('newchange')
    return render(request, 'tool/newchange.html',{'permission':permission})


@login_required(login_url='/login_render/')
def CDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            nchange = cl_New_change.objects.filter(id=i).first()
            nchange.delete()
        admin_name = request.session["username"]
        adminaction = "Delete the changes"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('newchange')
########## Assign Change For Change Management############

@login_required(login_url='/login_render/')
def assign_changeModal(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        p_Emp_id = request.POST.get('p')
        per = cl_Person.objects.filter(id=p_Emp_id).first()
        telegram_chat_id = per.telegram_chatid

        for i in list_id:
            nchange = cl_New_change.objects.filter(id=i).first()
            nchange.ch_assign_agent = per.ch_person_firstname
            nchange.ch_status = "Assigned"
            nchange.save()

        try:
            mail_sender()
            subject = 'Change Request Assign'
            message = f'Change Request ID : "{list_id}" is Assigned to you'
            sender = settings.EMAIL_HOST_USER
            recepient = [per.e_person_email]
            send_mail(subject, message, sender, recepient, fail_silently=False)
            send_telegram_message(token=settings.BOT_TOKEN, chat_id=telegram_chat_id, text= message)
            return JsonResponse({'result': 'success'})
        except:
            print('email not send')

        admin_name = request.session["username"]
        adminaction = "assign the changes"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        nchange = cl_New_change.objects.all()
        context = {
            'nchange': nchange,
            'permission':permission,
        }
    return render(request, 'tool/tassign.html', context)


def mail_sender():
    mail_host = email_notifier.objects.filter(id=1).first()
    if mail_host != None:
        settings.EMAIL_HOST = mail_host.host
        settings.EMAIL_PORT = mail_host.port
        settings.EMAIL_USE_SSL=True
        settings.EMAIL_HOST_USER = mail_host.host_user
        settings.EMAIL_HOST_PASSWORD = mail_host.host_password


########## Approve Change For Change Management############

@login_required(login_url='/login_render/')
def send_approval_Mail(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        helpdesk_team = cl_Team.objects.filter(ch_teamname='Helpdesk').first()
        L1_manager = cl_Person.objects.filter(id=helpdesk_team.L1_Manager_id).first()
        recepient = [L1_manager.e_person_email]
        telegram_chat_id=[L1_manager.telegram_chatid]
     

        for i in list_id:
            nchange = cl_New_change.objects.filter(id=i).first()
            nchange.ch_status = "Waiting for Approval"
            nchange.save()
        
        try:
            mail_sender()
            subject = 'Request for Approval of Change Request'
            message = f'Please approve Following Change Request for further process.\nRequest ID : "{ list_id }"'
            sender = settings.EMAIL_HOST_USER
            send_mail(subject, message, sender, recepient, fail_silently=False)
            send_telegram_message(token=settings.BOT_TOKEN, chat_id=telegram_chat_id, text= message)
        except:
            raise Exception('Please Configure Email Sender Details')
        # try:
        #     mail_sender()
        #     list_id = request.POST.getlist('id[]')
        #     change_approve = cl_New_change.objects.filter(id=list_id[0]).first()
        #     subject = 'Welcome to Olatech Solutions'
        #     message = f'Please approve Following Change for further process.\nChange ID : "{list_id[0]}" Change Description : "{change_approve.txt_description}" '
        #     sender = settings.EMAIL_HOST_USER
        #     # # recepient = ['ankush.n@olatechs.com', 'mangesh.b@olatechs.com']
        #     send_mail(subject, message, sender, recepient, fail_silently=False)
        #     send_telegram_message(token=settings.BOT_TOKEN, chat_id=telegram_chat_id, text= f'Please approve Following Change for further process. Change ID : "{list_id[0]}" ')

        # except:
        #     raise Exception('Please Configure Email Sender Details')
        
    return redirect('newchange')


######################### Incident Mangement ####################################

@login_required(login_url='/login_render/')
def user_request(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    user = adminuser.objects.filter(email=request.user).first()
    if user.ch_organization.ch_name == 'Inhouse':
        ur = cl_User_request.objects.all()
        allservice = cl_Service.objects.all()
        ser_sub = cl_Service_subcategory.objects.all()
        nchange = cl_New_change.objects.all()
        org = cl_New_organization.objects.all()
        allteam = cl_Team.objects.all()
        team_person = cl_Person.objects.all()
        if request.method == "GET":
            q = request.GET.get('searchstatus')
            if q != None:
                ur = cl_User_request.objects.filter(ch_status__icontains=q)

    elif user.ch_organization.ch_name != 'Inhouse':
        org = cl_New_organization.objects.filter(ch_name=user.ch_organization)
        allteam = cl_Team.objects.filter(ch_organization=user.ch_organization)
        team_person = cl_Person.objects.filter(e_person_email=user.email)
        ur = cl_User_request.objects.filter(fk_organization=user.ch_organization)
        customer_contract = cl_Customer_contract.objects.filter(ch_ccustomer=user.ch_organization)
        allservice = []
        for s in customer_contract:
            cust_ser = s.ch_services.through.objects.filter(cl_customer_contract_id=s.id)
            for x in cust_ser:
                service_in_contract = cl_Service.objects.filter(id=x.cl_service_id).first()
                if service_in_contract not in allservice:
                    allservice.append(service_in_contract)
        ser_sub = []
        for sub in allservice:
            s = sub.ch_service_subcategory.through.objects.filter(cl_service_id=sub.id)
            for x in s:
                sub_in_cont = cl_Service_subcategory.objects.filter(id=x.cl_service_subcategory_id).first()
                ser_sub.append(sub_in_cont)
        nchange = cl_New_change.objects.filter(ch_organization=user.ch_organization)
        if request.method == "GET":
            q = request.GET.get('searchstatus')
            if q != None:
                ur = cl_User_request.objects.filter(ch_status__icontains=q)
    page = request.GET.get('page', 1)
    paginator = Paginator(ur, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    TTO_Calculation()

    context = {
            'ur': ur,
            'users':users,
            'permission':permission,
            'org':org,
            'allteam':allteam,
            'team_person':team_person,
            'allservice':allservice,
            'ser_sub':ser_sub,
            'nchange':nchange
            }
    return render(request, 'tool/userrequest.html', context)

def escalation_mail(req_status, id):
        ur_raised = cl_User_request.objects.filter(id=id).first()

        if req_status == "TTO Escalated":
            message = f' User "{ur_raised.ch_request_type}" request raised by "{ur_raised.fk_organization}", Request ID : "{ur_raised.id}", Request Priority : "{ur_raised.ch_priority}" is {req_status} ' 
            subject = 'User Request TTO Escalation'
        elif req_status == "TTR Escalated":
            message = f'User "{ur_raised.ch_request_type}" request raised by "{ur_raised.fk_organization}", Request ID : "{ur_raised.id}", Request Priority : "{ur_raised.ch_priority}" is {req_status} ' 
            subject = 'User Request TTR Escalation'

        helpdesk_L2 = cl_Team.objects.filter(ch_teamname='Helpdesk').first()
        recepient = [helpdesk_L2.L2_Manager.e_person_email]
        telchat_id=helpdesk_L2.L2_Manager.telegram_chatid,

        try:
            mail_sender()
            sender = settings.EMAIL_HOST_USER
            send_mail(subject, message, sender, recepient, fail_silently=False)
        except:
            print('email not send')
        try:
            send_telegram_message(token=settings.BOT_TOKEN, chat_id=telchat_id, text=message)
        except:
            print('Telegram notification not send')


def TTO_Calculation():
    ur = cl_User_request.objects.all()
    for i in ur:
        ur_tto = None
        ur_ttr = None
        ur_sub_cate = i.ch_service_subcategory
        ur_sla = cl_Sla.objects.filter(id=ur_sub_cate.id).first()
        ur_slt = ur_sla.slts.through.objects.filter(cl_sla_id=ur_sla.id)
        if i.ch_status != "Waiting for Approval" and i.ch_status != "Resolved":
            if (i.ch_assign_agent == "Deallocate" and i.ch_status != "TTO Escalated") or i.ch_status == "Approved":
                for s in ur_slt:
                    queryset = cl_Slt.objects.filter(id=int(s.cl_slt_id), ch_priority=i.ch_priority, ch_request_type=i.ch_request_type)
                    if queryset != None:
                        for k in queryset:
                            if k.ch_metric == "TTO":
                                if k.ch_unit == "Hours":
                                    tto_min = int(k.ch_value)*60
                                    tto_escalation = i.dt_start_date + timedelta(minutes=tto_min)
                                    ur_tto = tto_escalation.strftime('%Y-%m-%dT%H:%M')
                                else:
                                    tto_escalation = i.dt_start_date + timedelta(minutes=int(k.ch_value))
                                    ur_tto = tto_escalation.strftime('%Y-%m-%dT%H:%M')
                                print(ur_tto)
                                ur_tto_Date = datetime.strptime(ur_tto, '%Y-%m-%dT%H:%M')
                                if datetime.date(ur_tto_Date) < datetime.date(datetime.now()) and i.ch_assign_agent == 'Deallocate':
                                    i.ch_status = "TTO Escalated"
                                    i.save()
                                    escalation_mail(i.ch_status,i.id)
                                    print("Status changed -> TTO Escalate")
                                elif datetime.date(ur_tto_Date) == datetime.date(datetime.now()) and datetime.time(ur_tto_Date) < datetime.time(datetime.now()) and i.ch_assign_agent == 'Deallocate':
                                    i.ch_status = "TTO Escalated"
                                    i.save()
                                    escalation_mail(i.ch_status,i.id)
                                    print("Status changed -> TTO Escalate")
                                else:
                                    i.ch_status = i.ch_status
                                    i.save()
            elif i.ch_status == "Assigned":
                for s in ur_slt:
                    queryset = cl_Slt.objects.filter(id=int(s.cl_slt_id), ch_priority=i.ch_priority, ch_request_type=i.ch_request_type)
                    if queryset != None:
                        for k in queryset:
                            if k.ch_metric == "TTR":
                                if k.ch_unit == "Hours":
                                    ttr_min = int(k.ch_value)*60
                                    ttr_escalation = i.dt_Request_Assign_date + timedelta(minutes=ttr_min)
                                    ur_ttr = ttr_escalation.strftime('%Y-%m-%dT%H:%M')
                                    ur_ttr_Date = datetime.strptime(ur_ttr, '%Y-%m-%dT%H:%M')
                                else:
                                    ttr_escalation = i.dt_Request_Assign_date + timedelta(minutes=int(k.ch_value))
                                    ur_ttr = ttr_escalation.strftime('%Y-%m-%dT%H:%M')
                                print(ur_ttr)
                                ur_ttr_Date = datetime.strptime(ur_ttr, '%Y-%m-%dT%H:%M')
                                if datetime.date(ur_ttr_Date) < datetime.date(datetime.now()) and i.ch_status == "Assigned":
                                    i.ch_status = "TTR Escalated"
                                    i.save()
                                    escalation_mail(i.ch_status,i.id)
                                    print("Status changed -> TTR Escalate")
                                elif datetime.date(ur_ttr_Date) == datetime.date(datetime.now()) and datetime.time(ur_ttr_Date) < datetime.time(datetime.now()) and i.ch_assign_agent != 'Deallocate':
                                    i.ch_status = "TTR Escalated"
                                    i.save()
                                    escalation_mail(i.ch_status,i.id)
                                    print("Status changed -> TTR Escalate")
                                else:
                                    i.ch_status = i.ch_status
                                    i.save()


def get_SubCategory_by_service_for_UR(request):
    service_id = request.GET.get('serviceId')
    services = cl_Service.objects.filter(id=int(service_id)).first()
    ser_subcategory = services.ch_service_subcategory.through.objects.filter(cl_service_id=services.id)
    subcategory_list = []

    for s in ser_subcategory:
        queryset = cl_Service_subcategory.objects.filter(id__icontains=int(s.cl_service_subcategory_id))
        data = []

        for obj in queryset:
            data.append({
                'id': obj.id,
                'ch_subname': obj.ch_subname,
                'ch_status': obj.ch_status,
                'ch_request_type': obj.ch_request_type,
                'txt_description': obj.txt_description,
            })
            subcategory_list.append(data)

    json_data = json.dumps(subcategory_list)
    return HttpResponse(json_data, content_type='application/json')



@login_required(login_url='/login_render/')
def UADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        fk_organization = cl_New_organization.objects.filter(
            id=request.POST.get('ch_organization')).first()
        fk_caller = cl_Person.objects.filter(id=request.POST.get('ch_caller')).first()
        ch_status = request.POST.get('ch_status')
        ch_origin = request.POST.get('ch_origin')
        ch_title = request.POST.get('ch_title')
        ch_request_type = request.POST.get('ch_request_type')
        ch_impact = request.POST.get('ch_impact')
        ch_priority = request.POST.get('ch_priority')   
        dt_start_date = request.POST.get('dt_start_date')
        dt_updated_date = request.POST.get('dt_Updated_date')
        ch_service =cl_Service.objects.filter(id=request.POST.get('ch_sername')).first()
        ch_service_subcategory = cl_Service_subcategory.objects.filter(id=request.POST.get('ch_ser_sub')).first()
        try:
            ch_parent_request = cl_User_request.objects.filter(id=request.POST.get('ch_parent_request_id')).first()
        except:
            ch_parent_request = None
        try:
            ch_parent_change = cl_New_change.objects.filter(id=request.POST.get('ch_parent_change_id')).first()
        except:
            ch_parent_change = None
        txt_description = request.POST.get('txt_description')
        
        ur = cl_User_request(
            fk_organization=fk_organization,
            fk_caller=fk_caller,
            ch_status=ch_status,
            ch_origin=ch_origin,
            ch_title=ch_title,
            ch_request_type=ch_request_type,
            ch_impact=ch_impact,
            ch_priority=ch_priority,
            dt_start_date =dt_start_date,
            dt_Updated_date =dt_updated_date,
            ch_service =ch_service,
            ch_service_subcategory =ch_service_subcategory,
            ch_parent_request=ch_parent_request,
            ch_parent_change =ch_parent_change,
            txt_description =txt_description,
            # reopen_reason = reopen_reason,
        )
        ur.save()

        ur_raised = cl_User_request.objects.latest('id')
        subject = 'New User request raised'
        message = f'User "{ur_raised.ch_request_type}" request raised by "{ur_raised.fk_organization}", Request ID : "{ur_raised.id}", Request Priority is "{ur_raised.ch_priority}"' 
        helpdesk_L1 = cl_Team.objects.filter(ch_teamname='Helpdesk').first()
        recepient = [helpdesk_L1.L1_Manager.e_person_email]
        telchat_id=helpdesk_L1.L1_Manager.telegram_chatid,

        try:
            mail_sender()
            sender = settings.EMAIL_HOST_USER
            send_mail(subject, message, sender, recepient, fail_silently=False)
        except:
            print('email not send')
        try:
            send_telegram_message(token=settings.BOT_TOKEN, chat_id=telchat_id, text=message)
        except:
            print('Telegram notification not send')

        admin_name = request.session["username"]
        adminaction = "addtion of user request"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('userrequest')
    return render(request, 'tool/userrequest.html',{'permission':permission})


@login_required(login_url='/login_render/')
def UEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    ur = cl_User_request.objects.all()
    context = {
        'ur': ur,
        'permission':permission
    }
    return render(request, 'tool/userrequest.html', context)



@login_required(login_url='/login_render/')
def UUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ur1 = cl_User_request.objects.filter(id=id).first()

        fk_organization = cl_New_organization.objects.filter(
            ch_name=request.POST.get('ch_organization')).first()
        fk_caller = cl_Person.objects.filter(ch_person_firstname=request.POST.get('ch_caller')).first()
        ch_status = request.POST.get('ch_status')
        ch_origin = request.POST.get('ch_origin')
        ch_title = request.POST.get('ch_title')
        ch_request_type = request.POST.get('ch_request_type')
        ch_impact = request.POST.get('ch_impact')
        ch_priority = request.POST.get('ch_priority')   
        dt_start_date = request.POST.get('dt_start_date')
        dt_updated_date = request.POST.get('dt_Updated_date')
        ch_service =cl_Service.objects.filter(id=request.POST.get('ch_sername')).first()
        ch_service_subcategory = cl_Service_subcategory.objects.filter(id=request.POST.get('ch_ser_sub')).first()
        # slt_id = int(request.POST.get('select_service_slt'))
        # ch_service_slts = cl_Slt.objects.filter(id=slt_id).first()
        try:
            ch_parent_request = cl_User_request.objects.filter(id=request.POST.get('ch_parent_request_id')).first()
        except:
            ch_parent_request = None
        
        try:
            ch_parent_change = cl_New_change.objects.filter(id=request.POST.get('ch_parent_change_id')).first()
        except:
            ch_parent_change = None

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
            ch_priority=ch_priority,
            dt_start_date =dt_start_date,
            dt_Updated_date =dt_updated_date,
            ch_service =ch_service,
            ch_service_subcategory =ch_service_subcategory,
            # ch_service_slts=ch_service_slts,
            ch_parent_request=ch_parent_request,
            ch_parent_change =ch_parent_change,
            txt_description =txt_description,
            ch_assign_agent =ur1.ch_assign_agent
        )
        ur.save()
        admin_name = request.session["username"]
        adminaction = "update the user request"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)

        return redirect('userrequest')
    return render(request, 'tool/userrequest.html',{'permission':permission})


@login_required(login_url='/login_render/')
def UDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            ur = cl_User_request.objects.filter(id=i).first()
            ur.delete()
    admin_name = request.session["username"]
    adminaction = "deletion of user request"
    event ="event"
    resultcode = "200"
    user_activity(admin_name, adminaction, event, resultcode)
    return redirect('userrequest')


@login_required(login_url='/login_render/')
def escalate_notify(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    ur = cl_User_request.objects.all()
    return render(request, 'tool/userrequest.html', {'ur': ur, 'permission':permission})

########## Assign For User Request ############


@login_required(login_url='/login_render/')
def assign_URModal(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        p_Emp_id = request.POST.get('p')
        per = cl_Person.objects.filter(id=p_Emp_id).first()
        telegram_chat_id = per.telegram_chatid
     
        for i in list_id:
            ur = cl_User_request.objects.filter(id=i).first()
            ur.ch_assign_agent = per.ch_person_firstname
            ur.ch_status = "Assigned" 
            now = datetime.now()
            ur.dt_Request_Assign_date = now.strftime("%Y-%m-%d %H:%M:00")  
            ur.save()

        try:
            mail_sender()
            subject = 'User Request Assign'
            message = f'User Request ID : "{list_id}" Assigned to you'
            sender = settings.EMAIL_HOST_USER
            recepient = [per.e_person_email]
            send_mail(subject, message, sender, recepient, fail_silently=False)
            send_telegram_message(token=settings.BOT_TOKEN, chat_id=telegram_chat_id, text= message)
            return JsonResponse({'result': 'success'})
        except:
            print('email not send')
        

        admin_name = request.session["username"]
        adminaction = "assign the changes"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        ur = cl_User_request.objects.all()
        context = {
            'ur': ur,
            'permission':permission
        }
    return render(request, 'tool/tassign.html', context)

########## Approved Change For Incident Management############

@login_required(login_url='/login_render/')
def change_approved(request):
    # permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
          
        for i in list_id:
            ur = cl_User_request.objects.filter(id=i).first()
            ur.ch_status = "Approved"
            ur.save()
    return redirect('userrequest')


########## Status Close For Incident Management############

@login_required(login_url='/login_render/')
def im_resolved(request):
    # permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')      
              
        for i in list_id:
            ur = cl_User_request.objects.filter(id=i).first()
            ur.ch_status = "Resolved"
            ur.save() 
            
        req_caller = cl_Person.objects.filter(id=ur.fk_caller_id).first()   
        helpdesk_team = cl_Team.objects.filter(ch_teamname='Helpdesk').first()
        L1_Manager = cl_Person.objects.filter(id=helpdesk_team.L1_Manager_id).first()  
        L2_Manager = cl_Person.objects.filter(id=helpdesk_team.L2_Manager_id).first()  
        all_chat_ids = [req_caller.telegram_chatid,L1_Manager.telegram_chatid,L2_Manager.telegram_chatid]
        try:
            mail_sender()
            subject = 'User Request Resolved'
            message = f'User Request ID : "{list_id}" is resolved successfully.'
            sender = settings.EMAIL_HOST_USER
            recepient = [req_caller.e_person_email,L1_Manager.e_person_email,L2_Manager.e_person_email]
            send_mail(subject, message, sender, recepient, fail_silently=False)
            for i in all_chat_ids:
                send_telegram_message(token=settings.BOT_TOKEN, chat_id=i, text= message)
            return JsonResponse({'result': 'success'})
        except:
            print('email not send')
    return redirect('userrequest')


########## Reopen Change For Incident Management############

@login_required(login_url='/login_render/')
def reopen(request):
    # permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')  
              
        for i in list_id:
            ur = cl_User_request.objects.filter(id=i).first()
            ur.ch_status = "Reopen"
            ur.save()

        subject = 'User request Reopened'
        message = f'User Request IDs : "{list_id}" are reopened' 
        helpdesk_L1 = cl_Team.objects.filter(ch_teamname='Helpdesk').first()
        recepient = [helpdesk_L1.L1_Manager.e_person_email]
        telchat_id=helpdesk_L1.L1_Manager.telegram_chatid,

        try:
            mail_sender()
            sender = settings.EMAIL_HOST_USER
            send_mail(subject, message, sender, recepient, fail_silently=False)
        except:
            print('email not send')
        try:
            send_telegram_message(token=settings.BOT_TOKEN, chat_id=telchat_id, text=message)
        except:
            print('Telegram notification not send')
        
    return redirect('userrequest')




########## Approved Change For Change Management############

@login_required(login_url='/login_render/')
def cm_approved(request):
    # permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
          
        for i in list_id:
            cm = cl_New_change.objects.filter(id=i).first()
            cm.ch_status = "Approved"
            cm.save()

    return redirect('newchange')


########## Status Close For Change Management############

@login_required(login_url='/login_render/')
def cm_close(request):
    # permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')      
              
        for i in list_id:
            cm = cl_New_change.objects.filter(id=i).first()
            cm.ch_status = "Resolved"
            cm.save()
        
        req_caller = cl_Person.objects.filter(id=cm.ch_caller_id).first()   
        helpdesk_team = cl_Team.objects.filter(ch_teamname='Helpdesk').first()
        L1_Manager = cl_Person.objects.filter(id=helpdesk_team.L1_Manager_id).first()  
        L2_Manager = cl_Person.objects.filter(id=helpdesk_team.L2_Manager_id).first()  
        all_chat_ids = [req_caller.telegram_chatid,L1_Manager.telegram_chatid,L2_Manager.telegram_chatid]
        try:
            mail_sender()
            subject = 'Change Request Resolved'
            message = f'Change Request ID : "{list_id}" is resolved successfully.'
            sender = settings.EMAIL_HOST_USER
            recepient = [req_caller.e_person_email,L1_Manager.e_person_email,L2_Manager.e_person_email]
            send_mail(subject, message, sender, recepient, fail_silently=False)
            for i in all_chat_ids:
                send_telegram_message(token=settings.BOT_TOKEN, chat_id=i, text= message)
            return JsonResponse({'result': 'success'})
        except:
            print('email not send')
            
    return redirect('newchange')


########## Reopen Change For Change Management############

@login_required(login_url='/login_render/')
def cm_reopen(request):
    if request.method == "POST":
        reason = request.POST.get('reason')
        ur_id = request.POST.getlist('ur_id[]')   
        cl_Reopen.objects.create(txt_reopen=reason,ureq_id=ur_id)
           
        for i in ur_id:
            cm = cl_New_change.objects.filter(id=i).first()
            cm.ch_status = "Reopen"
            cm.save()
        
        subject = 'Change request Reopened'
        message = f'Change Request IDs : "{list_id}" are reopened' 
        helpdesk_L1 = cl_Team.objects.filter(ch_teamname='Helpdesk').first()
        recepient = [helpdesk_L1.L1_Manager.e_person_email]
        telchat_id=helpdesk_L1.L1_Manager.telegram_chatid,

        try:
            mail_sender()
            sender = settings.EMAIL_HOST_USER
            send_mail(subject, message, sender, recepient, fail_silently=False)
        except:
            print('email not send')
        try:
            send_telegram_message(token=settings.BOT_TOKEN, chat_id=telchat_id, text=message)
        except:
            print('Telegram notification not send')
    return redirect('newchange')


########## Approve Change For Incident Management############

@login_required(login_url='/login_render/')
def send_approval_Mail_UR(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        helpdesk_team = cl_Team.objects.filter(ch_teamname='Helpdesk').first()
        L1_manager = cl_Person.objects.filter(id=helpdesk_team.L1_Manager_id).first()
        recepient = [L1_manager.e_person_email]
        telegram_chat_id=[L1_manager.telegram_chatid]
              
        for i in list_id:
            ur = cl_User_request.objects.filter(id=i).first()
            ur.ch_status = "Waiting for Approval"
            ur.save()

        try:
            mail_sender()
            subject = 'Request for Approval of User Request'
            message = f'Please approve Following User Request for further process.\nRequest ID : "{list_id}"'
            sender = settings.EMAIL_HOST_USER
            send_mail(subject, message, sender, recepient, fail_silently=False)
            send_telegram_message(token=settings.BOT_TOKEN, chat_id=telegram_chat_id, text= message)

        except:
            raise Exception('Please Configure Email Sender Details')
        
    return redirect('userrequest')

    # return render(request, 'tool/approve_change.html',{'permission':permission})
 


#######################################################

@login_required(login_url='/login_render/')
def customer_contract(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    cust = cl_Customer_contract.objects.all()
    servi = cl_Service.objects.all()

    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            cust = cl_Customer_contract.objects.filter(ch_cname__icontains=q)
    org = cl_New_organization.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(cust, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'tool/scustomer_contract.html', {'cust': cust,'servi':servi, 'org':org,'users':users,'permission':permission})

def get_service_by_Customer_contract(request):
    customer_contractID = request.GET.get('customer_contractID')
    customer_contract = cl_Customer_contract.objects.filter(id=int(customer_contractID)).first()

    services = customer_contract.ch_services.through.objects.filter(cl_customer_contract_id=customer_contract.id)
    print("HII",services)
    queryset_list = []

    for s in services:
        queryset = cl_Service.objects.filter(id__icontains=int(s.cl_service_id)).first()
        data = []
        
        data.append({
            'id': queryset.id,
            'ch_ssname': queryset.ch_ssname,
            'ch_status': queryset.ch_status,
        })
        queryset_list.append(data)

    json_data = json.dumps(queryset_list)
    return HttpResponse(json_data, content_type='application/json')

@login_required(login_url='/login_render/')
def SCADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_cname = request.POST.get('ch_cname')
        ch_ccustomer = cl_New_organization.objects.filter(ch_name=request.POST.get('ch_ccustomer_a')).first()
        ch_status = request.POST.get('ch_status')
        ch_contract_type = request.POST.get('ch_contract_type')
        ch_pprovider = cl_New_organization.objects.filter(ch_name=request.POST.get('ch_pprovider_a')).first()
        dt_start_date = request.POST.get('dt_start_date')
        dt_end_date = request.POST.get('dt_end_date')
        i_cost_unit = request.POST.get('i_cost_unit')
        i_cost = request.POST.get('i_cost')
        i_cost_currency = request.POST.get('i_cost_currency')
        i_billing_frequency = request.POST.get('i_billing_frequency')
        txt_description = request.POST.get('txt_description')

        services_ids = request.POST.getlist('service_ids')
        services = cl_Service.objects.filter(id__in=services_ids)

        cust = cl_Customer_contract(
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
        cust.ch_services.set(services)

        admin_name = request.session["username"]
        adminaction = "addition of customer"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('customercontract')
    return render(request, 'tool/scustomer_contract.html',{'permission':permission})


@login_required(login_url='/login_render/')
def SCEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    cust = cl_Customer_contract.objects.all()
    context = {
        'cust': cust,
        'permission':permission
    }
    return render(request, 'tool/scustomer_contract.html', context)


@login_required(login_url='/login_render/')
def SCUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    """
    Function for update change_information
    """
    if request.method == "POST":
        ch_cname = request.POST.get('ch_cname')
        ch_ccustomer = cl_New_organization.objects.filter(ch_name=request.POST.get('ch_ccustomer_e')).first()
        ch_status = request.POST.get('ch_status')
        ch_contract_type = request.POST.get('ch_contract_type')
        ch_pprovider = cl_New_organization.objects.filter(ch_name=request.POST.get('ch_pprovider_e')).first()
        dt_start_date = request.POST.get('dt_start_date')
        dt_end_date = request.POST.get('dt_end_date')
        i_cost_unit = request.POST.get('i_cost_unit')
        i_cost = request.POST.get('i_cost')
        i_cost_currency = request.POST.get('i_cost_currency')
        i_billing_frequency = request.POST.get('i_billing_frequency')
        txt_description = request.POST.get('txt_description')

        services_ids = request.POST.getlist('service_ids_e_'+id)
        services = cl_Service.objects.filter(id__in=services_ids)

        cust = cl_Customer_contract(
            id=id,
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
        cust.ch_services.set(services)

        admin_name = request.session["username"]
        adminaction = "Updation of customer"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)

        return redirect('customercontract')
    return render(request, 'tool/scustomer_contract.html',{'permission':permission})


@login_required(login_url='/login_render/')
def SCDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            cust = cl_Customer_contract.objects.filter(id=i).first()
            cust.delete()
    return redirect('customercontract')


################### Provider Contract ##################

@login_required(login_url='/login_render/')
def provider_contract(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    pro = cl_Providercontract.objects.all()
    org = cl_New_organization.objects.all()
    servi = cl_Service.objects.all()

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
    return render(request, 'tool/sprovidercontract.html', {'pro': pro,'org':org,'users':users,'servi':servi,'permission':permission})



def get_service_by_Provider_contract(request):
    provider_contractID = request.GET.get('provider_contractID')
    provider_contract = cl_Providercontract.objects.filter(id=int(provider_contractID)).first()

    services = provider_contract.ch_services.through.objects.filter(cl_providercontract_id=provider_contract.id)
    print("HII",services)
    queryset_list = []

    for s in services:
        queryset = cl_Service.objects.filter(id__icontains=int(s.cl_service_id)).first()
        data = []
        
        data.append({
            'id': queryset.id,
            'ch_ssname': queryset.ch_ssname,
            'ch_status': queryset.ch_status,
        })
        queryset_list.append(data)

    json_data = json.dumps(queryset_list)
    return HttpResponse(json_data, content_type='application/json')


@login_required(login_url='/login_render/')
def SPADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_pname = request.POST.get('ch_pname')
        ch_pcprovider = cl_New_organization.objects.filter(ch_name=request.POST.get('ch_customer')).first()
        ch_status = request.POST.get('ch_status')
        ch_contract_type = request.POST.get('ch_contract_type')
        ch_customer = cl_New_organization.objects.filter(ch_name=request.POST.get('ch_customer')).first()
        dt_start_date = request.POST.get('dt_start_date')
        dt_end_date = request.POST.get('dt_end_date')
        i_cost_unit = request.POST.get('i_cost_unit')
        i_cost = request.POST.get('i_cost')
        i_cost_currency = request.POST.get('i_cost_currency')
        i_billing_frequency = request.POST.get('i_billing_frequency')
        txt_description = request.POST.get('txt_description')
        
        services_ids = request.POST.getlist('service_ids')
        services = cl_Service.objects.filter(id__in=services_ids)

        pro = cl_Providercontract(
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
        )
        pro.save()
        pro.ch_services.set(services)

        admin_name = request.session["username"]
        adminaction = "deletion of user request"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('providercontract')
    return render(request, 'tool/sprovidercontract.html',{'permission':permission})


@login_required(login_url='/login_render/')
def SPEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    pro = cl_Providercontract.objects.all()
    context = {
        'pro': pro,
        'permission':permission
    }
    return render(request, 'tool/sprovidercontract.html', context)


@login_required(login_url='/login_render/')
def SPUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    """
    Function for update change_information
    """
    if request.method == "POST":
        pro_contract = cl_Providercontract.objects.filter(id=id).first()
        ch_pname = request.POST.get('ch_pname')
        ch_pcprovider = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_provider'))).first()
        ch_status = request.POST.get('ch_status')
        ch_contract_type = request.POST.get('ch_contract_type')
        ch_customer = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_customer'))).first()
        dt_start_date = pro_contract.dt_start_date
        dt_end_date = request.POST.get('dt_end_date')
        i_cost_unit = request.POST.get('i_cost_unit')
        i_cost = request.POST.get('i_cost')
        i_cost_currency = request.POST.get('i_cost_currency')
        i_billing_frequency = request.POST.get('i_billing_frequency')
        txt_description = request.POST.get('txt_description')

        services_ids = request.POST.getlist("service_ids_e_"+id)
        services = cl_Service.objects.filter(id__in=services_ids)
        
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
        )
        pro.save()
        pro.ch_services.set(services)
        return redirect('providercontract')
    return render(request, 'tool/sprovidercontract.html',{'permission':permission})


@login_required(login_url='/login_render/')
def SPDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            pro = cl_Providercontract.objects.filter(id=i).first()
            pro.delete()
    return redirect('providercontract')


@login_required(login_url='/login_render/')
def servicefamilies(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    sf = cl_Servicefamilies.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            sf = cl_Servicefamilies.objects.filter(ch_sname__icontains=q)

    page = request.GET.get('page', 1)
    paginator = Paginator(sf, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
 

    context = {
        'sf': sf,
        'users':users,
        'permission':permission
    }
    return render(request, 'tool/sservicefamily.html', context)


@login_required(login_url='/login_render/')
def SFADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_sname = request.POST.get('ch_sname')
        sf = cl_Servicefamilies(
            # id=id,
            ch_sname=ch_sname,
        )
        sf.save()
        return redirect('servicefamilies')
    return render(request, 'tool/sservicefamily.html',{'permission':permission})


@login_required(login_url='/login_render/')
def SFEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    sf = cl_Servicefamilies.objects.all()
    context = {
        'sf': sf,
        'permission':permission
    }
    return render(request, 'tool/sservicefamily.html', context)


@login_required(login_url='/login_render/')
def SFUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_sname = request.POST.get('ch_sname')
        sf = cl_Servicefamilies(
            id=id,
            ch_sname=ch_sname,
        )
        sf.save()
        return redirect('servicefamilies')
    return redirect(request, 'tool/sservicefamily.html',{'permission':permission})


@login_required(login_url='/login_render/')
def SFDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            sf = cl_Servicefamilies.objects.filter(id=i).first()
            sf.delete()
    return redirect('servicefamilies')

##################### Service #######################

@login_required(login_url='/login_render/')
def sservice(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    ser = cl_Service.objects.all()
    org = cl_New_organization.objects.all()
    s_sub_category = cl_Service_subcategory.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            ser = cl_Service.objects.filter( ch_ssname__icontains=q)
    page = request.GET.get('page', 1)
    paginator = Paginator(ser, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'tool/sservice.html', {'ser': ser,'s_sub_category':s_sub_category,'org':org,'users':users,'permission':permission})

def get_SubCategory_by_service_for_UR(request):
    service_id = request.GET.get('serviceId')
    services = cl_Service.objects.filter(id=int(service_id)).first()
    ser_subcategory = services.ch_service_subcategory.through.objects.filter(cl_service_id=services.id)
    subcategory_list = []
    for s in ser_subcategory:
        queryset = cl_Service_subcategory.objects.filter(id__icontains=int(s.cl_service_subcategory_id))
        data = []
        for obj in queryset:
            data.append({
                'id': obj.id,
                'ch_subname': obj.ch_subname,
                'ch_status': obj.ch_status,
                'ch_request_type': obj.ch_request_type,
                'txt_description': obj.txt_description,
            })
            subcategory_list.append(data)
    json_data = json.dumps(subcategory_list)
    return HttpResponse(json_data, content_type='application/json')

def get_service_sub_by_service_for_service_html(request):
    service_id = request.GET.get('serviceId')
    services = cl_Service.objects.filter(id=int(service_id)).first()

    ser_subcategory = services.ch_service_subcategory.through.objects.filter(cl_service_id=services.id)
    print("HII",ser_subcategory)
    queryset_list = []

    for s in ser_subcategory:
        queryset = cl_Service_subcategory.objects.filter(id__icontains=int(s.cl_service_subcategory_id)).first()
        data = []

        data.append({
            'id': queryset.id,
            'ch_subname': queryset.ch_subname,
            'ch_status': queryset.ch_status,
            'ch_request_type': queryset.ch_request_type,
            'txt_description': queryset.txt_description,
        })
        queryset_list.append(data)

    json_data = json.dumps(queryset_list)
    return HttpResponse(json_data, content_type='application/json')
    

@login_required(login_url='/login_render/')
def SSADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_ssname = request.POST.get('ch_ssname')
        ch_sprovider = cl_New_organization.objects.filter(ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        s_subcategory_ids = request.POST.getlist("s_sub_category_ids")
        ch_status = request.POST.get('ch_status')
        txt_description = request.POST.get('txt_description')

        subcategory = cl_Service_subcategory.objects.filter(id__in=s_subcategory_ids)

        ser = cl_Service(
            ch_ssname=ch_ssname,
            ch_sprovider=ch_sprovider,
            ch_status=ch_status,
            txt_description=txt_description,
        )
        ser.save()
        ser.ch_service_subcategory.set(subcategory)
        return redirect('service')
    return render(request, 'tool/sservice.html',{'permission':permission})


@login_required(login_url='/login_render/')
def SSEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    ser = cl_Service.objects.all()
    context = {
        'ser': ser,
        'permission':permission
    }
    return render(request, 'tool/sservice.html', context)


@login_required(login_url='/login_render/')
def SSUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    """
    Function for update change_information
    """
    if request.method == "POST":
        ch_ssname = request.POST.get('ch_ssname')
        ch_sprovider = cl_New_organization.objects.filter(ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        s_subcategory_ids = request.POST.getlist("e_s_sub_category_id_"+id)
        ch_status = request.POST.get('ch_status')
        txt_description = request.POST.get('txt_description')

        subcategory = cl_Service_subcategory.objects.filter(id__in=s_subcategory_ids)

        ser = cl_Service(
            id=id,
            ch_ssname=ch_ssname,
            ch_sprovider=ch_sprovider,
            ch_status=ch_status,
            txt_description=txt_description,
        )
        ser.save()
        ser.ch_service_subcategory.set(subcategory)
        return redirect('service')
    return render(request, 'tool/sservice.html',{'permission':permission})


@login_required(login_url='/login_render/')
def SSDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            ser = cl_Service.objects.filter(id=i).first()
            ser.delete()
    return redirect('service')

######################################################


@login_required(login_url='/login_render/')
def service_subcategory(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    sub = cl_Service_subcategory.objects.all()
    ser = cl_Service.objects.all()
    sla = cl_Sla.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            sub = cl_Service_subcategory.objects.filter(ch_subname__icontains=q)

    page = request.GET.get('page', 1)

    paginator = Paginator(sub, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {
        'sub': sub,
        'sla':sla,
        'ser':ser,
        'users':users,
        'permission':permission
    }

    return render(request, 'tool/service_subcategory.html', context)


@login_required(login_url='/login_render/')
def SADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_subname = request.POST.get('ch_subname')
        # ch_sservice = cl_Service.objects.filter(ch_ssname=request.POST.get('ch_sservice')).first()
        ch_status = request.POST.get('ch_status')	
        ch_sla = cl_Sla.objects.filter(ch_slname=request.POST.get('ch_sla')).first()
        ch_request_type = request.POST.get('ch_request_type')
        txt_description = request.POST.get('txt_description')

        sub = cl_Service_subcategory(
            ch_subname=ch_subname,
            # ch_sservice=ch_sservice,
            ch_status=ch_status,
            ch_sla=	ch_sla,
            ch_request_type=ch_request_type,
            txt_description=txt_description,
        )
        sub.save()
        return redirect('service_subcategory')
    return render(request, 'tool/service_subcategory.html',{'permission':permission})


@login_required(login_url='/login_render/')
def SEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    sub = cl_Service_subcategory.objects.all()
    context = {
        'sub': sub,
        'permission':permission
    }
    return render(request, 'tool/service_subcategory.html', context)


@login_required(login_url='/login_render/')
def SUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    """
    Function for update change_information
    """
    if request.method == "POST":
        ch_subname = request.POST.get('ch_subname')
        # ch_sservice = cl_Service.objects.filter(ch_ssname=request.POST.get('ch_sservice')).first()
        ch_status = request.POST.get('ch_status')	
        ch_sla = cl_Sla.objects.filter(ch_slname=request.POST.get('ch_sla')).first()
        ch_request_type = request.POST.get('ch_request_type')
        txt_description = request.POST.get('txt_description')
        sub = cl_Service_subcategory(
            id=id,
            ch_subname=ch_subname,
            # ch_sservice=ch_sservice,
            ch_status=ch_status,
            ch_sla=	ch_sla,
            ch_request_type=ch_request_type,
            txt_description=txt_description,
        )
        sub.save()
        return redirect('service_subcategory')
    return render(request, 'tool/service_subcategory.html',{'permission':permission})


@login_required(login_url='/login_render/')
def SDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            sub = cl_Service_subcategory.objects.filter(id=i).first()
            sub.delete() 
    return redirect('service_subcategory')


#########################################################

@login_required(login_url='/login_render/')
def sla(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    sl = cl_Sla.objects.all()
    slts = cl_Slt.objects.all()

    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            sl = cl_Sla.objects.filter(ch_slname__icontains=q)
    org = cl_New_organization.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(sl, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
   
    return render(request, 'tool/ssla.html', {'sl': sl, 'slts':slts, 'org':org,'users':users, 'permission':permission})


@login_required(login_url='/login_render/')
def SLADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_sl_name = request.POST.get('ch_slname')
        ch_slaprovider = cl_New_organization.objects.filter(ch_name=request.POST.get('ch_organization')).first()
        txt_description = request.POST.get('txt_description')
        slt_ids = request.POST.getlist("slt_ids")
        slts = []
        for i in slt_ids:
            x = (cl_Slt.objects.filter(id=i).first()).id
            slts.append(x)

        sl = cl_Sla(
            ch_slname=ch_sl_name,
            ch_slaprovider=ch_slaprovider,
            txt_description=txt_description,
        )
        sl.save()
        sl.slts.set(slts)
        return redirect('sla')
    return render(request, 'tool/ssla.html',{'permission':permission})


def get_slt_by_sla(request):
    slaId = request.GET.get('slaId')
    sla = cl_Sla.objects.filter(id=int(slaId)).first()

    slt = sla.slts.through.objects.filter(cl_sla_id=sla.id)
    
    queryset_list = []
    for i in slt:
        data = []
        queryset = cl_Slt.objects.filter(id__icontains=i.cl_slt_id).first()
        data.append({
            'id': queryset.id,
            'ch_name': queryset.ch_name,
            'ch_priority': queryset.ch_priority,
            'ch_request_type': queryset.ch_request_type,
            'ch_metric': queryset.ch_metric,
            'ch_value': queryset.ch_value,
            'ch_unit': queryset.ch_unit
        })
        queryset_list.append(data)

    json_data = json.dumps(queryset_list)
    return HttpResponse(json_data, content_type='application/json')


@login_required(login_url='/login_render/')
def SLEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    sl = cl_Sla.objects.all()
    context = {
        'sl': sl,
        'permission':permission
    }
    return render(request, 'tool/ssla.html', context)



@login_required(login_url='/login_render/')
def SLUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    """
    Function for update change_information
    """
    if request.method == "POST":
        ch_sl_name = request.POST.get('ch_slname')
        ch_slaprovider = cl_New_organization.objects.filter(ch_name=request.POST.get('ch_organization')).first()
        txt_description = request.POST.get('txt_description')
        slt_ids = request.POST.getlist("e_slt_id_"+id)
        slts = cl_Slt.objects.filter(id__in=slt_ids)

        sl = cl_Sla(
            id=id,
            ch_slname=ch_sl_name,
            ch_slaprovider=ch_slaprovider,
            txt_description=txt_description,
        )
        sl.save()
        sl.slts.set(slts)

        return redirect('sla')
    return render(request, 'tool/ssla.html',{'permission':permission})


@login_required(login_url='/login_render/')
def SLDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            sl = cl_Sla.objects.filter(id=i).first()
            sl.delete()
    return redirect('sla')

################################################

@login_required(login_url='/login_render/')
def SLT(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
   

            # Code to process form data and add to table
        # ...
       


    slt = cl_Slt.objects.all()
  
         
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            slt = cl_Slt.objects.filter(ch_name__icontains=q)

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
        'users':users,
        'permission':permission
    
         
    }
    return render(request, 'tool/sslt.html', context)




@login_required(login_url='/login_render/')
def STADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_name = request.POST.get('ch_name')
        ch_priority = request.POST.get('ch_priority')
        ch_request_type = request.POST.get('ch_request_type')
        ch_metric = request.POST.get('ch_metric')
        ch_value = request.POST.get('ch_value')
        ch_unit = request.POST.get('ch_unit')

        slt = cl_Slt(
            ch_name=ch_name,
            ch_priority=ch_priority,
            ch_request_type=ch_request_type,
            ch_metric=ch_metric,
            ch_value=ch_value,
            ch_unit=ch_unit,
        )
        slt.save()
        return redirect('slt')
    return render(request, 'tool/slt.html',{'permission':permission})


# @login_required(login_url='/login_render/')
# def SLTEdit(request):
#     permission = roles.objects.filter(id=request.session['user_role']).first()
#     slt = cl_Slt.objects.all()
#     context = {
#         'slt': slt,
#         'permission':permission
#     }
#     return render(request, 'tool/slt.html', context)


@login_required(login_url='/login_render/')
def SLTUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
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
    return redirect(request, 'tool/slt.html',{'permission':permission})


@login_required(login_url='/login_render/')
def SLTDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            slt = cl_Slt.objects.filter(id=i).first()
            slt.delete()
    return redirect('slt')


@login_required(login_url='/login_render/')
def servicedelivery(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    sd = cl_Servicedelivery.objects.all()
    org = cl_New_organization.objects.all()

    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            sd = cl_Servicedelivery.objects.filter(ch_sdname__icontains=q)
    page = request.GET.get('page', 1)

    paginator = Paginator(sd, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'tool/sdelivery.html', {'sd': sd,'org':org,'users':users, 'permission':permission})


@login_required(login_url='/login_render/')
def SDADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_sdname = request.POST.get('ch_sdname')
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        txt_description = request.POST.get('txt_description')

        sd = cl_Servicedelivery(
            ch_sdname=ch_sdname,
            ch_organization=ch_organization,
            txt_description=txt_description
        )
        sd.save()
        return redirect('servicedelivery')
    return render(request, 'tool/sdelivery.html',{'permission':permission})


@login_required(login_url='/login_render/')
def SDEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    sd = cl_Servicedelivery.objects.all()
    context = {
        'sd': sd,
        'permission':permission
    }
    return render(request, 'tool/sdelivery.html', context)


@login_required(login_url='/login_render/')
def SDUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    """
    Function for update change_information
    """
    if request.method == "POST":
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
        return redirect('servicedelivery')
    return render(request, 'tool/sdelivery.html',{'permission':permission})


@login_required(login_url='/login_render/')
def SDDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            sd = cl_Servicedelivery.objects.filter(id=i).first()
            sd.delete()
    return redirect('servicedelivery')


@login_required(login_url='/login_render/')
def synchro_data_source(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    form = SyncrodataForm()
    if request.method == 'POST':
        form = SyncrodataForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Add Successfully")
    context = {
        'form': form,
        'permission':permission
        }
    return render(request, 'tool/sysconfisynchro.html', context)


@login_required(login_url='/login_render/')
def oauth_mazuree(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    form = OauthmazureeForm()
    if request.method == 'POST':
        form = OauthmazureeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Add Successfully")
    context = {
        'form': form,
        'permission':permission
        }
    return render(request, 'tool/authmazure.html', context)


########### LDAP USER ############

@login_required(login_url='/login_render/')
def ldapuser(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    ldap = cl_Ldapuser.objects.all()
    call = cl_Person.objects.all()

  
    if request.method == "GET":
        q = request.GET.get('searchstatus')
        if q != None:
            ldap = cl_Ldapuser.objects.filter(ch_status__icontains=q)


    page = request.GET.get('page', 1)
    paginator = Paginator(ldap, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)        
    return render(request, 'tool/ldapuser.html', {'ldap': ldap, 'permission':permission,'users':users,'call':call})



@login_required(login_url='/login_render/')
def ldapADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_person = cl_Person.objects.filter(ch_person_firstname=request.POST.get('ch_person')).first()
        ch_ldapserver = request.POST.get('ch_ldapserver')
        e_email = str.lower(request.POST.get('e_email'))
        ch_login = request.POST.get('ch_login')
        ch_language = request.POST.get('ch_language')
        ch_status = request.POST.get('ch_status')
        ldap = cl_Ldapuser(
            ch_person=ch_person,
            ch_ldapserver=ch_ldapserver,
            e_email=e_email,
            ch_login=ch_login,
            ch_language=ch_language,
            ch_status=ch_status,
        )
        ldap.save()
        return redirect('ldapuser')
    return render(request, 'tool/ldapuser.html',{'permission':permission})


@login_required(login_url='/login_render/')
def ldapEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    ldap = cl_Ldapuser.objects.all()
    context = {
        'ldap': ldap,
        'permission':permission
    }
    return render(request, 'tool/ldapuser.html', context)


@login_required(login_url='/login_render/')
def ldapUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    """
    Function for update change_information
    """
    if request.method == "POST":
        id = request.POST.get('id')
        ch_person = cl_Person.objects.get(ch_person_firstname=request.POST.get('ch_person'))
        ch_ldapserver = request.POST.get('ch_ldapserver')
        e_email = request.POST.get('e_email')
        ch_login = request.POST.get('ch_login')
        ch_language = request.POST.get('ch_language')
        ch_status = request.POST.get('ch_status')
        ldap = cl_Ldapuser(
            id=id,
            ch_person=ch_person,
            ch_ldapserver=ch_ldapserver,
            e_email=e_email,
            ch_login=ch_login,
            ch_language=ch_language,
            ch_status=ch_status,
        )
        ldap.save()
        return redirect('ldapuser')
    return render(request, 'tool/ldapuser.html',{'permission':permission})


@login_required(login_url='/login_render/')
def ldapDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            ldap = cl_Ldapuser.objects.filter(id=i).first()
            ldap.delete()
    return redirect('ldapuser')






########### External User ##########

@login_required(login_url='/login_render/')
def externaluser(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    ext = cl_Externaluser.objects.all()
    call = cl_Person.objects.all()

    if request.method == "GET":
        q = request.GET.get('searchstatus')
        if q != None:
            ext = cl_Externaluser.objects.filter(ch_status__icontains=q)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(ext, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)        
        
    return render(request, 'tool/externaluser.html', {'ext': ext, 'permission':permission,'users':users,'call':call})


@login_required(login_url='/login_render/')
def extADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_person = cl_Person.objects.filter(ch_person_firstname=request.POST.get('ch_person')).first()
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
    return render(request, 'tool/externaluser.html',{'permission':permission})


@login_required(login_url='/login_render/')
def extEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    ext = cl_Externaluser.objects.all()
    context = {
        'ext': ext,
        'permission':permission
    }
    return render(request, 'tool/externaluser.html', context)


@login_required(login_url='/login_render/')
def extUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
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
    return render(request, 'tool/externaluser.html',{'permission':permission})


@login_required(login_url='/login_render/')
def extDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            ext = cl_Externaluser.objects.filter(id=i).first()
            ext.delete()
    return redirect('externaluser')


################### ITSM USER   ##############################

@login_required(login_url='/login_render/')
def itsmuser(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    itsm = cl_ITSM_USER.objects.all()
    call = cl_Person.objects.all()


    if request.method == "GET":
        q = request.GET.get('searchstatus')
        if q != None:
            itsm = cl_ITSM_USER.objects.filter(ch_status__icontains=q)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(itsm, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)       
    context = {
        'users': users,
        'permission':permission,
        'itsm':itsm,
        'call':call
        }
    return render(request, 'tool/itsmuser.html', context)


@login_required(login_url='/login_render/')
def itsmADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_person = cl_Person.objects.filter(ch_person_firstname=request.POST.get('ch_person')).first()
        ch_email = str.lower(request.POST.get('ch_email'))
        ch_login = request.POST.get('ch_login')
        ch_language = request.POST.get('ch_language')
        ch_status = request.POST.get('ch_status')
        ch_password = request.POST.get('ch_password')
        ch_password_expiration = request.POST.get('ch_password_expiration')
        dt_password_renewed_on = request.POST.get('dt_password_renewed_on')


        itsm = cl_ITSM_USER(
            
            ch_person=ch_person,
            ch_email=ch_email,
            ch_login=ch_login,
            ch_language=ch_language,
            ch_status=ch_status,
            ch_password=ch_password,
            ch_password_expiration=ch_password_expiration,
            dt_password_renewed_on=dt_password_renewed_on
        )
        itsm.save()
        return redirect('itsmuser')
    return render(request, 'tool/itsmuser.html',{'permission':permission})


@login_required(login_url='/login_render/')
def itsmEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    itsm = cl_ITSM_USER.objects.all()
    context = {
        'itsm': itsm,
        'permission':permission
    }
    return render(request, 'tool/itsmuser.html', context)


@login_required(login_url='/login_render/')
def itsmUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    """
    Function for update change_information
    """
    if request.method == "POST":
        id = request.POST.get('id')
        ch_person = cl_Person.objects.get(ch_person_firstname=request.POST.get('ch_person'))
        ch_email = str.lower(request.POST.get('ch_email'))
        ch_login = request.POST.get('ch_login')
        ch_language = request.POST.get('ch_language')
        ch_status = request.POST.get('ch_status')
        ch_password = request.POST.get('ch_password')
        ch_password_expiration = request.POST.get('ch_password_expiration')
        dt_password_renewed_on = request.POST.get('dt_password_renewed_on')


        itsm = cl_ITSM_USER(
            id = id,
            ch_person=ch_person,
            ch_email=ch_email,
            ch_login=ch_login,
            ch_language=ch_language,
            ch_status=ch_status,
            ch_password=ch_password,
            ch_password_expiration=ch_password_expiration,
            dt_password_renewed_on=dt_password_renewed_on
        )
        itsm.save()
        return redirect('itsmuser')
    return render(request, 'tool/itsmuser.html',{'permission':permission,'itsm':itsm})



@login_required(login_url='/login_render/')
def itsmDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            itsm = cl_ITSM_USER.objects.filter(id=i).first()
            itsm.delete()
    return redirect('itsmuser')
    
    
    


@login_required(login_url='/login_render/')
def slacknoti(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    form = SlacknotiForm()
    if request.method == 'POST':
        form = SlacknotiForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Add Successfully")
    context = {
        'form': form,
        'permission':permission
        }
    return render(request, 'tool/slacknoti.html', context)


@login_required(login_url='/login_render/')
def micronoti(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    form = MicronotiForm()
    if request.method == 'POST':
        form = MicronotiForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Add Successfully')
    context = {
        'form': form,
        'permission':permission
        }
    return render(request, 'tool/micronoti.html', context)


@login_required(login_url='/login_render/')
def webhook(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    form = WebhookForm()
    if request.method == 'POST':
        form = WebhookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Add Successfully')
    context = {
        'form': form,
        'permission':permission
        }
    return render(request, 'tool/webhook.html', context)


@login_required(login_url='/login_render/')
def googlechat(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    form = GooglechatForm()
    if request.method == 'POST':
        form = GooglechatForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Add Successfully')
    context = {
        'form': form,
        'permission':permission
        }
    return render(request, 'tool/googlechat.html', context)


@login_required(login_url='/login_render/')
def rocketchat(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    form = RocketchatForm()
    if request.method == 'POST':
        form = RocketchatForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Add Successfully')
    context = {
        'form': form,
        'permission':permission
        }
    return render(request, 'tool/rocketchat.html', context)


@login_required(login_url='/login_render/')
def itsmwebhook(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    form = ItsmwebhookForm()
    if request.method == 'POST':
        form = ItsmwebhookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Add Successfully')
    context = {
        'form': form,
        'permission':permission
        }
    return render(request, 'tool/itsmwebhook.html', context)


 ############ CSV ###############

@login_required(login_url='/login_render/')
def csvimport(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
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
    return render(request, 'tool/add_file1.html',{'permission':permission})



@login_required(login_url='/login_render/')
def csv_edit(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    csv = CSV_import.objects.filter(Id = id).first
    context = {
        'csv': csv,
        'permission':permission
    }
    return render(request, 'tool/edit_file.html', context)    


@login_required(login_url='/login_render/')
def csv_update(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
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
    return render(request, 'tool/edit_file.html',{'permission':permission})


@login_required(login_url='/login_render/')
def DeleteCSVAttachedPDF(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    id = request.GET['id']
    csv = CSV_import.objects.filter(Id = id).first()
    file_to_delete = str(csv.disc_Attachment)
    media_path = settings.MEDIA_ROOT
    file_path = os.path.join(media_path, file_to_delete)
    if os.path.exists(file_path):
        os.remove(file_path)
        return HttpResponse(request, 'tool/edit_file.html',{'permission':permission})
    else:
        return HttpResponse(request, 'tool/edit_file.html',{'permission':permission})



@login_required(login_url='/login_render/')
def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None



#####################ROLE Management###########################

@login_required(login_url='/login_render/')
def role_display(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "GET":
        role = roles.objects.all()
        q = request.GET.get('searchrole')
        if q != None:
            role = roles.objects.filter(role_name__icontains=q)        
        context = {
            'role': role,
            'permission':permission
        }
        return render(request, 'tool/roles.html', context)


@login_required(login_url='/login_render/')
def role_add(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        role_name = request.POST.get('role_name')

        ch_m_a = request.POST.get('ch_m_a') 
        ch_m_e = request.POST.get('ch_m_e')
        ch_m_d = request.POST.get('ch_m_d')
        ch_m_v = request.POST.get('ch_m_v')
        ch_m_approve = request.POST.get('ch_m_approve')
        ch_m_assign = request.POST.get('ch_m_assign')

        inci_m_a = request.POST.get('inci_m_a') 
        inci_m_e = request.POST.get('inci_m_e')
        inci_m_d = request.POST.get('inci_m_d')
        inci_m_v = request.POST.get('inci_m_v')
        inci_m_approve = request.POST.get('inci_m_approve')
        inci_m_assign = request.POST.get('inci_m_assign')

        confi_m_a = request.POST.get('confi_m_a') 
        confi_m_e = request.POST.get('confi_m_e')
        confi_m_d = request.POST.get('confi_m_d')
        confi_m_v = request.POST.get('confi_m_v')

        serv_m_a = request.POST.get('serv_m_a') 
        serv_m_e = request.POST.get('serv_m_e')
        serv_m_d = request.POST.get('serv_m_d')
        serv_m_v = request.POST.get('serv_m_v')

        user_m_a = request.POST.get('user_m_a') 
        user_m_e = request.POST.get('user_m_e')
        user_m_d = request.POST.get('user_m_d')
        user_m_v = request.POST.get('user_m_v')

        setting_a = request.POST.get('setting_a') 
        setting_e = request.POST.get('setting_e')
        setting_d = request.POST.get('setting_d')
        setting_v = request.POST.get('setting_v')

        history_a = request.POST.get('history_a') 
        history_e = request.POST.get('history_e')
        history_d = request.POST.get('history_d')
        history_v = request.POST.get('history_v')

        role = roles (
        role_name = role_name,

        ch_m_a = ch_m_a, 
        ch_m_e = ch_m_e,
        ch_m_d = ch_m_d,
        ch_m_v = ch_m_v,
        ch_m_approve = ch_m_approve,
        ch_m_assign = ch_m_assign,

        inci_m_a = inci_m_a, 
        inci_m_e = inci_m_e,
        inci_m_d = inci_m_d,
        inci_m_v = inci_m_v,
        inci_m_approve = inci_m_approve,
        inci_m_assign = inci_m_assign,

        confi_m_a = confi_m_a, 
        confi_m_e = confi_m_e,
        confi_m_d = confi_m_d,
        confi_m_v = confi_m_v,

        serv_m_a = serv_m_a, 
        serv_m_e = serv_m_e,
        serv_m_d = serv_m_d,
        serv_m_v = serv_m_v,

        user_m_a = user_m_a, 
        user_m_e = user_m_e,
        user_m_d = user_m_d,
        user_m_v = user_m_v,

        setting_a = setting_a, 
        setting_e = setting_e,
        setting_d = setting_d,
        setting_v = setting_v,

        history_a = history_a, 
        history_e = history_e,
        history_d = history_d,
        history_v = history_v,
        )
        role.save()
        return redirect('role_display')
    return render(request, 'tool/roles.html',{'permission':permission})

@login_required(login_url='/login_render/')
def role_edit(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        role_name = request.POST.get('role_name')

        ch_m_a = request.POST.get('ch_m_a') 
        ch_m_e = request.POST.get('ch_m_e')
        ch_m_d = request.POST.get('ch_m_d')
        ch_m_v = request.POST.get('ch_m_v')
        ch_m_approve = request.POST.get('ch_m_approve')
        ch_m_assign = request.POST.get('ch_m_assign')

        inci_m_a = request.POST.get('inci_m_a') 
        inci_m_e = request.POST.get('inci_m_e')
        inci_m_d = request.POST.get('inci_m_d')
        inci_m_v = request.POST.get('inci_m_v')
        inci_m_approve = request.POST.get('inci_m_approve')
        inci_m_assign = request.POST.get('inci_m_assign')

        confi_m_a = request.POST.get('confi_m_a') 
        confi_m_e = request.POST.get('confi_m_e')
        confi_m_d = request.POST.get('confi_m_d')
        confi_m_v = request.POST.get('confi_m_v')

        serv_m_a = request.POST.get('serv_m_a') 
        serv_m_e = request.POST.get('serv_m_e')
        serv_m_d = request.POST.get('serv_m_d')
        serv_m_v = request.POST.get('serv_m_v')

        user_m_a = request.POST.get('user_m_a') 
        user_m_e = request.POST.get('user_m_e')
        user_m_d = request.POST.get('user_m_d')
        user_m_v = request.POST.get('user_m_v')

        setting_a = request.POST.get('setting_a') 
        setting_e = request.POST.get('setting_e')
        setting_d = request.POST.get('setting_d')
        setting_v = request.POST.get('setting_v')

        history_a = request.POST.get('history_a') 
        history_e = request.POST.get('history_e')
        history_d = request.POST.get('history_d')
        history_v = request.POST.get('history_v')

        role = roles (
        id = id,
        role_name = role_name,

        ch_m_a = ch_m_a, 
        ch_m_e = ch_m_e,
        ch_m_d = ch_m_d,
        ch_m_v = ch_m_v,
        ch_m_approve = ch_m_approve,
        ch_m_assign = ch_m_assign,

        inci_m_a = inci_m_a, 
        inci_m_e = inci_m_e,
        inci_m_d = inci_m_d,
        inci_m_v = inci_m_v,
        inci_m_approve = inci_m_approve,
        inci_m_assign = inci_m_assign,

        confi_m_a = confi_m_a, 
        confi_m_e = confi_m_e,
        confi_m_d = confi_m_d,
        confi_m_v = confi_m_v,

        serv_m_a = serv_m_a, 
        serv_m_e = serv_m_e,
        serv_m_d = serv_m_d,
        serv_m_v = serv_m_v,

        user_m_a = user_m_a, 
        user_m_e = user_m_e,
        user_m_d = user_m_d,
        user_m_v = user_m_v,

        setting_a = setting_a, 
        setting_e = setting_e,
        setting_d = setting_d,
        setting_v = setting_v,

        history_a = history_a, 
        history_e = history_e,
        history_d = history_d,
        history_v = history_v,
        )
        role.save()
        return redirect('role_display')
    return render(request, 'tool/roles.html',{'permission':permission})


#############################################

@login_required(login_url='/login_render/')
def user_display(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "GET":
        user = adminuser.objects.exclude(ch_user_role_id=None)
        # user = adminuser.objects.all()
        org = cl_New_organization.objects.all()
        role = roles.objects.all()
        q = request.GET.get('searchrole')
        if q != None:
            user = adminuser.objects.filter(ch_user_firstname__icontains=q)        
        context = {
            'user': user,
            'role': role,
            'org': org,
            'permission':permission
        }
        return render(request, 'tool/user.html', context)


def get_Existing_user(request):
    ch_user_emailID = request.GET.get('user_emailID')
    print(ch_user_emailID)
    user = adminuser.objects.filter(email=ch_user_emailID).first()
    usercount = None
    if user != None:
        usercount = 1
    else:
        usercount = 0
    json_data = json.dumps(usercount)
    return HttpResponse(json_data, content_type='application/json')



@login_required(login_url='/login_render/')
def add_new_user(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_user_firstname = request.POST.get('ch_user_firstname')
        ch_user_lastname = request.POST.get('ch_user_lastname')
        ch_user_email = request.POST.get('ch_user_email')
        ch_user_password = request.POST.get('ch_user_password')
        ch_user_role = roles.objects.get(role_name=request.POST.get('role_name'))
        ch_user_mobilenumber = request.POST.get('ch_user_mobilenumber')
        org_id = request.POST.get('ch_organization')
        if org_id == '':
            ch_organization = None
        else:
            ch_organization = cl_New_organization.objects.filter(id = request.POST.get('ch_organization')).first()
            print("Organization",ch_organization)
        user = adminuser(
            first_name=ch_user_firstname,
            last_name=ch_user_lastname,
            email=ch_user_email,
            ch_user_role=ch_user_role,
            ch_user_mobilenumber = ch_user_mobilenumber,
            ch_organization = ch_organization
        )
        user.set_password(ch_user_password)
        user.save()
        return redirect('user_display')
    return render(request, 'tool/user.html',{'permission':permission})


@login_required(login_url='/login_render/')
def user_edit(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    user = adminuser.objects.filter(id=id).first()
    if request.method == "POST":
        print(request.POST.get('ch_organization_e'))
        ch_organization = cl_New_organization.objects.filter(id = request.POST.get('ch_organization_e')).first()
        ch_user_updated_role = roles.objects.get(role_name=request.POST.get('role_name_e'))
        user.ch_user_role = ch_user_updated_role
        user.ch_organization = ch_organization
        user.save()
        return redirect('user_display')
    return render(request, 'tool/user.html',{'permission':permission})


###################### Notification Menu ###############################

@login_required(login_url='/login_render/')
def email_display(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "GET":
        emails = email_notifier.objects.all()
        q = request.GET.get('searchname')
        if q != None:
            emails = email_notifier.objects.filter(name_icontains=q)        
    context = {
            'emails': emails,
            'permission':permission
        }
    return render(request, 'tool/email_notifier.html', context)

@login_required(login_url='/login_render/')
def add_new_email(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # name = request.POST.get('name')
        # host = request.POST.get('SMTP_server')
        # port = request.POST.get('SMTP_port')
        # use_SSL = True
        # host_user = request.POST.get('sender_email')
        # host_password = request.POST.get('sender_email_password')
        # message = request.POST.get('message')

        email = email_notifier(
            name = request.POST.get('name'),
            host = request.POST.get('SMTP_server'),
            port = request.POST.get('SMTP_port'),
            use_SSL = "True",
            host_user = request.POST.get('sender_email'),
            host_password = request.POST.get('sender_email_password'),
            message = request.POST.get('message')
        )
        email.save()
        return redirect('email_display')
    return render(request, 'tool/email_notifier.html',{'permission':permission})

# @login_required(login_url='/login_render/')
# def add_new_email(request):
#     permission = roles.objects.filter(id=request.session['user_role']).first()
#     if request.method == "POST":
#         name = request.POST.get('name')
#         SMTP_server = request.POST.get('SMTP_server')
#         SMTP_port = request.POST.get('SMTP_port')
#         sender_email = request.POST.get('sender_email')
#         sender_email_password = request.POST.get('sender_email_password')
#         message = request.POST.get('message')

#         email = email_notifier(
#             name=name,
#             SMTP_server=SMTP_server,
#             SMTP_port=SMTP_port,
#             sender_email=sender_email,
#             sender_email_password=sender_email_password,
#             message = message
#         )
#         email.save()
#         return redirect('email_display')
#     return render(request, 'tool/email_notifier.html',{'permission':permission})


############# Boat Id ################
@login_required(login_url='/login_render/')
def boat_display(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    boat = boat_notifier.objects.all()

    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            boat = boat_notifier.objects.filter(name_icontains=q)      

    
    page = request.GET.get('page', 1)

    paginator = Paginator(boat, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {
            'boat': boat,
            'permission':permission,
            'users':users

        }
    return render(request, 'tool/boat_notifier.html', context)

@login_required(login_url='/login_render/')
def add_new_boatid(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST": 
        boat_tokan = request.POST.get('boat_tokan')
        name = request.POST.get('name') 

        boat = boat_notifier(
            boat_tokan =boat_tokan,
            name = name
        
        )
        boat.save()
        return redirect('boat_display')
    return render(request, 'tool/boat_notifier.html',{'permission':permission})


@login_required(login_url='/login_render/')
def boatid_edit(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        boat_tokan = request.POST.get('boat_tokan')
        name = request.POST.get('name')  
        boat = boat_notifier(
            id = id,
            boat_tokan =boat_tokan,
            name = name
        )
       
        boat.save()
        return redirect('boat_display')
    return render(request, 'tool/boat_notifier.html',{'permission':permission})


@login_required(login_url='/login_render/')
def boatdelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            boat = boat_notifier.objects.filter(id=i).first()
            boat.delete()
    return redirect('boat_display')


# @login_required(login_url='/login_render/')
# def add_new_email(request):
#     permission = roles.objects.filter(id=request.session['user_role']).first()
#     if request.method == "POST":
#         name = request.POST.get('name')
#         SMTP_server = request.POST.get('SMTP_server')
#         SMTP_port = request.POST.get('SMTP_port')
#         sender_email = request.POST.get('sender_email')
#         sender_email_password = request.POST.get('sender_email_password')
#         message = request.POST.get('message')

#         email = email_notifier(
#             name=name,
#             SMTP_server=SMTP_server,
#             SMTP_port=SMTP_port,
#             sender_email=sender_email,
#             sender_email_password=sender_email_password,
#             message = message
#         )
#         email.save()
#         return redirect('email_display')
#     return render(request, 'tool/email_notifier.html',{'permission':permission})






@login_required(login_url='/login_render/')
def email_edit(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        email = email_notifier.objects.filter(id=id).first()
        # name = request.POST.get('name')
        # SMTP_server = request.POST.get('SMTP_server')
        # SMTP_port = request.POST.get('SMTP_port')
        # sender_email = request.POST.get('sender_email')
        # sender_email_password = request.POST.get('sender_email_password')
        # message = request.POST.get('message')

        email = email_notifier(
            id=id,
            name = request.POST.get('name'),
            host = request.POST.get('SMTP_server'),
            port = request.POST.get('SMTP_port'),
            use_SSL = "True",
            host_user = request.POST.get('sender_email'),
            host_password = request.POST.get('sender_email_password'),
            message = request.POST.get('message')
        )
        email.save()
        return redirect('email_display')
    return render(request, 'tool/email_notifier.html',{'permission':permission})

####################################################################


@login_required(login_url='/login_render/')
def sms_display(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "GET":
        sms = sms_notifier.objects.all()
        q = request.GET.get('searchname')
        if q != None:
            sms = sms_notifier.objects.filter(name_icontains=q)        
    context = {
            'sms': sms,
            'permission':permission
        }
    return render(request, 'tool/sms_notifier.html', context)


@login_required(login_url='/login_render/')
def add_new_sms(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        name = request.POST.get('name')
        url = request.POST.get('url')
        sender_sms_password = request.POST.get('sender_sms_password')
        description = request.POST.get('description')
        username = request.POST.get('username')
        sender = request.POST.get('sender')

        sms = sms_notifier(
            name=name,
            url=url,
            sender_sms_password=sender_sms_password,
            description=description,
            username=username,
            sender = sender
        )
        sms.save()
        return redirect('sms_display')
    return render(request, 'tool/sms_notifier.html',{'permission':permission})



@login_required(login_url='/login_render/')
def sms_edit(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        name = request.POST.get('name')
        url = request.POST.get('url')
        sender_sms_password = request.POST.get('sender_sms_password')
        description = request.POST.get('description')
        username = request.POST.get('username')
        sender = request.POST.get('sender')

        sms = sms_notifier(
            id=id,
            name=name,
            url=url,
            sender_sms_password=sender_sms_password,
            description=description,
            username=username,
            sender = sender
        )
        sms.save()
        return redirect('sms_display')
    return render(request, 'tool/sms_notifier.html',{'permission':permission})


@login_required(login_url='/login_render/')
def smsdelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            sms = sms_notifier.objects.filter(id=i).first()
            sms.delete()
    return redirect('sms_display')


# =============================================================================

@login_required(login_url='/login_render/')
def servicenav(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    return render(request, 'tool/servicenav.html',{'permission':permission})


@login_required(login_url='/login_render/')
def systemnav(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    return render(request, 'tool/systemnav.html',{'permission':permission})


@login_required(login_url='/login_render/')
def sysconfienav(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    return render(request, 'tool/sysconfinav.html',{'permission':permission})


@login_required(login_url='/login_render/')
def sysconfiauth(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    return render(request, 'tool/sysconfiauth.html',{'permission':permission})


@login_required(login_url='/login_render/')
def admuser(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    return render(request, 'tool/admuser.html',{'permission':permission})


@login_required(login_url='/login_render/')
def integrationav(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    return render(request, 'tool/integrationav.html',{'permission':permission})



################### Synchronization Data Source   #############################
@login_required(login_url='/login_render/')
def systemsynchro(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    syn = cl_Synchro_data_source.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchstatus')
        if q != None:
            syn = cl_Synchro_data_source.objects.filter(ch_status__icontains=q)
    page = request.GET.get('page', 1)
    paginator = Paginator(syn, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'tool/sysconfisynchro.html', {'syn': syn,'users':users, 'permission':permission})


@login_required(login_url='/login_render/')
def synadd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_name = request.POST.get('ch_name')
        ch_status = request.POST.get('ch_status')
        txt_description = request.POST.get('txt_description')
        ch_target_class = request.POST.get('ch_target_class')
        ch_user = request.POST.get('ch_user')
        ch_contact_notify = request.POST.get('ch_contact_notify')
        url_icon_hyperlink = request.POST.get('url_icon_hyperlink')
        url_Application_hyperlink = request.POST.get('url_Application_hyperlink')
        ch_data_table = request.POST.get('ch_data_table')
        ch_reconciliation_policy = request.POST.get('ch_reconciliation_policy')
        ch_action_on_zero = request.POST.get('ch_action_on_zero')
        ch_action_on_one = request.POST.get('ch_action_on_one')
        ch_action_on_many = request.POST.get('ch_action_on_many')
        ch_users_allowed = request.POST.get('ch_users_allowed')
        ch_update_rules = request.POST.get('ch_update_rules')
        ch_delete_policy = request.POST.get('ch_delete_policy')
        dt_full_load_interval = request.POST.get('dt_full_load_interval')
        dt_retention_duration = request.POST.get('dt_retention_duration')
        syn = cl_Synchro_data_source(
            ch_name=ch_name,
            ch_status=ch_status,
            txt_description=txt_description,
            ch_target_class=ch_target_class,
            ch_user=ch_user,
            ch_contact_notify=ch_contact_notify,
            url_icon_hyperlink=url_icon_hyperlink,
            url_Application_hyperlink=url_Application_hyperlink,
            ch_data_table = ch_data_table,
            ch_reconciliation_policy=ch_reconciliation_policy,
            ch_action_on_zero=ch_action_on_zero,
            ch_action_on_one=ch_action_on_one,
            ch_action_on_many=ch_action_on_many,
            ch_users_allowed=ch_users_allowed,
            ch_update_rules=ch_update_rules,
            ch_delete_policy=ch_delete_policy,
            dt_full_load_interval=dt_full_load_interval,
            dt_retention_duration = dt_retention_duration,
        )
        syn.save()
        admin_name = request.session["username"]
        adminaction = "addition of new changes"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('systemsynchro')
    return render(request, 'tool/sysconfisynchro.html',{'permission':permission})


@login_required(login_url='/login_render/')
def synedit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    syn = cl_Synchro_data_source.objects.all()
    context = {
        'syn': syn,
        'permission':permission
    }
    return render(request, 'tool/sysconfisynchro.html', context)


@login_required(login_url='/login_render/')
def synupdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    """
    Function for update change_information
    """
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_status = request.POST.get('ch_status')
        txt_description = request.POST.get('txt_description')
        ch_target_class = request.POST.get('ch_target_class')
        ch_user = request.POST.get('ch_user')
        ch_contact_notify = request.POST.get('ch_contact_notify')
        url_icon_hyperlink = request.POST.get('url_icon_hyperlink')
        url_Application_hyperlink = request.POST.get('url_Application_hyperlink')
        ch_data_table = request.POST.get('ch_data_table')
        ch_reconciliation_policy = request.POST.get('ch_reconciliation_policy')
        ch_action_on_zero = request.POST.get('ch_action_on_zero')
        ch_action_on_one = request.POST.get('ch_action_on_one')
        ch_action_on_many = request.POST.get('ch_action_on_many')
        ch_users_allowed = request.POST.get('ch_users_allowed')
        ch_update_rules = request.POST.get('ch_update_rules')
        ch_delete_policy = request.POST.get('ch_delete_policy')
        dt_full_load_interval = request.POST.get('dt_full_load_interval')
        dt_retention_duration = request.POST.get('dt_retention_duration')
        syn = cl_Synchro_data_source(
            id = id,
            ch_name=ch_name,
            ch_status=ch_status,
            txt_description=txt_description,
            ch_target_class=ch_target_class,
            ch_user=ch_user,
            ch_contact_notify=ch_contact_notify,
            url_icon_hyperlink=url_icon_hyperlink,
            url_Application_hyperlink=url_Application_hyperlink,
            ch_data_table = ch_data_table,
            ch_reconciliation_policy=ch_reconciliation_policy,
            ch_action_on_zero=ch_action_on_zero,
            ch_action_on_one=ch_action_on_one,
            ch_action_on_many=ch_action_on_many,
            ch_users_allowed=ch_users_allowed,
            ch_update_rules=ch_update_rules,
            ch_delete_policy=ch_delete_policy,
            dt_full_load_interval=dt_full_load_interval,
            dt_retention_duration = dt_retention_duration,
        )
        syn.save()
        admin_name = request.session["username"]
        adminaction = "addition of new changes"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('systemsynchro')
    return render(request, 'tool/sysconfisynchro.html',{'permission':permission})


@login_required(login_url='/login_render/')
def syndelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            syn = cl_Synchro_data_source.objects.filter(id=i).first()
            syn.delete()
        admin_name = request.session["username"]
        adminaction = "Delete the changes"
        event ="event"
        resultcode = "200"
        user_activity(admin_name, adminaction, event, resultcode)
        return redirect('systemsynchro')




######Delivery Model Views##############

@login_required(login_url='/login_render/')
def authgoogle(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    oauthg =  cl_Oauth_google.objects.all()
    if request.method == "GET":
        oauthg = cl_Oauth_google.objects.all()
        q = request.GET.get('searchstatus')
        if q != None:
            oauthg = cl_Oauth_google.objects.filter(ch_status__icontains=q)
    page = request.GET.get('page', 1)
    paginator = Paginator(oauthg, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'tool/authgoogle.html', {'oauthg': oauthg, 'permission':permission,'users':users})

@login_required(login_url='/login_render/')
def oauthadd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        e_login = request.POST.get('e_login')
        ch_status = request.POST.get('ch_status')
        ch_provider = request.POST.get('ch_provider')
        txt_description = request.POST.get('txt_description')
        ch_client_id = request.POST.get('ch_client_id')
        ch_client_secret = request.POST.get('ch_client_secret')
        ch_scope = request.POST.get('ch_scope')
        ch_advanced_scope = request.POST.get('ch_advanced_scope')
        ch_used_smtp = request.POST.get('ch_used_smtp')
        oauthg = cl_Oauth_google(
            e_login=e_login,
            ch_status=ch_status,
            ch_provider=ch_provider,
            txt_description=txt_description,
            ch_client_id = ch_client_id,
            ch_client_secret=ch_client_secret,
            ch_scope=ch_scope,
            ch_advanced_scope = ch_advanced_scope,
            ch_used_smtp = ch_used_smtp,
        )
        oauthg.save()
        return redirect('authgoogle')
    return render(request, 'tool/authgoogle.html',{'permission':permission})

@login_required(login_url='/login_render/')
def oauthedit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    oauthg =  cl_Oauth_google.objects.all()
    context = {
        'oauthg': oauthg,
        'permission':permission
    }
    return render(request, 'tool/authgoogle.html', context)

@login_required(login_url='/login_render/')
def oauthupdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    """
    Function for update change_information
    """
    if request.method == "POST":
        # id = request.POST.get('id')
        e_login = request.POST.get('e_login')
        ch_status = request.POST.get('ch_status')
        ch_provider = request.POST.get('ch_provider')
        txt_description = request.POST.get('txt_description')
        ch_client_id = request.POST.get('ch_client_id')
        ch_client_secret = request.POST.get('ch_client_secret')
        ch_scope = request.POST.get('ch_scope')
        ch_advanced_scope = request.POST.get('ch_advanced_scope')
        ch_used_smtp = request.POST.get('ch_used_smtp')
        oauthg = cl_Oauth_google(
            id = id,
            e_login=e_login,
            ch_status=ch_status,
            ch_provider=ch_provider,
            txt_description=txt_description,
            ch_client_id = ch_client_id,
            ch_client_secret=ch_client_secret,
            ch_scope=ch_scope,
            ch_advanced_scope = ch_advanced_scope,
            ch_used_smtp = ch_used_smtp,
        )
        oauthg.save()
        return redirect('authgoogle')
    return render(request, 'tool/authgoogle.html',{'permission':permission})

@login_required(login_url='/login_render/')
def oauthdelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            oauthg = cl_Oauth_google.objects.filter(id=i).first()
            oauthg.delete()
    return redirect('authgoogle')

def vreopen(request):
    # permission = roles.objects.filter(id=request.session['user_role']).first()
    ropen = cl_Reopen.objects.all()
    context = {
        'ropen': ropen,
        # 'permission':permission
    }
    return render(request, 'tool/userrequest.html', context)

# def addreopen(request):
#     if request.method == "POST":
#         txt_reopen = request.POST.get('txt_reopen')
#         ropen = cl_Reopen(
#             txt_reopen=txt_reopen,

#         )
#     return render(request, 'tool/userrequest.html', {'ropen':ropen})



def reopen(request):
    if request.method == "POST":
        reason = request.POST.get('reason')
        ur_id = request.POST.getlist('ur_id[]')
        # ur = cl_User_request.objects.get(id=ur_id)
        # create a new instance of cl_Reopen model
        cl_Reopen.objects.create(txt_reopen=reason,ureq_id=ur_id)

        # txt_reopen = cl_Reopen.objects.create(txt_reopen=reason)
        # update the user request instance with the new cl_Reopen instance
        # ur.ch_status = "Reopen"
        for i in ur_id:
            ur = cl_User_request.objects.filter(id=i).first()
            ur.ch_status = "Reopen"
            ur.save()
        
        return redirect('userrequest')
    
    return render(request, 'reopen.html')


  

# @login_required(login_url='/login_render/')
# def reopen(request):
#     # permission = roles.objects.filter(id=request.session['user_role']).first()
#     if request.method == "POST":
#         list_id = request.POST.getlist('id[]')  
#         reason = request.POST.get('txt_reopen')
#         ur_id = request.POST.get('ur_id')
#         ur = cl_User_request.objects.get(id=ur_id)
#         up = cl_Reopen.objects.get(id=i)
#         up.txt_reopen = reason
#         up.save()
#         print(up)
#         # ur.reopen_reason = reason
#         ur.save()
              
#         for i in list_id:
#             ur = cl_User_request.objects.filter(id=i).first()
#             ur.ch_status = "Reopen"
#             ur.save()
        
#     return redirect('userrequest')

# def store_reopen_reason(request):
#     if request.method == 'POST':
#         reason = request.POST.get('txt_reopen')
#         ur_id = request.POST.get('ur_id')
#         ur = cl_User_request.objects.get(id=ur_id)
#         ur.reopen_reason = reason
#         ur.save()
#         return HttpResponse('Reason stored successfully!')
#     else:
#         return HttpResponse('Invalid request method!')




        






