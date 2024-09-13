# Django-Auto-Actions

Generates Django admin actions based on your model's fields


## Installation

Use [pip](https://pip.pypa.io/en/stable/) to install django-auto-actions

```bash
  pip install django-auto-actions
```
    
## Usage

There are two ways to integrate django-auto-actions into your Django admin

**Using AutoActionsModelAdmin**

```python
from django_auto_actions import AutoActionsModelAdmin
# ...

@admin.register(YourModel)
class YourModelAdmin(AutoActionsModelAdmin):
    # ...
```

or **Using the mixin (AutoActionsMixin)**

```python
from django_auto_actions import AutoActionsMixin
# ...

@admin.register(YourModel)
class YourModelAdmin(AutoActionsMixin, admin.ModelAdmin):
    # ...
```

This will automatically create [admin actions](https://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/#admin-actions) for your model's [BooleanFields](https://docs.djangoproject.com/fr/4.2/ref/models/fields/#booleanfield), [DateTimeFields](https://docs.djangoproject.com/fr/4.2/ref/models/fields/#datetimefield), [DateFields](https://docs.djangoproject.com/fr/4.2/ref/models/fields/#datefield) and [TimeFields](https://docs.djangoproject.com/fr/4.2/ref/models/fields/#timefield). if you don't want auto-action on certain fields, you can define the `exclude_auto_actions` attribute.

```python
@admin.register(YourModel)
class YourModelAdmin(AutoActionsMixin, admin.ModelAdmin):
    exclude_auto_actions = ["is_example", "created_at"]
```

Here's an example of what it might look like:  
- TODO: Add a screenshot here :)
## Support & Contributing

Please consider giving the project a star. Your PRs are welcome!


## Authors

- **Félix Gravel** — [@Flexonze](https://www.github.com/flexonze)
