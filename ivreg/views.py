import json

from django.http import JsonResponse
from django.shortcuts import render, redirect

from ivreg.models import Voter, VoterData
from ivreg.forms import RegistrationForm, ValidationForm, CredentialsForm
from ivreg.services import generate_candidate_codes, generate_ballot_id, generate_voter_id

# for testing
from django.http import HttpResponse


CANDIDATES = [
    'Candidate 1',
    'Candidate 2',
    'Candidate 3',
]


def index(request):
    return render(request, 'index.html')


def registration(request):
    if request.method == "POST":
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST
        form = RegistrationForm(data)
        if form.is_valid():
            voter = Voter.objects.create(
                voter_id=form.cleaned_data['voter_id'],
                ballot_id=generate_ballot_id(),
                candidates=json.dumps(generate_candidate_codes(CANDIDATES))
            )
            if request.content_type == 'application/json':
                return JsonResponse({'redirect': request.build_absolute_uri(voter.get_absolute_url())})
            else:
                return redirect(voter)
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {
        'form': form,
    })


def validate(request):
    if request.method == "POST":
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            return JsonResponse({'errors': 'Only application/json requests are accepted.'})
        form = ValidationForm(data)
        if form.is_valid():
            voter = form.cleaned_data['voter']
            return redirect('https://example.com/validate/%s/' % voter.voter_id)
        elif request.content_type == 'application/json':
            return JsonResponse({'errors': form.errors})
    else:
        return JsonResponse({'errors': 'Only POST method allowed.'})


def authorization(request):
    return redirect('http://localhost:8000/ballot/2EIWLRVNVNCXFHQDOLXQGIHHAI/')

def authentication(request):
    # return redirect('http://localhost:8000/authentication/')

    return render(request, 'authentication.html', {})

def credentials(request):
    if request.method == "POST":
        data = request.POST

        form = CredentialsForm(data)

        if form.is_valid():
            # todo try if document exists
            voter_entry = VoterData.objects.create(
                name=form.cleaned_data['name'],
                surname=form.cleaned_data['surname'],
                id_code=form.cleaned_data['id_code'],
            )


            voter_id = generate_voter_id()
            return redirect('http://0.0.0.0:8000/authorization/{}'.format(voter_id))

        else:
            # todo doc exists check
            return HttpResponse("Invalid")
    else:

        form = CredentialsForm()

        return render(request, 'credentials.html', {
            'form': form,
        })


def authorization(request, voter_id=None):
    if voter_id == "POST":

        return render(request, 'authorization.html', {
            'voter_id': voter_id,
        })



def ballot(request, ballot_id):
    ballot = Voter.objects.get(ballot_id=ballot_id.upper())
    return render(request, 'ballot.html', {
        'ballot': ballot,
        'candidates': json.loads(ballot.candidates),
    })
