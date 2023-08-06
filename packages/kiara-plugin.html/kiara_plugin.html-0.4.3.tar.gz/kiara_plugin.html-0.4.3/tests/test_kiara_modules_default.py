#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `kiara_plugin.html` package."""

import pytest  # noqa

import kiara_plugin.html


def test_assert():

    assert kiara_plugin.html.get_version() is not None
