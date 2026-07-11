import json
from groq import Groq
from django.conf import settings
from .models import ChatSession, ChatMessage


SYSTEM_PROMPT = """You are MuscleForge AI Coach, a real personal fitness coach and nutritionist for an Indian guy trying to gain weight. You talk like a real coach — direct, motivating, no fluff.

You know:
- Workout planning (home, gym, beginner to advanced)
- Weight gain, muscle gain, Indian diet & nutrition
- Budget-friendly Indian meals (dal, roti, rice, paneer, eggs, chicken, soya, peanut butter)
- Supplements (whey, creatine, etc.), recovery, sleep
- BMI, body composition, injury prevention

How to respond based on real-time context you receive:
- If it's morning → motivate for the day, suggest a high-calorie breakfast
- If it's evening and workout not done → push them to work out
- If remaining calories are high → suggest specific Indian foods to close the gap RIGHT NOW
- If calories are on track → praise and suggest what to eat next
- If workout is done → focus on recovery nutrition (protein + carbs)
- Always be specific — name actual foods with quantities and calories

Rules:
- Talk like a real coach, not a robot. Short punchy sentences.
- Use markdown (bold, lists) but keep it tight
- Always use metric units and Indian food examples
- Never say "I'm just an AI" — act like a real coach who knows this person

User context is provided below."""


def get_or_create_session(user, session_id=None):
    if session_id:
        try:
            return ChatSession.objects.get(id=session_id, user=user)
        except ChatSession.DoesNotExist:
            pass
    # Don't auto-create — caller must handle None
    return None


def build_system_message(user):
    from django.utils import timezone
    from django.db.models import Sum

    now = timezone.localtime()
    hour = now.hour
    if hour < 12:
        time_of_day = 'morning'
    elif hour < 17:
        time_of_day = 'afternoon'
    elif hour < 21:
        time_of_day = 'evening'
    else:
        time_of_day = 'night'

    # Today's calories
    try:
        from apps.nutrition.models import MealLog
        today = now.date()
        logged_calories = MealLog.objects.filter(
            user=user, date=today
        ).aggregate(total=Sum('calories'))['total'] or 0
        calorie_goal = user.profile.daily_calorie_goal
        remaining_calories = max(0, calorie_goal - logged_calories)
        calorie_context = f"""\n- Time of day: {time_of_day} ({now.strftime('%H:%M')})
- Calories logged today: {round(logged_calories)} / {calorie_goal} kcal
- Remaining calories needed: {round(remaining_calories)} kcal"""
    except Exception:
        calorie_context = f"\n- Time of day: {time_of_day} ({now.strftime('%H:%M')})"

    # Workout done today?
    try:
        from apps.workout.models import WorkoutSession
        workout_done = WorkoutSession.objects.filter(
            user=user, date=today, is_completed=True
        ).exists()
        calorie_context += f"\n- Workout completed today: {'Yes' if workout_done else 'No'}"
    except Exception:
        pass

    try:
        profile = user.profile
        context = f"""

User Profile:
- Name: {user.full_name}
- Age: {profile.age or 'Not set'}
- Gender: {profile.get_gender_display() if profile.gender else 'Not set'}
- Height: {profile.height or 'Not set'} cm
- Weight: {profile.weight or 'Not set'} kg
- Goal: {profile.get_goal_display()}
- Activity Level: {profile.get_activity_level_display()}
- Diet Type: {profile.get_diet_type_display()}
- Workout Experience: {profile.get_workout_experience_display()}
- BMI: {profile.bmi or 'Not calculated'}
- Daily Calorie Goal: {profile.daily_calorie_goal} kcal
- Budget: ₹{profile.budget or 'Not set'}/month
- Medical Conditions: {profile.medical_conditions or 'None'}{calorie_context}
"""
        return SYSTEM_PROMPT + context
    except Exception:
        return SYSTEM_PROMPT + calorie_context


def get_conversation_history(session, limit=20):
    messages = session.messages.order_by('-created_at')[:limit]
    return [{'role': m.role, 'content': m.content} for m in reversed(messages)]


def chat_with_ai(user, message, session_id=None):
    """Non-streaming chat response"""
    client = Groq(api_key=settings.GROQ_API_KEY)
    session = get_or_create_session(user, session_id)
    if session is None:
        session = ChatSession.objects.create(user=user, title='New Chat')

    history = get_conversation_history(session)
    ChatMessage.objects.create(session=session, role='user', content=message)

    messages = [{'role': 'system', 'content': build_system_message(user)}] + history + [{'role': 'user', 'content': message}]

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=messages,
        max_tokens=2048,
        temperature=0.7,
    )

    ai_response = response.choices[0].message.content
    ChatMessage.objects.create(session=session, role='assistant', content=ai_response)

    if not session.title or session.title == 'New Chat':
        session.title = message[:50]
        session.save()

    return {'response': ai_response, 'session_id': session.id}


