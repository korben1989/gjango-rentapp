# Generated by Django 4.2.4 on 2023-10-08 11:22

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_propertyamenities_appliances_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyamenities',
            name='appliances',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Dishwasher', 'Dishwasher'), ('Dryer', 'Dryer'), ('Freezer', 'Freezer'), ('Garbage disposal', 'Garbage disposal'), ('Microwave', 'Microwave'), ('Range / Oven', 'Range / Oven'), ('Refrigerator', 'Refrigerator'), ('Trash compactor', 'Trash compactor'), ('Washer', 'Washer')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='propertyamenities',
            name='cooling_type',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Central', 'Central'), ('Evaporative', 'Evaporative'), ('Refrigeration', 'Refrigeration'), ('Geothermal', 'Geothermal'), ('Solar', 'Solar'), ('Wall', 'Wall'), ('Other', 'Other'), ('None', 'None')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='propertyamenities',
            name='floor_covering',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Carpet', 'Carpet'), ('Concrete', 'Concrete'), ('Hardwood', 'Hardwood'), ('Laminate', 'Laminate'), ('Slate', 'Slate'), ('Softwood', 'Softwood'), ('Tile', 'Tile'), ('Linoleum / Vinyl', 'Linoleum / Vinyl'), ('Other', 'Other')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='propertyamenities',
            name='heating_type',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Electric', 'Electric'), ('Forced air', 'Forced air'), ('Heat pump', 'Heat pump'), ('Geothermal', 'Geothermal'), ('Radiant', 'Radiant'), ('Stove', 'Stove'), ('Gas', 'Gas'), ('Solar', 'Solar'), ('Wall', 'Wall'), ('Other', 'Other')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='propertyamenities',
            name='rooms',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Gas', 'Gas'), ('Solar', 'Solar'), ('Gas', 'Gas'), ('Solar', 'Solar'), ('Gas', 'Gas'), ('Solar', 'Solar'), ('Gas', 'Gas'), ('Solar', 'Solar')], default='', max_length=20),
        ),
    ]
