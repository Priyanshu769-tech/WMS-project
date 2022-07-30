from pyexpat import model
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save


#(Rishabh Baranwal)
ITEM_CATEGORY_CHOICES = (
    ('Sensor', 'Sensor'),
    ('Engine', 'Engine'),
    ('Camera', 'Camera'),
    ('Cormen', 'Cormen'),
    ('Campbell', 'Campbell'),
    ('Thomas Calculus', 'Thomas Calculus'),
    ('Swevel chair', 'Swevel chair'),
    ('Minika Sofa', 'Minika Sofa'),
    ('Lamp Shed', 'Lamp Shed'),
    ('Olives', 'Olives'),
    ('Jalapeno', 'Jalapeno'),
    ('Paparika', 'Paparika'),
    ('Paracitamol', 'Paracitamol'),
    ('Sorbitol', 'Sorbitol'),
    ('Cetrizine', 'Cetrizine'),
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


ITEM_SKU_CHOIES = (
    ('pcs', 'Pcs'),
    ('box', 'Box'),
)
#
#
# did not find its purpose in any of classes
INVENTORY_TYPE_CHOICES = (
    ('fast-moving', 'Fast Moving'),
    ('slow-moving', 'Slow Moving'),
    ('seasonal', 'Seasonal'),
)
#
#
#
ITEM_MOVEMENT_TYPE_CHOICES = (
    ('fifo', 'FIFO'),
    ('lifo', 'LIFO'),
    ('random', 'RANDOM'),
)
ROLENAME_CHOICES = (
    ('worker', 'Worker'),
    ('supervisor', 'Supervisor'),
    ('customer', 'Customer'),
    ('supplier', 'Supplier'),
)
FLAG_TYPE_CHOICES = (
    ('false', 'false'),
    ('true', 'true'),
)

# all many to one or one to many relations are made by using foreign key concepts

# order for order dispatch will be - warehouse - zone - bin - orderecievemaster- orderapproval - orderrecievedetails(to be done by the worker) - orderprocessing - inventory - orderdispatch - dispatchdetails

# order for item recieve will be - warehouse - zone - bin - itemrecievemaster- recieveapproval - itemrecievedetails(to be done by the worker) -inventory- dockallocation - itemtagging - itemaster

# for orderrecievemaster, itemrecievemaster user coming from superuser

# the basic user model that has user roles(Ansh Gupta)
# 

#Ansh Gupta
class Role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_worker = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=not True)
    is_supervisor = models.BooleanField(default=not True)

    def __str__(self):
        return self.user.username + 'Role'

# Ansh Gupta
def create_user_role(sender, instance, created, *args, **kwargs):
    if created:
        newrole = Role.objects.create(user=instance)
        newrole.save()


post_save.connect(create_user_role, sender=User)


#(Rishabh Baranwal) model of new user
class NewUser(models.Model):
    UserId = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=50)
    MgrId = models.CharField(max_length=50)
    RoleName = models.CharField(
        max_length=15, choices=ROLENAME_CHOICES, default='worker')

    def __str__(self):
        return str(self.UserId)

# warehouse is a class that stores the information about the location of warehouse (Rishabh Baranwal)
class WareHouse(models.Model):  # done
    WareHouseId = models.AutoField(primary_key=True)
    WareHouseName = models.CharField(max_length=256)
    WareHouseAddress = models.CharField(max_length=256)

    def __str__(self):
        return str(self.WareHouseName)

# zone area is one column in warehouse which (Rishabh Baranwal)
class Zone_Area(models.Model):  # done
    ZoneId = models.AutoField(primary_key=True)
    ZoneName = models.CharField(max_length=256)
    WareHouseId = models.ForeignKey(WareHouse, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ZoneName)

# bin is one section in zone area (Rishabh Baranwal)
class Bin(models.Model):  # done
    BinId = models.AutoField(primary_key=True)
    BinName = models.CharField(max_length=256)
    ZoneId = models.ForeignKey(Zone_Area, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.BinName)

