from audioop import maxpp
from cgi import test
from statistics import mode
from time import time, timezone
from django.db import models
from django.core.validators import MinValueValidator
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from masterData.models import Zone_Area as z_a
from masterData.models import Bin as b

'''class User(models.Model):
   
   
    username = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=100, null=False)


class  Role(models.Model) :
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    
    role=models.CharField(
        choices=(('M','Manager'),('S','Supervisor'),('w','Worker')),max_length=1, null=True)
  

    #def __str__(self) -> str:
    #    return self().__str__()
'''

'''class Goods(models.Model):

    receiveID = models.CharField(max_length=10)
    receiveDate = models.DateTimeField(auto_now_add=True)
    supplierName = models.CharField(max_length=100,)
    vehicleNo = models.CharField(max_length=20)

    itemCode = models.CharField(max_length=10)
    itemDescription = models.CharField(max_length=100)
    batchNo = models.CharField(max_length=10)
    receiveQty = models.IntegerField(validators=[MinValueValidator(0)])
'''

FLAG_TYPE_CHOICES = (
    ('false', 'false'),
    ('true', 'true'),
)


ITEM_CATEGORY_CHOICES_ITEMCODE = (
    ('1000', 'Sensor'),
    ('1001', 'Engine'),
    ('1002', 'Camera'),
    ('1003', 'Cormen'),
    ('1004', 'Campbell'),
    ('1005', 'Thomas Calculus'),
    ('1006', 'Swevel chair'),
    ('1007', 'Minika Sofa'),
    ('1008', 'Lamp Shed'),
    ('1009', 'Olives'),
    ('1010', 'Jalapeno'),
    ('1011', 'Paparika'),
    ('1012', 'Paracitamol'),
    ('1013', 'Sorbitol'),
    ('1014', 'Cetrizine'),
)

class Supplier(models.Model):  # done
    SupplierId = models.AutoField(primary_key=True)
    SupplierName = models.CharField(max_length=256)
    SupplierAddress = models.CharField(max_length=256)
    SupplierCity = models.CharField(max_length=256)
    ContactNumber = models.CharField(max_length=20)

    def __str__(self):
        return str(self.SupplierName)


class ItemRecieveMaster(models.Model):
    RecieveID = models.AutoField(primary_key=True)
    RecieveDate = models.DateTimeField(default=timezone.now)
    SupplierName = models.ForeignKey(Supplier,on_delete=models.CASCADE)
    # SupplierId=models.ForeignKey(Supplier,on_delete=models.CASCADE)

    VehicleNo = models.CharField(max_length=256)
    # UserId = models.ForeignKey(User,on_delete=models.CASCADE)#error giving to change    #one one field
    UserId = models.CharField(max_length=184)
    # has to be one one field not sure
    RecApprovalStatus = models.CharField(max_length=256, default='test')
    RecTaggingStatus = models.CharField(max_length=256, default='test')
    RecDockingStatus = models.CharField(max_length=256, default='test')

    #ItemDetails = models.ManyToManyField(ItemRecieveDetails)

    def __str__(self):
        return str(self.RecieveID)


class ItemRecieveDetails(models.Model):  # ---- to be done
    # taken form itemrecievemaster
    RecieveId = models.ForeignKey(ItemRecieveMaster, on_delete=models.CASCADE)
    ItemCode = models.CharField(max_length=20, choices=ITEM_CATEGORY_CHOICES_ITEMCODE, default='1000')
    ItemDescription = models.CharField(max_length=100)
    BatchNo = models.CharField(max_length=256)
    RecieveQty = models.IntegerField(validators=[MinValueValidator(0)])


    def __str__(self):
        return self.ItemCode


class ReceiveApproval(models.Model):
    RecApproalId = models.AutoField(primary_key=True)
    RecApproalDate = models.DateTimeField(default=timezone.now)
    RecieveID = models.CharField(max_length=256)
    Remarks = models.CharField(max_length=256)

    def __str__(self):
        return str(self.RecApproalId)





class DockAllocation(models.Model):
    AllocationId = models.AutoField(primary_key=True)
    ReceiveId = models.ForeignKey(ItemRecieveMaster, on_delete=models.CASCADE)
    QRCode = models.CharField(max_length=256)
    ZoneId = models.ForeignKey(z_a, on_delete=models.CASCADE)
    BinId= models.ForeignKey(b,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.AllocationId)

    # def __str__(self):
    #     return str(self.ItemId)


class ItemTagging(models.Model):
    ItemId = models.AutoField(primary_key=True)
    ItemCode = models.CharField(max_length=20)
    ReceiveId = models.CharField(max_length=100)
    BatchNo = models.CharField(max_length=100)
    QRCode = models.CharField(max_length = 256)
