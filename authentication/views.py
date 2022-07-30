
import imp
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from masterData.models import Zone_Area
from masterData.models import Bin
# from .models import Role
from masterData.models import Role
from masterData.models import OrderRecieveDetail
from masterData.models import OrderRecieveMaster

from .models import ItemRecieveMaster as Its
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import *
from .decorators import admin_only
from django.views.decorators.csrf import csrf_protect
from .models import ItemRecieveMaster, ItemRecieveDetails
from django.views.generic import CreateView as cv
from django.contrib.auth.models import Group
from masterData.models import Zone_Area as z_a
from masterData.models import Bin as b
from masterData.models import Inventory as Inv


def registerPage(request):
    # if request.user.is_authenticated:
    # 	return redirect('homepage')
    # else:
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
    return render(request, 'authentication/register.html', context)


def orderApprovalView(request, id):
    ormData = ItemRecieveMaster.objects.filter(RecieveID=id).first()
    order = ItemRecieveMaster.objects.get(RecieveID=id)
    orderDetailList = ItemRecieveDetails.objects.all().filter(RecieveId=order)
    orm = ItemRecieveMaster.objects.all().filter(RecieveID=id).first()
    supp = Supplier.objects.all().filter(SupplierName=orm.SupplierName.SupplierName).first()
    object=DockAllocation.objects.all().filter(ReceiveId=ormData.RecieveID).first()
    print(object.BinId)
    # oa=ReceiveApprovalForm()
    if request.method == 'POST':
        oa = ReceiveApprovalForm(request.POST)
        if oa.is_valid():
            try:
                newA = ReceiveApproval.objects.create(
                    RecieveID=order.RecieveID,
                    Remarks=oa.cleaned_data.get('Remarks')
                )
                newA.save()
                return redirect('ita')
            except Exception as e:
                return HttpResponse(str(e))

    else:
        oa = ReceiveApprovalForm()

    return render(request, 'authentication/orderapproval_form.html', {'form': oa, 'ormData': ormData, 'orderDetailList': orderDetailList,'supp':supp,'RecieveID': id})


def ita(request):
    item = Its.objects.all()
    context = {"item": [{
        'RecieveID': Y.RecieveID,
        'RecieveDate': Y.RecieveDate.date,
        'SupplierName': Y.SupplierName,
        'VehicleNo': Y.VehicleNo,
        'is_approved': False
    }for Y in item], }
    for c in context['item']:
        if len(ReceiveApproval.objects.filter(RecieveID=str(c['RecieveID']))) > 0:
            c['is_approved'] = True

    return render(request, "masterData/ita.html", context)


def docksuptable(request):
    item = Its.objects.all()
    context = {"item": [{
        'RecieveID': Y.RecieveID,
        'RecieveDate': Y.RecieveDate.date,
        'SupplierName': Y.SupplierName,
        'VehicleNo': Y.VehicleNo,
        'is_approved': False,
    }for Y in item], }
    for c in context['item']:
        if len(DockAllocation.objects.filter(ReceiveId=str(c['RecieveID']))) > 0:
            c['is_approved'] = True


    return render(request, "authentication/docksuptable.html", context)


def dockitem(request,id):
    ormData = ItemRecieveMaster.objects.filter(RecieveID=id).first()
    order = ItemRecieveMaster.objects.get(RecieveID=id)
    orderDetailList = ItemRecieveDetails.objects.all().filter(RecieveId=order)
    zone=DockAllocation.objects.all().filter( ReceiveId=order)
    orm = ItemRecieveMaster.objects.all().filter(RecieveID=id).first()
    supp = Supplier.objects.all().filter(SupplierName=orm.SupplierName.SupplierName).first()
    context = {"orderDetailList": [{
        'RecieveId':Y.RecieveId,
        'id':Y.id,
        'ItemCode': Y.ItemCode,
        'ItemCode':Y.get_ItemCode_display,
        
        'BatchNo': Y.BatchNo ,
        'RecieveQty': Y.RecieveQty,
        'is_approved': False,
    }for Y in orderDetailList], 
    "zone":[{
        'ZoneId':X.ZoneId,
        'BinId':X.BinId,
    }for X in zone],
    'supp':supp,
    'RecieveID': id
    }
    
    
    # for c in context['orderDetailList']:
    #     if len(DockAllocation.objects.filter(ReceiveId=str(c['RecieveId']))) > 0:
    #         c['is_approved'] = True


    return render(request, "authentication/dockitem.html", context)    

