from django.contrib import admin 
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'created_at')  # show creation date too
    list_filter = ('category', 'created_at')  # ✅ filter sidebar
    search_fields = ('title', 'description')  # ✅ search box
    ordering = ('-created_at',)  # ✅ newest products first
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # show slug in list
    search_fields = ('name',)  # ✅ search categories
    prepopulated_fields = {'slug': ('name',)}
