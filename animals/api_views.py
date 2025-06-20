from rest_framework import viewsets, generics, permissions
from django.db.models import Prefetch

from .models import Animal, Procedure
from .serializers import AnimalSerializer, ProcedureSerializer


class AnimalViewSet(viewsets.ModelViewSet):
    serializer_class = AnimalSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Animal.objects.select_related('section').prefetch_related(
            Prefetch('procedures',
                     queryset=Procedure.objects.order_by('-datetime'),
                     to_attr='sorted_procedures')).order_by('-arrival_date')


class ProcedureViewSet(viewsets.ModelViewSet):
    serializer_class = ProcedureSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Procedure.objects.filter(animal_id=self.kwargs['animal_pk'])

    def perform_create(self, serializer):
        animal = generics.get_object_or_404(Animal, pk=self.kwargs['animal_pk'])
        serializer.save(animal=animal)


class AnimalListAPIView(generics.ListCreateAPIView):
    serializer_class = AnimalSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Animal.objects.select_related('section').prefetch_related(
            Prefetch('procedures',
                     queryset=Procedure.objects.order_by('-datetime'),
                     to_attr='prefetched_procedures')).order_by('-arrival_date')

        species = self.request.query_params.get('species')
        if species:
            queryset = queryset.filter(species__iexact=species)

        return queryset


class AnimalDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnimalSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Animal.objects.select_related('section').prefetch_related(
            Prefetch('procedures',
                     queryset=Procedure.objects.order_by('-datetime'),
                     to_attr='prefetched_procedures'))

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = generics.get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj


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
