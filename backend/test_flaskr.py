import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_password = os.environ.get('DATABASE_PASSWORD')
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres',self.database_password,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    creates at least a test for each successful operation and for expected errors.
    """
    
    def test_categories_request(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])
    
    def test_404_not_found_categoriesRequest_error(self):
        res = self.client().get('/categoriesssyyy')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'resource not found')
        
    def test_questions_request(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
    
    def test_404_not_found_beyond_available_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'resource not found')
        
    def test_delete_question(self):
        res = self.client().delete('/questions/11')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question_id'], 11)
    
    def test_404_question_not_found(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')

    def test_create_new_question(self):
        res = self.client().post('/create/questions', json={
            'question':'Which Project is Ridwan Currently working on?',
            'answer':'Trivia API Project',
            'category':'1',
            'difficulty':'3'
            })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)    
    
    def test_422_unprocessable_null_value_error(self):
        res = self.client().post('/create/questions', json={
            'question':'Which Project is Ridwan Currently working on?',
            'answer':'Trivia Api Project',            
            'difficulty':'3'
            })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')
    
    def test_searched_questions(self):
        res = self.client().post('/questions/search', json={'searchTerm':"movie"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)           
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
    
    def test_422_error_search_unprocessable(self):
        res = self.client().post('/questions/search', json={'searchTerm':""})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')
    
    def test_category_questions_success(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)   
        self.assertTrue(data['questions'])        
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'],'Science')
    
    def test_404_bad_request_category_questions_(self):
        res = self.client().get('/categories/something/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')
        
    def test_400_bad_request_category_questions_(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'bad request')
        
    def test_quizz_questions_success(self):
        res = self.client().post('/quizzes', json=
                                {
                                    'previous_questions':[],
                                    'quiz_category':{'type':'Science','id':1}
                                })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['question']['category'],'1')
        
    def test_404_quiz_resource_not_found_error(self):
        res = self.client().post('/quizzes/something')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')
        
    def test_422_unprocessable_error(self):
        res = self.client().post('/quizzes', json=
                                {
                                    'previous_questions':None,
                                    'quiz_category':None
                                })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()