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
    Includes a unified all_images list.
    """
    product = get_object_or_404(Product, pk=pk)

    # Build full image URLs
    all_images = []
    if product.featured_image:
        all_images.append(request.build_absolute_uri(product.featured_image.url))
    all_images += [request.build_absolute_uri(img.image.url) for img in product.images.all()]

    data = {
        'id': product.id,
        'title': product.title,
        'description': product.description,
        'price': str(product.price) if product.price else None,
        'all_images': all_images,
    }
    return JsonResponse(data)
