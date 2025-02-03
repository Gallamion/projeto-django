from django.urls import reverse, resolve
from recipe import views
from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipe:recipe', kwargs={'id': 1}))    
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipe:recipe', kwargs={'id': 500}))
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_detail_template_loads_correct_recipes(self):
        needed_title = 'this is a detail page - it load one recipe'
        self.make_recipe(title=needed_title)
        response = self.client.get(
            reverse(
                'recipe:recipe',
                kwargs={
                    'id': 1
                }
            )
        )
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse(
                'recipe:recipe',
                kwargs={
                    'id': recipe.id
                }
            )
        )
        self.assertEqual(response.status_code, 404)
