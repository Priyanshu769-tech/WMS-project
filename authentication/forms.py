# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import User
# from django.forms import ModelForm
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

'''
import pickle
from django.http import HttpResponse
from django import forms
from django.template import Context,Template
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import MinValueValidator
'''

# class NewUserForm(forms.ModelForm):
# 	username=forms.TextInput()
# 	password=forms.PasswordInput()
# 	email = forms.EmailField(required=True)

# 	class Meta:
# 		model = User
# 		fields = ["username", "email", "password",]
# 		widgets = {
#             'username': forms.TextInput(attrs={'class':'form-control'}),
#             'email': forms.TextInput(attrs={'class':'form-control'}),
#             'password': forms.PasswordInput(render_value=True, attrs={'class':'form-control'}),
			

#         }

# 	def save(self, commit=True):
# 		User = super(NewUserForm, self).save(commit=False)
# 		User.email = self.cleaned_data['email']
# 		if commit:
# 			User.save()
# 		return User

class CreateUserForm (UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


'''
class MultiWidgetBasic(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(),
                   forms.TextInput(),
				   forms.TextInput(),
				   forms.NumberInput()]
        super(MultiWidgetBasic, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return pickle.loads(value)
        else:
            return ['', '', '', '']

class MultiExampleField(forms.fields.MultiValueField):
    widget = MultiWidgetBasic

    def __init__(self, *args, **kwargs):
        list_fields = [forms.fields.CharField(max_length=10),
                       forms.fields.CharField(max_length=100),
					   forms.fields.CharField(max_length=10),
					   forms.fields.IntegerField(validators=[MinValueValidator(0)])]
        super(MultiExampleField, self).__init__(list_fields, *args, **kwargs)

    def compress(self, values):
        ## compress list to single object                                               
        ## eg. date() >> u'31/12/2012'                                                  
        return pickle.dumps(values)

class GoodsReceivedForm (forms.Form):
	a = forms.BooleanField()
    b = forms.CharField(max_length=32)
    c = forms.CharField(max_length=32, widget=forms.widgets.Textarea())
    d = forms.CharField(max_length=32, widget=forms.widgets.SplitDateTimeWidget())
    e = forms.CharField(max_length=32, widget=MultiWidgetBasic())
    f = MultiExampleField()
'''
'''
class GoodsReceivedForm (ModelForm):
	class Meta:
		model = ItemRecieveDetails
		fields = '__all__'

	def save(self, commit:True):
		Goods = super(GoodsReceivedForm, self).save(commit=True)
		if commit:
			Goods.save()
		return Goods
'''

class ItemRecieveMasterForm(ModelForm):
    class Meta:
        model = ItemRecieveMaster
        fields = ['RecieveID', 'SupplierName', 'VehicleNo']
        widgets = {
            'SupplierName': forms.Select(attrs={'class':'form-select'}),
            'VehicleNo': forms.TextInput(attrs={'class':'form-control'}),
        
        }


class ItemRecieveDetailsForm(ModelForm):
    class Meta:
        model = ItemRecieveDetails
        exclude = ('RecieveId',)
        fields = ['ItemCode','BatchNo', 'RecieveQty']
        widgets = {
            
            'ItemCode':forms.Select(attrs={'class':'form-select'}),
       
            'BatchNo': forms.TextInput(attrs={'class':'form-control'}),
            'RecieveQty': forms.NumberInput(attrs={'class':'form-control'}),
        
        }
    def __init__(self, *args, **kwargs):
        super(ItemRecieveDetailsForm, self).__init__(*args, **kwargs)
        self.fields['ItemCode'].label = "Item Name"
    
        self.fields['BatchNo'].label = "Batch No"
        self.fields['RecieveQty'].label = "Quantity"


class ReceiveApprovalForm(ModelForm):
    class Meta:
        model = ReceiveApproval
        fields = ['Remarks']
        widgets = {
            'Remarks': forms.TextInput(attrs={'class':'form-control'}),
        }

class DockAllocationForm(ModelForm):
    class Meta:
        model = DockAllocation
        exclude = ('RecieveId', 'ZoneId', 'BinId',)
        fields = ['AllocationId',]
        
    # def __init__(self, *args, **kwargs):
    #     super(DockAllocationForm, self).__init__(*args, **kwargs)
    #     self.fields['ZoneId'].label = "Zone Name"
    #     self.fields['BinId'].label = "Bin Name"







class SupplierForm(ModelForm):

    class Meta:
        model=Supplier
        fields=['SupplierName','SupplierAddress','SupplierCity','ContactNumber']
        widgets = {
            'SupplierName': forms.TextInput(attrs={'class':'form-control'}),
            'SupplierAddress': forms.TextInput(attrs={'class':'form-control'}),
            'SupplierCity': forms.TextInput(attrs={'class':'form-control'}),
            'ContactNumber': forms.NumberInput(attrs={'class':'form-control'}),
        
        }

class ItemTaggingForm(ModelForm):
    class Meta:
        model = ItemTagging
        fields = ['ItemCode', 'BatchNo','ReceiveId','QRCode']
        widgets = {
            'ItemCode': forms.TextInput(attrs={'class':'form-control'}),
            'BatchNo': forms.TextInput(attrs={'class':'form-control'}),
            'ReceiveId': forms.TextInput(attrs={'class':'form-control'}),
            'QRCode': forms.TextInput(attrs={'class':'form-control'}),
        }
        

       