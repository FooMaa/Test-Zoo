from django.db import models


class Section(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.name

class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, related_name='animals')
    arrival_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.species})"

PROCEDURE_TYPES = [
    ('FEEDING', 'Кормление'),
    ('WEIGHT', 'Взвешивание'),
    ('VET', 'Ветеринарный осмотр'),
]

class Procedure(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='procedures')
    procedure_type = models.CharField(max_length=20, choices=PROCEDURE_TYPES)
    datetime = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=3000)
    
    def __str__(self):
        return f"{self.get_procedure_type_display()} для {self.animal.name}"
