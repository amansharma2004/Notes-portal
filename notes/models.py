from django.db import models


class Subject(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    # NEW: semester field
    SEMESTER_CHOICES = [
        (1, "Semester 1"),
        (2, "Semester 2"),
        (3, "Semester 3"),
        (4, "Semester 4"),
        (5, "Semester 5"),
        (6, "Semester 6"),
        (7, "Semester 7"),
        (8, "Semester 8"),
    ]
    semester = models.PositiveSmallIntegerField(
        choices=SEMESTER_CHOICES,
        default=8,
    )

    # NEW: branch field
    BRANCH_CHOICES = [
        ("cse", "CSE"),
        ("it", "IT"),
        ("ece", "ECE"),
        ("eee", "EEE"),
        ("mech", "Mechanical"),
        ("civil", "Civil"),
        ("cse-ds", "CSE-Data Science"),
        ("cse-aiml", "CSE-AIML"),
        ("cse-aids", "CSE-AIDS"),
        ("cse-ai", "CSE-AI"),
    ]
    branch = models.CharField(
        max_length=20,
        choices=BRANCH_CHOICES,
        default="cse-ds",
    )

    def __str__(self):
        return self.name


class Unit(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='units')
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.subject.name} - {self.title}"


class Note(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='notes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Course(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True)
    short_description=models.CharField(max_length=300,blank=True)
    description=models.TextField(blank=True)
    difficulty=models.CharField(max_length=50,blank=True)
    target_exam=models.CharField(max_length=100,blank=True)
    notes_url=models.URLField(blank=True)
    video_url=models.URLField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title