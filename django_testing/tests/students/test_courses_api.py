from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from .models import Course

class CoursesApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.course_data = {'name': 'Math'}
        self.course = Course.objects.create(**self.course_data)
        self.course_url = reverse('course_detail', args=[self.course.id])

    def test_get_courses_list(self):
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_course(self):
        response = self.client.get(self.course_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_courses_by_id(self):
        filter_url = f"{reverse('course_list')}?id={self.course.id}"
        response = self.client.get(filter_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_courses_by_name(self):
        filter_url = f"{reverse('course_list')}?name={self.course_data['name']}"
        response = self.client.get(filter_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_course(self):
        new_course_data = {'name': 'Biology'}
        response = self.client.post(reverse('course_list'), data=new_course_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.filter(name='Biology').count(), 1)

    def test_update_course(self):
        updated_data = {'name': 'Mathematics'}
        response = self.client.put(self.course_url, data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.name, 'Mathematics')

    def test_delete_course(self):
        response = self.client.delete(self.course_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())
