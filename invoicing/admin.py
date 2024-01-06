# invoicing/admin.py
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
# from django.contrib import admin
from .models import Client, Company, Invoice

from .models import Client



admin.site.site_header = 'Africa Calling Safaris Invoicing System Admin'
admin.site.site_title = 'Africa Calling Safaris Admin'

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'download_pdf_link']

    def download_pdf_link(self, obj):
        url = reverse('generate_pdf', kwargs={'pk': obj.pk})
        return format_html(f'<a href="{url}" target="_blank">Download PDF</a>')

    download_pdf_link.short_description = 'Download PDF'

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'client', 'issue_date', 'prepared_by')

    def save_model(self, request, obj, form, change):
        # Set prepared_by to the username of the logged-in admin user
        obj.prepared_by = request.user.username
        super().save_model(request, obj, form, change)

admin.site.register(Client)
admin.site.register(Company)
admin.site.register(Invoice, InvoiceAdmin)
# admin.site.register(Client)
