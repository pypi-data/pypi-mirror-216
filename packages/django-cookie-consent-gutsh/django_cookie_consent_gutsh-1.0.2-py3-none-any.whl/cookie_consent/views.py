import logging

from django.shortcuts import render
from django.views.generic import View
from django.http import (
    JsonResponse
)

from . import models


LOGGER = logging.getLogger(__name__)


def index(request, *args, **kwargs):
    return JsonResponse({
        'version': '0.0.1',
        'links': {
            'template': 'template',
            'accept': 'accept'
        }
    })


def template(request, *args, **kwargs):
    return render(
        request,
        'cookie_consent/includes/consent.html',
        {}
    )


class Acceptor(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        u = request.user
        if u.is_authenticated:
            cons, created = models.CookieConsentAcceptance.objects.get_or_create(
                user=u
            )
        else:
            cons, created = None, False
            LOGGER.info("Cookie consent on not authenticated user")
        d = {
            'consent': cons,
            'created': created,
        }
        if not u.is_authenticated:
            request.session['cookie_consent'] = True
            d.update({
                'notice': 'anonymous user, cookie consent is in session'
            })
        return JsonResponse(d)
