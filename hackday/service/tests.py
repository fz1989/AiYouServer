#! /usr/bin/env python
#coding=utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
import json

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_service(self):
        self.client = Client()
        response = self.client.get('/get_photo/', {'galleryid':'帝都执行'})
        print json.loads(response.content)
