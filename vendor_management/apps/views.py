# from django.shortcuts import render

# # Create your views here.
# # views.py

# from rest_framework import generics
# from rest_framework.response import Response
# from .models import Vendor, PurchaseOrder
# from .serializers import VendorSerializer, PurchaseOrderSerializer

# class VendorListCreateView(generics.ListCreateAPIView):
#     queryset = Vendor.objects.all()
#     serializer_class = VendorSerializer

# class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Vendor.objects.all()
#     serializer_class = VendorSerializer

# class PurchaseOrderListCreateView(generics.ListCreateAPIView):
#     queryset = PurchaseOrder.objects.all()
#     serializer_class = PurchaseOrderSerializer

# class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = PurchaseOrder.objects.all()
#     serializer_class = PurchaseOrderSerializer

# class VendorPerformanceView(generics.RetrieveAPIView):
#     queryset = Vendor.objects.all()
#     serializer_class = VendorSerializer
#     lookup_field = 'id'

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         performance_metrics = {
#             'on_time_delivery_rate': instance.on_time_delivery_rate,
#             'quality_rating_avg': instance.quality_rating_avg,
#             'average_response_time': instance.average_response_time,
#             'fulfillment_rate': instance.fulfillment_rate,
#         }
#         return Response(performance_metrics)

# views.py

# views.py

from rest_framework import generics
from rest_framework.response import Response
from django.db.models import F, ExpressionWrapper, fields
from django.db.models.functions import Now
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Calculate performance metrics
        instance.calculate_on_time_delivery_rate()
        instance.calculate_quality_rating_avg()
        instance.calculate_average_response_time()
        instance.calculate_fulfillment_rate()

        performance_metrics = {
            'on_time_delivery_rate': instance.on_time_delivery_rate,
            'quality_rating_avg': instance.quality_rating_avg,
            'average_response_time': instance.average_response_time,
            'fulfillment_rate': instance.fulfillment_rate,
        }
        return Response(performance_metrics)

class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Update acknowledgment_date to the current timestamp
        instance.acknowledgment_date = Now()
        instance.save()

        # Trigger recalculation of average_response_time for the associated vendor
        if instance.vendor:
            instance.vendor.calculate_average_response_time()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
