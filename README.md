# Django Auto Actions

[![PyPI](https://img.shields.io/pypi/v/django-auto-actions?style=flat-square)](https://pypi.python.org/pypi/django-auto-actions/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-auto-actions?style=flat-square)](https://pypi.python.org/pypi/django-auto-actions/)
[![PyPI - License](https://img.shields.io/pypi/l/django-auto-actions?style=flat-square)](https://pypi.python.org/pypi/django-auto-actions/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Automatically generates Django admin actions based on your models' fields

## Installation

Install the package using [pip](https://pip.pypa.io/en/stable/)

```bash
pip install django-auto-actions
```

## Usage

There are two ways to integrate `django-auto-actions` into your project:

1. Using **AutoActionsMixin** *(recommended way)*

```python
from django.contrib.admin import ModelAdmin
from django_auto_actions import AutoActionsMixin


@admin.register(YourModel)
class YourModelAdmin(AutoActionsMixin, ModelAdmin):
    ...
```

2. Using **AutoActionsModelAdmin** instead of ModelAdmin

```python
from django_auto_actions import AutoActionsModelAdmin


@admin.register(YourModel)
class YourModelAdmin(AutoActionsModelAdmin):
    ...
```

With either method, `django-auto-actions` will automatically generate [admin actions](https://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/#admin-actions) for your model's [BooleanFields](https://docs.djangoproject.com/fr/4.2/ref/models/fields/#booleanfield), [DateTimeFields](https://docs.djangoproject.com/fr/4.2/ref/models/fields/#datetimefield), [DateFields](https://docs.djangoproject.com/fr/4.2/ref/models/fields/#datefield) and [TimeFields](https://docs.djangoproject.com/fr/4.2/ref/models/fields/#timefield).

To exclude certain fields from having automatic admin actions generated, set the `exclude_auto_actions` class-level attribute.

```python
@admin.register(YourModel)
class YourModelAdmin(AutoActionsMixin, ModelAdmin):
    exclude_auto_actions = ["is_example", "created_at"]
```

## Example

Here's an example of what it might look like for a simple `Homework` model:  
![Example auto actions](https://github.com/Flexonze/django-auto-actions/raw/main/images/example_actions.png)  
And will display a success message like this:  
![Example success message](https://github.com/Flexonze/django-auto-actions/raw/main/images/example_success_message.png)

## Support & Contributing

If you like it, please consider giving this project a star. If you’re using the package, let me know! You can also [create an issue](https://github.com/Flexonze/django-auto-actions/issues/new) for any problems or suggestions. PRs are always welcome!

## Authors

- **Félix Gravel** — [@Flexonze](https://www.github.com/flexonze)
