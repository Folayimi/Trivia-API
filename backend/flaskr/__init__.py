import os
import sys
from select import select
from tkinter.messagebox import QUESTION
from unicodedata import category
from xmlrpc.client import FastMarshaller
from flask import (
  Flask, 
  request, 
  abort, 
  jsonify
  )
from flask_sqlalchemy import SQLAlchemy #, _or
from flask_cors import *
from random import randint

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  # CORS Headers

  '''
    Use the after_request decorator to set Access-Control-Allow
  '''
  
  @app.after_request
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers', 'Content-Type,Authorization'
      )
    response.headers.add(
      'Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS'
      )
    response.headers.add(
      'Access-Control-Allow-Credentials', 'true'
      )                  
    return response
  
  def paginated_questions(request,response):
    page = request.args.get("page", 1, type=int)
    # per_page = QUESTIONS_PER_PAGE
    # modelList = Model.query.paginate(page,per_page,error_out=False)
    # return modelList    
    start= (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in response]
    selected_questions = questions[start:end]
    return selected_questions
    
  
  
  '''
  Creates an endpoint to handle GET requests 
  for all available categories.
  '''
  @cross_origin
  @app.route('/categories', methods=['GET'])  
  def get_categories(): 
    try:   
      categories = Category.query.order_by(Category.id).all()           
      selected_categories = {category.format()['id']:category.format()['type'] for category in categories}
      return jsonify({
        'success':True,
        'categories': selected_categories
      })    
    except Exception:
      abort(404)
      
      

  '''
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint returns a list of questions, 
  number of total questions, current category, categories. 
  '''
  @cross_origin
  @app.route('/questions')  
  def get_questions():     
    try:       
      questions = Question.query.order_by(Question.id).all()
      categories = Category.query.order_by(Category.id).all()
      selected_questions = paginated_questions(request,questions)                      
      categories = {category.format()['id']:category.format()['type'] for category in categories}
      current_category = Category.query.filter(Category.id == selected_questions[0]['category']).one_or_none()
      return jsonify({
        'success':True,
        'questions':selected_questions,
        'total_questions':len(questions),
        'categories':categories,
        'current_category':current_category.format()['type']
      })    
    except KeyError or IndexError:
      abort(422)
    except:
      abort(404)



  '''
  Creates an endpoint to DELETE question using a question ID. 
  '''
  @cross_origin
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):   
    try:
      if request.method == 'DELETE':
        question = Question.query.filter(Question.id == question_id).one_or_none()        
        question.delete()
        return jsonify({
          'success':True,
          'question_id':question.format()['id']
        })        
    except:
      abort(404)
                   
                   
                   
  ''' 
  Creates an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  '''
  @cross_origin
  @app.route('/create/questions', methods=['POST'])
  def submit_question():
    Error = False
    try:
      if request.method == 'POST':
        request_body = request.get_json()
        question = request_body.get('question',None)
        answer = request_body.get('answer',None)
        difficulty = request_body.get('difficulty',None)
        category = request_body.get('category',None)
        
        if question and answer and difficulty and category:
          new_question = Question(
            question = question,
            answer = answer,
            category = category,
            difficulty = difficulty                   
          )        
          new_question.insert()          
          return jsonify({
            'success':True,
          })              
        else :
          abort(422)
    except SystemError:      
      abort(404)        
        
        
        
  '''
  Creates a POST endpoint to get questions based on a search term. 
  It returns any question in which the search term 
  is a substring of the question. 
  '''
  
  @cross_origin
  @app.route('/questions/search', methods=['POST'])
  def search_question():
    Error = False
    try:
      if request.method == 'POST':
        request_body = request.get_json()
        searchTerm = request_body.get('searchTerm',None)               
        if searchTerm:
          questions = Question.query.order_by(Question.id).all()
          searchedQuestions = []
          for question in questions:
            if searchTerm.lower() in question.format()['question'].lower():
              searchedQuestions.append(question.format())
          if len(searchedQuestions) != 0:                             
            current_category = Category.query.filter(Category.id == searchedQuestions[0]['category']).one_or_none()       
            current_category = current_category.format()['type']        
          else:
            current_category = 'science'
          return jsonify({          
            'success':True,
            'questions':searchedQuestions,
            'total_questions':len(searchedQuestions),
            'current_category': current_category
          })
        else:
          abort(405)
    except:
      abort(422)
        
        
        
  '''
  Create a GET endpoint to get questions based on category.  
  '''
  @cross_origin
  @app.route('/categories/<int:category_id>/questions')
  def category_questions(category_id):
    try:      
        query_question = Question.query.filter(Question.category == category_id).all()                         
        questions = paginated_questions(request,query_question)      
        total_questions = len(questions)
        current_category = Category.query.filter(Category.id == category_id).one_or_none()      
          
        return jsonify({
          'success':True,        
          'questions': questions,
          'total_questions': total_questions,
          'current_category': current_category.type
        })
    except:          
      abort(400)
    
    
    
    
  '''
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  '''
  
  @cross_origin
  @app.route('/quizzes', methods=['POST'])
  def quiz_questions():
    try:
      request_data = request.get_json()
      previous_questions = request_data.get('previous_questions',None)
      quiz_category = request_data.get('quiz_category',None)               
      category = Category.query.filter(Category.type == quiz_category['type']).one_or_none()                                
      if category is None:
        questions = Question.query.all()
        questions = [question.format() for question in questions]        
        random_index = randint(0,len(questions)-1)                 
        question = questions[random_index]        
          
        while question in previous_questions:
          random_index = randint(0,len(questions)-1)
          question = questions[random_index]
        else:          
          return jsonify({
              'success':True,
              'question':question
            })
      else:          
        questions_objects = Question.query.filter(Question.category == category.id).all()                                  
        questions_objects = [question.format() for question in questions_objects]
        random_index = randint(0,len(questions_objects)-1)         
        random_question = questions_objects[random_index]        
        
        while random_question in previous_questions:
          random_index = randint(0,len(questions_objects)-1)
          random_question = questions_objects[random_index]
        else:          
          return jsonify({
            'success':True,
            'question':random_question
          })  
    except:
      abort(422)      
    
    
    
    

  '''
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success':False,
      'error':404,
      'message':'resource not found'
    }),404
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }),400
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'      
    }),422
  
  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed'
    }),405
  return app

    