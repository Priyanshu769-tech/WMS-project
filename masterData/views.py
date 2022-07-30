from array import array
from django.shortcuts import render, redirect
from django.core.exceptions import SuspiciousOperation
#from requests import request
from authentication.models import ReceiveApproval

from .forms import *
# import authentication
from .models import Role
from authentication.models import ItemRecieveMaster as Its
from authentication.models import DockAllocation as DA
from authentication.models import ItemRecieveDetails as Irds

from masterData.models import *
from authentication.models import ItemRecieveDetails as ItemRecieveDetailsAuth
from authentication.models import ItemTagging as ItemTaggingAuth


from django.contrib import messages

from django.views.generic import CreateView as cv
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.views import View

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken 
from rest_framework.authtoken.models import Token 
from rest_framework import authentication, permissions

from .serializers import *

# Create your views here.

# Ansh Gupta


def errorpage(request):
    return render(request, 'masterData/404page.html')
# page use for registering user to the app


def registerPage(request):
    if request.user.is_authenticated:
        role = Role.objects.get(user=request.user)
        if role.is_manager:
            return redirect('home')
        if role.is_supervisor:
            return redirect('suphome')
        if role.is_worker:
            return redirect('/dashboard/worker')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            # group = Group.objects.get(name='Worker')
            # user.groups.add(group)
            messages.success(
                request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'masterData/signup.html', context)

# Yash Kadam
# the first page ww see as a user


def landingpage(request):
    return render(request, 'masterData/landing.html')

# Ansh Gupta
# thi spage is used to login a already registered user


def loginPage(request):
    if request.user.is_authenticated:
        role = Role.objects.get(user=request.user)
        if role.is_manager:
            return redirect('home')
        if role.is_supervisor:
            return redirect('suphome')
        if role.is_worker:
            return redirect('/dashboard/worker')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            role = Role.objects.get(user=request.user)
            if role.is_manager:
                return redirect('home')
            if role.is_supervisor:
                return redirect('suphome')
            if role.is_worker:
                return redirect('/dashboard/worker')

        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'masterData/signin.html', context)

# Yash Kadam
# it logs the user out of the cureent session


def logoutUser(request):
    logout(request)
    return redirect('login')

# Ansh Gupta
# this is the manager dashboard


@login_required(login_url='login')
def homepage(request):
    warehouses = WareHouse.objects.all()
    zones = Zone_Area.objects.all()
    bins = Bin.objects.all()
    orms = OrderRecieveMaster.objects.all()
    cntware = WareHouse.objects.all().count()
    cntzone = Zone_Area.objects.all().count()
    cntbin = Bin.objects.all().count()
    cntorder = OrderRecieveMaster.objects.all().filter(isApproved='true').count()
    cntallorder = OrderRecieveMaster.objects.all().count()
    cntalldetail = OrderRecieveDetail.objects.all().filter(isApproved='true').count()
    dacount = DA.objects.all().count()
    itemcount = Its.objects.all().count()
    item = Its.objects.all()
    context = {"warehouses": warehouses,
               "zones": zones,
               "bins": bins,
               "orms": [{
                   'CustomerName': Customer.objects.get(CustomerId=x.CustomerId.CustomerId).CustomerName,
                   'OrderId': x.OrderId,
                   'OrderDate': x.OrderDate.date,
                   'isApproved': x.isApproved
               }for x in orms],
               "item": [{
                   'RecieveID': Y.RecieveID,
                   'RecieveDate': Y.RecieveDate.date,
                   'SupplierName': Y.SupplierName,
                   'VehicleNo': Y.VehicleNo
               }for Y in item],
               "cntware": cntware,
               "cntzone": cntzone,
               "cntbin": cntbin,
               "cntorder": cntorder,
               "item": item,
               'cntallorder': cntallorder,
               'cntalldetail': cntalldetail,
               'dacount': dacount,
               'itemcount': itemcount}
    return render(request, "masterData/home.html", context)
# ansh gupta


