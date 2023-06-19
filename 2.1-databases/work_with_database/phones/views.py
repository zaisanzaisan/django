from django.shortcuts import render, redirect, get_object_or_404
from .models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort_by = request.GET.get('sort')
    phones = Phone.objects.all()
    if sort_by:
        phones = Phone.objects.order_by(sort_by)

    context = {
        'phones': phones,
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    product = get_object_or_404(Phone, slug=slug)
    context = {
        'phone': product,
    }
    return render(request, template, context)


