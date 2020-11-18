from django.db import models

class Span(models.Model):
    span_id = models.IntegerField()
    text = models.CharField(max_length=200)
    pos = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.id}-{self.text}-{self.pos}"


class MadLib(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text =models.TextField()
    spans = models.ManyToManyField(Span)

    def __str__(self):
        return f"{self.id}-{self.created}"