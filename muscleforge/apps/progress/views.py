from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg
from .models import WeightLog, BodyMeasurement, ProgressPhoto
from .forms import WeightLogForm, BodyMeasurementForm, ProgressPhotoForm


@method_decorator(login_required, name='dispatch')
class ProgressDashboardView(View):
    template_name = 'progress/dashboard.html'

    def get(self, request):
        weight_logs = WeightLog.objects.filter(user=request.user)[:30]
        measurements = BodyMeasurement.objects.filter(user=request.user)[:10]
        photos = ProgressPhoto.objects.filter(user=request.user)[:12]
        latest_measurement = measurements.first()

        weight_data = list(weight_logs.order_by('date').values('date', 'weight'))

        return render(request, self.template_name, {
            'weight_logs': weight_logs,
            'measurements': measurements,
            'photos': photos,
            'latest_measurement': latest_measurement,
            'weight_data': weight_data,
            'weight_form': WeightLogForm(),
            'measurement_form': BodyMeasurementForm(),
            'photo_form': ProgressPhotoForm(),
        })


@login_required
def add_weight(request):
    if request.method == 'POST':
        form = WeightLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            # Update profile weight
            try:
                request.user.profile.weight = log.weight
                request.user.profile.save()
            except Exception:
                pass
            messages.success(request, f'Weight {log.weight}kg logged!')
    return redirect('progress:dashboard')


@login_required
def add_measurement(request):
    if request.method == 'POST':
        form = BodyMeasurementForm(request.POST)
        if form.is_valid():
            m = form.save(commit=False)
            m.user = request.user
            m.save()
            messages.success(request, 'Measurements saved!')
    return redirect('progress:dashboard')


@login_required
def add_photo(request):
    if request.method == 'POST':
        form = ProgressPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            messages.success(request, 'Progress photo uploaded!')
    return redirect('progress:dashboard')


@login_required
def delete_weight(request, pk):
    log = get_object_or_404(WeightLog, pk=pk, user=request.user)
    log.delete()
    messages.success(request, 'Weight log deleted.')
    return redirect('progress:dashboard')
