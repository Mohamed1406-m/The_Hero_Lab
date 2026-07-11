from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('goal_type', models.CharField(choices=[('weight_gain', 'Weight Gain'), ('muscle_gain', 'Muscle Gain'), ('high_calorie', 'High Calorie')], default='weight_gain', max_length=10)),
                ('ingredients', models.TextField(help_text='One ingredient per line')),
                ('steps', models.TextField(help_text='One step per line')),
                ('calories', models.PositiveIntegerField(default=0)),
                ('protein', models.FloatField(default=0)),
                ('carbs', models.FloatField(default=0)),
                ('fat', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
