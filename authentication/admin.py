from django.contrib import admin
from .models import ItemRecieveMaster, ItemRecieveDetails, DockAllocation, ItemTagging, Supplier, ReceiveApproval

# Register your models here.
# admin.site.register(User)
# class UserAdmin(admin.ModelAdmin):
#    readonly_fields = ('username','email','password',)

# admin.site.register(Role)
# admin.site.register(Goods)
admin.site.register(ItemRecieveDetails)
admin.site.register(ItemRecieveMaster)
admin.site.register(DockAllocation)


admin.site.register(ReceiveApproval)
admin.site.register(ItemTagging)
admin.site.register(Supplier)


# admin.site.register(Role)
