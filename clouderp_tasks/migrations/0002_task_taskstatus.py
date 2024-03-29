# Generated by Django 4.2.4 on 2024-02-06 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clouderp_tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_customer_task', to='clouderp_tasks.customer')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_order_task', to='clouderp_tasks.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_product_task', to='clouderp_tasks.product')),
            ],
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('status_category', models.CharField(choices=[('TO_DO', 'To Do'), ('IN_PROGRESS', 'In Progress'), ('DONE', 'Done')], default='TO_DO', max_length=15)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_status_task', to='clouderp_tasks.task')),
            ],
        ),
    ]
