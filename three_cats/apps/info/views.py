import json
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.db.models import Sum
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives

from apps.elephants.models import Items
from .forms import ContactForm, LoginForm
from .models import Info, Stores


def user_login(request):
    if request.user.is_authenticated():
        return redirect('/logout/')

    form = LoginForm()

    order = None

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            login(request, form.user)

            request.session.set_expiry(0)

            messages.add_message(request, messages.SUCCESS,
                                 _('You were successfully logged in.'))

            return redirect('/')

    return render(request, 'info/login.html', {'form': form})


def user_logout(request):
    if not request.user.is_authenticated():
        messages.add_message(request, messages.SUCCESS,
                             _('You are not logged in.'))

    else:
        logout(request)
        messages.add_message(request, messages.SUCCESS,
                             _('You were successfully logged out.'))

    return redirect('/')


def feedback(request):
    topic = get_object_or_404(Info, topic='feedback')

    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = _('[Contact form] New message')
            message = (form.cleaned_data.get('name') + '\n\n' +
                       form.cleaned_data.get('email') + '\n\n' +
                       form.cleaned_data.get('message'))
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [settings.INFO_EMAIL]
            fail_silently = True

            send_mail(subject, message, from_email,
                      recipient_list, fail_silently)

            messages.add_message(request, messages.SUCCESS,
                                 _('The message was successfully sent.'))

            return redirect('feedback')

    return render(request, 'info/feedback.html', {'form': form, 'topic': topic})


def topic_view(request, topic=None):
    topic = get_object_or_404(Info, topic=topic)

    if topic == 'partners':
        stores = Stores.objects.all()

    return render(request, 'info/simple_view.html', {'topic': topic, 'stores': stores})
