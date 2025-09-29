from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product

def index(request):
    """
    Render the homepage with all products displayed as cards.
    """
    products = Product.objects.prefetch_related('images').all()
    return render(request, 'store/index.html', {'products': products})


def product_detail_json(request, pk):
    """
    Return product details as JSON for the modal view.
    """
    product = get_object_or_404(Product, pk=pk)

    # Build absolute URLs for images
    images = [request.build_absolute_uri(img.image.url) for img in product.images.all()]
    
    data = {
        'id': product.id,
        'title': product.title,
        'description': product.description,
        'price': str(product.price) if product.price else None,
        'featured_image': request.build_absolute_uri(product.featured_image.url) if product.featured_image else None,
        'images': images,
    }
    return JsonResponse(data)
