from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from .models import Course
from .serializers import CourseSerializer

class CoursesApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.course_data = {'name': 'Math'}
        self.course = Course.objects.create(**self.course_data)
        self.course_url = reverse('course-detail', args=[self.course.id])

    def test_get_courses_list(self):
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_course(self):
        response = self.client.get(self.course_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_courses_by_id(self):
        filter_url = f"{reverse('course-list')}?id={self.course.id}"
        response = self.client.get(filter_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_courses_by_name(self):
        filter_url = f"{reverse('course-list')}?name={self.course_data['name']}"
        response = self.client.get(filter_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