def ota(request):
    warehouses = WareHouse.objects.all()
    zones = Zone_Area.objects.all()
    bins = Bin.objects.all()
    orms = OrderRecieveMaster.objects.all()
    cntware = WareHouse.objects.all().count()
    cntzone = Zone_Area.objects.all().count()
    cntbin = Bin.objects.all().count()
    cntorder = OrderRecieveMaster.objects.all().count()
    item = Its.objects.all()
    context = {"warehouses": warehouses,
               "zones": zones,
               "bins": bins,
               "orms": [{
                   'CustomerName': Customer.objects.get(CustomerId=x.CustomerId.CustomerId).CustomerName,
                   'OrderId': x.OrderId,
                   'OrderDate': x.OrderDate.date,
                   'isApproved': x.isApproved
               }for x in orms],
               "item": [{
                   'RecieveID': Y.RecieveID,
                   'RecieveDate': Y.RecieveDate.date,
                   'SupplierName': Y.SupplierName,
                   'VehicleNo': Y.VehicleNo
               }for Y in item],
               "cntware": cntware,
               "cntzone": cntzone,
               "cntbin": cntbin,
               "cntorder": cntorder,
               "item": item}
    return render(request, "masterData/ota.html", context)

# ansh gupta


# def ita(request):
#     item = Its.objects.all()
#     context = {"item": [{
#         'RecieveID': Y.RecieveID,
#         'RecieveDate': Y.RecieveDate.date,
#         'SupplierName': Y.SupplierName,
#         'VehicleNo': Y.VehicleNo,
#         'is_approved': False
#     }for Y in item], }
#     print(ReceiveApproval.objects.all())

#     return render(request, "masterData/ita.html", context)

# Swapnaneel Basu
# shows  all the zones


@login_required(login_url='login')
def zone_list(request, id):
    zones = Zone_Area.objects.all().filter(WareHouseId=id)
    return render(request, "masterData/zone_list.html", {"zones": zones})


@login_required(login_url='login')
def zone_list_sup(request, id):
    zones = Zone_Area.objects.all().filter(WareHouseId=id)
    return render(request, "masterData/supzonelist_id.html", {"zones": zones})

# Swapnaneel Basu
# thi shows all the bins


@login_required(login_url='login')
def bin_list(request, id):
    bins = Bin.objects.all().filter(ZoneId=id)
    return render(request, "masterData/bin_list.html", {"bins": bins})


@login_required(login_url='login')
def bin_list_sup(request, id):
    bins = Bin.objects.all().filter(ZoneId=id)
    return render(request, "masterData/supbinlist_id.html", {"bins": bins})

# @login_required(login_url='login')

# Swapnaneel Basu
# warehouse add


class WarehouseCreateView(cv):
    model = WareHouse
    form_class = WarehouseForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect('/warehouselist')

# @login_required(login_url='login')

# kumar krish
# zone add


class ZoneCreateView(cv):
    model = Zone_Area
    form_class = Zone_AreaForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect('/allzonelist')

# @login_required(login_url='login')

# kumar krish
# bin add


class BinCreateView(cv):
    model = Bin
    form_class = BinForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect('/allbinlist')

# kumar krish
# supplier add


class SupplierCreateView(cv):
    model = Supplier
    form_class = SupplierForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect('/home')

# kumar krish
# customer add


class CustomerCreateView(cv):
    model = Customer
    form_class = CustomerForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect('/home')

# Ansh Gupta
# order receive form


class OrderRecieveMasterCreateView(View):
    # model = OrderRecieveMaster
    # form_class = OrderRecieveMasterForm
    def get(self, request):
        form = OrderRecieveMasterForm()
        orm = OrderRecieveMaster.objects.all()
        context = {'form': form,
                   'orm': [{
                       'OrderId': x.OrderId,
                       'OrderDate': x.OrderDate.date,
                       'CustomerId': x.CustomerId,
                       'isApproved': x.isApproved
                   }for x in orm],
                   }
        return render(request, 'masterData/orderrecievemaster_form.html', context)

    def post(self, request):
        form_class = OrderRecieveMasterForm(request.POST)
        if form_class.is_valid():
            # form_class.instance.author = self.request.user
            # form_class.UserId = request.user.id
            ord = OrderRecieveMaster.objects.create(
                CustomerId=form_class.cleaned_data.get('CustomerId'))
            ord.save()
            # oid = ord.OrderId
            # print(oid)
            return redirect('ord', ord.OrderId)
        else:
            print(form_class.errors)
            return redirect('/home')
            # form_class.save()
        # print(form.instance.OrderId)
        # oid = form_class.instance.OrderId

