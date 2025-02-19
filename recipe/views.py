from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.recipe.factory import make_recipe
from recipe.models import Recipe


def home(request):
    recipe = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipe/pages/home.html', context={
        'recipes': recipe,
    })


def category(request, category_id):    
    recipe = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True
        ).order_by('-id'))

    return render(request, 'recipe/pages/category.html', context={
        'recipes': recipe,
        'title': f'{recipe[0].category.name} - Category | '
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(request, 'recipe/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    return render(request, 'recipe/pages/search.html', {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term
                  })
