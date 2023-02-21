import random
import time
import datetime
from datetime import *
from .forms import *
from io import BytesIO
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from tool.models import cl_Location, cl_Service, cl_Software,cl_New_organization
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

# from settings import ready


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
    permission = roles.objects.filter(id=request.session['user_role']).first()
    User = cl_User_request.objects.all().count()
    org = cl_New_organization.objects.all().count()
    service = cl_Service.objects.all().count()
    change = cl_New_change.objects.all().count()
    Assign = cl_User_request.objects.exclude(ch_assign_agent = 'Deallocate').count()
    newopen= cl_User_request.objects.filter(Q(ch_assign_agent = 'Deallocate') | Q(ch_status = 'Active')).count()
    Assign1 = cl_New_change.objects.filter(ch_status = 'Assigned').count()
    newopen1= cl_New_change.objects.exclude(Q(ch_assign_agent = 'request.session(username)') & Q(ch_status = 'Assigned')).count()
 

    context = {
        'User': User,
        'permission':permission,
        'org':org,
        'service':service,
        'change':change,
        'newopen':newopen,
        'Assign':Assign,
        'Assign1':Assign1,
        'newopen1':newopen1

     
        

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
    context = {
        "log" : log,
        'permission':permission
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
def Location(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    loc = cl_Location.objects.all()
    
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            loc = cl_Location.objects.filter(ch_location_name__icontains=q)
    page = request.GET.get('page', 1)
    org = cl_New_organization.objects.all()


    paginator = Paginator(loc, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)


    context = {
        'loc': loc,
        'users':users,
        'permission':permission,
        'org':org,
    }
    return render(request, 'tool/location.html', context)



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
        print(list_id)
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

    team1 =cl_Team.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(per, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'tool/client.html', {'per': per, 'org':org,'users':users,'permission':permission,'team1':team1})


@login_required(login_url='/login_render/')
def ADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_person_firstname = str.capitalize(
            request.POST.get('ch_person_firstname'))
        ch_person_lastname = str.capitalize(
            request.POST.get('ch_person_lastname'))
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        ch_team = cl_Team.objects.filter(ch_teamname=request.POST.get('ch_team_name')).first()
        ch_person_status = str.capitalize(request.POST.get('ch_person_status'))
        ch_person_location = str.capitalize(
            request.POST.get('ch_person_location')) 
        ch_person_function = str.capitalize(
            request.POST.get('ch_person_function'))
        ch_manager = cl_Person.objects.filter(ch_person_firstname=request.POST.get('ch_manager')).first()
        # ch_manager = request.POST.get('ch_manager')
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
        id = request.POST.get('id')
        ch_person_firstname = request.POST.get('ch_person_firstname')
        ch_person_lastname = request.POST.get('ch_person_lastname')
        ch_organization = cl_New_organization.objects.get(ch_name = request.POST.get('ch_organization'))    
        ch_team = cl_Team.objects.filter(ch_teamname=request.POST.get('ch_team_name')).first()
        ch_person_status = request.POST.get('ch_person_status')
        ch_person_location = request.POST.get('ch_person_location')
        ch_person_function = request.POST.get('ch_person_function')
        ch_manager = cl_Person.objects.filter(ch_person_firstname=request.POST.get('ch_manager')).first()
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
    return render(request, 'tool/service.html', {'tem': tem, 'org':org,'users':users,'permission':permission})


@login_required(login_url='/login_render/')
def TADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_teamname = request.POST.get('ch_teamname')
        ch_teamstatus = request.POST.get('ch_teamstatus')
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        e_team_emailfield = str.lower(request.POST.get('e_team_emailfield'))
        i_team_phonenumber = request.POST.get('i_team_phonenumber')
        b_team_notification = request.POST.get('b_team_notification')
        ch_team_function = request.POST.get('ch_team_function')
        tem = cl_Team(
            ch_teamname=ch_teamname,
            ch_teamstatus=ch_teamstatus,
            ch_organization=ch_organization,
            e_team_emailfield=e_team_emailfield,
            i_team_phonenumber=i_team_phonenumber,
            b_team_notification=b_team_notification,
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
        # id = request.POST.get('id')
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
    nchange = cl_New_change.objects.all()
    if request.method == "GET":
        allteam = cl_Team.objects.all()
        team_person = cl_Person.objects.all()
        q = request.GET.get('searchstatus')
        if q != None:
            nchange = cl_New_change.objects.filter(ch_status__icontains=q)

    page = request.GET.get('page', 1)
    org = cl_New_organization.objects.all()
    call = cl_Person.objects.all()


    paginator = Paginator(nchange, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.method == "GET":
        allteam = cl_Team.objects.all()
        # team_person = cl_Person.objects.all()
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
    print(service_id)
    subcategory = cl_Service_subcategory.objects.filter(ch_sservice_id=service_id)
    print(subcategory)
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
        s= "Assigned"
        for i in list_id:
            nchange = cl_New_change.objects.filter(id=i).first()
            nchange.ch_assign_agent = per.ch_person_firstname
            nchange.ch_status = s
            nchange.save()
        try:
            mail_sender()
            subject = 'Welcome to Olatech Solutions'
            message = 'Hope you are enjoying your Olatech Services'
            sender = settings.EMAIL_HOST_USER
            recepient = ['ankush.n@olatechs.com', 'mangesh.b@olatechs.com']
            send_mail(subject, message, sender, recepient, fail_silently=False)
            # return JsonResponse({'result': 'success'})
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
            'permission':permission
        }
    return render(request, 'tool/tassign.html', context)


def mail_sender():
    mail_host = email_notifier.objects.filter(id=1).first()
    print(mail_host)
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
        print(list_id)
        recepient = []

        for i in list_id:
            nchange = cl_New_change.objects.filter(id=i).first()
            nchange.ch_status = "Watting for Approval"
            nchange.save()
            c_mail = cl_Person.objects.filter(id=nchange.ch_caller_id).first()
            # print(c_mail.e_person_email)
            recepient.append(c_mail.e_person_email)

        # for i in recepient:
        #     print(i)
        print("hi")
        try:
            mail_sender()
            list_id = request.POST.getlist('id[]')
            change_approve = cl_New_change.objects.filter(id=list_id[0]).first()
            subject = 'Welcome to Olatech Solutions'
            message = f'Please approve Following Change for further process. Change ID : "{list_id[0]}" Change Description : "{change_approve.txt_description}" '
            sender = settings.EMAIL_HOST_USER
            # # recepient = ['ankush.n@olatechs.com', 'mangesh.b@olatechs.com']
            send_mail(subject, message, sender, recepient, fail_silently=False)
        except:
            raise Exception('Please Configure Email Sender Details')
    # return render(request, 'tool/approve_change.html',{'permission':permission})

######################### Incident Mangement ####################################

@login_required(login_url='/login_render/')
def user_request(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    ur = cl_User_request.objects.all()    
    ser = cl_Service.objects.all()
    allservice = cl_Service.objects.all()
    ser_sub = cl_Service_subcategory.objects.all()
    nchange = cl_New_change.objects.all()

    escalated_ur = escalation(ur)
    if request.method == "GET":
        q = request.GET.get('searchservice')
        if q != None:
            ur = cl_User_request.objects.filter(ch_service__icontains=q)
        # escalated_ur = escalation(ur)
    org = cl_New_organization.objects.all()
    allteam = cl_Team.objects.all()
    team_person = cl_Person.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(ur, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
   
    context = {
            'ur': ur,
            'escalated_ur': escalated_ur,
            'users':users,
            'permission':permission,
            'org':org,
            'allteam':allteam,
            'team_person':team_person,
            'ser':ser,
            'allservice':allservice,
            'ser_sub':ser_sub,
            'nchange':nchange
            }
    return render(request, 'tool/userrequest.html', context)


def escalation(ur):
    escalated_ur = []
    for req in ur:
        if datetime.date(req.dt_escalation_date) < datetime.date(datetime.now()) and req.ch_assign_agent == 'Deallocate':
            escalated_ur.append(req)
        elif datetime.date(req.dt_escalation_date) == datetime.date(datetime.now()) and datetime.time(req.dt_escalation_date) < datetime.time(datetime.now()):
            escalated_ur.append(req)
    return escalated_ur


@login_required(login_url='/login_render/')
def UADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        fk_organization = cl_New_organization.objects.filter(
            ch_name=request.POST.get('ch_organization')).first()
        fk_caller = cl_Person.objects.filter(ch_person_firstname=request.POST.get('ch_caller')).first()
        ch_status = request.POST.get('ch_status')
        ch_origin = request.POST.get('ch_origin')
        ch_title = request.POST.get('ch_title')
        ch_request_type = request.POST.get('ch_request_type')
        ch_impact = request.POST.get('ch_impact')
        ch_urgency = request.POST.get('ch_urgency')
        ch_priority = request.POST.get('ch_priority')   
        dt_start_date = request.POST.get('dt_start_date')
        dt_updated_date = request.POST.get('dt_Updated_date')
        dt_escalation_date = request.POST.get('dt_escalation_date')     
        ch_service =cl_Service.objects.filter(id=request.POST.get('ch_sername')).first()
        # print(request.POST.get(ch_service))
        ch_service_subcategory = cl_Service_subcategory.objects.filter(id=request.POST.get('ch_service_subcategory')).first()
        ch_parent_request = cl_User_request.objects.filter(id=request.POST.get('ch_parent_request_id')).first()
        # ch_parent_request = request.POST.get('id')
        ch_parent_change = cl_New_change.objects.filter(id=request.POST.get('ch_parent_change_id')).first()
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
            dt_Updated_date =dt_updated_date,
            dt_escalation_date = dt_escalation_date,
            ch_service =ch_service,
            ch_service_subcategory =ch_service_subcategory,
            ch_parent_request=ch_parent_request,
            ch_parent_change =ch_parent_change,
            txt_description =txt_description,
        )
        ur.save()
        # print(ur)
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
        # id = request.POST.get('id')
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
        dt_updated_date = request.POST.get('dt_Updated_date')
        ch_service =cl_Service.objects.filter(id=request.POST.get('ch_sername')).first()
        ch_service_subcategory = cl_Service_subcategory.objects.filter(id=request.POST.get('ch_service_subcategory')).first()
        ch_parent_request = cl_User_request.objects.filter(id=request.POST.get('ch_parent_request_id')).first()
        # ch_parent_request = request.POST.get('ch_parent_request_id')
        ch_parent_change = cl_New_change.objects.filter(id=request.POST.get('ch_parent_change_id')).first()

        # ch_parent_change = request.POST.get('ch_parent_change_id')
        txt_description = request.POST.get('txt_description')
        ch_assign_agent =  request.POST.get('ch_assign_agent')

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
            dt_Updated_date=dt_updated_date,
            ch_service=ch_service,
            ch_service_subcategory=ch_service_subcategory,
            ch_parent_request=ch_parent_request,
            ch_parent_change =ch_parent_change,
            txt_description =txt_description,
            ch_assign_agent=ch_assign_agent

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

########## Assign Change For User Request############


@login_required(login_url='/login_render/')
def assign_URModal(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        p_Emp_id = request.POST.get('p')
        per = cl_Person.objects.filter(id=p_Emp_id).first()
              
        for i in list_id:
            ur = cl_User_request.objects.filter(id=i).first()
            ur.ch_assign_agent = per.ch_person_firstname
            ur.ch_status = "Assigned"
            
            ur.save()
        try:
            mail_sender()
            subject = 'Welcome to Olatech Solutions'
            message = 'Hope you are enjoying your Olatech Services IN UR'
            sender = settings.EMAIL_HOST_USER
            recepient = ['ankush.n@olatechs.com', 'mangesh.b@olatechs.com']
            send_mail(subject, message, sender, recepient, fail_silently=False)
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

########## Approve Change For Incident Management############

@login_required(login_url='/login_render/')
def send_approval_Mail_UR(request):
    # permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        for i in list_id:
            ur = cl_User_request.objects.filter(id=i).first()
            ur.ch_status = "Waiting for Approval"
            ur.save()
        try:
            mail_sender()
            list_id = request.POST.getlist('id[]')
            ur_approve = cl_User_request.objects.filter(id=list_id[0]).first()
            subject = 'Welcome to Olatech Solutions'
            message = f'Please approve Following Change for further process. UR ID : "{list_id[0]}" UR Description : "{ur_approve.txt_description}" '
            sender = settings.EMAIL_HOST_USER
            recepient = ['ankush.n@olatechs.com', 'mangesh.b@olatechs.com','vidya.r@olatechs.com']
            send_mail(subject, message, sender, recepient, fail_silently=False)
        except:
            raise Exception('Please Configure Email Sender Details')
        
        # return redirect('user_request')

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

        services_ids = request.POST.getlist("services_ids")
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


@login_required(login_url='/login_render/')
def SSADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_ssname = request.POST.get('ch_ssname')
        ch_sprovider = cl_New_organization.objects.filter(ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        # ch_service_family = cl_Servicefamilies.objects.filter(ch_sname=request.POST.get('ch_sfamily')).first()
        s_subcategory_ids = request.POST.getlist("s_sub_category_ids")
        ch_status = request.POST.get('ch_status')
        txt_description = request.POST.get('txt_description')

        subcategory = cl_Service_subcategory.objects.filter(id__in=s_subcategory_ids)
        # print(subcategory)

        ser = cl_Service(
            # id=id,
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
        s_subcategory_ids = request.POST.getlist("s_sub_category_ids")
        ch_status = request.POST.get('ch_status')
        txt_description = request.POST.get('txt_description')

        subcategory = cl_Service_subcategory.objects.filter(id__in=s_subcategory_ids)
        # print(subcategory)

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
        ch_sservice = cl_Service.objects.filter(ch_ssname=request.POST.get('ch_sservice')).first()
        ch_status = request.POST.get('ch_status')	
        ch_sla = cl_Sla.objects.filter(ch_slname=request.POST.get('ch_sla')).first()
        ch_request_type = request.POST.get('ch_request_type')
        txt_description = request.POST.get('txt_description')
        sub = cl_Service_subcategory(
            ch_subname=ch_subname,
            ch_sservice=ch_sservice,
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
        ch_sservice = cl_Service.objects.filter(ch_ssname=request.POST.get('ch_sservice')).first()
        ch_status = request.POST.get('ch_status')	
        ch_sla = cl_Sla.objects.filter(ch_slname=request.POST.get('ch_sla')).first()
        ch_request_type = request.POST.get('ch_request_type')
        txt_description = request.POST.get('txt_description')
        sub = cl_Service_subcategory(
            id=id,
            ch_subname=ch_subname,
            ch_sservice=ch_sservice,
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


##############################################

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


# @login_required(login_url='/login_render/')
# def get_slt_by_sla(request):
#     slaId = request.GET.get('slaId')
#     sla = cl_Sla.objects.filter(id=int(slaId)).first()

#     slt = sla.slts.through.objects.filter(cl_sla_id=sla.id)

#     slll = []
#     for s in slt:
#         print('id :',s.id)
#         x = cl_Slt.objects.filter(id=s.id)
#         slll.append(x)

#     for s in slll:
#         print(s)
#     return JsonResponse([{'id': slt_in_sla.id, 'name': slt_in_sla.ch_name} for slt_in_sla in slll], safe=False)

import json

def get_slt_by_sla(request):
    slaId = request.GET.get('slaId')
    sla = cl_Sla.objects.filter(id=int(slaId)).first()

    slt = sla.slts.through.objects.filter(cl_sla_id=sla.id)
    
    queryset_list = []

    for s in slt:
        print('id :', s.cl_slt_id)
        queryset = cl_Slt.objects.filter(id__icontains=int(s.cl_slt_id))
        data = []
    
        for obj in queryset:
            data.append({
                'id': obj.id,
                'ch_name': obj.ch_name,
                'ch_priority': obj.ch_priority,
                'ch_request_type': obj.ch_request_type,
                'ch_metric': obj.ch_metric,
                'ch_value': obj.ch_value,
                'ch_unit': obj.ch_unit
            })
            queryset_list.append(data)

    json_data = json.dumps(queryset_list)
        
    # for queryset in queryset_list:
    #     for obj in queryset:
    #         print(obj['id'], obj['ch_name'], obj['ch_priority'])

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
        slt_ids = request.POST.getlist("slt_ids")

        slts = cl_Slt.objects.filter(id__in=slt_ids)

        sl = cl_Sla(
            id=id,
            ch_slname=ch_sl_name,
            ch_slaprovider=ch_slaprovider,
            txt_description=txt_description,
        )
        sl.save()
        sl.slts.set(slts)

        # id = request.POST.get('id')
        # ch_slname = request.POST.get('ch_slname')
        # ch_slaprovider = cl_New_organization.objects.get(
        #     ch_name=str.capitalize(request.POST.get('ch_organization')))
        # txt_description = request.POST.get('txt_description')
        # sl = cl_Sla(
        #     id=id,
        #     ch_slname=ch_slname,
        #     ch_slaprovider=ch_slaprovider,
        #     txt_description=txt_description
        # )
        # sl.save()
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
        print(id)

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
        role = roles.objects.all()
        q = request.GET.get('searchrole')
        if q != None:
            user = adminuser.objects.filter(ch_user_firstname__icontains=q)        
        context = {
            'user': user,
            'role': role,
            'permission':permission
        }
        return render(request, 'tool/user.html', context)

@login_required(login_url='/login_render/')
def add_new_user(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_user_firstname = request.POST.get('ch_user_firstname')
        ch_user_lastname = request.POST.get('ch_user_lastname')
        ch_user_email = request.POST.get('ch_user_email')
        ch_user_password = request.POST.get('ch_user_password')
        ch_user_role = roles.objects.get(
            role_name=request.POST.get('role_name'))
        # ch_user_expirydate = request.POST.get('ch_user_expirydate')
        ch_user_mobilenumber = request.POST.get('ch_user_mobilenumber')

        user = adminuser(
            first_name=ch_user_firstname,
            last_name=ch_user_lastname,
            email=ch_user_email,
            ch_user_role=ch_user_role,
            # ch_user_expirydate=ch_user_expirydate,
            ch_user_mobilenumber = ch_user_mobilenumber,
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
        ch_user_updated_role = roles.objects.get(
            role_name=request.POST.get('role_name'))
        user.ch_user_role = ch_user_updated_role
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


