from django.urls import reverse

class Student(models.Model):
    name = models.TextField()
    birth_date = models.DateField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('student_detail', args=[str(self.id)])

class Course(models.Model):
    name = models.TextField()
    students = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('course_detail', args=[str(self.id)])
