from flask import Blueprint, current_app
from flask import render_template
from student.flask_paralympics import db
from student.flask_paralympics.models import Event, Quiz, Question, QuizQuestion, AnswerChoice, StudentResponse, Host, HostEvent, Country
from sqlalchemy import func, text, exc
from flask import flash, get_flashed_messages, redirect, url_for, abort

import flask
main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# @main.route('/<string:name>')
# def show_post(name):
#     # show the post with the given id, the id is an integer
#     return f'Hello {name}'

@main.route('/get-event-<int:event_id>')
def get_event(event_id):
    # RETURN A SINGLE EVENT

    # event_id = 1
    # event = db.get_or_404(
    #     Event, event_id,
    #     description=f"No event with id '{event_id}'."
    # )
    # result = f"Event with id: {event.event_id} in year: {event.year}"
    # return result

    # RETURN ALL EVENTS 

    # events = db.session.query(Event).all()  # Fetch all events

    # result = []
    # for event in events:
    #     result.append(f"Event with id: {event.event_id} in year: {event.year}")

    # return "<br>".join(result)

    # RETURN A SPECIFIC YEAR

    event = db.get_or_404(
        Event, event_id,
        description=f"No event with id '{event_id}'."
    ) 
    result = f"Event with id: {event.event_id} in year: {event.year}"
    return result

@main.route('/add-sample-quiz-data')
def add_sample_quiz_data():
    # Create a Quiz object
    quiz = Quiz(quiz_name="Dummy quiz")

    # Create a Question
    question = Question(question="In what year was the summer paralympics last held in Barcelona?")

    # Create a QuizQuestion
    quiz_question = QuizQuestion()

    # Creat an AnswerChoice
    ans = AnswerChoice(choice_text="1992", choice_value=5, is_correct=True)

    # Create a StudentResponse
    student_response = StudentResponse(student_email="email@example.com", score=5)

    # The QuizQuestion is associated with the Quiz and Question tables by their relationship attribute,
    # called 'quiz_questions' in both cases
    quiz.quiz_questions.append(quiz_question)
    question.quiz_questions.append(quiz_question)
    # The answer choice is related to the question using the relationship that has been defined as 'answer_choices'
    question.answer_choice.append(ans)
    quiz.student_response.append(student_response)

    # Due to the relationships, adding the quiz will add the associated objects as well
    db.session.add(quiz)
    db.session.commit()

    # Check that there is now at least one row in each of the tables
    for table in [Quiz, Question, QuizQuestion, AnswerChoice, StudentResponse]:
        count_query = db.select(func.count()).select_from(table)
        if db.session.execute(count_query).scalar() == 0:
            return f"Failed to add data to {table} table."
    return "Data added"

@main.route('/update-quiz/<quiz_id>/<close_date>')
def update_quiz(quiz_id, close_date):
    """Update the close date for a quiz."""
    quiz = db.get_or_404(Quiz, quiz_id)
    quiz.date = close_date
    db.session.commit()
    return f"Quiz with id {quiz_id} updated with close date {close_date}"

@main.route('/update-question/<question_id>/<new_host>')
def update_question(question_id, new_host):
    """Update the event for a question."""
    question = db.get_or_404(Question, question_id)
    new_host_id = db.session.query(Host.host_id).filter(Host.host == new_host).scalar()
    new_event_id = db.session.query(HostEvent.event_id).filter(HostEvent.host_id == new_host_id).scalar()
    question.event_id = new_event_id
    db.session.commit()
    return f"Question with id {question_id} updated with event {new_host}"

@main.route('/delete-data')
def delete_data():
    """Delete all data from the database."""
    for table in [Quiz, Question, QuizQuestion, AnswerChoice, StudentResponse]:
        db.session.query(table).delete()
    db.session.commit()
    return "All data deleted."

@main.route('/delete-response/<response_id>')
def delete_response(response_id):
    """Delete a student response from the database."""
    response = db.get_or_404(StudentResponse, response_id)
    db.session.delete(response)
    db.session.commit()
    return f"Response with id {response_id} deleted."

@main.route('/delete-quiz-question-answer/<quiz_id>')
def delete_quiz_question_answer(quiz_id):
    """Delete a quiz question and its associated answer choices."""
    #db.session.query(text("PRAGMA foreign_keys = ON;"))
    quiz = db.get_or_404(Quiz, quiz_id)
    db.session.delete(quiz)
    # delete questions associa
    db.session.commit()
    return f"Quiz question with id {quiz_id} and its answer choices deleted."

@main.route('/flash')
def flash_message():
    # Generate a Flash message
    flash('This is a flash message!', 'info')
    flash('Invalid email address!', 'error')
    flash('You have successfully registered!', 'success')
    # Redirect to the homepage, the flash message should be displayed
    return redirect(url_for('main.index'))

@main.route('/cause-error')
def cause_error():
    flask.abort(404)

@main.route('/country/<country_code>')
def delete_country(country_code):
    """ Deletes the region with the given code.

    Args:
        param code (str): The 3-character code of the region to delete
    Returns:
        JSON If successful, otherwise abort with 404 Not Found
    """
    try:
        country = db.session.execute(db.select(Country).filter_by(code=country_code)).scalar_one()
        db.session.delete(country)
        db.session.commit()
        return {"message": f"Region {country_code} deleted."}
    except exc.SQLAlchemyError as e:
        # Optionally, log the exception
        current_app.logger.error(f"A database error occurred: {str(e)}")
        # Return a 404 error to the user who made the request
        # Currently won't work as registered custom error handler is not implemented
        msg_content = f'Region {country_code} not found'
        abort(404, description=msg_content)