# Rishabh Baranwal
# order recieve details


def orderreceivedetailview(request, id):
    order = OrderRecieveMaster.objects.get(OrderId=id)
    orderDetailList = OrderRecieveDetail.objects.all().filter(OrderId=order)
    orm = OrderRecieveMaster.objects.all().filter(OrderId=id).first()
    cust = Customer.objects.all().filter(CustomerId=orm.CustomerId.CustomerId).first()

    if request.method == 'POST':
        od = OrderRecieveDetailForm(request.POST)

        if od.is_valid():
            form = od.save(commit=False)
            form.OrderId = order
            form.save()

            return redirect('ord', id)

    else:
        od = OrderRecieveDetailForm()

    return render(request, 'masterData/orderrecievedetail_form.html', {'form': od, 'orderDetailList': orderDetailList, 'cust': cust, 'orderid': id})


# Ansh Gupta
# superviso dashboard
@login_required(login_url='login')
def suphome(request):
    warehouses = WareHouse.objects.all()
    zones = Zone_Area.objects.all()
    bins = Bin.objects.all()
    orms = OrderRecieveMaster.objects.all()
    cntware = WareHouse.objects.all().count()
    cntzone = Zone_Area.objects.all().count()
    cntbin = Bin.objects.all().count()
    cntorder = OrderRecieveMaster.objects.all().filter(isApproved='true').count()
    cntallorder = OrderRecieveMaster.objects.all().count()
    cntalldetail = OrderRecieveDetail.objects.all().filter(isApproved='true').count()
    dacount = DA.objects.all().count()
    itemcount = Its.objects.all().count()
    context = {"warehouses": warehouses,
               "zones": zones,
               "bins": bins,
               "orms": [{
                   'CustomerName': Customer.objects.get(CustomerId=x.CustomerId.CustomerId).CustomerName,
                   'OrderId': x.OrderId,
                   'OrderDate': x.OrderDate.date,
                   'isApproved': x.isApproved
               }for x in orms],
               "cntware": cntware,
               "cntzone": cntzone,
               "cntbin": cntbin,
               "cntorder": cntorder,
               'cntallorder': cntallorder,
               'cntalldetail': cntalldetail,
               'dacount': dacount,
               'itemcount': itemcount, }
    return render(request, 'masterData/suphome.html', context)

# Ansh Gupta
# approval page for order processing


@login_required(login_url='login')
def superapproval(request):
    allcustomer = Customer.objects.all()
    allOrderDetailList = OrderRecieveMaster.objects.all()
    context = {"cust": allcustomer,
               "list": [{
                   'CustomerName': Customer.objects.get(CustomerId=x.CustomerId.CustomerId).CustomerName,
                   'OrderId': x.OrderId,
                   'OrderDate': x.OrderDate.date,
                   'isApproved': x.isApproved
               }for x in allOrderDetailList],
               }

    return render(request, 'masterData/superapproval.html', context)

# Ansh Gupta
# worker dashboard


@login_required(login_url='login')
def worker_dashboard(request):
    role = Role.objects.get(user=request.user)
    if not role.is_worker:
        return redirect('/e404')
    return render(request, 'masterData/dashboard_worker.html')

# Swapnaneel Basu
# all order detils


def allOrderDetails(request, id):
    orm = OrderRecieveMaster.objects.all().filter(OrderId=id).first()
    cust = Customer.objects.all().filter(CustomerId=orm.CustomerId.CustomerId).first()
    allOrderDetailList = OrderRecieveDetail.objects.all().filter(OrderId=id)

    return render(request, 'masterData/allOrderDetails.html', {'list': allOrderDetailList, 'cust': cust})

