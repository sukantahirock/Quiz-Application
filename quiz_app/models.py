from django.db import models

class QuizConfiguration(models.Model):
    DIFFICULTY_CHOICES = [
        ('any', 'Any Difficulty'),
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    TYPE_CHOICES = [
        ('any', 'Any Type'),
        ('multiple', 'Multiple Choice'),
        ('boolean', 'True / False'),
    ]

    ENCODING_CHOICES = [
        ('default', 'Default Encoding'),
        ('urlLegacy', 'Legacy URL Encoding'),
        ('url3986', 'URL Encoding (RFC 3986)'),
        ('base64', 'Base64 Encoding'),
    ]

    amount = models.IntegerField(default=10)
    category = models.CharField(max_length=50, default='any')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='any')
    quiz_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='any')
    encoding = models.CharField(max_length=10, choices=ENCODING_CHOICES, default='default')
    created_at = models.DateTimeField(auto_now_add=True)

class QuizResult(models.Model):
    configuration = models.ForeignKey(QuizConfiguration, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)