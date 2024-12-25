"""
Views for core app
"""
from io import BytesIO

from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse_lazy

from django.views.generic import TemplateView, DetailView, CreateView, ListView, UpdateView
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import F

import json as JSON

from django.db.models import Count, Q

from qrcode import make, QRCode
from qrcode.image.svg import SvgPathImage


from .models import Place, Picture, User, Task
from .forms import PictureFormSet, PlaceForm

from google.cloud import storage


from .models import Place 

from django.core import serializers
from django.http import JsonResponse


class Index(TemplateView):
    """
    Base, home index for the site
    """

    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['places'] = Place.objects.all()

        return context
    
def onboarding(request):
    return render(request, 'core/onboarding.html')

def signup_redirect(request):
    return redirect("core:onboarding")

def checked_off(request,pk: int):
    place = Place.objects.get(pk=pk)
    return render(request, 'core/checked_off.html', {"place":place})

def revoke(request):
    if request.user.is_authenticated:
        request.user.role = "base"
        request.user.save()

    return redirect("core:account")

def is_valid_coordinate(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def map_view(request):
    """
    Fetches the map view for the user
    """
    if request.user.is_authenticated:
        approved_places = request.user.tasks.filter(completed=False).values_list('place', flat=True)
        approved_places = Place.objects.filter(pk__in=approved_places).prefetch_related('pictures')
    else:
        approved_places = Place.objects.filter(approved=True).prefetch_related('pictures')

    approved_places_json = serializers.serialize('json', approved_places)

    approved_places_json = JSON.loads(approved_places_json)
    for place, json in zip(approved_places, approved_places_json):
        json['thumbnail'] = place.thumbnail()
        json['url'] = reverse('core:place', kwargs={'pk': place.pk})

    approved_places_json = JSON.dumps(approved_places_json)

    # Add the JSON to the context for the template
    context = {'approved_places_json': approved_places_json}
    
    return render(request, 'core/map.html', context)


def refresh_tasks(request):
    """
    Manually tasks to users who don't have them
    """
    # if the user is not authenticated, redirect to place page
    if not request.user.is_authenticated:
        return redirect("core:index")

    # get 3 places that the user has not completed
    places = Place.objects.exclude(outgoing__user=request.user).order_by("added")[:3]

    # create a task for each place
    for place in places:
        task = Task.objects.create(user=request.user, place=place)
        task.save()

    return redirect("core:account")

class PlaceView(DetailView):    
    """
    A view which represents a place description.
    """
    model = Place
    template_name = "core/place.html"
    context_object_name = "place"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context["has_task"] = self.request.user.has_task(self.object)
            context["owner"] = self.request.user == self.object.added_by

        return context

class AccountView(LoginRequiredMixin, TemplateView):
    """
    Represents a user's account pages which displays statistics about them and open and closed tasks.
    """
    template_name = "core/account.html"


# https://github.com/lincolnloop/python-qrcode
def qr(request, pk: int):
    """
    Returns a SVG QR code image
    """
    host = request.get_host()
    path = reverse("core:complete", kwargs={"pk": pk})
    url = f"https://{host}{path}"

    img = make(url, image_factory=SvgPathImage, box_size=20)
    stream = BytesIO()
    img.save(stream)
    return HttpResponse(stream.getvalue(), content_type="image/svg+xml")


def shareTask(request, pk: int):
    if not request.user.is_authenticated:
        return redirect("core:index")

    task_temp = Task.objects.get(pk=pk)
    place = task_temp.place

    if not request.user.has_task(place):
        task = Task(user = request.user, place = place)
        task.save()
    
    return redirect("core:place", pk=place.pk)


def complete(request, pk: int):
    """
    Completes a place
    """
    # if the user is not authenticated, redirect to place page
    if not request.user.is_authenticated:
        return redirect("core:place", pk=pk)

    # check if the user has this place assigned to them
    place = Place.objects.get(pk=pk)

    request.user.tasks.filter(place=place).update(completed=True)

    if len(request.user.tasks.filter(completed=False)) < 3:
        refresh_tasks(request)
    
    return redirect("core:checked_off",pk=pk)

class PrintPlace(DetailView):
    """
    A view which represents a printable place description.
    """
    model = Place
    template_name = "core/components/place.html"
    context_object_name = "place"


class ApprovalQueue(ListView):
    """
    Represents where admin can approve places in a fifo queue
    """
    model = Place
    template_name = "core/approval_queue.html"
    context_object_name = "places"
    paginate_by = 20

    def get_queryset(self):
        """
        Sort unapproved places by date added ascending
        """
        return Place.objects.filter(approved=False).order_by("added")


class Approve(UpdateView):
    """
    Updates a place to be approved
    """
    model = Place
    template_name = "core/approve.html"
    fields = ["approved"]
    success_url = reverse_lazy("core:approvals")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_super():
            return HttpResponseForbidden("You do not have permission to update this object based on role.")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Set the approved_by field to the current user
        """
        form.instance.approved_by = self.request.user
        form.instance.approved_at = timezone.now()
        return super().form_valid(form)
    

def create_place(request):
    if request.method == 'POST':
        place_form = PlaceForm(request.POST)
        picture_formset = PictureFormSet(request.POST, request.FILES, queryset=Picture.objects.none())

        if place_form.is_valid() and picture_formset.is_valid():
            place = place_form.save(commit=False)
            place.added_by = request.user
            place.save()

            for form in picture_formset:
                if form.cleaned_data:
                    # make the place added by the current user
                    picture = form.save(commit=False)
                    picture.save()
                    place.pictures.add(picture)
            return redirect('core:place', pk=place.pk)
    else:
        place_form = PlaceForm()
        picture_formset = PictureFormSet(queryset=Picture.objects.none())

    return render(request, 'core/create_place.html', {'place_form': place_form, 'picture_formset': picture_formset})

def combined_leaderboard(request):
    user_ranking = User.objects.annotate(
        completed_tasks_count = Count('tasks', filter=Q(tasks__completed = True))
    ).order_by('-completed_tasks_count')[:5]
    place_ranking = Place.objects.filter(approved=True).annotate(
        completed_tasks_count = Count('outgoing', filter=Q(outgoing__completed = True))
    ).order_by('-completed_tasks_count')[:5]
    
    context = {
        'place_ranking': place_ranking, 
        'user_ranking': user_ranking
    }
    
    return render(request, 'core/leaderboard.html', context)