# supplier supplies item that are ordered by the warehouse (Urvish Mehta Kaushal)
class Supplier(models.Model):  # done
    SupplierId = models.AutoField(primary_key=True)
    SupplierName = models.CharField(max_length=256)
    SupplierAddress = models.CharField(max_length=256)
    SupplierCity = models.CharField(max_length=256)
    ContactNumber = models.CharField(max_length=20)

    def __str__(self):
        return str(self.SupplierId)

# customer orders order that have to be delivered by the warehouse (Ansh Gupta)
class Customer(models.Model):  # done
    CustomerId = models.AutoField(primary_key=True)  # auto generated
    CustomerName = models.CharField(max_length=256)
    CustomerAddress = models.CharField(max_length=256)
    CustomerCity = models.CharField(max_length=256)
    ContactNumber = models.CharField(max_length=15)  # Telephonic reference
    CustomerEmail = models.EmailField(max_length=256)

    def __str__(self):
        return str(self.CustomerName)


# to store the orders by customers (Ansh Gupta)
class OrderRecieveMaster(models.Model):  # 1
    OrderId = models.AutoField(primary_key=True)
    OrderDate = models.DateTimeField(default=timezone.now)
    CustomerId = models.ForeignKey(Customer, on_delete=models.CASCADE)  # randomly selected from DB
    # error giving to change   #one one field
    #UserId = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    isApproved = models.CharField(
        max_length=10, choices=FLAG_TYPE_CHOICES, default='false')

    def __str__(self):
        return str(self.OrderId)


# extension of order master that stores quantity and item code (Ansh Gupta)
class OrderRecieveDetail(models.Model):  # 2
    OrderId = models.ForeignKey(OrderRecieveMaster, on_delete=models.CASCADE)
    ItemCode = models.CharField(
        max_length=20, choices=ITEM_CATEGORY_CHOICES_ITEMCODE, default='1000')
    Qty = models.IntegerField(default=0)
    isApproved = models.CharField(
        max_length=10, choices=FLAG_TYPE_CHOICES, default='false')
    BatchNo = models.CharField(max_length=256, default=1000)

    def __str__(self):
        return str(self.id)

# this class contains complete detail of order which has to be process by the manager (Urvish Mehta Kaushal)
class OrderProcessing(models.Model):  # 3
    OPId = models.AutoField(primary_key=True)
    OPDate = models.DateTimeField(default=timezone.now)
    # one one field not sure # here this one ot one is scorrect
    OrderId = models.OneToOneField(
        OrderRecieveDetail, on_delete=models.CASCADE)
    Remarks = models.CharField(max_length=256, default="Processed")
    ZoneId = models.ForeignKey(Zone_Area, on_delete=models.CASCADE)
    BinId = models.ForeignKey(Bin, on_delete=models.CASCADE)
    # UserId = models.ForeignKey(NewUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.OPId)

# this class is for confirmation of the order processing, if it is apporved, the quantities will be changed in the warehouse (Yash Kadam)
class OrderApproval(models.Model):  # 4
    OdrApprovalId = models.AutoField(primary_key=True)
    OdrApprovalDate = models.DateTimeField(default=timezone.now)
    OrderId = models.OneToOneField(
        OrderRecieveMaster, on_delete=models.CASCADE)
    Remarks = models.CharField(max_length=256)

    def __str__(self):
        return str(self.OdrApprovalId)

# to store orders by warehouse (Yash Kadam)
class ItemRecieveMaster(models.Model):
    RecieveId = models.AutoField(primary_key=True)
    RecieveDate = models.DateTimeField(default=timezone.now)
    # randomly selected form the db
    SupplierId = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    VechileNo = models.CharField(max_length=256)
    # error giving to change    #one one field
    UserId = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    # has to be one one field not sure
    RecApprovalStatus = models.CharField(max_length=256)
    RecTaggingStatus = models.CharField(max_length=256)
    RecDockingStatus = models.CharField(max_length=256)

    def __str__(self):
        return str(self.RecieveId)

