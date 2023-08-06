from uuid import uuid4
from django.db import models
from django.utils.translation import pgettext_lazy, pgettext

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField

from .query import ConfirmationStateQuerySet


__all__ = 'ConfirmationState',


class ConfirmationState(models.Model):
    objects: models.Manager = (
        ConfirmationStateQuerySet.as_manager()
    )

    class Meta:
        verbose_name = pgettext_lazy('wcd_2factor', 'Confirmation state')
        verbose_name_plural = pgettext_lazy(
            'wcd_2factor', 'Confirmation states'
        )

    id = models.UUIDField(
        primary_key=True, verbose_name=pgettext_lazy('wcd_2factor', 'ID'),
        default=uuid4
    )
    code = models.TextField(
        verbose_name=pgettext_lazy('wcd_2factor', 'Confirmation code'),
        blank=False, null=False,
    )

    is_confirmed = models.BooleanField(
        verbose_name=pgettext_lazy('wcd_2factor', 'Confirmed'), max_length=512,
        null=False, blank=False, default=False
    )

    meta = JSONField(
        verbose_name=pgettext_lazy('wcd_2factor', 'Metadata'),
        null=False, blank=True, default=dict
    )

    created_at = models.DateTimeField(
        verbose_name=pgettext_lazy('wcd_2factor', 'Created at'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=pgettext_lazy('wcd_2factor', 'Updated at'), auto_now=True,
    )

    def __str__(self):
        return (
            pgettext(
                'wcd_2factor',
                '#{code} confirmation: {confirmed}.',
            )
            .format(
                code=self.code,
                confirmed='+' if self.is_confirmed else '-',
            )
        )

    def confirm(self):
        self.is_confirmed = True
        self.save(update_fields=('is_confirmed',))
