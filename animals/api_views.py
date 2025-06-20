from rest_framework import viewsets, generics, permissions

from .models import Animal, Procedure
from .serializers import AnimalSerializer, ProcedureSerializer


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
    