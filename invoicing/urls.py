# invoicing/urls.py
from django.urls import path, include
from .views import invoice_list
from .views import DownloadPDFView 
from .views import CustomSignupView
from .views import client_dashboard, client_login_redirect
from .views import view_invoices, view_invoice_details, make_payment, payment_notification, paypal_payment
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('invoices/', invoice_list, name='invoice_list'),
    path('download-pdf/<int:pk>/', DownloadPDFView.as_view(), name='download_pdf'),
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    path('dashboard/', client_dashboard, name='client_dashboard'),
    path('accounts/login/', client_login_redirect, name='account_login'),  # Redirect login to dashboard

    path('view-invoices/', view_invoices, name='view_invoices'),
    path('view_invoice_details/<int:invoice_id>/', view_invoice_details, name='view_invoice_details'),
    path('view_invoice_details/<int:pk>/', view_invoice_details, name='view_invoice_details'),
    path('make-payment/<int:invoice_id>/', make_payment, name='make_payment'),
    path('paypal-payment/<int:invoice_id>/', paypal_payment, name='paypal_payment'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('paypal-ipn/', include('paypal.standard.ipn.urls')),
    path('payment_notification/', payment_notification, name='payment_notification'),

]
