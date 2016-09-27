import json
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.db.models import Sum
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives

from .forms import ContactForm, CheckoutForm, LoginForm
from .models import Info, Stores
from ..elephants.models import Items
from ..orders.models import Cart, Orders, Orderitems


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

    return render(request, 'info/login.html',
                              {'form': form,
                               'order': order,
                               })


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

    order = get_object_or_404(Info, topic='feedback')

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

    return render(request, 'info/feedback.html',
                              {'form': form, 'order': order})


def contacts(request):

    topic = get_object_or_404(Info, topic='contacts')

    return render_to_response('info/simple_view.html',
                              {'topic': topic, 'photos': False, 'map': False},
                              context_instance=RequestContext(request))


def about(request):

    topic = get_object_or_404(Info, topic='about_as')

    return render_to_response('info/simple_view.html',
                              {'topic': topic, 'photos': False, 'map': False},
                              context_instance=RequestContext(request))


def partners(request):

    topic = get_object_or_404(Info, topic='partners')
    items = Stores.objects.all()

    return render_to_response('info/partners.html',
                              {'topic': topic,
                               'items': items},
                              context_instance=RequestContext(request))


def checkout(request):

    order = get_object_or_404(Info, topic='checkout')

    form = CheckoutForm()

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():

            if cart:

                o = Orders(name=form.cleaned_data.get('name'),
                           phone=form.cleaned_data.get('phone'),
                           email=form.cleaned_data.get('email'),
                           city=form.cleaned_data.get('city'),
                           delivery=int(form.cleaned_data.get('delivery')),
                           payment=int(form.cleaned_data.get('payment')),
                           massage=form.cleaned_data.get('message'))
                o.save()
                order_kod = o.id

                sum_buy = 0
                name_buy = ''
                purchases = Cart.objects.all().filter(session_key=request.session._session_key)
                for purchase in purchases:
                    item = get_object_or_404(Items, id=purchase.item.id)
                    sum_buy = sum_buy + item.price
                    name_buy = name_buy + item.name + ' (' + str(item.id) + ')\n'
                    o_item = Orderitems(order=o, item=item)
                    o_item.save()
                o.cost = sum_buy
                o.save()

                html = render_to_string('info/mail_order.html',
                                        {'order_number': order_kod, },
                                        context_instance=RequestContext(request))

                subject, from_email, to = (_('Your order is accepted')), \
                                          settings.EMAIL_HOST_USER, form.cleaned_data.get('email')

                msg = EmailMultiAlternatives(subject, from_email, settings.EMAIL_HOST_USER, [to])
                msg.attach_alternative(html, "text/html")
                msg.send()

                subject = _('New order!')
                message = (_('Order number: ') + str(order_kod) + '\n\n' +
                       '---------------------------------------------------------------------\n' +
                       _('Name: ') + form.cleaned_data.get('name') + '\n' +
                       _('Email: ') + form.cleaned_data.get('email') + '\n' +
                       _('Phone: ') + form.cleaned_data.get('phone') + '\n' +
                       _('City: ') + form.cleaned_data.get('city') + '\n' +
                       _('Delivery: ') + settings.DELIVERY[int(form.cleaned_data.get('delivery'))][1] + '\n' +
                       _('Payment: ') + settings.PAYMENT[int(form.cleaned_data.get('payment'))][1] + '\n\n' +
                       _('Message: ') + form.cleaned_data.get('message') + '\n\n' +
                       '---------------------------------------------------------------------\n' +
                       _('Order: ') + name_buy +
                       _('Sum: ') + str(sum_buy) + '\n' +
                       '---------------------------------------------------------------------')
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [settings.CONTACT_EMAIL]
                fail_silently = True

                send_mail(subject, message, from_email,
                      recipient_list, fail_silently)


                Cart.objects.select_related().filter(session_key=request.session._session_key).delete()

                messages.add_message(request, messages.SUCCESS, _(u'Your application is accepted.'))

            return redirect('/')

    return render_to_response('info/checkout.html',
                              {'form': form, 'order': order},
                              context_instance=RequestContext(request))


def feedback_order(request, id):

    order = get_object_or_404(Info, topic='feedback')

    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = _('[Contact form] New order. Items kod ') + str(id)
            message = (form.cleaned_data.get('name') + '\n\n' +
                       form.cleaned_data.get('email') + '\n\n' +
                       form.cleaned_data.get('message'))
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [settings.CONTACT_EMAIL]
            fail_silently = True

            send_mail(subject, message, from_email,
                      recipient_list, fail_silently)

            messages.add_message(request, messages.SUCCESS,
                                 _('The message was successfully sent.'))

            return redirect('feedback')

    return render_to_response('info/feedback.html',
                              {'form': form, 'order': order},
                              context_instance=RequestContext(request))
