# -*- coding: utf-8 -*-
# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
# Copyright (C) 2021-2023 J. Nathanael Philipp (jnphilipp) <nathanael@philipp.land>
#
# This file is part of django_markdowns.
#
# django_markdowns is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django_markdowns is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with django_markdowns.  If not, see <http://www.gnu.org/licenses/>.
"""Markdown Django app settings."""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from typing import Optional


USER_SETTINGS = getattr(settings, "MARKDOWNS", {})

USE_BOOTSTRAP: bool = False
IMG_CLASS: Optional[str] = None

if "USE_BOOTSTRAP" in USER_SETTINGS:
    USE_BOOTSTRAP = USER_SETTINGS["USE_BOOTSTRAP"]

    if not isinstance(USE_BOOTSTRAP, bool):
        raise ImproperlyConfigured("USE_BOOTSTRAP needs to be a boolean.")

    if USE_BOOTSTRAP:
        IMG_CLASS = "img-fluid"

if "IMG_CLASS" in USER_SETTINGS:
    IMG_CLASS = USER_SETTINGS["IMG_CLASS"]
