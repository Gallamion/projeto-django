from django.shortcuts import render
from utils.recipe.factory import make_recipe
from recipe.models import Recipe


def home(request):
    recipe = Recipe.objects.all().order_by('-id')
    return render(request, 'recipe/pages/home.html', context={
        'recipes': recipe,
    })


def category(request, category_id):
    recipe = Recipe.objects.filter(category__id=category_id).order_by('-id')
    return render(request, 'recipe/pages/home.html', context={
        'recipes': recipe,
    })


def recipe(request, id):
    return render(request, 'recipe/pages/recipe-view.html', context={
        'recipe': make_recipe(),
        'is_detail_page': True,
    })


