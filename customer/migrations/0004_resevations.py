# Generated by Django 4.2.1 on 2023-06-05 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0003_ordermodel_is_paid"),
    ]

    operations = [
        migrations.CreateModel(
            name="Resevations",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("reservation_number", models.CharField(max_length=10)),
                ("name", models.CharField(max_length=225)),
                ("contact", models.CharField(max_length=10)),
                ("email", models.CharField(max_length=50)),
                ("number_of_seats", models.IntegerField()),
                ("date", models.DateTimeField()),
                ("Resevation_time", models.TimeField()),
            ],
        ),
    ]
