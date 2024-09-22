from django.contrib import admin, messages
from django.db.models import BooleanField, DateField, DateTimeField, TimeField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext


class AutoActionsMixin:
    """
    Mixin for adding auto actions to your ModelAdmins subclasses.

    Usage:
    1. Add the mixin to your ModelAdmin subclass.
    2. Define a list of fields to exclude from auto actions in the `exclude_auto_actions` attribute.

    Example:
    ```python
    from django.db import models
    from django.contrib import admin
    from django_auto_actions import AutoActionsMixin

    class MyModel(models.Model):
        name = models.CharField(max_length=255)
        is_active = models.BooleanField(null=True, blank=True)
        submitted_at = models.DateTimeField(null=True, blank=True)
        created_at = models.DateTimeField(auto_now_add=True)

    @admin.register(MyModel)
    class MyModelAdmin(AutoActionsMixin, admin.ModelAdmin):
        exclude_auto_actions = ["created_at"]
    ```

    This will add the following actions:
    - Set is_active to False
    - Set is_active to None
    - Set is_active to True
    - Set submitted_at to None
    - Set submitted_at to now
    """

    def get_actions(self, request):
        actions = super().get_actions(request)
        auto_actions = self._get_auto_actions()
        auto_actions = dict(sorted(auto_actions.items()))
        actions.update(auto_actions)
        return actions

    def _get_auto_actions(self):
        auto_actions = {}
        exclude_fields = getattr(self, "exclude_auto_actions", [])
        now = timezone.now()

        def create_action(field_name, value, display_value):
            def action(modeladmin, request, queryset):
                updated_count = queryset.update(**{field_name: value})
                model_name = modeladmin.model._meta.verbose_name
                model_name_plural = modeladmin.model._meta.verbose_name_plural
                messages.success(
                    request,
                    ngettext(
                        f"Successfully updated {updated_count} {model_name} to {field_name} = {display_value}",
                        f"Successfully updated {updated_count} {model_name_plural} to {field_name} = {display_value}",
                        updated_count,
                    ),
                )

            return action

        for field in (
            f for f in self.model._meta.fields if f.name not in exclude_fields
        ):
            field_name = field.name

            if isinstance(field, BooleanField):
                possible_states = [True, False]
                if field.null:
                    possible_states.append(None)

                for state in possible_states:
                    action_name = f"set_{field_name}_{state}"
                    auto_actions[action_name] = (
                        create_action(field_name, state, state),
                        action_name,
                        _(f"Set {field_name} to {state}"),
                    )

            elif isinstance(field, (DateTimeField, DateField, TimeField)):
                possible_states = {}

                if isinstance(field, DateTimeField):
                    possible_states = {"now": now}

                elif isinstance(field, DateField):
                    possible_states = {"today": now.date()}

                elif isinstance(field, TimeField):
                    possible_states = {"now": now.time()}

                if field.null:
                    possible_states["None"] = None

                for display_value, state in possible_states.items():
                    action_name = f"set_{field_name}_{display_value}"
                    auto_actions[action_name] = (
                        create_action(field_name, state, display_value),
                        action_name,
                        _(f"Set {field_name} to {display_value}"),
                    )

        return auto_actions


class AutoActionsModelAdmin(AutoActionsMixin, admin.ModelAdmin):
    """
    A ModelAdmin subclass that includes the AutoActionsMixin to add auto actions.

    Usage:
    1. Replace `admin.ModelAdmin` with `AutoActionsModelAdmin` in your ModelAdmin subclass.
    2. Define a list of fields to exclude from auto actions in the `exclude_auto_actions` attribute.

    Example:
    ```python
    from django.db import models
    from django.contrib import admin
    from django_auto_actions import AutoActionsModelAdmin

    class MyModel(models.Model):
        name = models.CharField(max_length=255)
        is_active = models.BooleanField(null=True, blank=True)
        submitted_at = models.DateTimeField(null=True, blank=True)
        created_at = models.DateTimeField(auto_now_add=True)

    @admin.register(MyModel)
    class MyModelAdmin(AutoActionsModelAdmin):
        exclude_auto_actions = ["created_at"]
    ```

    This will add the following actions:
    - Set is_active to False
    - Set is_active to None
    - Set is_active to True
    - Set submitted_at to None
    - Set submitted_at to now
    """

    pass
