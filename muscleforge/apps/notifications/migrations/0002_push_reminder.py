from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationsettings',
            name='meal_reminder_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notificationsettings',
            name='push_subscription',
            field=models.TextField(blank=True, default=''),
        ),
    ]
