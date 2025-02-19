from django.urls import reverse, resolve
from recipe import views
from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):  
    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('recipe:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipe:search') + '?q=test')
        self.assertTemplateUsed(response, 'recipe/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipe:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipe:search') + '?q=Teste'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;Teste&quot;',
            response.content.decode('utf-8')
        )