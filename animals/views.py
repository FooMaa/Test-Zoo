from django.shortcuts import  get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone

from .models import Animal
from .forms import AnimalForm, ProcedureForm


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
        context['procedures'] = self.object.procedures.select_related('animal').order_by('-datetime')
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.accepts('text/html'):
            return super().render_to_response(context, **response_kwargs)
        return JsonResponse({'error': 'Use API endpoint for JSON requests'}, status=400)


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