# extension of item master that stores quantity and item code (Swapnaneel Basu)
class ItemRecieveDetails(models.Model):  # ---- to be done
    # taken form itemrecievemaster
    RecieveId = models.ForeignKey(ItemRecieveMaster, on_delete=models.CASCADE)
    ItemCode = models.CharField(
        max_length=20, choices=ITEM_CATEGORY_CHOICES_ITEMCODE, default='1000')
    BatchNo = models.CharField(max_length=256)
    RecieveQty = models.IntegerField(default=0)

# approval for recieving goods, status check by manager (Yash Kadam)
class ReceiveApproval(models.Model):
    RecApproalId = models.AutoField(primary_key=True)
    RecApproalDate = models.DateTimeField(default=timezone.now)
    ReceiveId = models.ForeignKey(ItemRecieveMaster, on_delete=models.CASCADE)
    Remarks = models.CharField(max_length=300)
    UserId = models.ForeignKey(NewUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.RecApproalId)

# contains the information about the inventory, will increase decrease accordingly (Urvish Mehta Kaushal)
class Inventory(models.Model):  # ---- to be done
    ItemId = models.AutoField(primary_key=True)
    ItemCode = models.CharField(max_length=20, choices=ITEM_CATEGORY_CHOICES_ITEMCODE, default='1000')
    InvDate = models.DateTimeField(default=timezone.now)
    MovementType = models.CharField(max_length=10, choices=ITEM_MOVEMENT_TYPE_CHOICES, default='fifo')

    # TransactionId = models.ForeignKey()

    Qty = models.IntegerField(default=0)
    BinId = models.ForeignKey(Bin, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ItemId)

# this class is for the dispatch of order to the customer contains the movement type and other fields (Kumar Krish)
class DispatchOrder(models.Model):
    DispatchId = models.AutoField(primary_key=True)
    DispatchDate = models.DateTimeField(default=timezone.now)
    VehicleNo = models.CharField(max_length=256)
    ASNStatus = models.CharField(max_length=256, default = "false")
    GatePassStatus = models.CharField(max_length=256, default = "false")

    def __str__(self):
        return str(self.DispatchId)

# extension of dispatch order, with item information (Kumar Krish)
class DispatchOrderDetail(models.Model):  # ---- to be done
    DispatchId = models.CharField(max_length=256)
    ItemCode = models.CharField(max_length=256)
    BatchNo = models.CharField(max_length=256)
    QRCode = models.CharField(max_length=256)
    OrderId = models.CharField(max_length=256)

    def __str__(self):
        return str(self.DispatchId)

# before storing in bin, all items are docked (Kumar Krish)


# a tag generated for tagging the items that are recieved (Swapnaneel Basu)
class ItemTagging(models.Model):
    ItemId = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    ItemCode = models.CharField(
        max_length=20, choices=ITEM_CATEGORY_CHOICES_ITEMCODE, default='1000')
    RecApproalId = models.ForeignKey(
        ReceiveApproval, on_delete=models.CASCADE)  # check once
    ReceiveId = models.ForeignKey(ItemRecieveMaster, on_delete=models.CASCADE)
    SupplierId = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    BatchNo = models.CharField(max_length=100)
    QRCode = models.CharField(max_length=256)
    QRCodeImage = models.ImageField()  # defualt to be put
    QRCodeImgPath = models.CharField(max_length=256)
    UserId = models.ForeignKey(NewUser, on_delete=models.CASCADE)

# the very structure of each item in the warehouse (Swapnaneel Basu)
class ItemMaster(models.Model):  # ---- to be done
    ItemCode = models.CharField(
        max_length=20, choices=ITEM_CATEGORY_CHOICES_ITEMCODE, default='1000')
    ItemDescription = models.CharField(max_length=300)
    ItemCategory = models.CharField(
        max_length=15, choices=ITEM_CATEGORY_CHOICES, default='tv')
    MovementType = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    ItemSKU = models.CharField(
        max_length=10, choices=ITEM_SKU_CHOIES, default='pcs')
    ItemMaxStock = models.IntegerField(default=0)
    ItemMinStock = models.IntegerField(default=0)
    PreferZone = models.CharField(max_length=100)
