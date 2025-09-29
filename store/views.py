from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product

def index(request):
    products = Product.objects.prefetch_related('images').all()
    return render(request, 'store/index.html', {'products': products})

def product_detail_json(request, pk):
    p = get_object_or_404(Product, pk=pk)
    images = [request.build_absolute_uri(img.image.url) for img in p.images.all()]
    data = {
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'price': str(p.price) if p.price else None,
        'featured_image': request.build_absolute_uri(p.featured_image.url) if p.featured_image else None,
        'images': images,
    }
    return JsonResponse(data)
