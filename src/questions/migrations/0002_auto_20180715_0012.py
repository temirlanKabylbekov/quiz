# Generated by Django 2.0.7 on 2018-07-14 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.AlterModelOptions(
            name='questionchoice',
            options={'verbose_name': 'Question choice', 'verbose_name_plural': 'Question choices'},
        ),
        migrations.AlterModelOptions(
            name='questionlist',
            options={'verbose_name': 'Question list', 'verbose_name_plural': 'Question lists'},
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=255, verbose_name='Question text'),
        ),
        migrations.AlterField(
            model_name='questionchoice',
            name='text',
            field=models.CharField(max_length=255, verbose_name='Question choice text'),
        ),
        migrations.AlterField(
            model_name='questionlist',
            name='has_published',
            field=models.BooleanField(default=False, verbose_name='To publsish'),
        ),
        migrations.AlterField(
            model_name='questionlist',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Question list name'),
        ),
    ]
