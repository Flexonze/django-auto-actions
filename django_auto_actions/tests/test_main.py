from django.contrib import admin, messages
from django.contrib.auth.models import AnonymousUser
from django.core.management import call_command
from django.db import models
from django.test import RequestFactory, TestCase
from django.contrib.messages import get_messages

from django_auto_actions.main import AutoActionsMixin


class TestModel(models.Model):
    is_approved = models.BooleanField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    presentation_time = models.TimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "django_auto_actions"


call_command("makemigrations", "django_auto_actions")
call_command("migrate", run_syncdb=True)


@admin.register(TestModel)
class TestModelAdmin(AutoActionsMixin, admin.ModelAdmin):
    exclude_auto_actions = []


class AutoActionsMixinTest(TestCase):
    def setUp(self):
        self.model_admin = TestModelAdmin(TestModel, admin.site)
        self.model_admin.model = TestModel

        self.request = RequestFactory().get("/admin/")
        self.request.user = AnonymousUser()
        self.request._messages = messages.storage.default_storage(self.request)
        # empty cookie storage

    def test_actions_generated(self):
        actions = self.model_admin.get_actions(self.request)
        expected_actions = [
            "set_is_approved_True",
            "set_is_approved_False",
            "set_is_approved_None",
            "set_due_date_today",
            "set_due_date_None",
            "set_presentation_time_now",
            "set_presentation_time_None",
            "set_submitted_at_now",
            "set_submitted_at_None",
        ]

        for action in expected_actions:
            self.assertIn(action, actions)

    def test_actions_can_be_excluded(self):
        class TestModelAdmin(AutoActionsMixin, admin.ModelAdmin):
            exclude_auto_actions = ["is_approved"]

        model_admin = TestModelAdmin(TestModel, admin.site)
        actions = model_admin.get_actions(self.request)
        self.assertEqual(len(actions), 6)  # 9 - 3 = 6

    def test_boolean_fields_actions(self):
        instance1 = TestModel.objects.create(is_approved=True)
        instance2 = TestModel.objects.create(is_approved=True)

        states = ["None", "True", "False"]

        message_index = 0
        for state in states:
            actions = self.model_admin.get_actions(self.request)
            set_is_approved_action = actions[f"set_is_approved_{state}"][0]

            queryset = TestModel.objects.all()
            set_is_approved_action(self.model_admin, self.request, queryset)

            instance1.refresh_from_db()
            instance2.refresh_from_db()

            if state == "None":
                self.assertIsNone(instance1.is_approved)
                self.assertIsNone(instance2.is_approved)
            else:
                self.assertEqual(instance1.is_approved, state == "True")
                self.assertEqual(instance2.is_approved, state == "True")

            expected_message = f"Successfully updated 2 test models to is_approved = {state}"
            message = list(get_messages(self.request))[message_index]
            message_index += 1

            self.assertEqual(message.message, expected_message)


    def test_datetime_fields_actions(self):
        instance1 = TestModel.objects.create(submitted_at=None)
        instance2 = TestModel.objects.create(submitted_at=None)

        states = ["None", "now"]

        message_index = 0
        for state in states:
            actions = self.model_admin.get_actions(self.request)
            set_submitted_at_action = actions[f"set_submitted_at_{state}"][0]

            queryset = TestModel.objects.all()
            set_submitted_at_action(self.model_admin, self.request, queryset)

            instance1.refresh_from_db()
            instance2.refresh_from_db()

            if state == "None":
                self.assertIsNone(instance1.submitted_at)
                self.assertIsNone(instance2.submitted_at)
            else:
                self.assertIsNotNone(instance1.submitted_at)
                self.assertIsNotNone(instance2.submitted_at)

            expected_message = f"Successfully updated 2 test models to submitted_at = {state}"
            message = list(get_messages(self.request))[message_index]
            message_index += 1

            self.assertEqual(message.message, expected_message)


    def test_date_fields_actions(self):
        instance1 = TestModel.objects.create(due_date=None)
        instance2 = TestModel.objects.create(due_date=None)

        states = ["None", "today"]

        message_index = 0
        for state in states:
            actions = self.model_admin.get_actions(self.request)
            set_due_date_action = actions[f"set_due_date_{state}"][0]

            queryset = TestModel.objects.all()
            set_due_date_action(self.model_admin, self.request, queryset)

            instance1.refresh_from_db()
            instance2.refresh_from_db()

            if state == "None":
                self.assertIsNone(instance1.due_date)
                self.assertIsNone(instance2.due_date)
            else:
                self.assertIsNotNone(instance1.due_date)
                self.assertIsNotNone(instance2.due_date)

            expected_message = f"Successfully updated 2 test models to due_date = {state}"
            message = list(get_messages(self.request))[message_index]
            message_index += 1

            self.assertEqual(message.message, expected_message)

    def test_time_fields_actions(self):
        instance1 = TestModel.objects.create(presentation_time=None)
        instance2 = TestModel.objects.create(presentation_time=None)

        states = ["None", "now"]

        message_index = 0
        for state in states:
            actions = self.model_admin.get_actions(self.request)
            set_presentation_time_action = actions[f"set_presentation_time_{state}"][0]

            queryset = TestModel.objects.all()
            set_presentation_time_action(self.model_admin, self.request, queryset)

            instance1.refresh_from_db()
            instance2.refresh_from_db()

            if state == "None":
                self.assertIsNone(instance1.presentation_time)
                self.assertIsNone(instance2.presentation_time)
            else:
                self.assertIsNotNone(instance1.presentation_time)
                self.assertIsNotNone(instance2.presentation_time)

            expected_message = f"Successfully updated 2 test models to presentation_time = {state}"
            message = list(get_messages(self.request))[message_index]
            message_index += 1

            self.assertEqual(message.message, expected_message)