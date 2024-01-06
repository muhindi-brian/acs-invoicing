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
from .models import Invoice, Company, Client
from allauth.account.views import SignupView


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
    # Your view logic here
    return HttpResponse(f"This is the view for invoice {invoice_id}.")




def make_payment(request, invoice_id):
    # Your payment logic here
    invoice = get_object_or_404(Invoice, pk=invoice_id)

    # Create a PayPal Payments form
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(invoice.total),  # Invoice total amount
        'item_name': f'Invoice {invoice.invoice_number}',
        'invoice': f'{invoice.invoice_number}',
        'currency_code': 'USD',  # Change to your currency code
        'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
        'return_url': request.build_absolute_uri(reverse('payment_success')),
        'cancel_return': request.build_absolute_uri(reverse('payment_cancel')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {'form': form, 'invoice': invoice}
    return render(request, 'make_payment.html', context)


@csrf_exempt
def payment_notification(sender, **kwargs):
    ipn_obj = sender

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Handle completed payments
        # Your logic here
        pass

valid_ipn_received.connect(payment_notification)

