from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from rest_framework import viewsets, generics
from rest_framework.response import Response
from django.contrib import messages

from .models import Animal, Procedure
from .forms import AnimalForm, ProcedureForm
from .serializers import AnimalSerializer, ProcedureSerializer


# Web views
class AnimalListView(ListView):
    model = Animal
    template_name = 'animals/animal_list.html'
    context_object_name = 'animals'
    paginate_by = 10


class AnimalDetailView(DetailView):
    model = Animal
    template_name = 'animals/animal_detail.html'
    context_object_name = 'animal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['procedures'] = self.object.procedures.all().order_by('-datetime')
        return context


class AnimalCreateView(CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/animal_form.html'
    success_url = reverse_lazy('animal-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Животное успешно добавлено!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме')
        return super().form_invalid(form)


class AnimalUpdateView(UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/animal_form.html'
    success_url = reverse_lazy('animal-list')


def add_procedure(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if request.method == 'POST':
        form = ProcedureForm(request.POST)
        if form.is_valid():
            procedure = form.save(commit=False)
            procedure.animal = animal
            procedure.save()
            return redirect('animal-detail', pk=animal.pk)
    else:
        form = ProcedureForm()
    return render(request, 'animals/procedure_form.html', {
        'form': form,
        'animal': animal
    })


# API views
class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all().select_related('section')
    serializer_class = AnimalSerializer


class AnimalProceduresView(generics.ListCreateAPIView):
    serializer_class = ProcedureSerializer

    def get_queryset(self):
        animal_id = self.kwargs['animal_id']
        return Procedure.objects.filter(animal_id=animal_id)

    def perform_create(self, serializer):
        animal_id = self.kwargs['animal_id']
        serializer.save(animal_id=animal_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        animal = Animal.objects.get(pk=self.kwargs['animal_id'])
        animal_data = AnimalSerializer(animal).data
        return Response({
            'animal': animal_data,
            'procedures': serializer.data
        })
