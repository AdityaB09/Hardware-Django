# Generated by Django 4.1.4 on 2022-12-31 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0006_rename_customer_orderplaced_profile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobileno', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=2000)),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.product')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
