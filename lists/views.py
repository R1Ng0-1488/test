from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Item
# Create your views here.

def home_page(request):
	'''home page'''
	return render(request, 'home.html')

def view_list(request):
	'''view of list'''
	items = Item.objects.all()
	return render(request, 'list.html', {"items": items})

def new_list(request):
	'''new list'''
	Item.objects.create(text=request.POST['item_text'])
	return redirect('/lists/one-list-in-the-world/')
