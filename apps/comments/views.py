# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from jsonview.decorators import json_view

from .models import Comments, Reply_to_comments
from apps.elephants.models import Items, Sets
from .forms import CommentForm, ReplayForm


@json_view
@login_required
def comment(request):

    if request.method == "POST":

        form = CommentForm(request.POST)
        if form.is_valid():

            item_id = form.cleaned_data.get("item_id")
            set_id = form.cleaned_data.get("set_id")
            item = None
            set = None
            if item_id:
                item = get_object_or_404(Items, id=item_id)
            if set_id:
                set = get_object_or_404(Sets, id=set_id)

            mod = False
            if request.user.is_authenticated:
                mod = True
            comment = Comments()
            comment.comment = form.cleaned_data.get("comment")
            comment.user = request.user
            comment.items = item
            comment.sets = set
            comment.moderated = mod
            comment.save()

            subject = _("[Comments] New comment")
            message = item.name + "\n\n" + form.cleaned_data.get("comment")
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.INFO_EMAIL]
            fail_silently = True

            send_mail(subject, message, from_email, recipient_list, fail_silently)

            if not mod:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _(
                        "Thank you for your comment. Moderators will check this comment."
                    ),
                )

            return {"success": True}

        else:
            ctx = {}
            ctx.update(csrf(request))

            form_html = render_crispy_form(form, form.helper, context=ctx)

            return {"success": False, "form_html": form_html}


@json_view
@login_required
def replay(request):

    if request.method == "POST":
        form = ReplayForm(request.POST)

        if form.is_valid():
            comment = Comments.objects.get(id=form.cleaned_data.get("comment_id"))
            mod = False
            if request.user.is_authenticated:
                mod = True
            replay = Reply_to_comments()
            replay.reply = form.cleaned_data.get("comment")
            replay.user = request.user
            replay.comments = comment
            replay.moderated = mod
            replay.save()

            if not mod:
                messages.add_message(
                    request, messages.SUCCESS, _("Thank you for your replay.")
                )

            return {"success": True}

        else:
            ctx = {}
            ctx.update(csrf(request))

            form_html = render_crispy_form(form, form.helper, context=ctx)

            return {"success": False, "form_html": form_html}


@json_view
@staff_member_required
def comment_activate(request, comm_id):

    if request.method == "POST":
        comment = get_object_or_404(Comments, id=comm_id)
        comment.moderated = True
        comment.save()

        return {"success": True}

    else:

        return {"success": False}


@json_view
@staff_member_required
def comment_deactivate(request, comm_id):

    if request.method == "POST":
        comment = get_object_or_404(Comments, id=comm_id)
        comment.moderated = False
        comment.save()

        return {"success": True}

    else:

        return {"success": False}


@json_view
@staff_member_required
def comment_delete(request, comm_id):

    if request.method == "POST":
        comment = get_object_or_404(Comments, id=comm_id)
        comment.delete()

        return {"success": True}

    else:

        return {"success": False}


@json_view
@staff_member_required
def replay_activate(request, comm_id):

    if request.method == "POST":
        reply = get_object_or_404(Reply_to_comments, id=comm_id)
        reply.moderated = True
        reply.save()

        return {"success": True}

    else:

        return {"success": False}


@json_view
@staff_member_required
def replay_deactivate(request, comm_id):

    if request.method == "POST":
        reply = get_object_or_404(Reply_to_comments, id=comm_id)
        reply.moderated = False
        reply.save()

        return {"success": True}

    else:

        return {"success": False}


@json_view
@staff_member_required
def replay_delete(request, comm_id):

    if request.method == "POST":
        reply = get_object_or_404(Reply_to_comments, id=comm_id)
        reply.delete()

        return {"success": True}

    else:

        return {"success": False}


def comments(request):
    comments = Comments.objects.all().order_by("-added")

    return render(request, "comments/comments.html", {"comments": comments})
