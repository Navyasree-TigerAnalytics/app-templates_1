# Generated by Django 4.1.3 on 2023-04-05 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_rename_category_id_category_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='promo_type_code',
        ),
        migrations.AlterField(
            model_name='item',
            name='category_id',
            field=models.ForeignKey(db_column='category_id', default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Productcategory', to='common.category'),
        ),
        migrations.AlterField(
            model_name='item',
            name='promo_type_id',
            field=models.ForeignKey(db_column='promo_type_id', default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Promotypes', to='common.promotypes'),
        ),
        migrations.AlterField(
            model_name='item',
            name='scenario_planner_flag',
            field=models.BooleanField(default=True),
        ),
    ]
