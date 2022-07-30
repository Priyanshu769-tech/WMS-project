from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

def items(request):
    return render(request, 'dashboard/items.html')

def orders(request):
    return render(request, 'dashboard/orders.html')