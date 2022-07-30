# Generated by Django 4.0.6 on 2022-07-30 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5)),
                ('subject', models.CharField(choices=[('r', 'Random'), ('0', 'Tieng Anh')], max_length=1)),
                ('date', models.DateField(auto_now=True, verbose_name='Paper Date')),
                ('type', models.CharField(choices=[('p', 'Past paper'), ('m', 'Mock paper'), ('c', 'Question collections')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_data', models.JSONField(verbose_name='Question JSON')),
                ('correct_answer', models.CharField(choices=[('0', '---'), ('1', 'A'), ('2', 'B'), ('3', 'C'), ('4', 'D')], max_length=1)),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='questions.paper')),
            ],
        ),
        migrations.CreateModel(
            name='UserQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('last_attempt', models.CharField(choices=[('0', '---'), ('1', 'A'), ('2', 'B'), ('3', 'C'), ('4', 'D')], max_length=1)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Section name')),
                ('instruction_text', models.TextField(verbose_name='Section instruction')),
                ('papers', models.ManyToManyField(related_name='sections', through='questions.Question', to='questions.paper')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='questions.section'),
        ),
        migrations.AddField(
            model_name='question',
            name='users',
            field=models.ManyToManyField(related_name='questions', through='questions.UserQuestion', to=settings.AUTH_USER_MODEL),
        ),
    ]
