# Generated by Django 4.1.7 on 2023-03-21 18:07
import json

from django.db import migrations, transaction


def fill_tests(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    Test = apps.get_model("content", "Test")
    Question = apps.get_model("content", "Question")
    Answer = apps.get_model("content", "Answer")

    with transaction.atomic():
        print("\nLoad tests from file")
        with open("content/tests.json", "r") as file:
            tests = json.load(file)
            print("\nFilling tests:")
            for test in tests:
                obj_test = Test(name=test["name"], type=test["type"])
                obj_test.save()

                for question in test["questions"]:
                    obj_question = Question(
                        test=obj_test,
                        order_num=question["order_num"],
                        text=question["text"],
                    )
                    obj_question.save()

                    for answer in question["answers"]:
                        Answer(
                            question=obj_question,
                            text=answer["text"],
                            value=answer["value"],
                        ).save()


def delete_tests(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    Test = apps.get_model("content", "Test")

    with transaction.atomic():
        print("\nDeleting tests:")

        for test in Test.objects.using(db_alias).all():
            test.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            fill_tests,
            reverse_code=delete_tests,
        )
    ]
