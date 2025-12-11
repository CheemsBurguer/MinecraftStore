from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest
from django.db.models import Q

def home(request: HttpRequest, category_slug=None):

    categories = None
    products = None

    if category_slug != None:

        categories = get_object_or_404(Category, category_slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('-created_date')
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        products = Product.objects.filter(is_available = True).order_by('-created_date')
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
    }

    return render(request, 'index.html', context)

def product_detail(request, category_slug=None, product_slug=None):

    try:
        single_product = Product.objects.get(category__category_slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart
    }

    return render(request, 'store/product.html', context)

def search(request: HttpRequest):
    if 'keyword' in request.GET:
        products = None
        product_count = 0
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword)).order_by('-created_date')
            product_count = products.count()


        context = {
            'products': products,
            'product_count': product_count,
        }

        return render(request, 'index.html',context=context)