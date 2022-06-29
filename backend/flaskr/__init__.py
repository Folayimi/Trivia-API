import os
from select import select
from tkinter.messagebox import QUESTION
from xmlrpc.client import FastMarshaller
from flask import (
  Flask, 
  request, 
  abort, 
  jsonify
  )
from flask_sqlalchemy import SQLAlchemy #, _or
from flask_cors import *
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  
  # CORS Headers

  @app.after_request
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers', 'Content-Type,Authorization,True'
      )
    response.headers.add(
      'Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS'
      )        
    return response
  
  def paginated_questions(request,response):
    page = request.args.get("page", 1, type=int)
    start= (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in response]
    selected_questions = questions[start:end]
    return selected_questions
    
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  
  @cross_origin
  @app.route('/categories', methods=['GET'])  
  def get_categories():    
    categories = Category.query.order_by(Category.id).all()
    if len(categories) == 0:
      abort(404)      
    else:       
      selected_categories = {category.format()['type']:category.format()['type'] for category in categories}
      return jsonify({
        'success':True,
        'categories': selected_categories
      })    

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  '''

  @app.route('/questions')  
  def get_questions():        
    questions = Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.id).all()
    selected_questions = paginated_questions(request,questions)            
    if len(selected_questions) == 0:
      abort(404)
    elif len(selected_questions):        
      categories = {category.format()['type']:category.format()['type'] for category in categories}
      current_category = Category.query.filter(Category.id == selected_questions[1]['category']).one_or_none()
      return jsonify({
        'success':True,
        'questions':selected_questions,
        'total_questions':len(questions),
        'categories':categories,
        'current_category':current_category.format()
      })       
  '''
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):   
    if request.method == 'DELETE':
      question = Question.query.filter(Question.id == question_id).one_or_none()
      if question is None:
        print('lyessll')
        abort(404)
      else:
        question.delete()
        return jsonify({
          'success':True
        })        
        
      
       
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def update_question():
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
          'success':True
        })
      else: 
        abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
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

    