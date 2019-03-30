# Generated by Django 2.1.7 on 2019-03-30 05:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone_num', models.CharField(max_length=50)),
                ('reservation_date', models.CharField(max_length=50)),
                ('reservation_time', models.CharField(max_length=50)),
                ('variety', models.IntegerField()),
                ('reg_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
