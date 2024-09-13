from django.db.models import BooleanField, DateTimeField, DateField, TimeField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib import messages, admin
from django.utils.translation import ngettext


class AutoActionsMixin:
    def get_actions(self, request):
        actions = super().get_actions(request)
        auto_actions = self._get_auto_actions()
        actions.update(auto_actions)
        return actions

    def _get_auto_actions(self):
        auto_actions = {}
        exclude_fields = getattr(self, "exclude_auto_actions", [])

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

            elif isinstance(field, DateTimeField):
                action_name = f"set_{field_name}_now"
                auto_actions[action_name] = (
                    create_action(field_name, timezone.now(), "now"),
                    action_name,
                    _(f"Set {field_name} to now"),
                )

            elif isinstance(field, DateField):
                action_name = f"set_{field_name}_today"
                auto_actions[action_name] = (
                    create_action(field_name, timezone.now().date(), "today"),
                    action_name,
                    _(f"Set {field_name} to today"),
                )

            elif isinstance(field, TimeField):
                action_name = f"set_{field_name}_now"
                auto_actions[action_name] = (
                    create_action(field_name, timezone.now().time(), "now"),
                    action_name,
                    _(f"Set {field_name} to now"),
                )

        return auto_actions


class AutoActionsModelAdmin(AutoActionsMixin, admin.ModelAdmin):
    pass
