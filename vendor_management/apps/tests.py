from django.test import TestCase
from django.utils import timezone
from datetime import timedelta


import json
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from .models import Vendor, PurchaseOrder

class VendorAPITests(APITestCase):
    def setUp(self):
        # Set up test data
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='123', address='Test Address', vendor_code='V001')

    def tearDown(self):
        Vendor.objects.all().delete()

    def test_create_vendor(self):
        url = reverse('vendor-list-create')
        data = {'name': 'New Vendor', 'contact_details': '456', 'address': 'New Address', 'vendor_code': 'V002'}

        # Get the initial count of vendors
        initial_count = Vendor.objects.count()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the count increased
        self.assertEqual(Vendor.objects.count(), initial_count + 1)

        # Check if the created vendor has the expected data
        new_vendor = Vendor.objects.get(name='New Vendor')
        self.assertEqual(new_vendor.contact_details, '456')
        # Add more assertions for other fields

    def test_retrieve_vendor(self):
        url = reverse('vendor-detail', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Vendor')


class PurchaseOrderAPITests(APITestCase):
    def setUp(self):
        # Set up test data
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='123', address='Test Address', vendor_code='V001')
        self.purchase_order = PurchaseOrder.objects.create(
            po_number='PO001',
            vendor=self.vendor,
            order_date=timezone.make_aware(timezone.datetime(2023, 11, 26, 14, 30, 0)),  # Make order_date timezone-aware
            delivery_date=timezone.make_aware(timezone.datetime(2023, 11, 28, 14, 30, 0)),  # Make delivery_date timezone-aware
            items='[{"item_name": "Item1", "price": 50}, {"item_name": "Item2", "price": 30}]',
            quantity=10,
            status='Pending',
            quality_rating=4.5,
            issue_date=timezone.now() - timedelta(days=2),
            acknowledgment_date=timezone.now() - timedelta(days=1),
            # Add other required fields
        )

    def tearDown(self):
        Vendor.objects.all().delete()
        PurchaseOrder.objects.all().delete()

    def test_retrieve_purchase_order(self):
        url = reverse('purchase-order-detail', args=[self.purchase_order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], 'PO001')
        # we can Add more assertions for other fields
