from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .managers import CustomUserManager


from .views import send_telegram_message


urlpatterns = [
    path('', views.dashboard, name='home'),
    path("register/", views.registerPage, name='register'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path('login', views.adminloginPage, name='login'),
    path('login_render/', views.login_render, name='login_render'),
    path('logout/', views.logoutUser, name='logout'),
    path('logs/', views.view_logs, name='logs'),
    path('delete/', views.LogsDelete, name='logsdelete'),


    path('send-telegram-message/', send_telegram_message, name='send_telegram_message'),

    
    #Url for person form
    path('add', views.ADD, name='add'),
    # path('edit', views.Edit, name='edit'),
    path('update/<str:id>', views.Update, name='update'),
    path('delete_person/', views.Delete, name='delete_person'),
    path("client/", views.client,name='client'),

    #Url For New Change
    path("newchange/", views.newchange, name='newchange'),
    path('cadd', views.CADD, name='cadd'),
    # path('cedit', views.CEdit, name='cedit'),
    path('cupdate/<str:id>', views.CUpdate, name='cupdate'),
    path('cdelete', views.CDelete, name='cdelete'),
    path('assign_change', views.assign_changeModal, name='assign_change'),
    path("get_people_by_team", views.get_people_by_team, name="get_people_by_team"),
    path("get_service_sub_by_service", views.get_service_sub_by_service, name="get_service_sub_by_service"),


    #Url For Team form
    path('tadd', views.TADD, name='tadd'),
    # path('tedit', views.TEdit, name='tedit'),
    path('tupdate/<str:id>', views.TUpdate, name='tupdate'),
    path('tdelete/', views.TDelete, name='tdelete'),
    path("team/", views.team, name='team'),
    path("configurationmanagement/", views.configuration, name='configurationmanagement'),
    path("configurationmanagement_copy/", views.configurationmanagement_copy, name='configurationmanagement_copy'),

    path("contact/", views.contact, name='contact'),
    path("newci/", views.newci, name='newci'),

    #Url for Loction form
    path("location/", views.Location,name='location'),
    path('ladd', views.LADD, name='ladd'),
    # path('ledit', views.LEdit, name='ledit'),
    path('lupdate/<str:id>', views.LUpdate, name='lupdate'),
    path('ldelete/', views.LDelete, name='ldelete'),
          
    #Url for Organization
    path("new_organization/", views.new_organization,name='new_organization'),
    path('OrgADD', views.OrgADD, name='OrgADD'),
    path('OrgEdit', views.OrgEdit, name='OrgEdit'),
    path('OrgUpdate/<str:id>', views.OrgUpdate, name='OrgUpdate'),
    path('OrgDelete/', views.OrgDelete, name='OrgDelete'),
          
    
    #url for document
    path("document/", views.document, name='document'),
    path('DocAdd', views.DocAdd, name='DocAdd'),
    path('DocEdit', views.DocEdit, name='DocEdit'),
    path('DocUpdate/<str:id>', views.DocUpdate, name='DocUpdate'),
    path('DocDelete/', views.DocDelete, name='DocDelete'),
    path('DeleteAttachedPDF', views.DeleteAttachedPDF, name="DeleteAttachedPDF"),
    path('show_attched_pdf/<str:path>', views.ViewAttachedPDF.as_view(), name="show_attched_pdf"),


    # Url Software
    path("software/", views.software, name='software'),
    path('softAdd', views.softAdd, name='softAdd'),
    path('softEdit', views.softEdit, name='softEdit'),
    path('softUpdate/<str:id>', views.softUpdate, name='softUpdate'),
    path('softDelete/', views.softDelete, name='softDelete'),
    
    #Url for Business Process
    path("businessprocess/", views.business_process, name='businessprocess'),
    path('bussAdd', views.bussAdd, name='bussAdd'),
    path('bussEdit', views.bussEdit, name='bussEdit'),
    path('bussUpdate/<str:id>', views.bussUpdate, name='bussUpdate'),
    path('bussDelete/', views.bussDelete, name='bussDelete'),


    #Url FOr Aplication Solution
    path("application/", views.application_solution, name='application'),
    path('appAdd', views.appAdd, name='appAdd'),
    path('appEdit', views.appEdit, name='appEdit'),
    path('appUpdate/<str:id>', views.appUpdate, name='appUpdate'),
    path('appDelete/', views.appDelete, name='appDelete'),

  
    #Url for New DB
    path("newdb/", views.newdb_server, name='newdb'),
    path('dbAdd', views.dbAdd, name='dbAdd'),
    path('dbEdit', views.dbEdit, name='dbEdit'),
    path('dbUpdate/<str:id>', views.dbUpdate, name='dbUpdate'),
    path('dbDelete/', views.dbDelete, name='dbDelete'),
    
  
  #Url for DB Schema   
    path("databaseschema/", views.dataschema, name='databaseschema'),
    path('DSADD', views.DSADD, name='DSADD'),
    path('DSEdit', views.DSEdit, name='DSEdit'),
    path('DSUpdate/<str:id>', views.DSUpdate, name='DSUpdate'),
    path('DSDelete/', views.DSDelete, name='DSDelete'),
    
  
  
    #Url for Pc SOftware  
    path("pcsoftware/", views.pc_software, name='pcsoftware'),
    path('pcAdd', views.pcAdd, name='pcAdd'),
    path('pcEdit', views.pcEdit, name='pcEdit'),
    path('pcUpdate/<str:id>', views.pcUpdate, name='pcUpdate'),
    path('pcDelete/', views.pcDelete, name='pcDelete'),
    
    
    # URL for Incident Management
    path("userrequest/", views.user_request, name='userrequest'),
    path('uadd', views.UADD, name='uadd'),
    path('uedit', views.UEdit, name='uedit'),
    path('uupdate/<str:id>', views.UUpdate, name='uupdate'),
    path('udelete/', views.UDelete, name='udelete'),
    path('escalate_notify', views.escalate_notify, name='escalate_notify'),
    path('sendMailUR', views.send_approval_Mail_UR, name='sendMailUR'),
    path('assign_UR', views.assign_URModal, name='assign_UR'),



    
    #URL For new middleware
    path("newmiddleware/", views.new_middleware, name='newmiddleware'),
    path('MWAdd', views.MWAdd, name='MWAdd'),
    path('MWEdit', views.MWEdit, name='MWEdit'),
    path('MWUpdate/<str:id>', views.MWUpdate, name='MWUpdate'),
    path('MWDelete/', views.MWDelete, name='MWDelete'),
    
    #Url for Middleware Instance
    path("middlewareinstance/", views.middlewareinstance, name='middlewareinstance'),
    path('MADD', views.MADD, name='MADD'),
    path('MEdit', views.MEdit, name='MEdit'),
    path('MUpdate/<str:id>', views.MUpdate, name='MUpdate'),
    path('MDelete/', views.MDelete, name='MDelete'),
    
    #URL for Network Type
    path("network_type/", views.network_type,name='network_type'),
    path('ntAdd', views.ntAdd, name='ntAdd'),
    path('ntEdit', views.ntEdit, name='ntEdit'),
    path('ntUpdate/<str:id>', views.ntUpdate, name='ntUpdate'),
    path('ntDelete/', views.ntDelete, name='ntDelete'),

    #URL for OS Family
    path("os_family/", views.os_family,name='os_family'),
    path('osfAdd', views.osfAdd, name='osfAdd'),
    path('osfEdit', views.osfEdit, name='osfEdit'),
    path('osfUpdate/<str:id>', views.osfUpdate, name='osfUpdate'),
    path('osfDelete/', views.osfDelete, name='osfDelete'),


    #URL for Brand Type
    path("brand/", views.brand,name='brand'),
    path('bnAdd', views.bnAdd, name='bnAdd'),
    path('bnEdit', views.bnEdit, name='bnEdit'),
    path('bnUpdate/<str:id>', views.bnUpdate, name='bnUpdate'),
    path('bnDelete/', views.bnDelete, name='bnDelete'),

    

    
      #URL for Model Type
    path("cmodel/", views.cmodel,name='cmodel'),
    path('mdAdd', views.mdAdd, name='mdAdd'),
    path('mdEdit', views.mdEdit, name='mdEdit'),
    path('mdUpdate/<str:id>', views.mdUpdate, name='mdUpdate'),
    path('mdDelete/', views.mdDelete, name='mdDelete'),


  #Url Path for IOS Version
    path("iosver/", views.iosver,name='iosver'),
    path('ivAdd', views.ivAdd, name='ivAdd'),
    path('ivEdit', views.ivEdit, name='ivEdit'),
    path('ivUpdate/<str:id>', views.ivUpdate, name='ivUpdate'),
    path('ivDelete/', views.ivDelete, name='ivDelete'),


  # URL for OS version
    path("os_version/", views.os_version,name='os_version'),
    path('osvAdd', views.osvAdd, name='osvAdd'),
    path('osvEdit', views.osvEdit, name='osvEdit'),
    path('osvUpdate/<str:id>', views.osvUpdate, name='osvUpdate'),
    path('osvDelete/', views.osvDelete, name='osvDelete'),
    path('sendMail', views.send_approval_Mail, name='sendMail'),



    #URL For Network Device
    path("networkdevice/", views.networkdevice,name='networkdevice'),
    path('ndAdd', views.ndAdd, name='ndAdd'),
    path('ndEdit', views.ndEdit, name='ndEdit'),
    path('ndUpdate/<str:id>', views.ndUpdate, name='ndUpdate'),
    path('ndDelete/', views.ndDelete, name='ndDelete'),

    #URL For Server
    path("server/", views.server,name='server'),
    path('serverAdd', views.serverAdd, name='serverAdd'),
    path('serverEdit', views.serverEdit, name='serverEdit'),
    path('serverUpdate/<str:id>', views.serverUpdate, name='serverUpdate'),
    path('serverDelete/', views.serverDelete, name='serverDelete'),


    #Url for Web Application
    path("webapplication/", views.web_application, name='webapplication'),
    path('waAdd', views.waAdd, name='waAdd'),
    path('wsEdit', views.wsEdit, name='waEdit'),
    path('waUpdate/<str:id>', views.waUpdate, name='waUpdate'),
    path('waDelete/', views.waDelete, name='waDelete'),



    #Url Path For Web Server
    path("webserver/", views.web_server, name='webserver'),
    path('wsAdd', views.wsAdd, name='wsAdd'),
    path('wsEdit', views.wsEdit, name='wsEdit'),
    path('wsUpdate/<str:id>', views.wsUpdate, name='wsUpdate'),
    path('wsDelete/', views.wsDelete, name='wsDelete'),



    #Url for customer contract

    path("customercontract/", views.customer_contract, name='customercontract'),
    path('scadd', views.SCADD, name='scadd'),
    path('scedit', views.SCEdit, name='scedit'),
    path('scupdate/<str:id>', views.SCUpdate, name='scupdate'),
    path('scdelete', views.SCDelete, name='scdelete'),
    
    #Url for provider contract

    path("providercontract/", views.provider_contract, name='providercontract'),
    path('spadd', views.SPADD, name='spadd'),
    path('spedit', views.SPEdit, name='spedit'),
    path('spupdate/<str:id>', views.SPUpdate, name='spupdate'),
    path('spdelete', views.SPDelete, name='spdelete'),

     #URL for System
     path("systemnav/", views.systemnav, name='systemnav'),


    #Url for services
    path("servicenav/", views.servicenav, name='servicenav'),
    # path("customercontract/", views.customer_contract, name='customercontract'),
    # path("providercontract/", views.provider_contract,name='providercontract'),


    #Url for services Family
    path("servicefamilies/", views.servicefamilies,name='servicefamilies'),
    path('sfadd', views.SFADD, name='sfadd'),
    path('sfedit', views.SFEdit, name='sfedit'),
    path('sfupdate/<str:id>', views.SFUpdate, name='sfupdate'),
    path('sfdelete', views.SFDelete, name='sfdelete'),


     #Url for services 

    path("sservice/", views.sservice, name='service'),
    path('ssadd', views.SSADD, name='ssadd'),
    path('ssedit', views.SSEdit, name='ssedit'),
    path('ssupdate/<str:id>', views.SSUpdate, name='ssupdate'),
    path('ssdelete', views.SSDelete, name='ssdelete'),



     #url for service subcategory
    path("service_subcategory/", views.service_subcategory, name='service_subcategory'),
    path('sadd', views.SADD, name='sadd'),
    path('sedit', views.SEdit, name='sedit'),
    path('supdate/<str:id>', views.SUpdate, name='supdate'),
    path('sdelete', views.SDelete, name='sdelete'),


    
     #url for Other Software
    path("other_software/", views.other_software, name='other_software'),
    path('osAdd', views.osAdd, name='osAdd'),
    path('osEdit', views.osEdit, name='osEdit'),
    path('osUpdate/<str:id>', views.osUpdate, name='osUpdate'),
    path('osDelete/', views.osDelete, name='osDelete'),


    #url for sla
    path("sla/", views.sla, name='sla'),
    path('sladd', views.SLADD, name='sladd'),
    path('sledit', views.SLEdit, name='sledit'),
    path('slupdate/<str:id>', views.SLUpdate, name='slupdate'),
    path('sldelete', views.SLDelete, name='sldelete'),
    path('get_slt_by_sla', views.get_slt_by_sla, name='get_slt_by_sla'),

    
    #url for sdelivery
    path("servicedelivery/", views.servicedelivery,name='servicedelivery'),
    path('sdadd', views.SDADD, name='sdadd'),
    path('sdedit', views.SDEdit, name='sdedit'),
    path('sdupdate/<str:id>', views.SDUpdate, name='sdupdate'),
    path('sddelete', views.SDDelete, name='sddelete'),


        #url for OS License
    path("os_license/", views.os_license,name='os_license'),
    path('olAdd', views.olAdd, name='olAdd'),
    path('olEdit', views.olEdit, name='olEdit'),
    path('olUpdate/<str:id>', views.olUpdate, name='olUpdate'),
    path('olDelete/', views.olDelete, name='olDelete'),




     #url for slt
    path("slt/", views.SLT,name='slt'),
    path('sltadd', views.STADD, name='sltadd'),
    # path('sltedit', views.SLTEdit, name='sltedit'),
    path('sltupdate/<str:id>', views.SLTUpdate, name='sltupdate'),
    path('sltdelete', views.SLTDelete, name='sltdelete'),


    # for user role 
    path("role_display", views.role_display, name='role_display'),
    path("role_add", views.role_add, name='role_add'),
    path("role_edit/<str:id>", views.role_edit, name='role_edit'),


    # for user  
    path("user_display", views.user_display, name='user_display'),
    path("add_new_user", views.add_new_user, name='add_new_user'),
    path("user_edit/<str:id>", views.user_edit, name='user_edit'),


    #url for system configuration
    path("synchro_data_source/", views.synchro_data_source,name='synchro_data_source'),
    path("sysconfinav/", views.sysconfienav,name='sysconfinav'),
    path("authmazure/", views.oauth_mazuree,name='authmazure'),
    path("sysconfiauth/", views.sysconfiauth,name='sysconfiauth'),

    #url for administration
    path("admuser/", views.admuser,name='admuser'),
    path("itsmuser/", views.itsmuser,name='itsmuser'),
    path("idapuser/", views.ldapuser,name='idapuser'),

    #url for Email Notification
    path("email_display", views.email_display,name='email_display'),
    path("add_new_email/", views.add_new_email,name='add_new_email'),
    path("email_edit/<str:id>", views.email_edit,name='email_edit'),


    #url for SMS Notification
    path("sms_display", views.sms_display,name='sms_display'),
    path("add_new_sms/", views.add_new_sms,name='add_new_sms'),
    path("sms_edit/<str:id>", views.sms_edit,name='sms_edit'),
    path('smsdelete', views.smsdelete, name='smsdelete'),



    #URL for External User
    path("externaluser/", views.externaluser,name='externaluser'),
    path('extadd', views.extADD, name='extadd'),
    path('extedit', views.extEdit, name='extedit'),
    path('extupdate/<str:id>', views.extUpdate, name='extupdate'),
    path('extdelete/', views.extDelete, name='extdelete'),
    #Assign
    # path("tassign/", views.assignform, name='assign'),
   
    ##### url for LDAP user 
    path("ldapuser/", views.ldapuser,name='ldapuser'),
    path('ldapadd', views.ldapADD, name='ldapadd'),
    path('ldapedit', views.ldapEdit, name='ldapedit'),
    path('ldapupdate/<str:id>', views.ldapUpdate, name='ldapupdate'),
    path('ldapdelete/', views.ldapDelete, name='ldapdelete'),
   

    ##### url for ITSM user 
    path("itsmuser/", views.itsmuser,name='itsmuser'),
    path('itsmadd', views.itsmADD, name='itsmadd'),
    path('itsmedit', views.itsmEdit, name='itsmedit'),
    path('itsmupdate/<str:id>', views.itsmUpdate, name='itsmupdate'),
    path('itsmdelete/', views.itsmDelete, name='itsmdelete'),

        


    #url for integration
    path("integration/", views.integrationav,name='integration'),
    path("slacknoti/", views.slacknoti,name='slacknoti'),
    path("micronoti/", views.micronoti,name='micronoti'),
    path("webhook/", views.webhook,name='webhook'),
    path("googlechat/", views.googlechat,name='googlechat'),
    path("rocketchat/", views.rocketchat,name='rocketchat'),
    path("itsmwebhook/", views.itsmwebhook,name='itsmwebhook'),



    path("systemsynchro/", views.systemsynchro,name='systemsynchro'),
    path('synadd', views.synadd, name='synadd'),
    path('synedit', views.synedit, name='synedit'),
    path('synupdate/<str:id>', views.synupdate, name='synupdate'),
    path('syndelete', views.syndelete, name='syndelete'),



    path("authgoogle/", views.authgoogle,name='authgoogle'),
    path('oauthadd', views.oauthadd, name='oauthadd'),
    path('oauthedit', views.oauthedit, name='oauthedit'),
    path('oauthupdate/<str:id>', views.oauthupdate, name='oauthupdate'),
    path('oauthdelete', views.oauthdelete, name='oauthdelete'),
    
   
    ]+ static(settings.MEDIA_URL, documents_root=settings.MEDIA_ROOT)