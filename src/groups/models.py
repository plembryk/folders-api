import uuid

from django.db import models


class Folder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)


class WordGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    folder = models.ForeignKey(Folder, on_delete=models.PROTECT, related_name="word_groups")

    def __str__(self):
        return self.name


class Word(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=False)
    word_group = models.ForeignKey(WordGroup, related_name="words", on_delete=models.PROTECT, null=True, blank=True)
    delimiter = models.CharField(max_length=1)
    batch_id = models.UUIDField(unique=False)
    add_date = models.DateTimeField()

    class Meta:
        unique_together = ("batch_id", "name")
        indexes = [
            models.Index(fields=["batch_id"]),
            models.Index(fields=["word_group"]),
        ]

    def __str__(self):
        return self.name
