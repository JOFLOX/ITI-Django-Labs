# Django Labs - Learning Django Framework

This repository contains three progressive Django labs designed to teach Django web development concepts from basic to advanced levels.

## Overview

Each lab builds upon the previous one, introducing new Django concepts and best practices:

- **Lab1**: Basic Django project setup and URL routing
- **Lab2**: Models, database integration, and CRUD operations
- **Lab3**: Advanced relationships, generic views, and ModelForms

---

## Lab 1: Basic Django Project Setup

### 📁 Project Structure
```
lab1/marketPlace/
├── manage.py
├── marketPlace/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── products/
├── contactus/
└── aboutus/
```

### 🎯 Django Concepts Covered

#### 1. **Project and App Creation**
```bash
django-admin startproject marketPlace
python manage.py startapp products
python manage.py startapp contactus
python manage.py startapp aboutus
```

#### 2. **Settings Configuration**
- Added apps to `INSTALLED_APPS`
- Basic Django settings understanding

#### 3. **URL Configuration**
- **Project-level URLs** (`marketPlace/urls.py`):
```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('contactus/', include('contactus.urls')),
    path('aboutus/', include('aboutus.urls')),
]
```

- **App-level URLs** (e.g., `products/urls.py`):
```python
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='products_index'),
]
```

#### 4. **Basic Views**
- Function-based views
- HttpResponse usage
```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Welcome to Products Page</h1>")
```

### 🔧 Key Learning Points
- Django project vs app concept
- URL routing and namespacing
- Basic view creation
- Django development server

---

## Lab 2: Models, Database, and CRUD Operations

### 📁 Project Structure
```
lab2/marketplace/
├── manage.py
├── marketplace/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── products/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── templates/
├── static/
└── media/
```

### 🎯 Django Concepts Covered

#### 1. **Model Definition**
```python
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Product Name")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    instock = models.PositiveIntegerField(default=0)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'pk': self.pk})
```

#### 2. **Database Operations**
- **Migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

- **Model Methods**: Custom save method, string representation
- **Meta Options**: Ordering, verbose names

#### 3. **Admin Interface**
```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'price', 'instock', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['code', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'instock')
        }),
    )
```

#### 4. **CRUD Views (Function-Based)**
```python
def product_list(request):
    products = Product.objects.all()
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Pagination
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/list.html', {'page_obj': page_obj})

def product_create(request):
    if request.method == 'POST':
        # Handle form submission without Django forms
        name = request.POST.get('name')
        price = request.POST.get('price')
        # ... validation and creation logic
        product = Product.objects.create(...)
        return redirect('products:detail', pk=product.pk)
    
    return render(request, 'products/create.html')
```

#### 5. **Template System**
- **Template Inheritance**: Base template with blocks
- **Template Tags**: URL reversing, filters
- **Static Files**: CSS, JavaScript, images
- **Media Files**: User-uploaded content

#### 6. **URL Namespacing**
```python
# products/urls.py
app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('create/', views.product_create, name='create'),
    path('<int:pk>/', views.product_detail, name='detail'),
    path('<int:pk>/delete/', views.product_delete, name='delete'),
]
```

### 🔧 Key Learning Points
- Django ORM and model fields
- Database migrations
- Admin interface customization
- Template inheritance and context
- Static and media file handling
- Pagination implementation
- Search functionality
- CRUD operations without forms

---

## Lab 3: Advanced Relationships and Generic Views

### 📁 Project Structure
```
lab3/marketplace/
├── manage.py
├── marketplace/
├── products/
├── category/          # New app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   └── urls.py
├── templates/
│   ├── base.html
│   ├── products/
│   └── category/      # New templates
└── static/
```

### 🎯 Django Concepts Covered

#### 1. **Model Relationships**
```python
# category/models.py
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_products_count(self):
        return self.products.count()  # Using related_name

# products/models.py (updated)
class Product(models.Model):
    # ... existing fields
    category = models.ForeignKey(
        'category.Category', 
        on_delete=models.CASCADE, 
        related_name='products'
    )
```

#### 2. **ModelForms**
```python
# category/forms.py
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        # Custom validation logic
        return name
```

#### 3. **Generic Class-Based Views**
```python
# category/views.py
class CategoryListView(ListView):
    model = Category
    template_name = 'category/list.html'
    context_object_name = 'categories'
    paginate_by = 8
    
    def get_queryset(self):
        queryset = Category.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('category:list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Category "{form.instance.name}" created!')
        return super().form_valid(form)

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category/detail.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add related products with pagination
        products = self.object.products.all()
        paginator = Paginator(products, 6)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        return context
```

#### 4. **Advanced Querying**
```python
# Using Q objects for complex queries
from django.db.models import Q

queryset = Category.objects.filter(
    Q(name__icontains=search_query) |
    Q(description__icontains=search_query)
)

# Related object access
category = Category.objects.get(pk=1)
products_in_category = category.products.all()  # Using related_name
product_count = category.products.count()
```

#### 5. **Form Handling and Validation**
```python
# Custom form validation
def clean_name(self):
    name = self.cleaned_data.get('name')
    if name:
        qs = Category.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Category with this name exists.')
    return name

# View-level form handling
def form_valid(self, form):
    messages.success(self.request, 'Category created successfully!')
    return super().form_valid(form)

def form_invalid(self, form):
    messages.error(self.request, 'Please correct the errors below.')
    return super().form_invalid(form)
```

### 🔧 Key Learning Points
- ForeignKey relationships and related_name
- Generic class-based views (ListView, DetailView, CreateView, UpdateView, DeleteView)
- ModelForms and form validation
- Complex database queries with Q objects
- Context data manipulation in CBVs
- Message framework integration
- Advanced admin customization

---

## 🚀 Running the Labs

### Prerequisites
```bash
pip install Django==5.2.5
pip install Pillow  # For ImageField support
```

### For each lab:
```bash
cd lab[1|2|3]/[project_name]
python manage.py migrate
python manage.py createsuperuser  # For labs 2 & 3
python manage.py runserver
```

---

## 📚 Django Concepts Progression

| Concept | Lab 1 | Lab 2 | Lab 3 |
|---------|-------|-------|-------|
| Project Setup | ✅ | ✅ | ✅ |
| URL Routing | ✅ | ✅ | ✅ |
| Function-Based Views | ✅ | ✅ | ✅ |
| Models & ORM | ❌ | ✅ | ✅ |
| Admin Interface | ❌ | ✅ | ✅ |
| Templates | ❌ | ✅ | ✅ |
| Static/Media Files | ❌ | ✅ | ✅ |
| CRUD Operations | ❌ | ✅ | ✅ |
| Model Relationships | ❌ | ❌ | ✅ |
| Generic Views | ❌ | ❌ | ✅ |
| ModelForms | ❌ | ❌ | ✅ |
| Advanced Querying | ❌ | ❌ | ✅ |

---

## 🎓 Learning Outcomes

By completing these labs, you will understand:

1. **Django Architecture**: MVT pattern, project vs app structure
2. **Database Integration**: Models, migrations, ORM queries
3. **View Patterns**: Function-based vs class-based views
4. **Template System**: Inheritance, context, tags, and filters
5. **Form Handling**: Manual forms vs ModelForms
6. **Admin Interface**: Customization and management
7. **URL Design**: Routing, namespacing, and reversing
8. **Relationships**: ForeignKey, related objects, and queries
9. **Best Practices**: Code organization, validation, and error handling

Each lab represents a realistic development scenario, progressing from simple static pages to a full-featured web application with database relationships and modern Django patterns.
