from django_filters import rest_framework as filters
from students.models import Course

class CourseFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Course
        fields = ("id", "name")
