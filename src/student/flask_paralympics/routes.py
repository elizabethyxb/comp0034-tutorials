from flask import Blueprint
from flask import render_template
from student.flask_paralympics import db
from student.flask_paralympics.models import Event

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/<string:name>')
def show_post(name):
    # show the post with the given id, the id is an integer
    return f'Hello {name}'

@main.route('/get-event')
def get_event():
    # RETURN A SINGLE EVENT

    # event_id = 1
    # event = db.get_or_404(
    #     Event, event_id,
    #     description=f"No event with id '{event_id}'."
    # )
    # result = f"Event with id: {event.event_id} in year: {event.year}"
    # return result

    # RETURN ALL EVENTS 

    events = db.session.query(Event).all()  # Fetch all events

    result = []
    for event in events:
        result.append(f"Event with id: {event.event_id} in year: {event.year}")

    return "<br>".join(result)

    # 