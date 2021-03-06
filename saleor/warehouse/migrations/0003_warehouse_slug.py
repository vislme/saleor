# Generated by Django 2.2.9 on 2020-01-29 06:52

from django.db import migrations, models
from django.utils.text import slugify


def create_unique_slug_for_warehouses(apps, schema_editor):
    Warehouse = apps.get_model("warehouse", "Warehouse")

    for warehouse in Warehouse.objects.all():
        if not warehouse.slug:
            warehouse.slug = generate_unique_slug(warehouse)
            warehouse.save(update_fields=["slug"])


def generate_unique_slug(instance):
    slug = slugify(instance.name)
    unique_slug = slug

    ModelClass = instance.__class__
    extension = 1

    pattern = rf"{slug}-\d+$|{slug}$"
    slug_values = (
        ModelClass._default_manager.filter(slug__iregex=pattern)
        .exclude(pk=instance.pk)
        .values_list("slug", flat=True)
    )

    while unique_slug in slug_values:
        extension += 1
        unique_slug = f"{slug}-{extension}"

    return unique_slug


class Migration(migrations.Migration):

    dependencies = [
        ("warehouse", "0002_auto_20200123_0036"),
    ]

    operations = [
        migrations.AddField(
            model_name="warehouse",
            name="slug",
            field=models.SlugField(null=True, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.RunPython(
            create_unique_slug_for_warehouses, migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name="warehouse",
            name="slug",
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
