# Generated by Django 2.2.13 on 2020-07-28 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testresults", "0017_merge_20200728_0348"),
    ]

    operations = [
        migrations.AddField(
            model_name="testresult",
            name="robot_tags",
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
