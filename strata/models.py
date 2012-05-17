from django.db import models


class Counter(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    count = models.IntegerField(default=0, db_index=True)
    money = models.DecimalField(max_digits=32, decimal_places=2, default=0, db_index=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class CounterInc(models.Model):
    counter = models.ForeignKey(Counter)
    money = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    total_count = models.IntegerField()
    total_money = models.DecimalField(max_digits=32, decimal_places=2)
