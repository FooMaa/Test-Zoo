from django import forms
from .models import Animal, Procedure, Section

from django import forms
from .models import Animal, Section


class AnimalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['section'].queryset = Section.objects.all()
        self.fields['section'].empty_label = "Выберите секцию"
        self.fields['section'].widget.attrs.update({'class': 'form-select'})

    class Meta:
        model = Animal
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя животного'
            }),
            'species': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите вид животного'
            }),
        }
        labels = {
            'name': 'Имя животного',
            'species': 'Вид животного',
            'section': 'Секция зоопарка',
            'birth_date': 'Дата рождения'
        }


class ProcedureForm(forms.ModelForm):
    class Meta:
        model = Procedure
        fields = ['procedure_type', 'details']
        widgets = {
            'procedure_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'details': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Введите детали процедуры'
            }),
        }