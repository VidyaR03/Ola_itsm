from tool.forms import *
from django.shortcuts import render, redirect
from django.contrib import messages
from tool.models import *


def configuration(request):
    return render(request, 'tool/configurationmanagement.html')


def contact(request):
    return render(request, 'tool/contact.html')


def software(request):
    soft = cl_Software.objects.all()
    context = {
        'soft': soft,
    }
    return render(request, 'tool/software.html', context)


def softAdd(request):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        # ch_organization = cl_New_organization.objects.get(ch_name = request.POST.get('ch_organization'))
        # print('organization :',ch_organization)
        ch_vendor = request.POST.get('ch_vendor')
        chversion = request.POST.get('chversion')
        ch_type = request.POST.get('ch_type')
        soft = cl_Software(
            id=id,
            ch_name=ch_name,
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
        ch_name = request.POST.get('ch_name')
        ch_vendor = request.POST.get('ch_vendor')
        chversion = request.POST.get('chversion')
        ch_type = request.POST.get('ch_type')
        soft = cl_Software(
            id=id,
            ch_name=ch_name,
            ch_vendor=ch_vendor,
            chversion=chversion,
            ch_type=ch_type,
        )
        soft.save()
        return redirect('software')
    return redirect(request, 'tool/software.html')


def softDelete(request, id):
    soft = cl_Software.objects.filter(id=id)
    soft.delete()
    context = {
        'soft': soft,
    }
    return redirect('software')


def newci(request):
    return render(request, 'tool/newci.html')


def document(request):
    doc = cl_Document.objects.all()
    context = {
        'doc': doc,
    }
    return render(request, 'tool/document.html', context)


def DocAdd(request):
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
    return render(request, 'tool/document.html')


def DocEdit(request):
    doc = cl_Document.objects.all()
    context = {
        'doc': doc,
    }
    return render(request, 'tool/document.html', context)


def DocUpdate(request, id):
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
    return redirect(request, 'tool/document.html')


def DocDelete(request, id):
    doc = cl_Document.objects.filter(id=id)
    doc.delete()
    context = {
        'doc': doc,
    }
    return redirect('document')

# def software(request):
#     form=SoftwareForm()
#     if request.method=='POST':
#         form=SoftwareForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Data Add Successfully")
#     context={'form':form}
#     return render(request, 'tool/software.html',context)


def application_solution(request):
    appso = cl_Application_solution.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            appso = cl_Application_solution.objects.filter(
                ch_name__icontains=q)
    return render(request, 'tool/application_solution.html', {'appso': appso})


def appAdd(request):
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
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
    return render(request, 'tool/application_solution.html')


def appEdit(request):
    appso = cl_Application_solution.objects.all()
    context = {
        'appso': appso,
    }
    return render(request, 'tool/application_solution.html', context)


def appUpdate(request, id):
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
    return render(request, 'tool/application_solution.html')


def appDelete(request, id):
    appso = cl_Application_solution.objects.filter(id=id)
    appso.delete()
    context = {
        'appso': appso,
    }
    return redirect('application')


def delivery_model(request):
    form = DeliverymodelForm()
    if request.method == 'POST':
        form = DeliverymodelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Add Successfully")
    context = {'form': form}
    return render(request, 'tool/delivery_model.html', context)


def business_process(request):
    buss = cl_Business_process.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchbusinessname')
        if q != None:
            buss = cl_Business_process.objects.filter(
                ch_business_name__icontains=q)
    return render(request, 'tool/business_process.html', {'buss': buss})


def bussAdd(request):
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_business_name = request.POST.get('ch_business_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
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
        print(buss)
        buss.save()
        return redirect('businessprocess')
    return render(request, 'tool/business_process.html')


def bussEdit(request):
    buss = cl_Business_process.objects.all()
    context = {
        'buss': buss,
    }
    return render(request, 'tool/business_process.html', context)


def bussUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_business_name = request.POST.get('ch_business_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
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
    return render(request, 'tool/business_process.html')


def bussDelete(request, id):
    buss = cl_Business_process.objects.filter(id=id)
    buss.delete()
    context = {
        'buss': buss,
    }
    return redirect('businessprocess')


def newdb_server(request):
    db = cl_Newdb_server.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            db = cl_Newdb_server.objects.filter(
                ch_name__icontains=q)
    return render(request, 'tool/newdb_server.html', {'db': db})


def dbAdd(request):
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_dbname = request.POST.get('ch_dbname')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
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
    return render(request, 'tool/newdb_server.html')


def dbEdit(request):
    db = cl_Newdb_server.objects.all()
    context = {
        'db': db,
    }
    return render(request, 'tool/newdb_server.html', context)


def dbUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_dbname = request.POST.get('ch_dbname')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
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
    return render(request, 'tool/newdb_server.html')


def dbDelete(request, id):
    db = cl_Newdb_server.objects.filter(id=id)
    db.delete()
    context = {
        'db': db,
    }
    return redirect('newdb')


def dataschema(request):
    schema = cl_Database_schema.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            schema = cl_Database_schema.objects.filter(ch_name__icontains=q)
    return render(request, 'tool/database_schema.html', {'schema': schema})


def DSADD(request):
    if request.method == "POST":
        # id = request.POST.get('id')
        print(id)
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_db_server = request.POST.get('ch_db_server')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        txt_description = request.POST.get('txt_description')
        schema = cl_Database_schema(
            # id=id,
            ch_name=ch_name,
            ch_organization=ch_organization,
            ch_db_server=ch_db_server,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            txt_description=txt_description,
        )
        schema.save()
        print(schema)

        return redirect('databaseschema')

    return render(request, 'tool/database_schema.html')


def DSEdit(request):
    schema = cl_Database_schema.objects.all()
    context = {
        'schema': schema,
    }
    return render(request, 'tool/database_schema.html', context)


def DSUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_db_server = request.POST.get('ch_db_server')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        txt_description = request.POST.get('txt_description')
        schema = cl_Database_schema(
            id=id,
            ch_name=ch_name,
            ch_organization=ch_organization,
            ch_db_server=ch_db_server,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            txt_description=txt_description,
        )
        schema.save()
        return redirect('databaseschema')
    return render(request, 'tool/database_schema.html')


def DSDelete(request, id):
    schema = cl_Database_schema.objects.filter(id=id)
    schema.delete()
    context = {
        'schema': schema,
    }
    return redirect('databaseschema')


def middlewareinstance(request):
    mi = cl_Middleware_instance.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            mi = cl_Middleware_instance.objects.filter(ch_name__icontains=q)
    return render(request, 'tool/middleware_instance.html', {'mi': mi})


def MADD(request):
    if request.method == "POST":
        # id = request.POST.get('id')
        print(id)
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_middleware = request.POST.get('ch_middleware')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        txt_description = request.POST.get('txt_description')
        mi = cl_Middleware_instance(
            # id=id,
            ch_name=ch_name,
            ch_organization=ch_organization,
            ch_middleware=ch_middleware,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            txt_description=txt_description,
        )
        mi.save()
        print(mi)

        return redirect('middlewareinstance')

    return render(request, 'tool/middleware_instance.html')


def MEdit(request):
    mi = cl_Middleware_instance.objects.all()
    context = {
        'mi': mi,
    }
    return render(request, 'tool/middleware_instance.html', context)


def MUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = request.POST.get('ch_organization')
        ch_middleware = request.POST.get('ch_middleware')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        txt_description = request.POST.get('txt_description')
        mi = cl_Middleware_instance(
            id=id,
            ch_name=ch_name,
            ch_organization=ch_organization,
            ch_middleware=ch_middleware,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            txt_description=txt_description,
        )
        mi.save()
        return redirect('middlewareinstance')
    return render(request, 'tool/middleware_instance.html')


def MDelete(request, id):
    mi = cl_Middleware_instance.objects.filter(id=id)
    mi.delete()
    context = {
        'mi': mi,
    }
    return redirect('middlewareinstance')


# def new_middleware(request):
#     form=NewmiddldbewareForm()

#     if request.method=='POST':
#         form=NewmiddlewareForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Data Add Successfully")
#     context={'form':form}
#     return render(request, 'tool/new_middleware.html', context)

def new_middleware(request):
    middle = cl_New_middleware.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            middle = cl_New_middleware.objects.filter(
                ch_name__icontains=q)
    return render(request, 'tool/new_middleware.html', {'middle': middle})


def MWAdd(request):
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        ch_software = request.POST.get('ch_software')
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        middle = cl_New_middleware(
            # id=id,
            ch_name=ch_name,
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
    return render(request, 'tool/new_middleware.html')


def MWEdit(request):
    middle = cl_New_middleware.objects.all()
    context = {
        'middle': middle,
    }
    return render(request, 'tool/new_middleware.html', context)


def MWUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        ch_software = request.POST.get('ch_software')
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        middle = cl_New_middleware(
            id=id,
            ch_name=ch_name,
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
    return render(request, 'tool/new_middleware.html')


def MWDelete(request, id):
    middle = cl_New_middleware.objects.filter(id=id)
    middle.delete()
    context = {
        'middle': middle,
    }
    return redirect('newmiddleware')


def other_software(request):
    os = cl_Other_software.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            os = cl_Other_software.objects.filter(
                ch_name__icontains=q)
    return render(request, 'tool/othersoftware.html', {'os': os})


def osAdd(request):
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        ch_software = request.POST.get('ch_software')
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        os = cl_Other_software(
            # id=id,
            ch_name=ch_name,
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
    return render(request, 'tool/othersoftware.html')


def osEdit(request):
    os = cl_Other_software.objects.all()
    context = {
        'os': os,
    }
    return render(request, 'tool/othersoftware.html', context)


def osUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        ch_software = request.POST.get('ch_software')
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        os = cl_Other_software(
            id=id,
            ch_name=ch_name,
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
    return render(request, 'tool/othersoftware.html')


def osDelete(request, id):
    os = cl_Other_software.objects.filter(id=id)
    os.delete()
    context = {
        'os': os,
    }
    return redirect('other_software')

# def middleware_instance(request):
#     form=MiddlewareinstanceForm()
#     if request.method=='POST':
#         form=MiddlewareinstanceForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Data Add Successfully")
#     context={'form':form}
#     return render(request, 'tool/middleware_instance.html',context)


# def network_device(request):
#     form=NetworkForm()
#     if request.method=='POST':
#         form=NetworkForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Data Add Successfully")
#     context={'form':form}
#     return render(request, 'tool/network_device.html',context)


# def other_software(request):
#     form=OthersoftwareForm()
#     if request.method=='POST':
#         form=OthersoftwareForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Data Add Successfully")
#     context={'form':form}
#     return render(request, 'tool/othersoftware.html',context)

# def web_application(request):
#     form=WebapplicationForm()
#     if request.method=='POST':
#         form=WebapplicationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Data Add Successfully")
#     context={'form':form}
#     return render(request, 'tool/webapplication.html',context)


def web_application(request):
    wa = cl_Web_application.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            wa = cl_Web_application.objects.filter(
                ch_name__icontains=q)
    return render(request, 'tool/webapplication.html', {'wa': wa})


def waAdd(request):
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_webserver = cl_Web_server.objects.get(
            ch_name=request.POST.get('ch_webserver'))
        url_website = request.POST.get('url_website')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        txt_description = request.POST.get('txt_description')
        wa = cl_Web_application(
            # id=id,
            ch_name=ch_name,
            ch_organization=ch_organization,
            ch_webserver=ch_webserver,
            url_website=url_website,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            txt_description=txt_description,
        )
        wa.save()
        return redirect('webapplication')
    return render(request, 'tool/webapplication.html')


def wsEdit(request):
    wa = cl_Web_application.objects.all()
    context = {
        'wa': wa,
    }
    return render(request, 'tool/webapplication.html', context)


def waUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_webserver = cl_Web_server.objects.get(
            ch_name=request.POST.get('ch_webserver'))
        url_website = request.POST.get('url_website')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        txt_description = request.POST.get('txt_description')
        wa = cl_Web_application(
            id=id,
            ch_name=ch_name,
            ch_organization=ch_organization,
            ch_webserver=ch_webserver,
            url_website=url_website,
            ch_business_criticality=ch_business_criticality,
            dt_move_to_production_date=dt_move_to_production_date,
            txt_description=txt_description,
        )
        wa.save()
        return redirect('webapplication')
    return render(request, 'tool/webapplication.html')


def waDelete(request, id):
    wa = cl_Web_application.objects.filter(id=id)
    wa.delete()
    context = {
        'wa': wa,
    }
    return redirect('webapplication')


def networkdevice(request):
    nd = cl_Network_device.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            nd = cl_Network_device.objects.filter(
                ch_name__icontains=q)
    return render(request, 'tool/network_device.html', {'nd': nd})


def ndAdd(request):
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        ch_location = request.POST.get('ch_location')
        ch_network_type = cl_network_type.objects.get(
            ch_nname=request.POST.get('ch_network_type'))
        ch_brand = cl_Brand.objects.get(ch_brandname=request.POST.get('ch_brand'))
        ch_model = cl_model.objects.get(ch_modelname=request.POST.get('ch_model'))
        i_ios_version = cl_ios_version.objects.get(ch_iosname=request.POST.get('i_os_version'))
        i_management_ip = request.POST.get('i_management_ip')
        ch_ram = request.POST.get('ch_ram')
        i_rack_unit = request.POST.get('i_rack_unit')
        i_serial_number = request.POST.get('i_serial_number')
        i_asset_number = request.POST.get('i_asset_number')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        dt_purchase_date = request.POST.get('Purchase-date')
        dt_end_of_warranty = request.POST.get('Warrenty-end')
        txt_description = request.POST.get('txt_description')
        nd = cl_Network_device(
            # id=id,
            ch_name=ch_name,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            ch_location=ch_location,
            ch_network_type=ch_network_type,
            ch_brand=ch_brand,
            ch_model=ch_model,
            i_os_version=i_ios_version,
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
    return render(request, 'tool/network_device.html')


def ndEdit(request):
    nd = cl_Network_device.objects.all()
    context = {
        'nd': nd,
    }
    return render(request, 'tool/network_device.html', context)


def ndUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        ch_location = request.POST.get('ch_location')
        ch_network_type = cl_network_type.objects.get(
            ch_nname=request.POST.get('ch_network_type'))
        ch_brand = cl_Brand.objects.get(ch_brandname=request.POST.get('ch_brand'))
        ch_model = cl_model.objects.get(ch_modelname=request.POST.get('ch_model'))
        i_ios_version = cl_ios_version.objects.get(ch_iosname=request.POST.get('i_os_version'))
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
            ch_name=ch_name,
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
    return render(request, 'tool/network_device.html')


def ndDelete(request, id):
    nd = cl_Network_device.objects.filter(id=id)
    nd.delete()
    context = {
        'nd': nd,
    }
    return redirect('networkdevice')


def network_type(request):
    nt = cl_network_type.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            nt = cl_network_type.objects.filter(ch_nname__icontains=q)
    return render(request, 'tool/network_type.html', {'nt': nt})


def ntAdd(request):
    if request.method == "POST":
        id = request.POST.get('id')
        print(id)
        ch_nname = request.POST.get('ch_nname')
        nt = cl_network_type(
            id=id,
            ch_nname=ch_nname,
        )
        nt.save()
      
        return redirect('network_type')
    return render(request, 'tool/network_type.html')


def ntEdit(request):
    nt = cl_network_type.objects.all()
    context = {
        'nt': nt,
    }
    return render(request, 'tool/network_type.html', context)


def ntUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_nname = request.POST.get('ch_nname')

        nt = cl_network_type(
            id=id,
            ch_nname=ch_nname,

        )
        nt.save()
        return redirect('network_type')
    return render(request, 'tool/network_type.html')


def ntDelete(request, id):
    nt = cl_network_type.objects.filter(id=id)
    nt.delete()
    context = {
        'nt': nt,
    }
    return redirect('network_type')



def os_family(request):
    osf = cl_os_family.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchfname')
        if q != None:
            osf = cl_os_family.objects.filter(ch_fname__icontains=q)
    return render(request, 'tool/os_family.html', {'osf': osf})


def osfAdd(request):
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
    return render(request, 'tool/os_family.html')


def osfEdit(request):
    osf = cl_os_family.objects.all()
    context = {
        'osf': osf,
    }
    return render(request, 'tool/os_family.html', context)


def osfUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_fname = request.POST.get('ch_fname')

        osf = cl_os_family(
            id=id,
            ch_fname=ch_fname,

        )
        osf.save()
        return redirect('os_family')
    return render(request, 'tool/os_family.html')


def osfDelete(request, id):
    osf = cl_os_family.objects.filter(id=id)
    osf.delete()
    context = {
        'osf': osf,
    }
    return redirect('os_family')




def os_version(request):
    osv = cl_os_version.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchfname')
        if q != None:
            osf = cl_os_version.objects.filter(ch_fname__icontains=q)
    return render(request, 'tool/os_version.html', {'osv': osv})


def osvAdd(request):
    if request.method == "POST":
        id = request.POST.get('id')
        print(id)
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
    return render(request, 'tool/os_version.html')


def osvEdit(request):
    osv = cl_os_version.objects.all()
    context = {
        'osv': osv,
    }
    return render(request, 'tool/os_version.html', context)


def osvUpdate(request, id):
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
    return render(request, 'tool/os_version.html')


def osvDelete(request, id):
    osv = cl_os_version.objects.filter(id=id)
    osv.delete()
    context = {
        'osv': osv,
    }
    return redirect('os_version')


def os_license(request):
    ol = cl_os_license.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            ol = cl_os_license.objects.filter(
                ch_name__icontains=q)
    return render(request, 'tool/os_license.html', {'ol': ol})


def olAdd(request):
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_version = cl_os_version.objects.get(ch_iosname=request.POST.get('ch_version'))
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
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
    return render(request, 'tool/os_license.html')


def olEdit(request):
    ol = cl_os_license.objects.all()
    context = {
        'ol': ol,
    }
    return render(request, 'tool/os_license.html', context)


def olUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_version = cl_os_version.objects.get(ch_iosname=request.POST.get('ch_version'))
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
    return render(request, 'tool/os_license.html')



def olDelete(request, id):
    ol = cl_os_license.objects.filter(id=id)
    ol.delete()
    context = {
        'ol': ol,
    }
    return redirect('os_license')




def brand(request):
    brand = cl_Brand.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            brand = cl_Brand.objects.filter(ch_brandname__icontains=q)
    return render(request, 'tool/brand.html', {'brand': brand})


def bnAdd(request):
    if request.method == "POST":
        id = request.POST.get('id')
        print(id)
        ch_brandname = request.POST.get('ch_brandname')
        brand = cl_Brand(
            id=id,
            ch_brandname=ch_brandname,
        )
        brand.save()
        print(brand)
        return redirect('brand')

    return render(request, 'tool/brand.html')


def bnEdit(request):
    brand = cl_Brand.objects.all()
    context = {
        'brand': brand,
    }
    return render(request, 'tool/brand.html', context)


def bnUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_brandname = request.POST.get('ch_brandname')

        brand = cl_Brand(
            id=id,
            ch_brandname=ch_brandname,

        )
        brand.save()
        return redirect('brand')
    return render(request, 'tool/brand.html')


def bnDelete(request, id):
    brand = cl_Brand.objects.filter(id=id)
    brand.delete()
    context = {
        'brand': brand,
    }
    return redirect('brand')


def cmodel(request):
    model = cl_model.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            model = cl_model.objects.filter(ch_modelname__icontains=q)
    return render(request, 'tool/model.html', {'model': model})


def mdAdd(request):
    if request.method == "POST":
        id = request.POST.get('id')
        print(id)
        ch_modelname = request.POST.get('ch_modelname')
        ch_brandname = cl_Brand.objects.get(
            ch_brandname=request.POST.get('ch_brandname'))

        model = cl_model(
            id=id,
            ch_modelname=ch_modelname,
            ch_brandname=ch_brandname,

        )
        model.save()
        print(model)
        return redirect('cmodel')

    return render(request, 'tool/model.html')


def mdEdit(request):
    model = cl_model.objects.all()
    context = {
        'model': model,
    }
    return render(request, 'tool/model.html', context)


def mdUpdate(request, id):
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
    return render(request, 'tool/model.html')


def mdDelete(request, id):
    model = cl_model.objects.filter(id=id)
    model.delete()
    context = {
        'model': model,
    }
    return redirect('cmodel')


def iosver(request):
    iv = cl_ios_version.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            iv = cl_ios_version.objects.filter(ch_name__icontains=q)
    return render(request, 'tool/ios_version.html', {'iv': iv})


def ivAdd(request):
    if request.method == "POST":
        id = request.POST.get('id')
        print(id)
        ch_iosname = request.POST.get('ch_iosname')
        ch_brandname = cl_Brand.objects.get(
            ch_brandname=request.POST.get('ch_brandname'))

        iv = cl_ios_version(
            id=id,
            ch_iosname=ch_iosname,
            ch_brandname=ch_brandname,
        )
        iv.save()
        print(iv)
        return redirect('iosver')

    return render(request, 'tool/ios_version.html')


def ivEdit(request):
    iv = cl_ios_version.objects.all()
    context = {
        'iv': iv,
    }
    return render(request, 'tool/ios_version.html', context)


def ivUpdate(request, id):
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
    return render(request, 'tool/ios_version.html')


def ivDelete(request, id):
    iv = cl_ios_version.objects.filter(id=id)
    iv.delete()
    context = {
        'iv': iv,
    }
    return redirect('iosver')









############ Server ############

def server(request):
    se = cl_Server.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            se = cl_Server.objects.filter(
                ch_name__icontains=q)
    return render(request, 'tool/server.html', {'se': se})


def serverAdd(request):
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        ch_location = request.POST.get('ch_location')
        ch_os_family =  cl_os_family.objects.get(ch_fname=request.POST.get('ch_os_family'))

        ch_brand = cl_Brand.objects.get(ch_brandname=request.POST.get('ch_brand'))
        ch_model = cl_model.objects.get(ch_modelname=request.POST.get('ch_model'))
        i_os_version = cl_os_version.objects.get(ch_osname=request.POST.get('i_os_version'))

        i_management_ip = request.POST.get('i_management_ip')
        ch_ram = request.POST.get('ch_ram')
        ch_cpu = request.POST.get('ch_cpu')

        i_rack_unit = request.POST.get('i_rack_unit')
        i_serial_number = request.POST.get('i_serial_number')
        i_asset_number = request.POST.get('i_asset_number')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        dt_purchase_date = request.POST.get('Purchase-date')
        dt_end_of_warranty = request.POST.get('Warrenty-end')
        txt_description = request.POST.get('txt_description')
        se = cl_Server(
            # id=id,
            ch_name=ch_name,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            ch_location=ch_location,
            ch_os_family=ch_os_family,
            ch_brand=ch_brand,
            ch_model=ch_model,
            i_os_version=i_os_version,
            i_management_ip=i_management_ip,
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
    return render(request, 'tool/server.html')


def serverEdit(request):
    se = cl_Server.objects.all()
    context = {
        'se': se,
    }
    return render(request, 'tool/server.html', context)


def serverUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        ch_location = request.POST.get('ch_location')
        ch_os_family =  cl_os_family.objects.get(ch_fname=request.POST.get('ch_os_family'))

        ch_brand = cl_Brand.objects.get(ch_brandname=request.POST.get('ch_brand'))
        ch_model = cl_model.objects.get(ch_modelname=request.POST.get('ch_model'))
        i_os_version = cl_os_version.objects.get(ch_osname=request.POST.get('i_os_version'))

        i_management_ip = request.POST.get('i_management_ip')
        ch_ram = request.POST.get('ch_ram')
        ch_cpu = request.POST.get('ch_cpu')

        i_rack_unit = request.POST.get('i_rack_unit')
        i_serial_number = request.POST.get('i_serial_number')
        i_asset_number = request.POST.get('i_asset_number')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        dt_purchase_date = request.POST.get('Purchase-date')
        dt_end_of_warranty = request.POST.get('Warrenty-end')
        txt_description = request.POST.get('txt_description')
        se = cl_Server(
             id=id,
            ch_name=ch_name,
            ch_organization=ch_organization,
            ch_status=ch_status,
            ch_business_criticality=ch_business_criticality,
            ch_location=ch_location,
            ch_os_family=ch_os_family,
            ch_brand=ch_brand,
            ch_model=ch_model,
            i_os_version=i_os_version,
            i_management_ip=i_management_ip,
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
    return render(request, 'tool/server.html')


def serverDelete(request, id):
    se = cl_Server.objects.filter(id=id)
    se.delete()
    context = {
        'se': se,
    }
    return redirect('server')



# def web_server(request):
#     form=WebserverForm()
#     if request.method=='POST':
#         form=WebserverForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Data Add Successfully")
#     context={'form':form}
#     return render(request, 'tool/webserver.html',context)


def web_server(request):
    ws = cl_Web_server.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            ws = cl_Web_server.objects.filter(
                ch_name__icontains=q)
    return render(request, 'tool/webserver.html', {'ws': ws})


def wsAdd(request):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        ch_software = request.POST.get('ch_software')
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        ws = cl_Web_server(
            id=id,
            ch_name=ch_name,
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
    return render(request, 'tool/webserver.html')


def wsEdit(request):
    ws = cl_Web_server.objects.all()
    context = {
        'ws': ws,
    }
    return render(request, 'tool/webserver.html', context)


def wsUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        ch_software = request.POST.get('ch_software')
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        ws = cl_Web_server(
            id=id,
            ch_name=ch_name,
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
    return render(request, 'tool/webserver.html')


def wsDelete(request, id):
    ws = cl_Web_server.objects.filter(id=id)
    ws.delete()
    context = {
        'ws': ws,
    }
    return redirect('webserver')

# def network_device(request):
#     form=NetworkdeviceForm()
#     if request.method=='POST':
#         form=NetworkdeviceForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Data Add Successfully")
#     context={'form':form}
#     return render(request, 'tool/network_device.html',context)




# def server(request):
#     form = ServerForm()
#     if request.method == 'POST':
#         form = ServerForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Data Add Successfully")
#     context = {'form': form}
#     return render(request, 'tool/server.html', context)


# def pc_software(request):
#     form=PcsoftwareForm()
#     if request.method=='POST':
#         form=PcsoftwareForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Data Add Successfully")
#     context={'form':form}
#     return render(request, 'tool/pc_software.html',context)
def pc_software(request):
    pc = cl_Pc_software.objects.all()
    if request.method == "GET":
        q = request.GET.get('searchname')
        if q != None:
            pc = cl_Pc_software.objects.filter(
                ch_name__icontains=q)
    return render(request, 'tool/pc_software.html', {'pc': pc})


def pcAdd(request):
    if request.method == "POST":
        # id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        ch_software = request.POST.get('ch_software')
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        pc = cl_Pc_software(
            # id=id,
            ch_name=ch_name,
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
    return render(request, 'tool/pc_software.html')


def pcEdit(request):
    pc = cl_Pc_software.objects.all()
    context = {
        'pc': pc,
    }
    return render(request, 'tool/pc_software.html', context)


def pcUpdate(request, id):
    if request.method == "POST":
        id = request.POST.get('id')
        ch_name = request.POST.get('ch_name')
        ch_organization = cl_New_organization.objects.get(
            ch_name=str.capitalize(request.POST.get('ch_organization')))
        ch_status = request.POST.get('ch_status')
        ch_business_criticality = request.POST.get('ch_business_criticality')
        dt_move_to_production_date = request.POST.get(
            'dt_move_to_production_date')
        ch_software = request.POST.get('ch_software')
        ch_software_license = request.POST.get('ch_software_license')
        ch_system = request.POST.get('ch_system')
        ch_path = request.POST.get('ch_path')
        txt_description = request.POST.get('txt_description')
        pc = cl_Pc_software(
            id=id,
            ch_name=ch_name,
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
    return render(request, 'tool/pc_software.html')


def pcDelete(request, id):
    pc = cl_Pc_software.objects.filter(id=id)
    pc.delete()
    context = {
        'pc': pc,
    }
    return redirect('pcsoftware')
