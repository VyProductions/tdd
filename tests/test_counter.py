"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase

from src.counter import app

from src import status

class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        result = self.client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
    
    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)
    
    def test_update_a_counter(self):
        """It should update a counter or return error for unknown name"""
        result=self.client.put('/counters/NULL')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

        result = self.client.post('/counters/foobar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        base_value = result.get_json()['foobar']
        result = self.client.put('/counters/foobar')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        new_value = result.get_json()['foobar']
        self.assertEqual(base_value + 1, new_value)
    
    def test_read_a_counter(self):
        """It should read a counter or return error for unknown name"""
        result = self.client.get('/counters/NULL')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

        result = self.client.post('/counters/barfoo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        base_value = result.get_json()['barfoo']
        self.assertEqual(base_value, 0)

        for i in range(15):
            result = self.client.put('/counters/barfoo')
            self.assertEqual(result.status_code, status.HTTP_200_OK)
            upd_value = result.get_json()['barfoo']
            self.assertEqual(base_value + i + 1, upd_value)
        
        result = self.client.get('/counters/barfoo')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        new_value = result.get_json()['barfoo']
        self.assertEqual(base_value + 15, new_value)

    def test_delete_a_counter(self):
        """It should delete a counter or return error for unknown name"""
        result = self.client.delete('/counters/NULL')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

        result = self.client.post('/counters/foofoo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        base_value = result.get_json()['foofoo']
        self.assertEqual(base_value, 0)

        for i in range(12):
            result = self.client.put('/counters/foofoo')
            self.assertEqual(result.status_code, status.HTTP_200_OK)
            upd_value = result.get_json()['foofoo']
            self.assertEqual(base_value + i + 1, upd_value)

        result = self.client.get('/counters/foofoo')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        new_value = result.get_json()['foofoo']
        self.assertEqual(base_value + 12, new_value)

        result = self.client.delete('/counters/foofoo')
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)
        result = self.client.put('/counters/foofoo')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
        result = self.client.get('/counters/foofoo')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
        result = self.client.delete('/counters/foofoo')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
