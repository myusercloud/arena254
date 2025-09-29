from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Category


def index(request):
    """
    Render the homepage with all products displayed as cards.
    Includes search (q) and category filter.
    """
    query = request.GET.get('q')  # search term
    category_id = request.GET.get('category')  # category filter
    products = Product.objects.prefetch_related('images').all()

    # Apply search filter
    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    # Apply category filter
    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all().order_by('name')

    context = {
        'products': products,
        'query': query,
        'categories': categories,
    }
    return render(request, 'store/index.html', context)


def product_detail_json(request, pk):
    """
    Return product details as JSON for the modal view.
    """
    product = get_object_or_404(Product, pk=pk)

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
