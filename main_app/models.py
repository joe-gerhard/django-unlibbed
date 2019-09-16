from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.shortcuts import reverse
from django.contrib.auth.models import User

class Template(models.Model):
    name = models.CharField(max_length=50)
    blanks = ArrayField(models.CharField(max_length=50))
    text = models.TextField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("template_detail", kwargs={"pk": self.pk})

    def get_blanks_count(self):
        return len(self.blanks)

    def get_formatted_text(self):
        result = self.text
        for idx, word in enumerate(self.blanks):
            result = result.replace(f'[{idx}]', f'[{word}]')
        return result

    def get_text_with_blanks(self):
        result = self.text
        for idx, word in enumerate(self.blanks):
            result = result.replace(f'[{idx}]', f'[blank]')
        return result
            
    

class Madlib(models.Model):
    name = models.CharField(max_length=50)
    words = ArrayField(models.CharField(max_length=50))
    text = models.TextField()
    date_completed = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("madlib_detail", kwargs={"pk": self.pk})
    
    def get_formatted_text(self):
        result = self.text
        for idx, word in enumerate(self.words):
            result = result.replace(f'[{idx}]', f'[{word}]')
        return result  