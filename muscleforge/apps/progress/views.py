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
        weight_logs = list(
            WeightLog.objects.filter(user=request.user).order_by('-date')[:30]
        )
        measurements = BodyMeasurement.objects.filter(user=request.user).order_by('-date')[:10]
        photos = ProgressPhoto.objects.filter(user=request.user).order_by('-date')[:12]
        latest_measurement = measurements.first()

        # Chart data, oldest -> newest (independent query so slicing/ordering never collide)
        chart_rows = list(
            WeightLog.objects.filter(user=request.user)
            .order_by('date')[:30]
            .values('date', 'weight')
        )
        chart_labels = [row['date'].strftime('%b %d') for row in chart_rows]
        chart_weights = [float(row['weight']) for row in chart_rows]

        # Overall change: oldest entry vs. latest entry shown on the chart
        weight_change = None
        if len(chart_rows) >= 2:
            weight_change = chart_rows[-1]['weight'] - chart_rows[0]['weight']

        # Per-row change vs. the next (older) entry, since weight_logs is newest-first
        weight_rows = []
        for i, log in enumerate(weight_logs):
            change = None
            if i + 1 < len(weight_logs):
                change = log.weight - weight_logs[i + 1].weight
            weight_rows.append({'log': log, 'change': change})

        return render(request, self.template_name, {
            'weight_logs': weight_logs,
            'weight_rows': weight_rows,
            'measurements': measurements,
            'photos': photos,
            'latest_measurement': latest_measurement,
            'chart_labels': chart_labels,
            'chart_weights': chart_weights,
            'weight_change': weight_change,
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