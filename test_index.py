try:
    import os
    import unittest 
    from library import app
 
except Exception as e:
    print("some modules are missing ", format((e)))
 
class BasicTests(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/')
        statuscode = response.status_code
        self.assertEqual((statuscode), 200)
    

    def test_book_content(self):
        tester = app.test_client(self)
        response = tester.get('/books')
        self.assertEqual(response.content_type, "text/html")


    def test_member_borrowed(self):
        tester = app.test_client(self)
        response = tester.get('/book/3')
        self.assertEqual(response.data, 'inaya')

if __name__ == '__main__':
    unittest.main()