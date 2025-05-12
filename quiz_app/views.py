import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import QuizConfiguration, QuizResult

def get_categories():
    categories = [
        {'id': 'any', 'name': 'Any Category'},
        {'id': '9', 'name': 'General Knowledge'},
        {'id': '10', 'name': 'Entertainment: Books'},
        {'id': '11', 'name': 'Entertainment: Film'},
        {'id': '12', 'name': 'Entertainment: Music'},
        {'id': '13', 'name': 'Entertainment: Musicals & Theatres'},
        {'id': '14', 'name': 'Entertainment: Television'},
        {'id': '15', 'name': 'Entertainment: Video Games'},
        {'id': '16', 'name': 'Entertainment: Board Games'},
        {'id': '17', 'name': 'Science & Nature'},
        {'id': '18', 'name': 'Science: Computers'},
        {'id': '19', 'name': 'Science: Mathematics'},
        {'id': '20', 'name': 'Mythology'},
        {'id': '21', 'name': 'Sports'},
        {'id': '22', 'name': 'Geography'},
        {'id': '23', 'name': 'History'},
        {'id': '24', 'name': 'Politics'},
        {'id': '25', 'name': 'Art'},
        {'id': '26', 'name': 'Celebrities'},
        {'id': '27', 'name': 'Animals'},
        {'id': '28', 'name': 'Vehicles'},
        {'id': '29', 'name': 'Entertainment: Comics'},
        {'id': '30', 'name': 'Science: Gadgets'},
        {'id': '31', 'name': 'Entertainment: Japanese Anime & Manga'},
        {'id': '32', 'name': 'Entertainment: Cartoon & Animations'}
    ]
    return categories

def index(request):
    context = {
        'categories': get_categories(),
        'difficulties': QuizConfiguration.DIFFICULTY_CHOICES,
        'types': QuizConfiguration.TYPE_CHOICES,
        'encodings': QuizConfiguration.ENCODING_CHOICES
    }
    return render(request, 'quiz_app/index.html', context)

def start_quiz(request):
    if request.method == 'POST':
        config = QuizConfiguration(
            amount=request.POST.get('amount', 10),
            category=request.POST.get('category', 'any'),
            difficulty=request.POST.get('difficulty', 'any'),
            quiz_type=request.POST.get('type', 'any'),
            encoding=request.POST.get('encoding', 'default')
        )
        config.save()

        # Build API URL
        api_url = 'https://opentdb.com/api.php'
        params = {'amount': config.amount}
        
        if config.category != 'any':
            params['category'] = config.category
        if config.difficulty != 'any':
            params['difficulty'] = config.difficulty
        if config.quiz_type != 'any':
            params['type'] = config.quiz_type
        if config.encoding != 'default':
            params['encode'] = config.encoding

        try:
            response = requests.get(api_url, params=params)
            questions = response.json()
            
            if questions['response_code'] == 0:
                request.session['questions'] = questions['results']
                request.session['current_question'] = 0
                request.session['score'] = 0
                request.session['config_id'] = config.id
                return redirect('quiz')
            else:
                messages.error(request, 'Failed to fetch questions. Please try different parameters.')
                return redirect('index')
        except Exception as e:
            messages.error(request, 'Error connecting to the quiz API. Please try again.')
            return redirect('index')

    return redirect('index')

def quiz(request):
    questions = request.session.get('questions')
    current = request.session.get('current_question', 0)
    
    if not questions or current >= len(questions):
        return redirect('index')
    
    question = questions[current]
    context = {
        'question': question,
        'current': current + 1,
        'total': len(questions)
    }
    return render(request, 'quiz_app/quiz.html', context)

def submit_answer(request):
    if request.method == 'POST':
        questions = request.session.get('questions')
        current = request.session.get('current_question')
        score = request.session.get('score', 0)

        if questions and current < len(questions):
            user_answer = request.POST.get('answer')
            correct_answer = questions[current]['correct_answer']
            
            if user_answer == correct_answer:
                score += 1
                request.session['score'] = score

            current += 1
            request.session['current_question'] = current

            if current >= len(questions):
                config_id = request.session.get('config_id')
                if config_id:
                    config = QuizConfiguration.objects.get(id=config_id)
                    QuizResult.objects.create(
                        configuration=config,
                        score=score,
                        total_questions=len(questions)
                    )
                return redirect('results')

        return redirect('quiz')
    return redirect('index')

def results(request):
    score = request.session.get('score', 0)
    questions = request.session.get('questions', [])
    total = len(questions)
    
    # Clear session data
    for key in ['questions', 'current_question', 'score', 'config_id']:
        request.session.pop(key, None)
    
    context = {
        'score': score,
        'total': total,
        'percentage': (score / total * 100) if total > 0 else 0
    }
    return render(request, 'quiz_app/results.html', context)