def dockallocation(request, id):

    # order = ItemRecieveMaster.objects.get(RecieveID=id)
    # x=ItemRecieveDetails.objects.get(RecieveId=id)
    orderDetailList = ItemRecieveDetails.objects.get(id=id)
    order=ItemRecieveMaster.objects.get(RecieveID=orderDetailList.RecieveId.RecieveID)
    object = Inv.objects.all().filter(ItemCode = orderDetailList.ItemCode).first()

    print(object.BinId)
    binobj = Bin.objects.get(BinId = object.BinId.BinId)
    print(binobj)
    zoneobj = Zone_Area.objects.get(ZoneId = binobj.ZoneId.ZoneId)
    print(zoneobj)
    item = DockAllocation.objects.all().filter(ReceiveId=order)
    invobj = Inv.objects.get(BinId = binobj)
    print(invobj.Qty)
    print(orderDetailList.RecieveQty)
    
    # return render(request, 'authentication/itemrecievedetails_form.html', locals())
    if request.method == 'POST':
        detailsForm = DockAllocationForm(request.POST)

        if detailsForm.is_valid():
            # form = detailsForm
            # form.RecieveId =order

            # form.save()
            irdc = DockAllocation.objects.create(
                ReceiveId=order,
                ZoneId=zoneobj,
                BinId=binobj,

            )
            try:
                irdc.save()
                invobj.Qty += orderDetailList.RecieveQty
                invobj.save(update_fields=['Qty'])
            except Exception as e:
                print(e)

            return redirect('dockitem',order.RecieveID)
    else:
        detailsForm = DockAllocationForm()

    return render(request, 'authentication/dockallocation_form.html', {'form': detailsForm, 'item': item, 'RecieveID': id, 'zoneobj':zoneobj, 'binobj':binobj, 'orderDetailList':orderDetailList, 'object':object})



def itemtable(request):
    
    item = Its.objects.all()
    context = {"item": [{
        'RecieveID': Y.RecieveID,
        'RecieveDate': Y.RecieveDate.date,
        'SupplierName': Y.SupplierName,
        'VehicleNo': Y.VehicleNo,
        'is_approved': False,
    }for Y in item], }    

    return render(request, "authentication/itemtable.html", context)

def itemtag(request,id):
    ormData = ItemRecieveMaster.objects.filter(RecieveID=id).first()
    order = ItemRecieveMaster.objects.get(RecieveID=id)
    orderDetailList = ItemRecieveDetails.objects.all().filter(RecieveId=order)
    orm = ItemRecieveMaster.objects.all().filter(RecieveID=id).first()
    supp = Supplier.objects.all().filter(SupplierName=orm.SupplierName.SupplierName).first()
    
    context = {"orderDetailList": [{
        'RecieveId':Y.RecieveId,
        'ItemCode': Y.ItemCode,
        'ItemCode':Y.get_ItemCode_display,
        
        'BatchNo': Y.BatchNo ,
        'RecieveQty': Y.RecieveQty,
        'is_approved': False,
    }for Y in orderDetailList], 
    'supp':supp,
    'RecieveID': id

    
    }
    # for c in context['orderDetailList']:
    #     if len(DockAllocation.objects.filter(ReceiveId=str(c['RecieveId']))) > 0:
    #         c['is_approved'] = True


    return render(request, "authentication/itemtag.html", context)        

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            role = Role.objects.get(user=request.user)
            if role.is_manager:
                return redirect('/dashboard/manager')
            if role.is_supervisor:
                return redirect('/dashboard/supervisor')
            if role.is_worker:
                return redirect('/dashboard/worker')

        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'authentication/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def manager_dashboard(request):
    role = Role.objects.get(user=request.user)
    if not role.is_manager:
        return redirect('/404')
    item = ItemRecieveMaster.objects.all()
    return render(request, 'authentication/dashboard_manager.html', {'item': item})


