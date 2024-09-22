from django.core.management import call_command
from django.db import models
from django.contrib import admin, messages
from django.test import TestCase, RequestFactory
from django_auto_actions.main import AutoActionsMixin
from django.contrib.auth.models import AnonymousUser


class TestModel(models.Model):
    is_active = models.BooleanField(null=True, blank=True)

    class Meta:
        app_label = "django_auto_actions"


call_command('makemigrations', 'django_auto_actions')
call_command('migrate', run_syncdb=True)


@admin.register(TestModel)
class TestModelAdmin(AutoActionsMixin, admin.ModelAdmin):
    exclude_auto_actions = []


class AutoActionsMixinTest(TestCase):
    def setUp(self):
        self.model_admin = TestModelAdmin(TestModel, admin.site)
        self.model_admin.model = TestModel

        self.request = RequestFactory().get('/admin/')
        self.request.user = AnonymousUser()
        self.request._messages = messages.storage.default_storage(self.request)

    def test_actions_generated(self):
        actions = self.model_admin.get_actions(self.request)
        expected_actions = [
            "set_is_active_True",
            "set_is_active_False",
            "set_is_active_None",
        ]
        for action in expected_actions:
            self.assertIn(action, actions)

    def test_nullable_boolean_actions_are_working_as_expected(self):
        instance1 = TestModel.objects.create(is_active=True)
        instance2 = TestModel.objects.create(is_active=True)

        states = ["None", "True", "False"]

        for state in states:
            actions = self.model_admin.get_actions(self.request)
            set_is_active_action = actions[f"set_is_active_{state}"][0]

            queryset = TestModel.objects.all()
            set_is_active_action(self.model_admin, self.request, queryset)

            instance1.refresh_from_db()
            instance2.refresh_from_db()
            if state == "None":
                self.assertIsNone(instance1.is_active)
                self.assertIsNone(instance2.is_active)
            else:
                self.assertEqual(instance1.is_active, state == "True")
                self.assertEqual(instance2.is_active, state == "True")