# kumar krish
# pickslip generation


def pickslip(request, id):
    pickslip_1 = OrderRecieveMaster.objects.all().filter(OrderId=id)
    pickslip_2 = OrderRecieveDetail.objects.all().filter(OrderId=id)
    orm = OrderRecieveMaster.objects.all().filter(OrderId=id).first()
    cust = Customer.objects.all().filter(CustomerId=orm.CustomerId.CustomerId).first()
    op = []
    for i in pickslip_2:
        if i.isApproved == 'true':
            op.append(OrderProcessing.objects.filter(OrderId=i.id).first())

    return render(request, 'masterData/pickslip.html', {'list1': pickslip_1, 'list2': pickslip_2, 'cust': cust, 'op': op})

# Urvish Mehta
# order procesing func


def orderprocesscreateview(request, id):
    inv = Inventory.objects.all()
    order = OrderRecieveDetail.objects.get(id=id)
    orm = OrderRecieveMaster.objects.get(OrderId=order.OrderId.OrderId)

    selectedItem = Inventory.objects.get(Qty__range=(
        order.Qty, 10000000), ItemCode=order.ItemCode)
    binid = selectedItem.BinId
    binobject = Bin.objects.get(BinName=binid)
    zoneid = binobject.ZoneId
    if request.method == 'POST':
        op = OrderProcessingForm(request.POST)

        if op.is_valid() and selectedItem.Qty >= order.Qty:

            selectedItem.Qty -= order.Qty
            selectedItem.save(update_fields=['Qty'])

            form = op.save(commit=False)
            form.BinId = binid
            form.ZoneId = zoneid
            form.OrderId = order
            form.save()

            order.isApproved = "true"
            order.save(update_fields=['isApproved'])

            return redirect("allorderdetail", orm.OrderId)

        else:
            return redirect('/e404')

    else:
        op = OrderProcessingForm()

    return render(request, 'masterData/orderprocess.html', {'form': op, 'inv': inv, 'order': order})


# Urvish Mehta
# order approval
def orderApprovalView(request, id):
    ormData = OrderRecieveMaster.objects.filter(OrderId=id).first()
    order = OrderRecieveMaster.objects.get(OrderId=id)
    orderDetailList = OrderRecieveDetail.objects.all().filter(OrderId=order)
    orm = OrderRecieveMaster.objects.all().filter(OrderId=id).first()
    cust = Customer.objects.all().filter(CustomerId=orm.CustomerId.CustomerId).first()

    if request.method == 'POST':
        oa = OrderApprovalForm(request.POST)

        if oa.is_valid():
            form = oa.save(commit=False)
            form.OrderId = order
            form.save()

            order.isApproved = "true"
            order.save(update_fields=['isApproved'])

            return redirect("/home")

    else:
        oa = OrderApprovalForm()

    return render(request, 'masterData/orderapproval_form.html', {'form': oa, 'ormData': ormData, 'orderDetailList': orderDetailList, 'cust': cust})

# Rishabh Baranwal
# dispatch order
# Rishabh Baranwal

class ItemRecieveDetailsCreateView(cv):
    model = ItemRecieveDetails
    form_class = ItemRecieveDetailsForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect('/home')

# Rishabh Baranwal
# inventory
class InventoryCreateView(cv):
    model = Inventory
    form_class = InventoryForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect('/home')

# Rishabh Baranwal
class ItemMasterCreateView(cv):
    model = ItemMaster
    form_class = ItemMasterForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect('/home')

# Urvish Mehta
# delete enrtry
def deleteorder(request, id):
    ordmas = OrderRecieveMaster.objects.get(OrderId=id)
    ordmas.delete()
    return redirect('ota')

# Urvish Mehta
# delete enrtry
def deletedetail(request, id):
    ordmas = OrderRecieveDetail.objects.get(id=id)
    ordmas.delete()

    return redirect('ord', ordmas.OrderId.OrderId)

# Rishabh Baranwal
# update ntry