@login_required(login_url='login')
def supervisor_dashboard(request):

    role = Role.objects.get(user=request.user)
    if not role.is_supervisor:
        return redirect('/404')
    warehouses = WareHouse.objects.all()
    zones = Zone_Area.objects.all()
    bins = Bin.objects.all()
    ormData = ItemRecieveMaster.objects.all()

    context = {"warehouses": warehouses,
               "zones": zones,
               "bins": bins,
               "ormData": ormData, }
    return render(request, "authentication/dashboard_supervisor.html", context=context)



    # return render(request, 'authentication/dashboard_supervisor.html')


@login_required(login_url='login')
def worker_dashboard(request):
    # ormData = ItemRecieveMaster.objects.filter(RecieveID=id).first()
    cntallorder = OrderRecieveMaster.objects.all().count()
    itemcount = Its.objects.all().count()

    # orderDetailList = ItemRecieveDetails.objects.all().filter(RecieveId=id)
    role = Role.objects.get(user=request.user)
    if not role.is_worker:
        return redirect('/404')
    item = ItemRecieveDetails.objects.all()
    return render(request, 'dashboard/home.html', {"item": item, "cntallorder": cntallorder, 'itemcount': itemcount})


def goods_received(request):
    if request.method == 'POST':
        form = ItemRecieveMasterForm(request.POST)
        if form.is_valid():
            form.save()
        context = {'form': form}
        # if request.method=="POST":
        # 	itemReceivedMaster = request.POST.get('itemReceivedMaster')
        # 	email=request.POST.get('email')
        # 	password=request.POST.get('password')
        return render(request, 'authentication/goods_received.html', context)
    else:
        return redirect('dashboard/worker/goods_received')


def goods_item_details(request):
    form = ItemRecieveDetailsForm()
    if form.is_valid():
        form.save()
    context = {'form': form}
    # if request.method=="POST":
    # 	itemReceivedMaster = request.POST.get('itemReceivedMaster')
    # 	email=request.POST.get('email')
    # 	password=request.POST.get('password')
    return render(request, 'authentication/goods_received.html', context)


class ItemMasterCreateView(cv):
    model = ItemRecieveMaster
    form_class = ItemRecieveMasterForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect('itemdetails')


class ItemRecieveDetailsCreateView(cv):
    model = ItemRecieveDetails
    form_class = ItemRecieveDetailsForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect('itemdetails')


def Item_DetailsTable(request, id):

    order = ItemRecieveMaster.objects.get(RecieveID=id)
    item = ItemRecieveDetails.objects.all().filter(RecieveId=order)
    orm = ItemRecieveMaster.objects.all().filter(RecieveID=id).first()
    supp = Supplier.objects.all().filter(SupplierName=orm.SupplierName.SupplierName).first()
    # return render(request, 'authentication/itemrecievedetails_form.html', locals())
    if request.method == 'POST':
        detailsForm = ItemRecieveDetailsForm(request.POST)

        if detailsForm.is_valid():
            # form = detailsForm
            # form.RecieveId =order

            # form.save()
            irdc = ItemRecieveDetails.objects.create(
                RecieveId=order,
                ItemCode=detailsForm.cleaned_data.get('ItemCode'),
                
                BatchNo=detailsForm.cleaned_data.get('BatchNo'),
                RecieveQty=detailsForm.cleaned_data.get('RecieveQty'),

            )
            try:
                irdc.save()
            except Exception as e:
                print(e)

            return redirect('item_details', id)
    else:
        detailsForm = ItemRecieveDetailsForm()

    return render(request, 'authentication/itemrecievedetails_form.html', {'form': detailsForm, 'item': item,'supp':supp,'RecieveID':id})


