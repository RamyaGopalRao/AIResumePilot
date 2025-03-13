from django.db import models

class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Resume(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    skills = models.TextField()
    years = models.IntegerField()
    is_duplicate = models.BooleanField(default=False)  # New field to mark duplicates

    def __str__(self):
        return self

class Education(models.Model):
    id = models.AutoField(primary_key=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=100)
    field = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    year = models.CharField(max_length=4)

    def __str__(self):
        return self.degree

class Experience(models.Model):
    id = models.AutoField(primary_key=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experience')
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    def __str__(self):
        return self.position

class JobListing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    required_skills = models.ManyToManyField(Skill)
    specifications = models.TextField(blank=True, null=True)
    years_of_experience_required = models.IntegerField(default=0)  # New field

    def __str__(self):
        return self.title

