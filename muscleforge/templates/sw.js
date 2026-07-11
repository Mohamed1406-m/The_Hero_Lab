const CACHE_NAME = 'muscleforge-v1';

self.addEventListener('install', e => self.skipWaiting());
self.addEventListener('activate', e => self.clients.claim());

self.addEventListener('message', e => {
    if (e.data === 'CHECK_REMINDERS') checkReminders();
});

async function checkReminders() {
    try {
        const res = await fetch('/notifications/reminder-data/', { credentials: 'include' });
        if (!res.ok) return;
        const data = await res.json();
        const now = new Date();
        const hhmm = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;

        if (data.workout_reminder && data.workout_time && data.workout_time.slice(0,5) === hhmm) {
            self.registration.showNotification('💪 Workout Time!', {
                body: "Time for your workout. Let's get stronger today!",
                icon: '/static/images/default-avatar.png',
                tag: 'workout-reminder',
            });
        }

        if (data.meal_reminder && data.meal_reminder_time && data.meal_reminder_time.slice(0,5) === hhmm) {
            const body = data.remaining_calories > 0
                ? `You still need ${data.remaining_calories} kcal to hit your goal. Eat up!`
                : `You've hit your ${data.calorie_goal} kcal goal today. Great job!`;
            self.registration.showNotification('🍽️ Meal Reminder', {
                body,
                icon: '/static/images/default-avatar.png',
                tag: 'meal-reminder',
            });
        }
    } catch (e) {}
}

self.addEventListener('notificationclick', e => {
    e.notification.close();
    e.waitUntil(clients.openWindow('/nutrition/'));
});
