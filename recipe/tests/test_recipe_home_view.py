from django.urls import reverse, resolve
from recipe import views
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

    