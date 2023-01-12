from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path("register/", views.registerPage, name='register'),
    path('login', views.loginPage, name='login'),
    path('login_render/', views.login_render, name='login_render'),
    path('logout/', views.logoutUser, name='logout'),
    
    #Url for person form
    path('add', views.ADD, name='add'),
    path('edit', views.Edit, name='edit'),
    path('update/<str:id>', views.Update, name='update'),
    path('delete/<str:id>', views.Delete, name='delete'),
    path("client/", views.client,name='client'),

    #Url For New Change
    path("newchange/", views.newchange, name='newchange'),
    path('cadd', views.CADD, name='cadd'),
    path('cedit', views.CEdit, name='cedit'),
    path('cupdate/<str:id>', views.CUpdate, name='cupdate'),
    path('cdelete', views.CDelete, name='cdelete'),
    path('assign_change', views.assign_changeModal, name='assign_change'),

    #Url For Team form
    path('tadd', views.TADD, name='tadd'),
    path('tedit', views.TEdit, name='tedit'),
    path('tupdate/<str:id>', views.TUpdate, name='tupdate'),
    path('tdelete/<str:id>', views.TDelete, name='tdelete'),
    path("team/", views.team, name='team'),
    path("configurationmanagement/", views.configuration, name='configurationmanagement'),
    path("contact/", views.contact, name='contact'),
    path("newci/", views.newci, name='newci'),
   
     
    #Url for Loction form
    path("location/", views.Location,name='location'),
    path('ladd', views.LADD, name='ladd'),
    path('ledit', views.LEdit, name='ledit'),
    path('lupdate/<str:id>', views.LUpdate, name='lupdate'),
    path('ldelete/<str:id>', views.LDelete, name='ldelete'),
          
     #Url for Organization
    path("new_organization/", views.new_organization,name='new_organization'),
    path('OrgADD', views.OrgADD, name='OrgADD'),
    path('OrgEdit', views.OrgEdit, name='OrgEdit'),
    path('OrgUpdate/<str:id>', views.OrgUpdate, name='OrgUpdate'),
    path('OrgDelete/<str:id>', views.OrgDelete, name='OrgDelete'),
          
    
     #url for document
    path("document/", views.document, name='document'),
    path('DocAdd', views.DocAdd, name='DocAdd'),
    path('DocEdit', views.DocEdit, name='DocEdit'),
    path('DocUpdate/<str:id>', views.DocUpdate, name='DocUpdate'),
    path('DocDelete/<str:id>', views.DocDelete, name='DocDelete'),

     # Url Software
    path("software/", views.software, name='software'),
    path('softAdd', views.softAdd, name='softAdd'),
    path('softEdit', views.softEdit, name='softEdit'),
    path('softUpdate/<str:id>', views.softUpdate, name='softUpdate'),
    path('softDelete/<str:id>', views.softDelete, name='softDelete'),
    
    #Url for Business Process
    path("businessprocess/", views.business_process, name='businessprocess'),
    path('bussAdd', views.bussAdd, name='bussAdd'),
    path('bussEdit', views.bussEdit, name='bussEdit'),
    path('bussUpdate/<str:id>', views.bussUpdate, name='bussUpdate'),
    path('bussDelete/<str:id>', views.bussDelete, name='bussDelete'),


    #Url FOr Aplication Solution
    path("application/", views.application_solution, name='application'),
    path('appAdd', views.appAdd, name='appAdd'),
    path('appEdit', views.appEdit, name='appEdit'),
    path('appUpdate/<str:id>', views.appUpdate, name='appUpdate'),
    path('appDelete/<str:id>', views.appDelete, name='appDelete'),

   
    #Url for New DB
    path("newdb/", views.newdb_server, name='newdb'),
    path('dbAdd', views.dbAdd, name='dbAdd'),
    path('dbEdit', views.dbEdit, name='dbEdit'),
    path('dbUpdate/<str:id>', views.dbUpdate, name='dbUpdate'),
    path('dbDelete/<str:id>', views.dbDelete, name='dbDelete'),
    
   

    
    path("deliverymodel/", views.delivery_model,name='deliverymodel'),
   
   #Url for DB Schema   
    path("databaseschema/", views.dataschema, name='databaseschema'),
    path('DSADD', views.DSADD, name='DSADD'),
    path('DSEdit', views.DSEdit, name='DSEdit'),
    path('DSUpdate/<str:id>', views.DSUpdate, name='DSUpdate'),
    path('DSDelete/<str:id>', views.DSDelete, name='DSDelete'),
    
   
   
   
    #Url for Pc SOftware  
    path("pcsoftware/", views.pc_software, name='pcsoftware'),
    path('pcAdd', views.pcAdd, name='pcAdd'),
    path('pcEdit', views.pcEdit, name='pcEdit'),
    path('pcUpdate/<str:id>', views.pcUpdate, name='pcUpdate'),
    path('pcDelete/<str:id>', views.pcDelete, name='pcDelete'),
    



    
    # URL for Incident Management
    path("userrequest/", views.user_request, name='userrequest'),
    path('uadd', views.UADD, name='uadd'),
    path('uedit', views.UEdit, name='uedit'),
    path('uupdate/<str:id>', views.UUpdate, name='uupdate'),
    path('udelete/<str:id>', views.UDelete, name='udelete'),
    path('assign_userModal', views.assign_userModal, name='assign_userModal'),

    
    #URL For new middleware
    path("newmiddleware/", views.new_middleware, name='newmiddleware'),
    path('MWAdd', views.MWAdd, name='MWAdd'),
    path('MWEdit', views.MWEdit, name='MWEdit'),
    path('MWUpdate/<str:id>', views.MWUpdate, name='MWUpdate'),
    path('MWDelete/<str:id>', views.MWDelete, name='MWDelete'),
    
    #Url for Middleware Instance
    path("middlewareinstance/", views.middlewareinstance, name='middlewareinstance'),
    path('MADD', views.MADD, name='MADD'),
    path('MEdit', views.MEdit, name='MEdit'),
    path('MUpdate/<str:id>', views.MUpdate, name='MUpdate'),
    path('MDelete/<str:id>', views.MDelete, name='MDelete'),
     
     #URL for Network Type
    path("network_type/", views.network_type,name='network_type'),
    path('ntAdd', views.ntAdd, name='ntAdd'),
    path('ntEdit', views.ntEdit, name='ntEdit'),
    path('ntUpdate/<str:id>', views.ntUpdate, name='ntUpdate'),
    path('ntDelete/<str:id>', views.ntDelete, name='ntDelete'),

     #URL for OS Family
    path("os_family/", views.os_family,name='os_family'),
    path('osfAdd', views.osfAdd, name='osfAdd'),
    path('osfEdit', views.osfEdit, name='osfEdit'),
    path('osfUpdate/<str:id>', views.osfUpdate, name='osfUpdate'),
    path('osfDelete/<str:id>', views.osfDelete, name='osfDelete'),


     #URL for Brand Type
    path("brand/", views.brand,name='brand'),
    path('bnAdd', views.bnAdd, name='bnAdd'),
    path('bnEdit', views.bnEdit, name='bnEdit'),
    path('bnUpdate/<str:id>', views.bnUpdate, name='bnUpdate'),
    path('bnDelete/<str:id>', views.bnDelete, name='bnDelete'),

    
      #URL for Model Type
    path("cmodel/", views.cmodel,name='cmodel'),
    path('mdAdd', views.mdAdd, name='mdAdd'),
    path('mdEdit', views.mdEdit, name='mdEdit'),
    path('mdUpdate/<str:id>', views.mdUpdate, name='mdUpdate'),
    path('mdDelete/<str:id>', views.mdDelete, name='mdDelete'),


  #Url Path for IOS Version

    path("iosver/", views.iosver,name='iosver'),
    path('ivAdd', views.ivAdd, name='ivAdd'),
    path('ivEdit', views.ivEdit, name='ivEdit'),
    path('ivUpdate/<str:id>', views.ivUpdate, name='ivUpdate'),
    path('ivDelete/<str:id>', views.ivDelete, name='ivDelete'),


  # URL for OS version
    path("os_version/", views.os_version,name='os_version'),
    path('osvAdd', views.osvAdd, name='osvAdd'),
    path('osvEdit', views.osvEdit, name='osvEdit'),
    path('osvUpdate/<str:id>', views.osvUpdate, name='osvUpdate'),
    path('osvDelete/<str:id>', views.osvDelete, name='osvDelete'),
    
   
    #URL For Network Device
    path("networkdevice/", views.networkdevice,name='networkdevice'),
    path('ndAdd', views.ndAdd, name='ndAdd'),
    path('ndEdit', views.ndEdit, name='ndEdit'),
    path('ndUpdate/<str:id>', views.ndUpdate, name='ndUpdate'),
    path('ndDelete/<str:id>', views.ndDelete, name='ndDelete'),

    #URL For Server
    path("server/", views.server,name='server'),
    path('serverAdd', views.serverAdd, name='serverAdd'),
    path('serverEdit', views.serverEdit, name='serverEdit'),
    path('serverUpdate/<str:id>', views.serverUpdate, name='serverUpdate'),
    path('serverDelete/<str:id>', views.serverDelete, name='serverDelete'),




    #Url for Web Application
    path("webapplication/", views.web_application, name='webapplication'),
    path('waAdd', views.waAdd, name='waAdd'),
    path('wsEdit', views.wsEdit, name='waEdit'),
    path('waUpdate/<str:id>', views.waUpdate, name='waUpdate'),
    path('waDelete/<str:id>', views.waDelete, name='waDelete'),



    #Url Path For Web Server
    path("webserver/", views.web_server, name='webserver'),
    path('wsAdd', views.wsAdd, name='wsAdd'),
    path('wsEdit', views.wsEdit, name='wsEdit'),
    path('wsUpdate/<str:id>', views.wsUpdate, name='wsUpdate'),
    path('wsDelete/<str:id>', views.wsDelete, name='wsDelete'),



    #Url for customer contract

    path("customercontract/", views.customer_contract, name='customercontract'),
    path('scadd', views.SCADD, name='scadd'),
    path('scedit', views.SCEdit, name='scedit'),
    path('scupdate/<str:id>', views.SCUpdate, name='scupdate'),
    path('scdelete/<str:id>', views.SCDelete, name='scdelete'),
    
     #Url for provider contract

    path("providercontract/", views.provider_contract, name='providercontract'),
    path('spadd', views.SPADD, name='spadd'),
    path('spedit', views.SPEdit, name='spedit'),
    path('spupdate/<str:id>', views.SPUpdate, name='spupdate'),
    path('spdelete/<str:id>', views.SPDelete, name='spdelete'),


    #Url for services


    path("servicenav/", views.servicenav, name='servicenav'),
    # path("customercontract/", views.customer_contract, name='customercontract'),
    # path("providercontract/", views.provider_contract,name='providercontract'),


    #Url for services Family

    path("servicefamilies/", views.servicefamilies,name='servicefamilies'),
    path('sfadd', views.SFADD, name='sfadd'),
    path('sfedit', views.SFEdit, name='sfedit'),
    path('sfupdate/<str:id>', views.SFUpdate, name='sfupdate'),
    path('sfdelete/<str:id>', views.SFDelete, name='sfdelete'),


     #Url for services 

    path("sservice/", views.sservice, name='service'),
    path('ssadd', views.SSADD, name='ssadd'),
    path('ssedit', views.SSEdit, name='ssedit'),
    path('ssupdate/<str:id>', views.SSUpdate, name='ssupdate'),
    path('ssdelete/<str:id>', views.SSDelete, name='ssdelete'),



     #url for service subcategory
    path("service_subcategory/", views.service_subcategory, name='service_subcategory'),
    path('sadd', views.SADD, name='sadd'),
    path('sedit', views.SEdit, name='sedit'),
    path('supdate/<str:id>', views.SUpdate, name='supdate'),
    path('sdelete/<str:id>', views.SDelete, name='sdelete'),


    
     #url for Other Software
    path("other_software/", views.other_software, name='other_software'),
    path('osAdd', views.osAdd, name='osAdd'),
    path('osEdit', views.osEdit, name='osEdit'),
    path('osUpdate/<str:id>', views.osUpdate, name='osUpdate'),
    path('osDelete/<str:id>', views.osDelete, name='osDelete'),





    

    #url for sla
    path("sla/", views.sla, name='sla'),
    path('sladd', views.SLADD, name='sladd'),
    path('sledit', views.SLEdit, name='sledit'),
    path('slupdate/<str:id>', views.SLUpdate, name='slupdate'),
    path('sldelete/<str:id>', views.SLDelete, name='sldelete'),


    
    
    #url for sdelivery
    path("servicedelivery/", views.servicedelivery,name='servicedelivery'),
    path('sdadd', views.SDADD, name='sdadd'),
    path('sdedit', views.SDEdit, name='sdedit'),
    path('sdupdate/<str:id>', views.SDUpdate, name='sdupdate'),
    path('sddelete/<str:id>', views.SDDelete, name='sddelete'),




     #url for slt
    path("slt/", views.SLT,name='slt'),
    path('sltadd', views.STADD, name='sltadd'),
    path('sltedit', views.SLTEdit, name='sltedit'),
    path('sltupdate/<str:id>', views.SLTUpdate, name='sltupdate'),
    path('sltdelete/<str:id>', views.SLTDelete, name='sltdelete'),







    #url for system configuration
    path("synchro_data_source/", views.synchro_data_source,name='synchro_data_source'),
    path("sysconfinav/", views.sysconfienav,name='sysconfinav'),
    path("authgoogle/", views.oauth_google,name='authgoogle'),
    path("authmazure/", views.oauth_mazuree,name='authmazure'),
    path("sysconfiauth/", views.sysconfiauth,name='sysconfiauth'),

    #url for administration
    path("admuser/", views.admuser,name='admuser'),
    path("itsmuser/", views.itsmuser,name='itsmuser'),
    path("idapuser/", views.ldapuser,name='idapuser'),
    path("externaluser/", views.externaluser,name='externaluser'),

    #Assign
    # path("tassign/", views.assignform, name='assign'),


    #url for integration
    path("integration/", views.integrationav,name='integration'),
    path("slacknoti/", views.slacknoti,name='slacknoti'),
    path("micronoti/", views.micronoti,name='micronoti'),
    path("webhook/", views.webhook,name='webhook'),
    path("googlechat/", views.googlechat,name='googlechat'),
    path("rocketchat/", views.rocketchat,name='rocketchat'),
    path("itsmwebhook/", views.itsmwebhook,name='itsmwebhook'),
   
    ]