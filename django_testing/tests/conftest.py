from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Student, Course
from .serializers import StudentSerializer, CourseSerializer
from django.urls import reverse

class StudentTests(TestCase):

    def setUp(self):
        self.student_data = {'name': 'John Doe', 'birth_date': '1990-01-01'}
        self.student = Student.objects.create(**self.student_data)

    def test_student_str_method(self):
        self.assertEqual(str(self.student), 'John Doe')

    def test_student_absolute_url(self):
        url = reverse('student_detail', args=[str(self.student.id)])
        self.assertEqual(self.student.get_absolute_url(), url)

    def test_student_serializer(self):
        serializer = StudentSerializer(instance=self.student)
        self.assertEqual(serializer.data, self.student_data)

class CourseTests(TestCase):

    def setUp(self):
        self.course_data = {'name': 'Math'}
        self.course = Course.objects.create(**self.course_data)

    def test_course_str_method(self):
        self.assertEqual(str(self.course), 'Math')

    def test_course_absolute_url(self):
        url = reverse('course_detail', args=[str(self.course.id)])
        self.assertEqual(self.course.get_absolute_url(), url)

    def test_course_serializer(self):
        serializer = CourseSerializer(instance=self.course)
        self.assertEqual(serializer.data, self.course_data)

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
