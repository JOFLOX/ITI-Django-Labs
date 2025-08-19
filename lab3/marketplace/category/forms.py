from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter category description',
                'required': True
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom styling and validation
        for field_name, field in self.fields.items():
            if field_name != 'image':
                field.widget.attrs.update({'class': 'form-control'})
            
        # Add help text
        self.fields['name'].help_text = 'Choose a unique name for your category'
        self.fields['description'].help_text = 'Provide a detailed description of this category'
        self.fields['image'].help_text = 'Upload an image to represent this category (optional)'
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Check for duplicate names (excluding current instance if editing)
            qs = Category.objects.filter(name__iexact=name)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('A category with this name already exists.')
        return name
