from django.contrib import admin

from .models import CustomerProfile, Address, SupportTicket, NewsletterSubscriber



@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone", "created_at"]
    search_fields = ["user__username", "user__email", "phone"]

    
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["recipient_name", "user", "city", "state", "country", "is_default"]
    list_filter = ["country", "is_default"]
    search_fields = ["recipient_name", "user__username", "city", "phone"]


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ["ticket_number", "name", "email", "inquiry_type", "product_name", "status", "created_at"]
    list_filter = ["status", "inquiry_type", "created_at"]
    search_fields = ["ticket_number", "name", "email", "subject", "product_name", "order_number"]


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["email"]