def updatedetail(request, id):
    objd = OrderRecieveDetail.objects.get(id=id)
    objm = OrderRecieveMaster.objects.get(OrderId=objd.OrderId.OrderId)
    if request.method == 'POST':
        fm = OrderRecieveDetailForm(request.POST)
        if fm.is_valid():
            ic = fm.cleaned_data['ItemCode']
            qty = fm.cleaned_data['Qty']
            ord = OrderRecieveDetail.objects.get(id=id)
            ord.ItemCode = ic
            ord.Qty = qty
            ord.save(update_fields=['ItemCode', 'Qty'])
            return redirect('ord', objm.OrderId)
    else:
        fm = OrderRecieveDetailForm()
    return render(request, 'masterData/update.html', {'form': fm})

# Urvish Mehta
# inventory display


def inventoryDisplay(request, id):
    form = Inventory.objects.all().filter(BinId=id)

    return render(request, 'masterData/inventoryDisplay.html', {'form': form})


def inventoryDisplaysup(request, id):
    form = Inventory.objects.all().filter(BinId=id)

    return render(request, 'masterData/inventoryDisplaysup.html', {'form': form})

# Yash Kadam
# warehouse lost


def warehouselist(request):
    form = WareHouse.objects.all()
    return render(request, 'masterData/warehouse_list.html', {'form': form})

# Yash Kadam
# zone list


def allzonelist(request):
    form = Zone_Area.objects.all()
    return render(request, 'masterData/allzone_list.html', {'form': form})

# Yash Kadam
# bin list


def allbinlist(request):
    form = Bin.objects.all()
    return render(request, 'masterData/allbin_list.html', {'form': form})

# Kumar Krish
# supervisor warehouse list


def warelistsup(request):
    form = WareHouse.objects.all()
    return render(request, 'masterData/warelistsup.html', {'form': form})


def zonelistsup(request):
    form = Zone_Area.objects.all()
    return render(request, 'masterData/zonelistsup.html', {'form': form})


def binlistsup(request):
    form = Bin.objects.all()
    return render(request, 'masterData/binlistsup.html', {'form': form})

#
#
#
class VerificationAPI(APIView):
    serializer_class = VerificationSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        if data["username"] == "KD" and data["password"] == "KDPASSWORD":
            return Response("User Verified")

        else:
            return Response("User not Valid")

