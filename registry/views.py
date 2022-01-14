from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count, Exists, F
from anymail.signals import tracking
from django.dispatch import receiver
from django.core.mail import send_mail

import uuid, json

from .models import Item, Claim



def verify_claim(request):
    claim_key = request.session.get('claim_key', False)
    if not claim_key:
        new_key = uuid.uuid4().hex
        request.session['claim_key'] = new_key

    claim = None
    try:
        claim = Claim.objects.get(claim_key=request.session['claim_key'])
    except Claim.DoesNotExist:
        claim = Claim.objects.create(claim_key=request.session['claim_key'])
        claim.save()
    return claim



def index(request):
    claim = verify_claim(request)

    claimed_item_list = Item.objects.all().annotate(
        claim_count=Count('claims')
    ).filter(
        claims__claim_key=claim.claim_key
    )

    available_item_list = Item.objects.all().annotate(
        claim_count=Count('claims')
    ).exclude(
        claims__claim_key=claim.claim_key
    ).exclude(
        claim_count__gte=F('want_count')
    ).annotate(
        remaining_count=F('want_count') - F('claim_count')
    ).order_by(
        '-remaining_count'
    )

    unavailable_item_list = Item.objects.all().annotate(
        claim_count=Count('claims')
    ).exclude(
        claims__claim_key=claim.claim_key
    ).filter(
        claim_count__gte=F('want_count')
    )

    print(available_item_list.query)

    context = {
        'available_item_list': available_item_list,
        'claimed_item_list': claimed_item_list,
        'unavailable_item_list': unavailable_item_list,
        'claim': claim
    }

    return render(request, 'registry/index.html', context)



def set_email(request):
    claim = verify_claim(request)
    new_email = request.POST.get('email_address', False)

    if not new_email:
        messages.warning(request, 'No email address was supplied.')
        return HttpResponseRedirect(reverse('index'))
    
    if new_email != claim.email_address:
        claim.email_sent = False

    claim.email_address = new_email
    claim.save()

    #if(claim.email_sent == False):
    send_key_email(claim.email_address, claim.claim_key, request.get_host())

    messages.success(request, "Email address saved. You should receive an email soon. If you don't, try submit this again.")
    return HttpResponseRedirect(reverse('index'))



def claim(request, claim_key):
    claim = get_object_or_404(Claim, claim_key=claim_key)
    request.session['claim_key'] = claim.claim_key
    return HttpResponseRedirect(reverse('index'))



def add_claim(request):
    body = json.loads(request.body)
    print(body)
    item_id = int(body.get('item_id', None))

    if item_id is None:
        messages.warning(request, 'Cannot find item')
        return(JsonResponse({ 'response': 'bad' }))

    claim = verify_claim(request)

    item = get_object_or_404(Item, id=item_id)

    item.claims.add(claim)
    
    messages.success(request, "Marked %s as bought" % item.name)
    return(JsonResponse({ 'response': 'ok' }))

def remove_claim(request):
    body = json.loads(request.body)
    print(body)
    item_id = int(body.get('item_id', None))

    if item_id is None:
        messages.warning(request, 'Cannot find item')
        return(JsonResponse({ 'response': 'bad' }))

    claim = verify_claim(request)

    item = get_object_or_404(Item, id=item_id)

    item.claims.remove(claim)
    
    messages.success(request, "Marked %s as available" % item.name)
    return(JsonResponse({ 'response': 'ok' }))

def send_key_email(to, key, host):
    message = """Hi,

You can use this link at any time to return to the list of items you've bought.

https://%s/key/%s

If you need help, let us know.

Thanks for your support, C + J.""" % (host, key)
    send_mail("Baby Registry Items", message, None, [to])

@receiver(tracking)  # add weak=False if inside some other function/class
def handle_email_delivered(sender, event, esp_name, **kwargs):
    if event.event_type == 'delivered':
        claim = None
        try:
            claim = Claim.objects.get(email_address=event.recipient)
        except Claim.DoesNotExist:
            return(JsonResponse({ 'response': 'fail' }))
        claim.email_sent = True
        claim.save()
        return(JsonResponse({ 'response': 'ok' }))
        