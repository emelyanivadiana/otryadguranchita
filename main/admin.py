from django.contrib import admin
from .models import *

@admin.register(FoundationInfo)
class FoundationInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date', 'is_published', 'views_count']
    list_filter = ['is_published', 'published_date']
    search_fields = ['title', 'content']

@admin.register(FundraisingGoal)
class FundraisingGoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'target_amount', 'current_amount', 'status', 'progress_percentage']
    list_filter = ['status', 'priority']
    search_fields = ['title', 'description']

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'amount', 'payment_method', 'payment_status', 'created_at']
    list_filter = ['payment_method', 'payment_status', 'created_at']
    search_fields = ['donor_name', 'donor_email']

@admin.register(ExpenseReport)
class ExpenseReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'amount_spent', 'goal', 'report_date']
    list_filter = ['report_type', 'report_date']
    search_fields = ['title', 'description']

@admin.register(ExpensePhoto)
class ExpensePhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title']
# Register your models here.
