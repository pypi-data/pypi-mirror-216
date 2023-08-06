# django-markdowns

Provides markdown functionality for Django via a template filter.

## Features:
 * Adding `md` Django template filter.
   * Add `django_markdowns` to `INSTALLED_APPS` in `settings.py`.
   * Load in template with `{% load markdowns %}`.
 * Adding `DjangoExtension` extension for markdown package.
   * use of Django URL syntax.
     ```
     [Some link](APP_NAME:VIEW_NAME|PARAMS,COMMA,SEPARATED)
     ```
