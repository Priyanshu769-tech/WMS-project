
from django.forms import ModelForm
from .models import *
from django import forms
from django.db.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User

#(Ansh Gupta)
class CreateUserForm (UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
# widgets = {
#             'username': forms.TextInput(attrs={'id':"floatingText"}),
#             'email': forms.EmailInput(attrs={'id':"floatingInput"}),
#             'password1': forms.PasswordInput(attrs={'id':"floatingPassword"}),
#             'password2': forms.PasswordInput(attrs={'id':"floatingPassword2"})
#         }
  
  
#(Ansh Gupta)
class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = ['SupplierName', 'SupplierAddress', 'SupplierCity', 'ContactNumber']
        widgets = {
            'SupplierName': forms.TextInput(attrs={'class':'form-control'}),
            'SupplierAddress': forms.TextInput(attrs={'class':'form-control'}),
            'SupplierCity': forms.TextInput(attrs={'class':'form-control'}),
            'ContactNumber': forms.NumberInput(attrs={'class':'form-control'}),
        
        }

#(Ansh Gupta)
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['CustomerName', 'CustomerAddress', 'CustomerCity',  'CustomerEmail', 'ContactNumber']
        widgets = {
            'CustomerName': forms.TextInput(attrs={'class':'form-control'}),
            'CustomerAddress': forms.TextInput(attrs={'class':'form-control'}),
            'CustomerCity': forms.TextInput(attrs={'class':'form-control'}),
            'CustomerEmail': forms.EmailInput(attrs={'class':'form-control'}),
            'ContactNumber': forms.NumberInput(attrs={'class':'form-control'}),
            
        
        }
        
#(Ansh Gupta)
class OrderRecieveMasterForm(ModelForm):
    class Meta:
        model = OrderRecieveMaster
        fields = ['OrderId', 'CustomerId'] #customer id to be taken as a dropdown
        widgets = {
            'CustomerId': forms.Select(attrs={'class':'form-select'}),
        
        }
    def __init__(self, *args, **kwargs):
        super(OrderRecieveMasterForm, self).__init__(*args, **kwargs)
        self.fields['CustomerId'].label = "Customer Name"
#(Rishabh Baranwal)
class OrderRecieveDetailForm(ModelForm):
    class Meta:
        model = OrderRecieveDetail
        exclude = ('OrderId',)
        fields = ['ItemCode', 'BatchNo', 'Qty']
        widgets = {
            'ItemCode': forms.Select(attrs={'class':'form-select'}),
            'BatchNo': forms.NumberInput(attrs={'class':'form-control'}),
            'Qty': forms.NumberInput(attrs={'class':'form-control'}),
        
        }
    def __init__(self, *args, **kwargs):
        super(OrderRecieveDetailForm, self).__init__(*args, **kwargs)
        self.fields['ItemCode'].label = "Item Name"
        self.fields['Qty'].label = "Quantity"
        self.fields['BatchNo'].label = "Batch Number"


#(Rishabh Baranwal)
class OrderProcessingForm(ModelForm):
    class Meta:
        model = OrderProcessing
        exclude = ('OrderId','ZoneId','BinId',)
        fields = ['Remarks']
        widgets = {
            'Remarks': forms.TextInput(attrs={'class':'form-control'})
        }
    
#(Rishabh Baranwal)
class OrderApprovalForm(ModelForm):
    class Meta:
        model = OrderApproval
        exclude = ('OrderId',)
        fields = ['Remarks']
        widgets = {
            'Remarks': forms.TextInput(attrs={'class':'form-control'}),
        
        }
#(Rishabh Baranwal)
class ItemRecieveMasterForm(ModelForm):
    class Meta:
        model = ItemRecieveMaster
        fields = ['SupplierId', 'VechileNo', 'RecApprovalStatus', 'RecTaggingStatus', 'RecDockingStatus']
        
        
#(Kumar Krish)

class ItemRecieveDetailsForm(ModelForm):
    class Meta:
        model = ItemRecieveDetails
        fields = ['RecieveId','ItemCode', 'BatchNo', 'RecieveQty']
        
#(Swapnaneel Basu)
class UserForm(ModelForm):
    class Meta:
        model = NewUser
        fields = ['UserName', 'MgrId', 'RoleName']
        
#(Kumar Krish)


class WarehouseForm(ModelForm):
    class Meta:
        model = WareHouse
        fields = ['WareHouseName', 'WareHouseAddress']
        widgets = {
            'WareHouseName': forms.TextInput(attrs={'class':'form-control'}),
            'WareHouseAddress': forms.TextInput(attrs={'class':'form-control'}),
        
        }
#(Kumar Krish)

class Zone_AreaForm(ModelForm):
    # WareHouseId=forms.ModelChoiceField(queryset=models.Warehouse.objects.all().filter(status=True),empty_label="Select Warehouse", to_field_name="WareHouseId")
    class Meta:
        model = Zone_Area
        fields = ['ZoneName','WareHouseId']
        widgets = {
            'ZoneName': forms.TextInput(attrs={'class':'form-control'}),
            'WareHouseId': forms.Select(attrs={'class':'form-select'}),
        
        }
    def __init__(self, *args, **kwargs):
        super(Zone_AreaForm, self).__init__(*args, **kwargs)
        self.fields['ZoneName'].label = "Zone Name"
        self.fields['WareHouseId'].label = "Warehouse Name"
#(Kumar Krish)

class BinForm(ModelForm):
    class Meta:
        model = Bin
        fields = ['BinName','ZoneId']
        widgets = {
            'BinName': forms.TextInput(attrs={'class':'form-control'}),
            'ZoneId': forms.Select(attrs={'class':'form-select'}),
        
        }
    def __init__(self, *args, **kwargs):
        super(BinForm, self).__init__(*args, **kwargs)
        self.fields['BinName'].label = "Bin Name"
        self.fields['ZoneId'].label = "Zone Name"


#(Swapnaneel Basu)

class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['BinId', 'ItemCode', 'MovementType', 'Qty']
        widgets = {
            'BinId': forms.Select(attrs={'class':'form-select'}),
            'ItemCode': forms.Select(attrs={'class':'form-select'}),
            'MovementType': forms.Select(attrs={'class':'form-select'}),
            'Qty': forms.NumberInput(attrs={'class':'form-control'}),
        
        }
        
#(Urvish Mehta)
class ReceiveApprovalForm(ModelForm):
    class Meta:
        model = ReceiveApproval
        fields = ['Remarks']
        
#(Urvish Mehta)
class ItemTaggingForm(ModelForm):
    class Meta:
        model = ItemTagging
        fields = ['ItemId','ItemCode', 'BatchNo', 'QRCode', 'QRCodeImage', 'QRCodeImgPath']
#(Urvish Mehta)
class ItemMasterForm(ModelForm):
    class Meta:
        model = ItemMaster
        fields = ['ItemCode','ItemDescription', 'ItemCategory', 'MovementType', 'ItemSKU', 'ItemMaxStock', 'ItemMinStock', 'PreferZone']
        
        
        
# class DispatchOrderForm(ModelForm):
#     class Meta:
#         model = DispatchOrder
#         fields = ['VechileNo', 'ASNStatus']

# class DispatchOrderDetailForm(ModelForm):
#     class Meta:
#         model = DispatchOrderDetail
#         fields = ['ItemCode','BatchNo', 'QRCode']

