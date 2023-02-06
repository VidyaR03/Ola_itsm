from tool.forms import *
from django.shortcuts import render, redirect
from django.contrib import messages
from tool.models import *
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



@login_required(login_url='/login_render/')
def configuration(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    return render(request, 'tool/configurationmanagement.html',{'permission':permission})


@login_required(login_url='/login_render/')
def configurationmanagement_copy(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    return render(request, 'tool/configurationmanagement_COPY.html',{'permission':permission})


@login_required(login_url='/login_render/')
def contact(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    return render(request, 'tool/contact.html',{'permission':permission})


@login_required(login_url='/login_render/')
def software(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    soft = cl_Software.objects.all()
    org = cl_New_organization.objects.all()

    context = {
        'soft': soft,
        'org':org,
        'permission':permission
    }
    return render(request, 'tool/software.html', context)


@login_required(login_url='/login_render/')
def softAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_sofname = request.POST.get('ch_sofname')
        # ch_organization = cl_New_organization.objects.get(ch_name = request.POST.get('ch_organization'))
        # print('organization :',ch_organization)
        ch_vendor = request.POST.get('ch_vendor')
        chversion = request.POST.get('chversion')
        ch_type = request.POST.get('ch_type')
        soft = cl_Software(
            # id=id,
            ch_sofname=ch_sofname,
            ch_vendor=ch_vendor,
            chversion=chversion,
            ch_type=ch_type,
        )
        soft.save()
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
    return redirect(request, 'tool/software.html',{'permission':permission})


@login_required(login_url='/login_render/')
def softDelete(request, id):
    soft = cl_Software.objects.filter(id=id)
    soft.delete()
    return redirect('software')


@login_required(login_url='/login_render/')
def newci(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    return render(request, 'tool/newci.html',{'permission':permission})


@login_required(login_url='/login_render/')
def document(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    doc = cl_Document.objects.all()
    context = {
        'doc': doc,
        'permission':permission
    }
    return render(request, 'tool/document.html', context)


@login_required(login_url='/login_render/')
def DocAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_version = request.POST.get('ch_version')
        txt_description = request.POST.get('txt_description')
        txt_text = request.POST.get('txt_text')
        url_URL = request.POST.get('url_URL')
        ch_File = request.POST.get('ch_File')
        doc = cl_Document(
            # id=id,
            ch_name=ch_name,
            ch_organization=ch_organization,
            ch_version=ch_version,
            txt_description=txt_description,
            txt_text=txt_text,
            url_URL=url_URL,
            ch_File=ch_File,
        )
        doc.save()
        return redirect('document')
    return render(request, 'tool/document.html',{'permission':permission})


@login_required(login_url='/login_render/')
def DocEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    doc = cl_Document.objects.all()
    context = {
        'doc': doc,
        'permission':permission
    }
    return render(request, 'tool/document.html', context)


@login_required(login_url='/login_render/')
def DocUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_version = request.POST.get('ch_version')
        txt_description = request.POST.get('txt_description')
        txt_text = request.POST.get('txt_text')
        url_URL = request.POST.get('url_URL')
        ch_File = request.POST.get('ch_File')
        doc = cl_Document(
            id=id,
            ch_name=ch_name,
            ch_organization=ch_organization,
            ch_version=ch_version,
            txt_description=txt_description,
            txt_text=txt_text,
            url_URL=url_URL,
            ch_File=ch_File,
        )
        doc.save()
        return redirect('document')
    return redirect(request, 'tool/document.html',{'permission':permission})


@login_required(login_url='/login_render/')
def DocDelete(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    doc = cl_Document.objects.filter(id=id)
    doc.delete()
    return redirect('document')



@login_required(login_url='/login_render/')
def application_solution(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    appso = cl_Application_solution.objects.all()
    org = cl_New_organization.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(appso, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            appso = cl_Application_solution.objects.filter(
                ch_name__icontains=q)
    return render(request, 'tool/application_solution.html', {'appso': appso,'org':org,'users':users,'permission':permission})


@login_required(login_url='/login_render/')
def appAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        txt_description = request.POST.get('txt_description')
        appso = cl_Application_solution(
            # id=id,
            ch_name=ch_name,
            ch_organization=ch_organization,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            txt_description=txt_description,
        )
        appso.save()
        return redirect('application')
    return render(request, 'tool/application_solution.html',{'permission':permission})


@login_required(login_url='/login_render/')
def appEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    appso = cl_Application_solution.objects.all()
    context = {
        'appso': appso,
        'permission':permission
    }
    return render(request, 'tool/application_solution.html', context)


@login_required(login_url='/login_render/')
def appUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        txt_description = request.POST.get('txt_description')
        appso = cl_Application_solution(
            id=id,
            ch_name=ch_name,
            ch_organization=ch_organization,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            txt_description=txt_description,
        )
        appso.save()
        return redirect('application')
    return render(request, 'tool/application_solution.html',{'permission':permission})


@login_required(login_url='/login_render/')
def appDelete(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            appso = cl_Application_solution.objects.filter(id=i).first()
            appso.delete()
    return redirect('application')


############ Delivery Model #############

# @login_required(login_url='/login_render/')
# def delivery_model(request):
#     form = DeliverymodelForm()
#     if request.method == 'POST':AutoField(primary_key=True) 
#     id = models.AutoField(primary_key=True, editable=False
#         form = DeliverymodelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Data Add Successfully")
#     context = {'form': form}
#     return render(request, 'tool/delivery_model.html', context)

 ########## Business Processs #############

@login_required(login_url='/login_render/')
def business_process(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    buss = cl_Business_process.objects.all()
    org = cl_New_organization.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(buss, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchbusinessname')
        if q != None:
            buss = cl_Business_process.objects.filter(
                ch_business_name__icontains=q)
    return render(request, 'tool/business_process.html', {'buss': buss,'org':org,'users':users,'permission':permission})


@login_required(login_url='/login_render/')
def bussAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_business_name = request.POST.get('ch_business_name')
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get('dt_move_to_production_date')
        txt_description = request.POST.get('txt_description')
        print(ch_business_name)
        buss = cl_Business_process(
            # id=id,
            ch_business_name=ch_business_name,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            txt_description=txt_description,
        )
        # print(buss)
        buss.save()
        return redirect('businessprocess')
    return render(request, 'tool/business_process.html',{'permission':permission})


@login_required(login_url='/login_render/')
def bussEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    buss = cl_Business_process.objects.all()
    context = {
        'buss': buss,
        'permission':permission
    }
    return render(request, 'tool/business_process.html', context)


@login_required(login_url='/login_render/')
def bussUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_business_name = request.POST.get('ch_business_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get('dt_move_to_production_date')
        txt_description = request.POST.get('txt_description')
        buss = cl_Business_process(
            id=id,
            ch_business_name=ch_business_name,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            txt_description=txt_description,
        )
        buss.save()
        return redirect('businessprocess')
    return render(request, 'tool/business_process.html',{'permission':permission})


@login_required(login_url='/login_render/')
def bussDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            buss = cl_Business_process.objects.filter(id=i).first()
            buss.delete()
        return redirect('businessprocess')



############# NewDB ###############

@login_required(login_url='/login_render/')
def newdb_server(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    db = cl_Newdb_server.objects.all()
    org = cl_New_organization.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(db, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            db = cl_Newdb_server.objects.filter(
               ch_dbname__icontains=q)
    return render(request, 'tool/newdb_server.html', {'db': db,'org':org,'users':users, 'permission':permission})


@login_required(login_url='/login_render/')
def dbAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_dbname = request.POST.get('ch_dbname')
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get('dt_move_to_production_date')
        ch_software = request.POST.get('ch_software')
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        db = cl_Newdb_server(
            # id=id,
            ch_dbname=ch_dbname,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            ch_software=ch_software,
            ch_software_license=ch_software_license,
            ch_system=ch_system,
            ch_path=ch_path,
            txt_description=txt_description,
        )
        db.save()
        return redirect('newdb')
    return render(request, 'tool/newdb_server.html',{'permission':permission})


@login_required(login_url='/login_render/')
def dbEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    db = cl_Newdb_server.objects.all()
    context = {
        'db': db,
        'permission':permission
    }
    return render(request, 'tool/newdb_server.html', context)


@login_required(login_url='/login_render/')
def dbUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_dbname = request.POST.get('ch_dbname')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get('dt_move_to_production_date')
        ch_software = request.POST.get('ch_software')
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        db = cl_Newdb_server(
            id=id,
            ch_dbname=ch_dbname,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            ch_software=ch_software,
            ch_software_license=ch_software_license,
            ch_system=ch_system,
            ch_path=ch_path,
            txt_description=txt_description,
        )
        db.save()
        return redirect('newdb')
    return render(request, 'tool/newdb_server.html',{'permission':permission})


@login_required(login_url='/login_render/')
def dbDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            db = cl_Newdb_server.objects.filter(id=i).first()
            db.delete()
    return redirect('newdb')

######### Data Base Schema #####

@login_required(login_url='/login_render/')
def dataschema(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    schema = cl_Database_schema.objects.all()
    org = cl_New_organization.objects.all()
    server = cl_Newdb_server.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(schema, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            schema = cl_Database_schema.objects.filter(ch_dsname__icontains=q)
    return render(request, 'tool/database_schema.html', {'schema': schema,'server':server,'org':org,'users':users, 'permission':permission})


@login_required(login_url='/login_render/')
def DSADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":     
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()   

        ch_dsname = request.POST.get('ch_dsname')        
        ch_db_server =cl_Newdb_server.objects.get(ch_dbname=request.POST.get('ch_db_server'))
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        txt_description = request.POST.get('txt_description')
        schema = cl_Database_schema(
            # id=id,
            ch_dsname=ch_dsname,
            ch_organization=ch_organization,
            ch_db_server=ch_db_server,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            txt_description=txt_description,
        )
        schema.save()
        return redirect('databaseschema')
    return render(request, 'tool/database_schema.html',{'permission':permission})


@login_required(login_url='/login_render/')
def DSEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    schema = cl_Database_schema.objects.all()
    context = {
        'schema': schema,
        'permission':permission
    }
    return render(request, 'tool/database_schema.html', context)


@login_required(login_url='/login_render/')
def DSUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')        
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))        
        ch_dsname = request.POST.get('ch_dsname')        
        ch_db_server =cl_Newdb_server.objects.get(ch_dbname=request.POST.get('ch_db_server'))
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get('dt_move_to_production_date')
        txt_description = request.POST.get('txt_description')
        schema = cl_Database_schema(
            id=id,
            ch_dsname=ch_dsname,
            ch_organization=ch_organization,
            ch_db_server=ch_db_server,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            txt_description=txt_description,
        )
        schema.save()
        return redirect('databaseschema')
    return render(request, 'tool/database_schema.html',{'permission':permission})


@login_required(login_url='/login_render/')
def DSDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            schema = cl_Database_schema.objects.filter(id=i).first()
            schema.delete()
    return redirect('databaseschema')



############## Middleware ##########

@login_required(login_url='/login_render/')
def middlewareinstance(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    mi = cl_Middleware_instance.objects.all()
    org = cl_New_organization.objects.all()
    middle = cl_New_middleware.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(mi, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            mi = cl_Middleware_instance.objects.filter(ch_name__icontains=q)
    return render(request, 'tool/middleware_instance.html', {'mi': mi,'middle':middle,'org':org,'users':users, 'permission':permission})


@login_required(login_url='/login_render/')
def MADD(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()       
        ch_miname = request.POST.get('ch_miname')
        ch_middleware = cl_New_middleware.objects.filter(ch_midname=request.POST.get('ch_middleware')).first()
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get('dt_move_to_production_date')
        txt_description = request.POST.get('txt_description')
        mi = cl_Middleware_instance(
            
            ch_miname=ch_miname,
            ch_organization=ch_organization,
            ch_middleware=ch_middleware,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            txt_description=txt_description,
        )
        mi.save()
        return redirect('middlewareinstance')
    return render(request, 'tool/middleware_instance.html',{'permission':permission})


@login_required(login_url='/login_render/')
def MEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    mi = cl_Middleware_instance.objects.all()
    context = {
        'mi': mi,
        'permission':permission
    }
    return render(request, 'tool/middleware_instance.html', context)


@login_required(login_url='/login_render/')
def MUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_miname = request.POST.get('ch_miname')
        ch_organization = cl_New_organization.objects.get(ch_name=request.POST.get('ch_organization'))
        ch_middleware = cl_New_middleware.objects.get(ch_midname=request.POST.get('ch_middleware'))
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        txt_description = request.POST.get('txt_description')
        mi = cl_Middleware_instance(
            id=id,
            ch_miname=ch_miname,
            ch_organization=ch_organization,
            ch_middleware=ch_middleware,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            txt_description=txt_description,
        )
        mi.save()
        return redirect('middlewareinstance')
    return render(request, 'tool/middleware_instance.html',{'permission':permission})


@login_required(login_url='/login_render/')
def MDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            mi = cl_Middleware_instance.objects.filter(id=i).first()
            mi.delete()
    return redirect('middlewareinstance')



##################  New Middleware  ##########

@login_required(login_url='/login_render/')
def new_middleware(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    middle = cl_New_middleware.objects.all()
    org = cl_New_organization.objects.all()
    soft = cl_Software.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(middle, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            middle = cl_New_middleware.objects.filter(ch_midname__icontains=q)
    return render(request, 'tool/new_middleware.html', {'middle': middle,'soft':soft,'org':org,'users':users, 'permission':permission})


@login_required(login_url='/login_render/')
def MWAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        ch_midname = request.POST.get('ch_midname')
        # ch_organization = cl_New_organization.objects.get(ch_name=request.POST.get('ch_organization'))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get( 'dt_move_to_production_date')
        ch_software = cl_Software.objects.filter(ch_sofname=request.POST.get('ch_software')).first()
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        middle = cl_New_middleware(
            # id=id,
            ch_midname=ch_midname,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            ch_software=ch_software,
            ch_software_license=ch_software_license,
            ch_system=ch_system,
            ch_path=ch_path,
            txt_description=txt_description,
        )
        middle.save()
        return redirect('newmiddleware')
    return render(request, 'tool/new_middleware.html',{'permission':permission})


@login_required(login_url='/login_render/')
def MWEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    middle = cl_New_middleware.objects.all()
    context = {
        'middle': middle,
        'permission':permission
    }
    return render(request, 'tool/new_middleware.html', context)


@login_required(login_url='/login_render/')
def MWUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_midname = request.POST.get('ch_midname')
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get('dt_move_to_production_date')
        ch_software = cl_Software.objects.get(ch_sofname=request.POST.get('ch_software'))
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        middle = cl_New_middleware(
            id=id,
            ch_midname=ch_midname,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            ch_software=ch_software,
            ch_software_license=ch_software_license,
            ch_system=ch_system,
            ch_path=ch_path,
            txt_description=txt_description,
        )
        middle.save()
        return redirect('newmiddleware')
    return render(request, 'tool/new_middleware.html',{'permission':permission})


@login_required(login_url='/login_render/')
def MWDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            middle = cl_New_middleware.objects.filter(id=i).first()
            middle.delete()
    return redirect('newmiddleware')

 
######### Other Software ###########

@login_required(login_url='/login_render/')
def other_software(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    os = cl_Other_software.objects.all()
    org = cl_New_organization.objects.all()
    soft = cl_Software.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(os, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            os = cl_Other_software.objects.filter(
                ch_name__icontains=q)
    return render(request, 'tool/othersoftware.html', {'os': os,'soft':soft,'org':org,'users':users, 'permission':permission})


@login_required(login_url='/login_render/')
def osAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        ch_osname = request.POST.get('ch_osname')
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get('dt_move_to_production_date')
        ch_software = cl_Software.objects.filter(ch_sofname=request.POST.get('ch_software')).first()
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        os = cl_Other_software(
            # id=id,
            ch_osname=ch_osname,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            ch_software=ch_software,
            ch_software_license=ch_software_license,
            ch_system=ch_system,
            ch_path=ch_path,
            txt_description=txt_description,
        )
        os.save()
        return redirect('other_software')
    return render(request, 'tool/othersoftware.html',{'permission':permission})


@login_required(login_url='/login_render/')
def osEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    os = cl_Other_software.objects.all()
    context = {
        'os': os,
        'permission':permission
    }
    return render(request, 'tool/othersoftware.html', context)


@login_required(login_url='/login_render/')
def osUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_osname = request.POST.get('ch_osname')
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get('dt_move_to_production_date')
        ch_software = cl_Software.objects.get(ch_sofname=request.POST.get('ch_software'))
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        os = cl_Other_software(
            id=id,
            ch_osname=ch_osname,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            ch_software=ch_software,
            ch_software_license=ch_software_license,
            ch_system=ch_system,
            ch_path=ch_path,
            txt_description=txt_description,
        )
        os.save()
        return redirect('other_software')
    return render(request, 'tool/othersoftware.html',{'permission':permission})


@login_required(login_url='/login_render/')
def osDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            os = cl_Other_software.objects.filter(id=i).first()
            os.delete()
    return redirect('other_software')


############ Web App ############

@login_required(login_url='/login_render/')
def web_application(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    wa = cl_Web_application.objects.all()
    org = cl_New_organization.objects.all()
    sweb = cl_Web_server.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(wa, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            wa = cl_Web_application.objects.filter(
                ch_waname__icontains=q)
    return render(request, 'tool/webapplication.html', {'wa': wa,'sweb':sweb,'org':org,'users':users,'permission':permission})


@login_required(login_url='/login_render/')
def waAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()

        ch_waname = request.POST.get('ch_waname')
        ch_webserver = cl_Web_server.objects.filter(ch_wsname=request.POST.get('ch_webserver')).first()
        url_website = request.POST.get('url_website')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get('dt_move_to_production_date')
        txt_description = request.POST.get('txt_description')
        wa = cl_Web_application(
            # id=id,
            ch_waname=ch_waname,
            ch_organization=ch_organization,
            ch_webserver=ch_webserver,
            url_website=url_website,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            txt_description=txt_description,
        )
        wa.save()
        return redirect('webapplication')
    return render(request, 'tool/webapplication.html',{'permission':permission})


@login_required(login_url='/login_render/')
def wsEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    wa = cl_Web_application.objects.all()
    context = {
        'wa': wa,
        'permission':permission
    }
    return render(request, 'tool/webapplication.html', context)


@login_required(login_url='/login_render/')
def waUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_waname = request.POST.get('ch_waname')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_webserver = cl_Web_server.objects.get(
            ch_wsname=request.POST.get('ch_webserver'))
        url_website = request.POST.get('url_website')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        txt_description = request.POST.get('txt_description')
        wa = cl_Web_application(
            id=id,
            ch_waname=ch_waname,
            ch_organization=ch_organization,
            ch_webserver=ch_webserver,
            url_website=url_website,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            txt_description=txt_description,
        )
        wa.save()
        return redirect('webapplication')
    return render(request, 'tool/webapplication.html',{'permission':permission})


@login_required(login_url='/login_render/')
def waDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            wa = cl_Web_application.objects.filter(id=i).first()
            wa.delete()

    return redirect('webapplication')

########## OS License ######



########## network Device ######

@login_required(login_url='/login_render/')
def networkdevice(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    nd = cl_Network_device.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            nd = cl_Network_device.objects.filter(ch_ndname__icontains=q)

    org = cl_New_organization.objects.all()
    nttype = cl_network_type.objects.all()
    brnd = cl_Brand.objects.all()
    model = cl_model.objects.all()
    ios = cl_ios_version.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(nd, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
   
    return render(request, 'tool/network_device.html', {'nd': nd,'org':org,'users':users,'nttype':nttype,'brnd':brnd,'model':model,'ios':ios,'permission':permission})


@login_required(login_url='/login_render/')
def ndAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_ndname = request.POST.get('ch_ndname')
        ch_organization = cl_New_organization.objects.filter(ch_name=request.POST.get('ch_organization')).first()
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        ch_location = request.POST.get('ch_location')
        ch_network_type = cl_network_type.objects.filter(ch_nname=request.POST.get('ch_network_type')).first()
        ch_brand = cl_Brand.objects.filter(ch_brandname=request.POST.get('ch_brand')).first()
        ch_model = cl_model.objects.filter(ch_modelname=request.POST.get('ch_model')).first()
        i_ios_version = cl_ios_version.objects.filter(ch_iosname=request.POST.get('i_ios_version')).first()
        i_management_ip = request.POST.get('i_management_ip')
        ch_ram = request.POST.get('ch_ram')
        i_rack_unit = request.POST.get('i_rack_unit')
        i_serial_number = request.POST.get('i_serial_number')
        i_asset_number = request.POST.get('i_asset_number')
        dt_move_to_production_date = request.POST.get('dt_move_to_production_date')
        dt_purchase_date = request.POST.get('dt_purchase_date')
        dt_end_of_warranty = request.POST.get('dt_end_of_warranty')
        txt_description = request.POST.get('txt_description')
        nd = cl_Network_device(
            # id=id,
            ch_ndname=ch_ndname,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            ch_location=ch_location,
            ch_network_type=ch_network_type,
            ch_brand=ch_brand,
            ch_model=ch_model,
            i_ios_version=i_ios_version,
            i_management_ip=i_management_ip,
            ch_ram=ch_ram,
            i_rack_unit=i_rack_unit,
            i_serial_number=i_serial_number,
            i_asset_number=i_asset_number,
            dt_move_to_production_date=dt_move_to_production_date,
            dt_purchase_date=dt_purchase_date,
            dt_end_of_warranty=dt_end_of_warranty,
            txt_description=txt_description,
        )
        nd.save()
        return redirect('networkdevice')
    return render(request, 'tool/network_device.html',{'permission':permission})


@login_required(login_url='/login_render/')
def ndEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    nd = cl_Network_device.objects.all()
    context = {
        'nd': nd,
        'permission':permission
    }
    return render(request, 'tool/network_device.html', context)


@login_required(login_url='/login_render/')
def ndUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_ndname = request.POST.get('ch_ndname')
        ch_organization = cl_New_organization.objects.get(ch_name=request.POST.get('ch_organization'))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        ch_location = request.POST.get('ch_location')
        ch_network_type = cl_network_type.objects.get( ch_nname=request.POST.get('ch_network_type'))
        ch_brand = cl_Brand.objects.get(ch_brandname=request.POST.get('ch_brand'))
        ch_model = cl_model.objects.get(ch_modelname=request.POST.get('ch_model'))
        i_ios_version = cl_ios_version.objects.get(ch_iosname=request.POST.get('i_ios_version'))
        i_management_ip = request.POST.get('i_management_ip')
        ch_ram = request.POST.get('ch_ram')
        i_rack_unit = request.POST.get('i_rack_unit')
        i_serial_number = request.POST.get('i_serial_number')
        i_asset_number = request.POST.get('i_asset_number')
        dt_move_to_production_date = request.POST.get('dt_move_to_production_date')
        dt_purchase_date = request.POST.get('dt_purchase_date')
        dt_end_of_warranty = request.POST.get('dt_end_of_warranty')
        txt_description = request.POST.get('txt_description')
        nd = cl_Network_device(
            id=id,
            ch_ndname=ch_ndname,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            ch_location=ch_location,
            ch_network_type=ch_network_type,
            ch_brand=ch_brand,
            ch_model=ch_model,
            i_ios_version=i_ios_version,
            i_management_ip=i_management_ip,
            ch_ram=ch_ram,
            i_rack_unit=i_rack_unit,
            i_serial_number=i_serial_number,
            i_asset_number=i_asset_number,
            dt_move_to_production_date=dt_move_to_production_date,
            dt_purchase_date=dt_purchase_date,
            dt_end_of_warranty=dt_end_of_warranty,
            txt_description=txt_description,
        )
        nd.save()
        return redirect('networkdevice')
    return render(request, 'tool/network_device.html',{'permission':permission})


@login_required(login_url='/login_render/')
def ndDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            nd = cl_Network_device.objects.filter(id=i).first()
            nd.delete()
    return redirect('networkdevice')

########## Network Type #########

@login_required(login_url='/login_render/')
def network_type(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    nt = cl_network_type.objects.all()
    org = cl_New_organization.objects.all()

    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            nt = cl_network_type.objects.filter(ch_nname__icontains=q)

    page = request.GET.get('page', 1)

    paginator = Paginator(nt, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            nt = cl_network_type.objects.filter(ch_nname__icontains=q)
    return render(request, 'tool/network_type.html', {'nt': nt,'org':org,'users':users,'permission':permission})


@login_required(login_url='/login_render/')
def ntAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        print(id)
        ch_nname = request.POST.get('ch_nname')
        nt = cl_network_type(
            # id=id,
            ch_nname=ch_nname,
        )
        nt.save()
      
        return redirect('network_type')
    return render(request, 'tool/network_type.html',{'permission':permission})


@login_required(login_url='/login_render/')
def ntEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    nt = cl_network_type.objects.all()
    context = {
        'nt': nt,
        'permission':permission
    }
    return render(request, 'tool/network_type.html', context)


@login_required(login_url='/login_render/')
def ntUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_nname = request.POST.get('ch_nname')
        nt = cl_network_type(
            id=id,
            ch_nname=ch_nname,
        )
        nt.save()
        return redirect('network_type')
    return render(request, 'tool/network_type.html',{'permission':permission})


@login_required(login_url='/login_render/')
def ntDelete(request, id):
    nt = cl_network_type.objects.filter(id=id)
    nt.delete()
    return redirect('network_type')


@login_required(login_url='/login_render/')
def os_family(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    osf = cl_os_family.objects.all()
    org = cl_New_organization.objects.all()

    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            osf = cl_os_family.objects.filter(ch_fname__icontains=q)

    page = request.GET.get('page', 1)

    paginator = Paginator(osf, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchfname')
        if q != None:
            osf = cl_os_family.objects.filter(ch_fname__icontains=q)
    return render(request, 'tool/os_family.html', {'osf': osf,'org':org,'users':users, 'permission':permission})


@login_required(login_url='/login_render/')
def osfAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        print(id)
        ch_fname = request.POST.get('ch_fname')
        
        osf = cl_os_family(
            id=id,
            ch_fname=ch_fname,
        )
        osf.save()
        print(osf)
        return redirect('os_family')
    return render(request, 'tool/os_family.html',{'permission':permission})


@login_required(login_url='/login_render/')
def osfEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    osf = cl_os_family.objects.all()
    context = {
        'osf': osf,
        'permission':permission
    }
    return render(request, 'tool/os_family.html', context)


@login_required(login_url='/login_render/')
def osfUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_fname = request.POST.get('ch_fname')
        osf = cl_os_family(
            id=id,
            ch_fname=ch_fname,
        )
        osf.save()
        return redirect('os_family')
    return render(request, 'tool/os_family.html',{'permission':permission})


@login_required(login_url='/login_render/')
def osfDelete(request, id):
    osf = cl_os_family.objects.filter(id=id)
    osf.delete()
    return redirect('os_family')



@login_required(login_url='/login_render/')
def os_version(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    osv = cl_os_version.objects.all()
    org = cl_New_organization.objects.all()

    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            osv = cl_os_version.objects.filter(ch_osname__icontains=q)

    page = request.GET.get('page', 1)

    paginator = Paginator(osv, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchfname')
        if q != None:
            osf = cl_os_version.objects.filter(ch_fname__icontains=q)
    return render(request, 'tool/os_version.html', {'osv': osv,'org':org,'users':users,'permission':permission})


@login_required(login_url='/login_render/')
def osvAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_osname = request.POST.get('ch_osname')
        ch_fname = cl_os_family.objects.get(
            ch_fname=request.POST.get('ch_fname'))
        
        osv = cl_os_version(
            id=id,
            ch_osname=ch_osname,
            ch_fname =ch_fname, 
        )
        osv.save()
        print(osv)
        return redirect('os_version')
    return render(request, 'tool/os_version.html',{'permission':permission})


@login_required(login_url='/login_render/')
def osvEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    osv = cl_os_version.objects.all()
    context = {
        'osv': osv,
        'permission':permission
    }
    return render(request, 'tool/os_version.html', context)


@login_required(login_url='/login_render/')
def osvUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_osname = request.POST.get('ch_osname')
        ch_fname = cl_os_family.objects.get(
            ch_fname=request.POST.get('ch_fname'))
        osv = cl_os_version(
            id=id,
            ch_osname=ch_osname,
            ch_fname=ch_fname,
        )
        osv.save()
        return redirect('os_version')
    return render(request, 'tool/os_version.html',{'permission':permission})


@login_required(login_url='/login_render/')
def osvDelete(request, id):
    osv = cl_os_version.objects.filter(id=id)
    osv.delete()
    return redirect('os_version')


@login_required(login_url='/login_render/')
def os_license(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    ol = cl_os_license.objects.all()
    org = cl_New_organization.objects.all()

    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            ol = cl_os_license.objects.filter(ch_name__icontains=q)
    page = request.GET.get('page', 1)

    paginator = Paginator(ol, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            ol = cl_os_license.objects.filter(
                ch_name__icontains=q)
    return render(request, 'tool/os_license.html', {'ol': ol,'org':org,'users':users, 'permission':permission})



@login_required(login_url='/login_render/')
def olAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_version = cl_os_version.objects.get(ch_osname=request.POST.get('ch_version'))
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        ch_usage_limit = request.POST.get('ch_usage_limit')
        ch_perpetual = request.POST.get('ch_perpetual')
        dt_start_date = request.POST.get('dt_start_date')
        dt_end_date = request.POST.get('dt_end_date')
        ch_key = request.POST.get('ch_key')
        txt_description = request.POST.get('txt_description')
        ol = cl_os_license(
            # id=id,
            ch_name=ch_name,
            ch_version =ch_version,
            ch_organization=ch_organization,
            ch_usage_limit=ch_usage_limit,          
            ch_perpetual=ch_perpetual,
            dt_start_date=dt_start_date,
            dt_end_date=dt_end_date,
            ch_key = ch_key,
            txt_description=txt_description,
        )
        ol.save()
        return redirect('os_license')
    return render(request, 'tool/os_license.html',{'permission':permission})


@login_required(login_url='/login_render/')
def olEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    ol = cl_os_license.objects.all()
    context = {
        'ol': ol,
    }
    return render(request, 'tool/os_license.html', context)


@login_required(login_url='/login_render/')
def olUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_version = cl_os_version.objects.get(ch_osname=request.POST.get('ch_version'))
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_usage_limit = request.POST.get('ch_usage_limit')
        ch_perpetual = request.POST.get('ch_perpetual')
        dt_start_date = request.POST.get('dt_start_date')
        dt_end_date = request.POST.get('dt_end_date')
        ch_key = request.POST.get('ch_key')
        txt_description = request.POST.get('txt_description')
        ol = cl_os_license(
            id=id,
            ch_name=ch_name,
            ch_version =ch_version,
            ch_organization=ch_organization,
            ch_usage_limit=ch_usage_limit,          
            ch_perpetual=ch_perpetual,
            dt_start_date=dt_start_date,
            dt_end_date=dt_end_date,
            ch_key = ch_key,
            txt_description=txt_description,
        )
        ol.save()
        return redirect('os_license')
    return render(request, 'tool/os_license.html',{'permission':permission})



@login_required(login_url='/login_render/')
def olDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            ol = cl_os_license.objects.filter(id=i).first()
            ol.delete()
    return redirect('os_license')



@login_required(login_url='/login_render/')
def brand(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    brand = cl_Brand.objects.all()
    org = cl_New_organization.objects.all()

    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            brand = cl_Brand.objects.filter(ch_brandname__icontains=q)
    page = request.GET.get('page', 1)

    paginator = Paginator(brand, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            brand = cl_Brand.objects.filter(ch_brandname__icontains=q)
    return render(request, 'tool/brand.html', {'brand': brand,'org':org,'users':users,'permission':permission})


@login_required(login_url='/login_render/')
def bnAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        print(id)
        ch_brandname = request.POST.get('ch_brandname')
        brand = cl_Brand(
            ch_brandname=ch_brandname,
        )
        brand.save()
        print(brand)
        return redirect('brand')

    return render(request, 'tool/brand.html',{'permission':permission})


@login_required(login_url='/login_render/')
def bnEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    brand = cl_Brand.objects.all()
    context = {
        'brand': brand,
        'permission':permission
    }
    return render(request, 'tool/brand.html', context)


@login_required(login_url='/login_render/')
def bnUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_brandname = request.POST.get('ch_brandname')

        brand = cl_Brand(
            id=id,
            ch_brandname=ch_brandname,

        )
        brand.save()
        return redirect('brand')
    return render(request, 'tool/brand.html',{'permission':permission})


@login_required(login_url='/login_render/')
def bnDelete(request, id):
    brand = cl_Brand.objects.filter(id=id)
    brand.delete()
    return redirect('brand')


@login_required(login_url='/login_render/')
def cmodel(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    model = cl_model.objects.all()
    org = cl_New_organization.objects.all()
    brnd = cl_Brand.objects.all()


    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            model = cl_model.objects.filter(ch_modelname__icontains=q)

    page = request.GET.get('page', 1)

    paginator = Paginator(model, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            model = cl_model.objects.filter(ch_modelname__icontains=q)
    return render(request, 'tool/model.html', {'model': model,'brnd':brnd,'users':users,'org':org, 'permission':permission})



@login_required(login_url='/login_render/')
def mdAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        print(id)
        ch_modelname = request.POST.get('ch_modelname')
        ch_brandname = cl_Brand.objects.filter(
            ch_brandname=request.POST.get('ch_brandname')).first()

        model = cl_model(
            # id=id,
            ch_modelname=ch_modelname,
            ch_brandname=ch_brandname,

        )
        model.save()
        print(model)
        return redirect('cmodel')

    return render(request, 'tool/model.html',{'permission':permission})



@login_required(login_url='/login_render/')
def mdEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    model = cl_model.objects.all()
    context = {
        'model': model,
        'permission':permission
    }
    return render(request, 'tool/model.html', context)


@login_required(login_url='/login_render/')
def mdUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_modelname = request.POST.get('ch_modelname')
        ch_brandname = cl_Brand.objects.get(
            ch_brandname=request.POST.get('ch_brandname'))

        model = cl_model(
            id=id,
            ch_modelname=ch_modelname,
            ch_brandname=ch_brandname,

        )
        model.save()
        return redirect('cmodel')
    return render(request, 'tool/model.html',{'permission':permission})


@login_required(login_url='/login_render/')
def mdDelete(request, id):
    model = cl_model.objects.filter(id=id)
    model.delete()
    return redirect('cmodel')


@login_required(login_url='/login_render/')
def iosver(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    iv = cl_ios_version.objects.all()
    org = cl_New_organization.objects.all()
    brnd = cl_Brand.objects.all()


    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            iv = cl_ios_version.objects.filter(ch_iosname__icontains=q)
    page = request.GET.get('page', 1)

    paginator = Paginator(iv, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            iv = cl_ios_version.objects.filter(ch_name__icontains=q)
    return render(request, 'tool/ios_version.html', {'iv': iv,'users':users,'org':org,'brnd':brnd, 'permission':permission})



@login_required(login_url='/login_render/')
def ivAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        print(id)
        ch_iosname = request.POST.get('ch_iosname')
        ch_brandname = cl_Brand.objects.filter(
            ch_brandname=request.POST.get('ch_brandname')).first()

        iv = cl_ios_version(
            # id=id,
            ch_iosname=ch_iosname,
            ch_brandname=ch_brandname,
        )
        iv.save()
        print(iv)
        return redirect('iosver')
    return render(request, 'tool/ios_version.html',{'permission':permission})



@login_required(login_url='/login_render/')
def ivEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    iv = cl_ios_version.objects.all()
    context = {
        'iv': iv,
        'permission':permission
    }
    return render(request, 'tool/ios_version.html', context)



@login_required(login_url='/login_render/')
def ivUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_iosname = request.POST.get('ch_iosname')
        ch_brandname = cl_Brand.objects.get(
            ch_brandname=request.POST.get('ch_brandname'))

        iv = cl_ios_version(
            id=id,
            ch_iosname=ch_iosname,
            ch_brandname=ch_brandname,

        )
        iv.save()
        return redirect('iosver')
    return render(request, 'tool/ios_version.html',{'permission':permission})



@login_required(login_url='/login_render/')
def ivDelete(request, id):
    iv = cl_ios_version.objects.filter(id=id)
    iv.delete()
    return redirect('iosver')



############ Server ############

@login_required(login_url='/login_render/')
def server(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    se = cl_Server.objects.all()
    org = cl_New_organization.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(se, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            se = cl_Server.objects.filter(
                ch_sname__icontains=q)
    return render(request, 'tool/server.html', {'se': se,'users':users,'org':org, 'permission':permission})



@login_required(login_url='/login_render/')
def serverAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_organization = cl_New_organization.objects.filter(ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        ch_sname = request.POST.get('ch_sname')
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        ch_location = request.POST.get('ch_location')
        ch_os_family =  cl_os_family.objects.get(ch_fname=request.POST.get('ch_os_family'))
        ch_brand = cl_Brand.objects.get(ch_brandname=request.POST.get('ch_brand'))
        ch_model = cl_model.objects.get(ch_modelname=request.POST.get('ch_model'))
        i_os_version = cl_os_version.objects.get(ch_osname=request.POST.get('i_os_version'))
        i_management_ip = request.POST.get('i_management_ip')
        i_os_license = cl_os_license.objects.get(ch_name=request.POST.get('i_os_license'))
        ch_ram = request.POST.get('ch_ram')
        ch_cpu = request.POST.get('ch_cpu')
        i_rack_unit = request.POST.get('i_rack_unit')
        i_serial_number = request.POST.get('i_serial_number')
        i_asset_number = request.POST.get('i_asset_number')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        dt_purchase_date = request.POST.get('dt_purchase_date')
        dt_end_of_warranty = request.POST.get('dt_end_of_warranty')
        txt_description = request.POST.get('txt_description')
        se = cl_Server(
            # id=id,
            ch_sname=ch_sname,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            ch_location=ch_location,
            ch_os_family=ch_os_family,
            ch_brand=ch_brand,
            ch_model=ch_model,
            i_os_version=i_os_version,
            i_management_ip=i_management_ip,
            i_os_license = i_os_license,
            ch_ram=ch_ram,
            ch_cpu = ch_cpu,
            i_rack_unit=i_rack_unit,
            i_serial_number=i_serial_number,
            i_asset_number=i_asset_number,
            dt_move_to_production_date=dt_move_to_production_date,
            dt_purchase_date=dt_purchase_date,
            dt_end_of_warranty=dt_end_of_warranty,
            txt_description=txt_description,
        )
        se.save()
        return redirect('server')
    return render(request, 'tool/server.html',{'permission':permission})



@login_required(login_url='/login_render/')
def serverEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    se = cl_Server.objects.all()
    context = {
        'se': se,
        'permission':permission
    }
    return render(request, 'tool/server.html', context)


@login_required(login_url='/login_render/')
def serverUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_organization = cl_New_organization.objects.get(ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_sname = request.POST.get('ch_sname')
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        ch_location = request.POST.get('ch_location')
        ch_os_family =  cl_os_family.objects.get(ch_fname=request.POST.get('ch_os_family'))
        ch_brand = cl_Brand.objects.get(ch_brandname=request.POST.get('ch_brand'))
        ch_model = cl_model.objects.get(ch_modelname=request.POST.get('ch_model'))
        i_os_version = cl_os_version.objects.get(ch_osname=request.POST.get('i_os_version'))
        i_management_ip = request.POST.get('i_management_ip')
        i_os_license = cl_os_license.objects.get(ch_name=request.POST.get('i_os_license'))
        ch_ram = request.POST.get('ch_ram')
        ch_cpu = request.POST.get('ch_cpu')
        i_rack_unit = request.POST.get('i_rack_unit')
        i_serial_number = request.POST.get('i_serial_number')
        i_asset_number = request.POST.get('i_asset_number')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        dt_purchase_date = request.POST.get('dt_purchase_date')
        dt_end_of_warranty = request.POST.get('dt_end_of_warranty')
        txt_description = request.POST.get('txt_description')
        se = cl_Server(
             id=id,
            ch_sname=ch_sname,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            ch_location=ch_location,
            ch_os_family=ch_os_family,
            ch_brand=ch_brand,
            ch_model=ch_model,
            i_os_version=i_os_version,
            i_management_ip=i_management_ip,
            i_os_license = i_os_license,
            ch_ram=ch_ram,
            ch_cpu = ch_cpu,
            i_rack_unit=i_rack_unit,
            i_serial_number=i_serial_number,
            i_asset_number=i_asset_number,
            dt_move_to_production_date=dt_move_to_production_date,
            dt_purchase_date=dt_purchase_date,
            dt_end_of_warranty=dt_end_of_warranty,
            txt_description=txt_description,
        )
        se.save()
        return redirect('server')
    return render(request, 'tool/server.html',{'permission':permission})



@login_required(login_url='/login_render/')
def serverDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            se = cl_Server.objects.filter(id=i).first()
            se.delete()
    return redirect('server')


############## Web Server ################

@login_required(login_url='/login_render/')
def web_server(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    ws = cl_Web_server.objects.all()
    org = cl_New_organization.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(ws, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            ws = cl_Web_server.objects.filter(ch_wsname__icontains=q)
    return render(request, 'tool/webserver.html', {'ws': ws,'users':users,'org':org, 'permission':permission})



@login_required(login_url='/login_render/')
def wsAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        # id = request.POST.get('id')
        ch_wsname = request.POST.get('ch_wsname')
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get('dt_move_to_production_date')
        ch_software = cl_Software.objects.get(ch_sofname=request.POST.get('ch_software'))
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        ws = cl_Web_server(
            # id=id,
            ch_wsname=ch_wsname,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            ch_software=ch_software,
            ch_software_license=ch_software_license,
            ch_system=ch_system,
            ch_path=ch_path,
            txt_description=txt_description,
        )
        ws.save()
        return redirect('webserver')
    return render(request, 'tool/webserver.html',{'permission':permission})



@login_required(login_url='/login_render/')
def wsEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    ws = cl_Web_server.objects.all()
    context = {
        'ws': ws,
        'permission':permission
    }
    return render(request, 'tool/webserver.html', context)



@login_required(login_url='/login_render/')
def wsUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_wsname = request.POST.get('ch_wsname')
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get('dt_move_to_production_date')
        ch_software = cl_Software.objects.get(ch_sofname=request.POST.get('ch_software'))
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        ws = cl_Web_server(
            id=id,
            ch_wsname=ch_wsname,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            ch_software=ch_software,
            ch_software_license=ch_software_license,
            ch_system=ch_system,
            ch_path=ch_path,
            txt_description=txt_description,
        )
        ws.save()
        return redirect('webserver')
    return render(request, 'tool/webserver.html',{'permission':permission})



@login_required(login_url='/login_render/')
def wsDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            ws = cl_Web_server.objects.filter(id=i).first()
            ws.delete()
    return redirect('webserver')


######## PC Software ######

@login_required(login_url='/login_render/')
def pc_software(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    pc = cl_Pc_software.objects.all()
    org = cl_New_organization.objects.all()
    soft = cl_Software.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(pc, 7)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            pc = cl_Pc_software.objects.filter(ch_pcname_icontains=q)
    return render(request, 'tool/pc_software.html', {'pc': pc,'soft':soft,'users':users,'org':org, 'permission':permission})



@login_required(login_url='/login_render/')
def pcAdd(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_organization = cl_New_organization.objects.filter(
            ch_name=str.capitalize(request.POST.get('ch_organization'))).first()
        ch_pcname = request.POST.get('ch_pcname')
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get('dt_move_to_production_date')
        ch_software = cl_Software.objects.filter(ch_sofname=request.POST.get('ch_software')).first()
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        pc = cl_Pc_software(
            # id=id,
            ch_pcname=ch_pcname,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            ch_software=ch_software,
            ch_software_license=ch_software_license,
            ch_system=ch_system,
            ch_path=ch_path,
            txt_description=txt_description,
        )
        pc.save()
        return redirect('pcsoftware')
    return render(request, 'tool/pc_software.html',{'permission':permission})



@login_required(login_url='/login_render/')
def pcEdit(request):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    pc = cl_Pc_software.objects.all()
    context = {
        'pc': pc,
        
        'permission':permission
    }
    return render(request, 'tool/pc_software.html', context)



@login_required(login_url='/login_render/')
def pcUpdate(request, id):
    permission = roles.objects.filter(id=request.session['user_role']).first()
    if request.method == "POST":
        id = request.POST.get('id')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_pcname = request.POST.get('ch_pcname')
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get('dt_move_to_production_date')
        ch_software = cl_Software.objects.get(ch_sofname=request.POST.get('ch_software'))
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        pc = cl_Pc_software(
            id=id,
            ch_pcname=ch_pcname,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            ch_software=ch_software,
            ch_software_license=ch_software_license,
            ch_system=ch_system,
            ch_path=ch_path,
            txt_description=txt_description,
        )
        pc.save()
        return redirect('pcsoftware')
    return render(request, 'tool/pc_software.html',{'permission':permission})



@login_required(login_url='/login_render/')
def pcDelete(request):
    if request.method == "POST":
        list_id = request.POST.getlist('id[]')
        print(list_id)
        for i in list_id:
            pc = cl_Pc_software.objects.filter(id=i).first()
            pc.delete()
    return redirect('pcsoftware')
