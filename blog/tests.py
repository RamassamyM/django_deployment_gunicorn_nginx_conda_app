from django.test import TestCase
from datetime import timedelta, datetime
from .models import Article
# Create your tests here.

class ArticleTest(TestCase):
    """
    class pour tester le modèle Article
    """
    
    @classmethod
    def setUpTestData(cls):
        # method appelée une fois au début de la suite de tests
        Category.objects.create(title="Par défaut")

    def setUp(self):
        # method appelée avant chaque test
        self.une_variable = "Ma variable !"


    def test_est_recent_avec_futur_article(self):
        """
        Verify if the method est_recent of an article does not
        return True if the Article has a publishing date in the future.
        """

        futur_article = Article(date=datetime.now() + timedelta(days=20))
        # Il n'y a pas besoin de remplir tous les champs, ni de sauvegarder
        self.assertEqual(futur_article.est_recent(), False)
        # ci_dessous les différentes méthodes assert :
        # assertEqualt(a, b) ; assertTrue(x) ; assertFalse(x) ; assertIs(a, b) ; assertIsNone(x) ; assertIn(a, b) ; assertIsInstance(a, b)
        # assertNotEqual... assertIsNot ... assertNotIn...
        # lancer les tests : python manage.py test
