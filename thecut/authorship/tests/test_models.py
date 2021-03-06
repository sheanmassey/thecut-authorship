# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.test import TestCase
from django import VERSION as DJANGO_VERSION
from test_app.factories import AuthorshipModelFactory as AuthorshipFactory
from test_app.models import AuthorshipModel
from unittest import skipIf
from thecut.authorship.factories import UserFakerFactory


class TestAuthorshipModel(TestCase):

    def test_sets_created_by_when_model_instance_is_first_saved(self):
        """Check if ``created_by`` is correctly set on first save."""
        authored = AuthorshipModel()
        user = UserFakerFactory()
        user.save()

        authored.save(user=user)

        self.assertEqual(user, authored.created_by)

    def test_sets_updated_by_when_model_instance_is_saved(self):
        """Ensure that
        :py:class:`thecut.authorship.models.Authorship.updated_by` is
        updated on save."""
        authored = AuthorshipFactory()
        update_user = UserFakerFactory(username='update user')

        authored.save(user=update_user)

        self.assertEqual(update_user, authored.updated_by)

    def test_does_not_change_created_by_when_model_instance_is_saved(self):
        """Ensure that
        :py:class:`thecut.authorship.models.Authorship.created_by` is
        not updated for existing models."""
        authored = AuthorshipFactory()
        update_user = UserFakerFactory(username='update user')

        authored.save(user=update_user)

        self.assertNotEqual(update_user, authored.created_by)

    def test_sets_updated_at_if_update_fields_is_specified(self):
        """Ensure that
        :py:class:`thecut.authorship.models.Authorship.updated_at` is
        updated, even when ``update_fields`` is specified."""
        authored = AuthorshipFactory()
        original_updated_at = authored.updated_at

        authored.save(update_fields=[])
        authored = AuthorshipModel.objects.get(pk=authored.pk)

        self.assertGreater(authored.updated_at, original_updated_at)

    def test_sets_updated_by_if_update_fields_is_specified(self):
        """Ensure that
        :py:class:`thecut.authorship.models.Authorship.updated_by` is
        updated, even when ``update_fields`` is specified."""
        authored = AuthorshipFactory()
        update_user = UserFakerFactory(username='update user')

        authored.save(user=update_user, update_fields=['updated_at'])
        updated = AuthorshipModel.objects.get(pk=authored.pk)

        self.assertEqual(updated.updated_by, update_user)
