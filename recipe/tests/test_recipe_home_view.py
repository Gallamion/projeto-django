from django.urls import reverse, resolve
from recipe import views
from unittest.mock import patch
from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipe:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipe:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipe:home'))
        self.assertTemplateUsed(response, 'recipe/pages/home.html')

    def test_recipe_home_shows_no_recipes_found_if_no_recipes(self):

        response = self.client.get(reverse('recipe:home'))
        self.assertIn(
            'No recipes found',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipe:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipe:home'))

        self.assertIn(
            'No recipes found',
            response.content.decode('utf-8')
        )

    def test_recipe_home_is_paginated(self):
        for i in range(18):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        with patch('recipe.views.PER_PAGE', new=6):
            response = self.client.get(reverse('recipe:home'))
            recipe = response.context['recipes']
            paginator = recipe.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 6)
            self.assertEqual(len(paginator.get_page(2)), 6)
            self.assertEqual(len(paginator.get_page(3)), 6)

    def test_invalid_page_query_uses_page_one(self):
        for i in range(8):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        with patch('recipe.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipe:home') + '?page=12A')
            self.assertEqual(
                response.context['recipes'].number,
                1
            )
            response = self.client.get(reverse('recipe:home') + '?page=2')
            self.assertEqual(
                response.context['recipes'].number,
                2
            )
            response = self.client.get(reverse('recipe:home') + '?page=3')
            self.assertEqual(
                response.context['recipes'].number,
                3
            )

