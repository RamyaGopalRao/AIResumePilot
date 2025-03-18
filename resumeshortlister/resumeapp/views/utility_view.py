from django.http import JsonResponse
from ..utils.utils import send_email
from twilio.rest import Client
def send_email_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message', 'Job Match Notification')
        subject = "You've Been Matched to a Job!"
        send_email(email, subject, message)
        return JsonResponse({'status': 'Email Sent Successfully'})

def send_whatsapp_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        message = request.POST.get('message', 'Job Match Notification')
        send_whatsapp_message(phone, message)
        return JsonResponse({'status': 'WhatsApp Message Sent Successfully'})