class DispatchOrderAPI(APIView):
    serializer_class = DispatchOrderSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        orders = DispatchOrder.objects.all()
        serializer = DispatchOrderSerializer(orders, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        DOdata = request.data

        newDispatchOrder = DispatchOrder.objects.create(VehicleNo = DOdata["VehicleNo"])
        newDispatchOrder.save()

        serializer = DispatchOrderSerializer(newDispatchOrder)

        return Response(serializer.data)

class OrderRecieveDetailAPI(APIView):
    serializer_class = OrderRecieveDetailSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        orders = OrderRecieveDetail.objects.all().filter(isApproved = 'true')
        serializer = OrderRecieveDetailSerializer(orders, many=True)

        return Response(serializer.data)

class ItemRecieveDetailsAPI(APIView):
    serializer_class = ItemRecieveDetailsSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        items = ItemRecieveDetailsAuth.objects.all()
        serializer = ItemRecieveDetailsSerializer(items, many=True)

        return Response(serializer.data)

class DispatchOrderDetailsAPI(APIView):
    serializer_class = DispatchOrderDetailSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        orders = DispatchOrderDetail.objects.all()
        serializer = DispatchOrderDetailSerializer(orders, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        DODdata = request.data

        newDispatchOrderDetail = DispatchOrderDetail.objects.create(DispatchId = DODdata["DispatchId"], 
                                                                    ItemCode = DODdata["ItemCode"],
                                                                    BatchNo = DODdata["BatchNo"],
                                                                    QRCode = DODdata["QRCode"],
                                                                    OrderId = DODdata["OrderId"],)
        newDispatchOrderDetail.save()

        serializer = DispatchOrderDetailSerializer(newDispatchOrderDetail)
        return Response(serializer.data)


class ItemTaggingAPI(APIView):
    serializer_class = ItemTaggingSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        items = ItemTaggingAuth.objects.all()
        serializer = ItemTaggingSerializer(items, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        ItemData = request.data

        newItem = ItemTaggingAuth.objects.create(   ItemCode = ItemData["ItemCode"], 
                                                    ReceiveId = ItemData["ReceiveId"],
                                                    BatchNo = ItemData["BatchNo"],
                                                    QRCode = ItemData["QRCode"],)
        newItem.save()

        serializer = ItemTaggingSerializer(newItem)
        return Response(serializer.data)


def inventory(request, id):
    inv = Inventory.objects.get(ItemId=id)
    invcode = inv.ItemCode
    ord = OrderRecieveDetail.objects.all().filter(isApproved="true", ItemCode=invcode)
    ird = Irds.objects.all().filter(ItemCode=invcode)
    # for i in inv:
    #         inv.append(Bin.objects.filter(ZoneId=i.BinId).first())

    return render(request, 'masterData/inventory.html', {'inv': inv, 'ord': ord, 'ird':ird})


def ihome(request):
    inv = Inventory.objects.all()
    return render(request, 'masterData/ihome.html', {'inv': inv,})


def dispatchorder(request):
    disp = DispatchOrder.objects.all()
    context = {
        "disp": [{
                   'DispatchId': Y.DispatchId,
                   'DispatchDate': Y.DispatchDate.date,
                   'ASNStatus': Y.ASNStatus,
                   'GatePassStatus': Y.GatePassStatus
               }for Y in disp],
    }
    return render(request , 'masterData/dispa.html' , context)


def gatepass(request , id):
     dispd = DispatchOrderDetail.objects.all().filter(DispatchId = id)
     return render(request , 'masterData/gatepass.html', {"d":dispd, "doid":id})
 
def getgp(request,id):
    dispa = DispatchOrderDetail.objects.all().filter(DispatchId = id).first()
    varid = int(dispa.OrderId)
    print(varid)
    dispalist = DispatchOrderDetail.objects.all().filter(DispatchId = id)
    dom  = DispatchOrder.objects.get(DispatchId = id)
    
    oid  = OrderRecieveDetail.objects.all().filter(id = varid).first()

    array = []
    for i in dispalist:
        varidd = int(i.OrderId)
        print(varidd)
        array.append(OrderRecieveDetail.objects.get(id = varidd))

    dom.GatePassStatus = "true"
    dom.save(update_fields=['GatePassStatus'])

    oidid = oid.OrderId
    orm = OrderRecieveMaster.objects.get(OrderId = oidid.OrderId)
    custid = orm.CustomerId
    cust = Customer.objects.all().filter(CustomerId  = custid.CustomerId).first()
    return render(request , 'masterData/getgatepass.html', {"diss":dispa,"dom":dom ,"disl":dispalist, "ord":oid,"ordl":array, "orm":orm,"cust":cust,"doid":id})
 
def getsn(request,id):
    dispa = DispatchOrderDetail.objects.all().filter(DispatchId = id).first()
    varid = int(dispa.OrderId)
    
    dispalist = DispatchOrderDetail.objects.all().filter(DispatchId = id)
    dom  = DispatchOrder.objects.get(DispatchId = id)
    
    oid  = OrderRecieveDetail.objects.all().filter(id = varid).first()

    array = []
    for i in dispalist:
        varidd = int(i.OrderId)
        array.append(OrderRecieveDetail.objects.get(id = varidd))

    dom.ASNStatus = "true"
    dom.save(update_fields=['ASNStatus'])


    oidid = oid.OrderId
    orm = OrderRecieveMaster.objects.get(OrderId = oidid.OrderId)
    custid = orm.CustomerId
    cust = Customer.objects.all().filter(CustomerId  = custid.CustomerId).first()
    return render(request , 'masterData/getsn.html', {"diss":dispa,"dom":dom ,"disl":dispalist, "ord":oid,"ordl":array, "orm":orm,"cust":cust,"doid":id})
 
     
