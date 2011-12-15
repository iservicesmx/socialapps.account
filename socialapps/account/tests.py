from django.test import TestCase

class AppTestCase(TestCase):
    """
    Populate this class with unit tests for your application
    """
    
    urls = 'account.test_urls'
    
    def testApp(self):
        a = 1
        b = 2
        self.assertEqual(a,b)
        
