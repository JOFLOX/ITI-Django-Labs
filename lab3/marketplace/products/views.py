from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Product
import uuid

# Create your views here.

def product_list(request):
    """Display all products with pagination"""
    products = Product.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            name__icontains=search_query
        ) | products.filter(
            description__icontains=search_query
        ) | products.filter(
            code__icontains=search_query
        )

    # Pagination
    paginator = Paginator(products, 6)  # Show 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_products': products.count()
    }
    return render(request, 'products/list.html', context)

def product_detail(request, pk):
    """Display single product details"""
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product
    }
    return render(request, 'products/detail.html', context)

def product_create(request):
    """Create a new product"""
    from category.models import Category

    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        instock = request.POST.get('instock')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        # Validation
        if not all([name, price, description, instock, category_id]):
            messages.error(request, 'All fields are required!')
            categories = Category.objects.all()
            return render(request, 'products/create.html', {'categories': categories})

        try:
            category = Category.objects.get(id=category_id)
            # Create product
            product = Product.objects.create(
                name=name,
                price=float(price),
                description=description,
                instock=int(instock),
                category=category,
                image=image,
                code=str(uuid.uuid4())[:8].upper()
            )
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('products:detail', pk=product.pk)
        except Category.DoesNotExist:
            messages.error(request, 'Invalid category selected!')
            categories = Category.objects.all()
            return render(request, 'products/create.html', {'categories': categories})
        except ValueError as e:
            messages.error(request, 'Invalid price or stock value!')
            categories = Category.objects.all()
            return render(request, 'products/create.html', {'categories': categories})
        except Exception as e:
            messages.error(request, f'Error creating product: {str(e)}')
            categories = Category.objects.all()
            return render(request, 'products/create.html', {'categories': categories})

    categories = Category.objects.all()
    return render(request, 'products/create.html', {'categories': categories})

def product_delete(request, pk):
    """Delete a product"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('products:list')

    context = {
        'product': product
    }
    return render(request, 'products/delete.html', context)
