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
"""Markdowns Django app tests."""


from django.test import TestCase

from .templatetags import markdowns


class MarkdownsTestCase(TestCase):
    def test_templatefilter(self):
        html = markdowns.md("This is a simple paragraph.")
        self.assertEqual(html, "<p>This is a simple paragraph.</p>")

        html = markdowns.md("* this\n* is\n* a\n* list")
        self.assertEqual(
            html, "<ul><li>this</li><li>is</li><li>a</li><li>list</li></ul>"
        )
