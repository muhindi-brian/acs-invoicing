from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from django.views import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import login
from django.shortcuts import redirect

from django.views.decorators.csrf import csrf_exempt
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from .models import Invoice
from .models import Invoice, Company, Client, PaymentMethod  
from allauth.account.views import SignupView
from django.urls import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm


def invoice_list(request):
    company = Company.objects.first()
    return render(request, 'invoicing/invoice_list.html', {'company': company})

class CustomSignupView(SignupView):
    def form_valid(self, form):
        # Perform any additional actions before saving the form
        response = super().form_valid(form)

        # Automatically log in the user after signup
        self.user = self.form.save(self.request)
        login(self.request, self.user)

        return response


class DownloadPDFView(View):
    template_name = 'invoice_template.html'

    def get(self, request, *args, **kwargs):
        invoice = get_object_or_404(Invoice, pk=kwargs['pk'])
        template = get_template(self.template_name)
        html = template.render({'invoice': invoice})
        pdf_file = HTML(string=html).write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=invoice_{invoice.invoice_number}.pdf'
        return response




# def client_dashboard(request):
    # invoices = Invoice.objects.filter(client=request.user.client)
    # return render(request, 'client_dashboard.html', {'invoices': invoices})

def client_login_redirect(request):
    return redirect('/dashboard/')

@login_required
def client_dashboard(request):
    client = get_object_or_404(Client, user=request.user)
    invoices = Invoice.objects.filter(client=client)
    return render(request, 'invoicing/client_dashboard.html', {'invoices': invoices})
    # return render(request, 'invoicing/client_dashboard.html')

# def view_invoices(request):
    # client = get_object_or_404(Client, user=request.user)
    # invoices = Invoice.objects.filter(client=client)
    # return render(request, 'invoicing/view_invoices.html', {'invoices': invoices})   
# 

def view_invoices(request):
    print(f"Logged-in User: {request.user}")
    print(f"User's Client: {request.user.client}")
    invoices = Invoice.objects.filter(client=request.user.client)
    print(f"Invoices for Client: {invoices}")
    return render(request, 'invoicing/view_invoices.html', {'invoices': invoices})

# def view_invoice_details(request, invoice_id):
    # invoice = get_object_or_404(Invoice, pk=invoice_id)
    # return render(request, 'invoicing/view_invoice_details.html', {'invoice': invoice})

# def view_invoice_details(request, pk):
    # invoice = get_object_or_404(Invoice, pk=pk)
    # return render(request, 'invoicing/view_invoice_details.html', {'invoice': invoice})

def view_invoice_details(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    return render(request, 'invoicing/view_invoice_details.html', {'invoice': invoice})


def make_payment(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)

    # Assuming you have a payments model with different modes like Paypal, Pesapal, Mpesa
    # Replace PaymentMethod with your actual model for storing payment methods
    payment_methods = PaymentMethod.objects.all()  # Replace PaymentMethod with your actual model

    # Automatically pick the amount and currency from the invoice
    amount = invoice.total
    currency = invoice.currency

    if request.method == 'POST':
        selected_method = request.POST.get('payment_method')
        # Redirect to the specific payment method's view based on user selection
        if selected_method == 'paypal':
            return redirect('paypal_payment', invoice_id=invoice_id)
        elif selected_method == 'pesapal':
            return redirect('pesapal_payment', invoice_id=invoice_id)
        elif selected_method == 'mpesa':
            return redirect('mpesa_payment', invoice_id=invoice_id)
        else:
            # Handle invalid or unsupported payment method
            pass

    context = {'invoice': invoice, 'amount': amount, 'currency': currency, 'payment_methods': payment_methods}
    return render(request, 'invoicing/choose_payment_method.html', context)

def payment_notification(sender, **kwargs):
    ipn_obj = sender

    if ipn_obj.payment_status == "Completed":
        # Handle completed payments
        # Your logic here
        pass

valid_ipn_received.connect(payment_notification)


def paypal_payment(request, invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id)

    # Your PayPal payment logic here
    # For simplicity, we'll just render a template
    context = {'invoice': invoice}
    return render(request, 'invoicing/paypal_payment.html', context)

@csrf_exempt
def payment_notification(sender, **kwargs):
    ipn_obj = sender

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Handle completed payments
        # Your logic here
        invoice_id = ipn_obj.invoice
        invoice = Invoice.objects.get(pk=invoice_id)

        # Update the invoice status or perform any other necessary actions

    return HttpResponse("OK")

valid_ipn_received.connect(payment_notification)