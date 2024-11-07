from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Recipe
from .forms import RecipeForm

from . import models

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_recipes = Recipe.objects.filter(author=self.request.user)
            other_recipes = Recipe.objects.exclude(author=self.request.user)
            return list(user_recipes) + list(other_recipes)
        else:
            return Recipe.objects.all()

# Create your views here.
def home(request):
  recipes = models.Recipe.objects.all()
  context = {
    'recipes': recipes
  }
  return render(request, 'recipes/home.html', context)

def about(request):
  return render(request, 'recipes/about.html', {'title': 'about page'})


class RecipeDetailView(DetailView):
  model = Recipe

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Recipe
  success_url = reverse_lazy('recipes-home')

  def test_func(self):
    recipe = self.get_object()
    return self.request.user == recipe.author

class RecipeCreateView(LoginRequiredMixin, CreateView):
  model = Recipe
  form_class = RecipeForm

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Recipe
  form_class = RecipeForm

  def test_func(self):
    recipe = self.get_object()
    return self.request.user == recipe.author

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)