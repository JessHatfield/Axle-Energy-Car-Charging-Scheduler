import uuid
from typing import Any

from django.db import models


class AeModel(models.Model):
    """
    Abstract base class model that provides self-updating
    created_at and updated_at fields and additionally sets
    an internal Axle Energy ID (i.e., ae_id) uuid.
    """

    ae_id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
        verbose_name="ae_id",
        help_text="Internal reference code.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Item created at.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
        help_text="Item updated at.",
    )

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> None:
        update_fields = kwargs.get("update_fields", None)
        if update_fields:
            kwargs["update_fields"] = set(update_fields).union({"updated_at"})
        super().save(*args, **kwargs)