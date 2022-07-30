"""EWMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from masterData import views as masterData_views
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from dashboard import views as dbviews

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', masterData_views.landingpage, name="landing"),
    path('register/', masterData_views.registerPage, name="register"),
    path('e404/', masterData_views.errorpage, name="e404"),

    path('login/', masterData_views.loginPage, name="login"),
    path('logout/', masterData_views.logoutUser, name="logout"),

    path("home/", masterData_views.homepage, name="home"),
    path("ota/", masterData_views.ota, name="ota"),

    path("addwarehouse/", masterData_views.WarehouseCreateView.as_view(),
         name="addwarehouse"),
    path("addzone/", masterData_views.ZoneCreateView.as_view(), name="addzone"),
    path("addbin/", masterData_views.BinCreateView.as_view(), name="addbin"),
    path("addsupp/", masterData_views.SupplierCreateView.as_view(), name="addsupp"),
    path("addcustomer/", masterData_views.CustomerCreateView.as_view(),
         name="addcustomer"),

    path("ird/", masterData_views.ItemRecieveDetailsCreateView.as_view(), name="ird"),
    path("inventory/", masterData_views.InventoryCreateView.as_view(), name="inventory"),
    path("itemmaster/", masterData_views.ItemMasterCreateView.as_view(),
         name="itemmaster"),

    path("zone_list/<int:id>", masterData_views.zone_list, name="zone_list"),
    path("bin_list/<int:id>", masterData_views.bin_list, name="bin_list"),

    path("orm/", masterData_views.OrderRecieveMasterCreateView.as_view(), name="orm"),
    path("ord/<int:id>", masterData_views.orderreceivedetailview, name="ord"),
    path("allorderdetail/<int:id>",
         masterData_views.allOrderDetails, name="allorderdetail"),

    path("orderprocess/<int:id>",
         masterData_views.orderprocesscreateview, name="orderprocess"),
    path("orderapproval/<int:id>",
         masterData_views.orderApprovalView, name="orderapproval"),

    path("delete_order_event/<int:id>",
         masterData_views.deleteorder, name="deleteOrder"),
    path("delete_order_detail/<int:id>",
         masterData_views.deletedetail, name="deleteDetail"),

    path("pickslip/<int:id>", masterData_views.pickslip,
         name="pickslip"),  
    path("suphome/", masterData_views.suphome, name="suphome"),

    path("superapproval/", masterData_views.superapproval, name="superapproval"),
    path("updatedetail/<int:id>", masterData_views.updatedetail, name="updatedetail"),

    path("inventoryDisplay/<int:id>",
         masterData_views.inventoryDisplay, name="inventory_display"),

    path("warehouselist/", masterData_views.warehouselist, name="warehouselist"),
    path("allzonelist/", masterData_views.allzonelist, name="allzonelist"),
    path("allbinlist/", masterData_views.allbinlist, name="allbinlist"),
    path('', include('authentication.urls')),
    path('dashboard/items/', dbviews.items, name="items"),
    path('dashboard/orders/', dbviews.orders, name="orders"),
    path('warelistsup/', masterData_views.warelistsup, name="warelistsup"),
    path('zonelistsup/', masterData_views.zonelistsup, name="zonelistsup"),
    path('binlistsup/', masterData_views.binlistsup, name="binlistsup"),
    path("supzonelist_id/<int:id>",
         masterData_views.zone_list_sup, name="supzonelist_id"),
    path("supbinlist_id/<int:id>",
         masterData_views.bin_list_sup, name="supbinlist_id"),
    path("inventoryDisplaysup/<int:id>",
         masterData_views.inventoryDisplaysup, name="inventory_displaysup"),
     
     path("inventory/<int:id>", masterData_views.inventory, name="inventory"),
     path("ihome/", masterData_views.ihome, name="ihome"),
     path("dispa/", masterData_views.dispatchorder, name="dispa"),
     path("gat/<int:id>", masterData_views.gatepass, name="gat"),
     path("getgp/<int:id>", masterData_views.getgp, name="getgp"),
     path("getsn/<int:id>", masterData_views.getsn, name="getsn"),




     path("doapi/", masterData_views.DispatchOrderAPI.as_view(), name="doapi"),
     path("ordapi/", masterData_views.OrderRecieveDetailAPI.as_view(), name="ordapi"),
     path("dodapi/", masterData_views.DispatchOrderDetailsAPI.as_view(), name="dodapi"),

     path("irdapi/", masterData_views.ItemRecieveDetailsAPI.as_view(), name="irdapi"),
     path("itapi/", masterData_views.ItemTaggingAPI.as_view(), name="itapi"),

     path("dapi/", masterData_views.VerificationAPI.as_view(), name="dapi"),
     
     

     path("api-auth/", include('rest_framework.urls')),
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
