from unicodedata import name
from django.urls import path
from . import views


urlpatterns = [
    path('', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    # path('home/', views.homepage, name="home"),
    # path('dashboard',views.home, name="dashboard")
    path('dashboard/manager', views.manager_dashboard, name="manager_dashboard"),
    path('dashboard/supervisor/', views.supervisor_dashboard,
         name="supervisor_dashboard"),
    path('dashboard/worker/', views.worker_dashboard, name="worker_dashboard"),
    # path('dashboard/',views.dashboard,name="dashboard"),
    path('dashboard/worker/goods_received',
         views.goods_received, name="goods_received"),
    path('dashboard/worker/goods_received',
         views.goods_item_details, name="goods_item_details"),
    path("dashboard/itemmaster/",
         views.ItemMasterCreateView.as_view(), name="itemmaster"),
    path("itemdetails/", views.ItemDetailsTable, name="itemdetails"),
    path("receiveapproval/<int:id>",
         views.orderApprovalView, name="receiveapproval"),
    path("dashbaord/supervisor/dockallocation_form/<int:id>",
         views.dockallocation, name="dockallocation"),
     path("dashbaord/supervisor/dockallocation_table/",
         views.docksuptable, name="dockallocation_table"),
    
    #     path("dashbaord/supervisor/addzone/",
    #          views.ZoneCreateView.as_view(), name="addzone"),
    #     path("dashbaord/supervisor/addbin/",
    #          views.BinCreateView.as_view(), name="addbin"),
    #     path("dashbaord/supervisor/addwarehouse/",
    #          views.WarehouseCreateView.as_view(), name="addwarehouse"),
    path("supplier/", views.SupplierCreateView.as_view(), name="supplier"),
  
    path("dockslip/<int:id>", views.dockslip, name="dockslip"),
    path("delete_item_event/<int:id>",
         views.deleteitem, name="delete"),
    path("delete_order_detail/<int:id>",
         views.deletedetail, name="deleteDetail"),
    path("allzonelist/", views.allzonelist, name="allzonelist"),
    path("allbinlist/", views.allbinlist, name="allbinlist"),
    #     path("dashboard/itemmaster/",
    #          views.Itemrecievemaster, name="itemmaster"),
    path("delete_item2_event/<int:id>",
         views.delete_item, name="deleteitem"),
    path("ita/", views.ita, name="ita"),
    path("supplierdetails/", views.SupplierTable, name="supplierdetails"),
    path("item_details/<int:id>", views.Item_DetailsTable, name="item_details"),
    path("dockitem/<int:id>",
         views.dockitem, name="dockitem"),
     path("binapi/<int:id>",views.binapi, name="binapi"),
     path("Itemtagging/", views.itemtable, name="itemtagging"),
      path("itemtag/<int:id>",
         views.itemtag, name="itemtag"),





]
