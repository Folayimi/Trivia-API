# Trivia App API Documentaion


## Introduction

Trivia App is a Game based Webpage in which Udacity is invested in creating bonding experiences for its Employees and Students.

## Getting Started

- ### Base URL: 
Basically, the present version of this app is not hosted in any base URL and can only be run locally. 
The backend app remains hosted at the default, 'http://127.0.0.1:5000/'

- ### Authentication: 
This version of the application does not require authentication or API keys. 

## Error Handling
Errors are returned as JSON objects in the specific format as follow:
```
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```
The API returns three error types when requests fail:
- 404 Resource Not Found
- 422 Unprocessable
- 400 Bad Request

## Endpoints

### GET /categories
- General:
    - Returns success and categories objects as dictionary    
- Sample: `curl http://127.0.0.1:5000/categories`
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

### GET /questions
- General:
    - returns a list of questions, success, number of total questions, current category, categories. 
    - results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions?page=1`
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "Entertainment", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 20
}
```

### DELETE /questions/<int:question_id>
- General:
    - Returns success and the URL takes in a parameteter of the question id     
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/3?page=1`
```
{
  "success": true
}
```

### POST /create/questions
- General:
    - Creates a new question using the submitted question text, answer text, category and difficulty score. uses sqlalchemy to add the new question to the database to update the frontend 
    - Returns Success
- `curl http://127.0.0.1:5000/books?page=3 -X POST -H "Content-Type: application/json" -d ' 
```         
{
     'question':'Which Project is Ridwan Currently working on?',
     'answer':'Trivia Api Project',
     'category':'1',
     'difficulty':'3''
}
```
'
```
{
  "success": true
}
```

### POST /questions/search
- General:
    - Gets questions based on a search term. 
  It returns any question in which the search term 
  is a substring of the question. 
    - Returns a list of questions, success, total_questions and current_category

- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{'searchTerm':'movie'}'`
```
{
  'current_category':'Entertainment',
  'questions':[
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  'total_questions': 1,
  'successs': 'true'
}
```

### GET /categories/science/questions
- General:
    - Gets questions based on category.  
    - Returns a list of questions, success, total_questions and current_category

- Sample: `curl http://127.0.0.1:5000/categories/science/questions`
```
{
  "current_category": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Ridwan", 
      "category": 1, 
      "difficulty": 1, 
      "id": 30, 
      "question": "Who am I"
    }
  ], 
  "success": true, 
  "total_questions": 4
}
```
### POST /quizzes
- General:
    - Gets questions to play the quiz. It takes the category and previous question parameters and returns a random question within the given category, if provided, and that is not one of the previous questions.  
    - Returns success and a random question within the given category, if provided, and that is not one of the previous questions.
    
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{'previous_questions':[],'quiz_category':{'type':'science','id':'1'}}'`

```
{
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }
  ],
  'successs': 'true'
}
```


