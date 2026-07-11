from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum
from .models import Exercise, WorkoutPlan, WorkoutDay, WorkoutExercise, WorkoutSession, SessionExercise
from .forms import WorkoutSessionForm, WorkoutPlanForm
from apps.ai_coach.services import generate_workout_plan



@method_decorator(login_required, name='dispatch')
class ExerciseListView(View):
    template_name = 'workout/exercises.html'

    def get(self, request):
        exercises = Exercise.objects.filter(is_active=True)
        difficulty = request.GET.get('difficulty')
        category = request.GET.get('category')
        equipment = request.GET.get('equipment')
        search = request.GET.get('search')

        if difficulty:
            exercises = exercises.filter(difficulty=difficulty)
        if category:
            exercises = exercises.filter(category=category)
        if equipment:
            exercises = exercises.filter(equipment=equipment)
        if search:
            exercises = exercises.filter(name__icontains=search)

        return render(request, self.template_name, {
            'exercises': exercises.prefetch_related('muscles_worked'),
            'difficulty_choices': Exercise.DIFFICULTY_CHOICES,
            'category_choices': Exercise.CATEGORY_CHOICES,
            'equipment_choices': Exercise.EQUIPMENT_CHOICES,
        })


@method_decorator(login_required, name='dispatch')
class ExerciseDetailView(View):
    template_name = 'workout/exercise_detail.html'

    def get(self, request, slug):
        exercise = get_object_or_404(Exercise, slug=slug, is_active=True)
        return render(request, self.template_name, {'exercise': exercise})


@method_decorator(login_required, name='dispatch')
class WorkoutPlanListView(View):
    template_name = 'workout/plans.html'

    def get(self, request):
        my_plans = WorkoutPlan.objects.filter(user=request.user)
        public_plans = WorkoutPlan.objects.filter(is_public=True).exclude(user=request.user)
        return render(request, self.template_name, {
            'my_plans': my_plans, 'public_plans': public_plans
        })


@method_decorator(login_required, name='dispatch')
class WorkoutPlanDetailView(View):
    template_name = 'workout/plan_detail.html'

    def get(self, request, pk):
        plan = get_object_or_404(WorkoutPlan, pk=pk)
        days = plan.days.prefetch_related('exercises__exercise__muscles_worked')
        return render(request, self.template_name, {'plan': plan, 'days': days})


@method_decorator(login_required, name='dispatch')
class GenerateWorkoutPlanView(View):
    template_name = 'workout/generate_plan.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        goal = request.POST.get('goal', 'muscle_gain')
        plan_type = request.POST.get('plan_type', 'gym')
        difficulty = request.POST.get('difficulty', 'beginner')
        days_per_week = int(request.POST.get('days_per_week', 3))

        plan_data = generate_workout_plan(request.user, goal, plan_type, difficulty, days_per_week)
        if plan_data:
            plan = WorkoutPlan.objects.create(
                user=request.user,
                name=plan_data.get('name', 'AI Generated Plan'),
                description=plan_data.get('description', ''),
                plan_type=plan_type,
                difficulty=difficulty,
                goal=goal,
                days_per_week=days_per_week,
                is_ai_generated=True,
            )
            for day_data in plan_data.get('days', []):
                day = WorkoutDay.objects.create(
                    plan=plan,
                    day_number=day_data['day'],
                    name=day_data.get('name', ''),
                    focus=day_data.get('focus', ''),
                )
                for i, ex_data in enumerate(day_data.get('exercises', [])):
                    exercise = Exercise.objects.filter(name__icontains=ex_data['name']).first()
                    if exercise:
                        WorkoutExercise.objects.create(
                            workout_day=day, exercise=exercise,
                            sets=ex_data.get('sets', 3),
                            reps=str(ex_data.get('reps', '10-12')),
                            rest_seconds=ex_data.get('rest_seconds', 60),
                            notes=ex_data.get('notes', ''),
                            order=i,
                        )
            messages.success(request, f'Workout plan "{plan.name}" generated!')
            return redirect('workout:plan_detail', pk=plan.pk)

        messages.error(request, 'Failed to generate plan. Please try again.')
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class WorkoutSessionView(View):
    template_name = 'workout/session.html'

    def get(self, request):
        sessions = WorkoutSession.objects.filter(user=request.user).select_related('workout_plan')[:20]
        form = WorkoutSessionForm()
        return render(request, self.template_name, {'sessions': sessions, 'form': form})

    def post(self, request):
        form = WorkoutSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.is_completed = True  # auto-complete on log
            session.save()
            messages.success(request, 'Workout logged!')
            return redirect('workout:sessions')
        sessions = WorkoutSession.objects.filter(user=request.user)[:20]
        return render(request, self.template_name, {'sessions': sessions, 'form': form})


@login_required
def complete_session(request, pk):
    session = get_object_or_404(WorkoutSession, pk=pk, user=request.user)
    session.is_completed = True
    session.save()
    return JsonResponse({'status': 'ok'})
