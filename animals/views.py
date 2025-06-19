from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from rest_framework import viewsets, generics, permissions, status
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone

from .models import Animal, Procedure
from .forms import AnimalForm, ProcedureForm
from .serializers import AnimalSerializer, ProcedureSerializer


# Web views
class AnimalListView(ListView):
    model = Animal
    template_name = 'animals/animal_list.html'
    context_object_name = 'animals'
    paginate_by = None


class AnimalDetailView(DetailView):
    model = Animal
    template_name = 'animals/animal_detail.html'
    context_object_name = 'animal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(f"Процедуры для животного {self.object.id}: {list(self.object.procedures.all())}")
        context['procedures'] = self.object.procedures.select_related('animal').order_by('-datetime')
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.accepts('text/html'):
            return super().render_to_response(context, **response_kwargs)
        return JsonResponse(
            {'error': 'Use API endpoint for JSON requests'},
            status=400
        )


class AnimalCreateView(CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/animal_form.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            return HttpResponseRedirect('/')
        if 'application/json' in request.content_type:
            return JsonResponse({'error': 'Use the API endpoint at /api/animals/'}, status=400)
        return super().post(request, *args, **kwargs)


class AnimalUpdateView(UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/animal_form.html'
    success_url = '/'


class ProcedureCreateView(CreateView):
    form_class = ProcedureForm
    template_name = 'animals/procedure_form.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.animal = get_object_or_404(Animal, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animal'] = self.animal
        return context

    def form_valid(self, form):
        try:
            procedure = form.save(commit=False)
            procedure.animal = self.animal
            if not procedure.datetime:
                procedure.datetime = timezone.now()
            procedure.save()
            form.save_m2m()
            return HttpResponseRedirect(self.get_success_url())
        except Exception as e:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('animal', kwargs={'pk': self.animal.pk})


# API views
class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [permissions.AllowAny]


class ProcedureViewSet(viewsets.ModelViewSet):
    serializer_class = ProcedureSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Procedure.objects.filter(animal_id=self.kwargs['animal_pk'])

    def perform_create(self, serializer):
        animal = generics.get_object_or_404(Animal, pk=self.kwargs['animal_pk'])
        serializer.save(animal=animal)


class AnimalListAPIView(generics.ListCreateAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [permissions.AllowAny]


class AnimalDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [permissions.AllowAny]


class ProcedureListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProcedureSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Procedure.objects.filter(animal_id=self.kwargs['pk'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['animal_pk'] = self.kwargs['pk']
        return context

    def perform_create(self, serializer):
        serializer.save(animal_id=self.kwargs['pk'])


class ProcedureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProcedureSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        animal_id = self.kwargs['animal_pk']
        return Procedure.objects.filter(animal_id=animal_id)
