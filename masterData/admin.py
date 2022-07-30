from django.contrib import admin
from .models import (ItemRecieveDetails, ItemRecieveMaster, OrderProcessing,
                     OrderApproval,
                     DispatchOrder,
                     Inventory,
                     DispatchOrderDetail, Supplier,
                     Customer, OrderRecieveMaster,
                     OrderRecieveDetail,
                     ReceiveApproval, ItemTagging,
                     NewUser,
                     ItemMaster, WareHouse, Zone_Area, Bin, Role)

admin.site.register(OrderProcessing)
admin.site.register(OrderApproval)
admin.site.register(DispatchOrder)
admin.site.register(Inventory)
admin.site.register(DispatchOrderDetail)
admin.site.register(Supplier)
admin.site.register(ItemRecieveMaster)
admin.site.register(ItemRecieveDetails)
admin.site.register(Customer)
admin.site.register(OrderRecieveMaster)
admin.site.register(OrderRecieveDetail)
admin.site.register(ReceiveApproval)
admin.site.register(ItemTagging)
admin.site.register(NewUser)
admin.site.register(ItemMaster)
admin.site.register(Role)

# Register your models here.
admin.site.register(WareHouse)
admin.site.register(Zone_Area)
admin.site.register(Bin)
