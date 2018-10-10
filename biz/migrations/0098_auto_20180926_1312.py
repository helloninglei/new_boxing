# Generated by Django 2.0.8 on 2018-09-26 05:12

from django.db import migrations, models


def alter_course_table_for_course_name(apps, schema_editor):
    Course = apps.get_model('biz', 'Course')
    courses = Course.objects.all()
    for course in courses:
        if course.course_name == "泰拳":
            course.course_name = "自由搏击"
            course.save()


def alter_course_order_table_for_course_name(apps, schema_editor):
    CourseOrder = apps.get_model('biz', 'CourseOrder')
    course_orders = CourseOrder.objects.all()
    for course_order in course_orders:
        if course_order.course_name == "泰拳":
            course_order.course_name = "自由搏击"
            course_order.save()


def alter_boxer_table_for_allow_course(apps, schema_editor):
    BoxerIdentification = apps.get_model('biz', 'BoxerIdentification')
    boxers = BoxerIdentification.objects.all()
    for boxer in boxers:
        if boxer.allowed_course:
            boxer.allowed_course = ["自由搏击" if course == "泰拳" else course for course in boxer.allowed_course]
            boxer.save()


class Migration(migrations.Migration):

    dependencies = [
        ('biz', '0097_merge_20180921_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_name',
            field=models.CharField(choices=[('自由搏击', '自由搏击'), ('MMA', 'MMA'), ('拳击', '拳击')], max_length=20),
        ),
        migrations.RunPython(alter_course_table_for_course_name),
        migrations.RunPython(alter_course_order_table_for_course_name),
        migrations.RunPython(alter_boxer_table_for_allow_course)

    ]