def stream_chat_with_ai(user, message, session_id=None):
    """Streaming chat response - yields chunks"""
    client = Groq(api_key=settings.GROQ_API_KEY)
    session = get_or_create_session(user, session_id)
    if session is None:
        session = ChatSession.objects.create(user=user, title='New Chat')

    # Get history BEFORE saving the new user message
    history = get_conversation_history(session)
    ChatMessage.objects.create(session=session, role='user', content=message)

    messages = [{'role': 'system', 'content': build_system_message(user)}] + history + [{'role': 'user', 'content': message}]

    stream = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=messages,
        max_tokens=2048,
        temperature=0.7,
        stream=True,
    )

    full_response = ''
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_response += content
            yield f"data: {json.dumps({'content': content, 'session_id': session.id})}\n\n"

    ChatMessage.objects.create(session=session, role='assistant', content=full_response)

    if not session.title or session.title == 'New Chat':
        session.title = message[:50]
        session.save()

    yield f"data: {json.dumps({'done': True, 'session_id': session.id})}\n\n"


def generate_workout_plan(user, goal, plan_type, difficulty, days_per_week):
    """Generate AI workout plan"""
    client = Groq(api_key=settings.GROQ_API_KEY)
    prompt = f"""Create a detailed {days_per_week}-day per week {plan_type} workout plan for:
- Goal: {goal}
- Difficulty: {difficulty}
- User profile: {build_system_message(user)}

Format as JSON with structure:
{{
  "name": "Plan Name",
  "description": "Brief description",
  "days": [
    {{
      "day": 1,
      "name": "Day Name",
      "focus": "Muscle group focus",
      "exercises": [
        {{
          "name": "Exercise Name",
          "sets": 3,
          "reps": "10-12",
          "rest_seconds": 60,
          "notes": "Form tips"
        }}
      ]
    }}
  ]
}}"""

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=3000,
        temperature=0.5,
    )
    try:
        content = response.choices[0].message.content
        start = content.find('{')
        end = content.rfind('}') + 1
        return json.loads(content[start:end])
    except Exception:
        return None


def generate_diet_plan(user):
    """Generate personalized Indian diet plan"""
    client = Groq(api_key=settings.GROQ_API_KEY)
    try:
        profile = user.profile
        prompt = f"""Create a 7-day Indian diet plan for:
- Goal: {profile.get_goal_display()}
- Diet Type: {profile.get_diet_type_display()}
- Daily Calories: {profile.daily_calorie_goal} kcal
- Daily Protein: {profile.daily_protein_goal}g
- Budget: ₹{profile.budget or 5000}/month
- Medical Conditions: {profile.medical_conditions or 'None'}

Include breakfast, lunch, dinner, and snacks with calories and macros for each meal.
Use common Indian foods. Format as detailed markdown."""
    except Exception:
        prompt = "Create a balanced 7-day Indian diet plan with breakfast, lunch, dinner, and snacks."

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=3000,
        temperature=0.5,
    )
    return response.choices[0].message.content


def generate_ai_report(user, report_type='weekly'):
    """Generate weekly/monthly AI progress report"""
    from django.utils import timezone
    from datetime import timedelta
    from apps.progress.models import WeightLog
    from apps.workout.models import WorkoutSession

    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=7 if report_type == 'weekly' else 30)

    weight_logs = WeightLog.objects.filter(user=user, date__range=[start_date, end_date])
    sessions = WorkoutSession.objects.filter(user=user, date__range=[start_date, end_date], is_completed=True)

    client = Groq(api_key=settings.GROQ_API_KEY)
    prompt = f"""Generate a {report_type} fitness progress report for {user.full_name}:

Period: {start_date} to {end_date}
Workouts completed: {sessions.count()}
Weight entries: {weight_logs.count()}
{f"Weight range: {weight_logs.order_by('weight').first().weight if weight_logs.exists() else 'N/A'} - {weight_logs.order_by('-weight').first().weight if weight_logs.exists() else 'N/A'} kg" if weight_logs.exists() else ""}

Provide:
1. Progress summary
2. Key achievements
3. Areas for improvement
4. Next {report_type} goals
5. Motivational message

Format with markdown."""

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=1500,
        temperature=0.7,
    )
    return response.choices[0].message.content
