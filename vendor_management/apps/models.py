
# Create your models here.
# models.py

from django.db import models
from django.db import models
from django.db.models import Count, Avg, F, ExpressionWrapper, fields
from django.db.models.functions import Now

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)


    def calculate_on_time_delivery_rate(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        if completed_pos.exists():
            on_time_deliveries = completed_pos.filter(delivery_date__lte=Now())
            on_time_delivery_rate = (on_time_deliveries.count() / completed_pos.count()) * 100
            self.on_time_delivery_rate = round(on_time_delivery_rate, 2)
        else:
            self.on_time_delivery_rate = 0.0
        self.save()
    
    def calculate_quality_rating_avg(self):
        completed_pos = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
        if completed_pos.exists():
            quality_rating_avg = completed_pos.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating']
            self.quality_rating_avg = round(quality_rating_avg, 2)
        else:
            self.quality_rating_avg = 0.0
        self.save()

    def calculate_average_response_time(self):
        acknowledged_pos = self.purchaseorder_set.filter(status='completed', acknowledgment_date__isnull=False)
        if acknowledged_pos.exists():
            response_times = acknowledged_pos.annotate(
                response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=fields.DurationField())
            )
            average_response_time = response_times.aggregate(avg_response_time=Avg('response_time'))['avg_response_time']
            self.average_response_time = round(average_response_time.total_seconds() / 60, 2)  # convert to minutes
        else:
            self.average_response_time = 0.0
        self.save()

    def calculate_fulfillment_rate(self):
        all_pos = self.purchaseorder_set.all()
        if all_pos.exists():
            successful_fulfillments = all_pos.filter(status='completed', issue_date__isnull=False)
            fulfillment_rate = (successful_fulfillments.count() / all_pos.count()) * 100
            self.fulfillment_rate = round(fulfillment_rate, 2)
        else:
            self.fulfillment_rate = 0.0
        self.save()

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
