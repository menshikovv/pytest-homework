from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from .models import Course
from .serializers import CourseSerializer

class CoursesViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.course_data = {'name': 'Math'}
        self.course = Course.objects.create(**self.course_data)
        self.course_url = reverse('course-detail', args=[self.course.id])

    def test_get_courses_list(self):
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course(self):
        data = {'name': 'History'}
        response = self.client.post(reverse('course-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_update_course(self):
        updated_name = 'Updated Math'
        data = {'name': updated_name}
        response = self.client.put(self.course_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.get(id=self.course.id).name, updated_name)

    def test_delete_course(self):
        response = self.client.delete(self.course_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)