def ItemDetailsTable(request):
    #itemmaster = ItemRecieveMaster.objects.get(RecieveId=id)
    detailsForm = ItemRecieveDetailsForm(request.POST)
    item = ItemRecieveDetails.objects.all()
    # return render(request, 'authentication/itemrecievedetails_form.html', locals())
    if request.method == 'POST':

        if detailsForm.is_valid():
            form = detailsForm.save()
            item_id = form.RecieveId
            form.save()

            return redirect(f'/item_details/{item_id}')
        else:
            detailsForm = ItemRecieveDetailsForm()
    return render(request, 'authentication/itemrecievedetails_form.html', {'form': detailsForm, 'item': item})


def SupplierTable(request):
    #itemmaster = ItemRecieveMaster.objects.get(RecieveId=id)
    detailsForm = ItemRecieveMasterForm(request.POST)
    supp = Supplier.objects.all()
    item = ItemRecieveDetails.objects.all()
    # return render(request, 'authentication/itemrecievedetails_form.html', locals())
    if request.method == 'POST':

        if detailsForm.is_valid():
            form = detailsForm.save()
            item_id = form.RecieveID
            form.save()

            return redirect(f'/item_details/{item_id}')
        else:
            detailsForm = ItemRecieveDetailsForm()
    return render(request, 'authentication/itemrecievemaster_form.html', {'form': detailsForm, 'supp': supp})


# class DockAllocationCreateView(cv):
#     model = DockAllocation
#     form_class = DockAllocationForm

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.save()
#         return redirect('suphome')


# def Warehouse(request):
#     form =WarehouseForm()
#     context = {'form': form}
#     return render(request, "authentication/warehouse.html", context)


# class WarehouseCreateView(cv):
#     model = WareHouse
#     form_class = WarehouseForm

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.save()
#         return redirect("/dashboard/supervisor")


# class ZoneCreateView(cv):
#     model = Zone_Area
#     form_class = Zone_AreaForm

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.save()
#         return redirect('/dashboard/supervisor')


# class BinCreateView(cv):
#     model = Zone_Area
#     form_class = BinForm

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.save()
#         return redirect('/dashboard/supervisor')


class SupplierCreateView(cv):
    model = Supplier
    form_class = SupplierForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect('home')


def dockslip(request, id):
    dockslip_1 = ItemRecieveMaster.objects.all().filter(RecieveID=id)
    dockslip_2 = ItemRecieveDetails.objects.all().filter(RecieveId=id)
    dockslip_3 = DockAllocation.objects.all().filter(ReceiveId=id)
    ormData = ItemRecieveMaster.objects.all().filter(RecieveID=id).first()

    # op = []
    # for i in dockslip_2:
    #     op.append(.objects.filter(RecieveId=i.id).first())

    return render(request, 'authentication/dockslip.html', {'list1': dockslip_1, 'list2': dockslip_2, 'list3': dockslip_3})


class ItemTaggingCreateView(cv):
    model = ItemTagging
    form_class = ItemTaggingForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect('/dashboard/worker')


def deleteitem(request, id):
    idmas = ItemRecieveMaster.objects.get(RecieveID=id)
    idmas.delete()
    return redirect('ita')


def delete_item(request, id):
    idmas = ItemRecieveDetails.objects.get(RecieveId=id)
    idmas.delete()
    return redirect('itemdetails')


def deletedetail(request, id):
    ordmas = ItemRecieveDetails.objects.get(Recieveid=id)
    ordmas.delete()

    return redirect()


def allzonelist(request):
    form = Zone_Area.objects.all()
    return render(request, 'authentication/allzone_list.html', {'form': form})


def allbinlist(request):
    form = Bin.objects.all()
    return render(request, 'authentication/allbin_list.html', {'form': form})

def binapi(request,id):
    bins= b.objects.filter(ZoneId=z_a.objects.get(ZoneId=id))
    print(bins)
    return JsonResponse([{'binId':X.BinId,
    'binName':X.BinName} for X in bins],safe=False)
