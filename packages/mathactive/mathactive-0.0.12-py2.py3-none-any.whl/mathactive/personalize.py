# personalize.py
import pandas as pd
from pathlib import Path

try:
    DATA_DIR = Path(__file__).parent / 'data'
    assert DATA_DIR.is_dir()
except NameError:
    DATA_DIR = Path.cwd() / 'mathactive' / 'data'  
except AssertionError:
    try:
        DATA_DIR = Path(__file__).parent.parent / 'data'
        assert DATA_DIR.is_dir()
    except AssertionError:
        DATA_DIR = Path.cwd() / 'data'

if not DATA_DIR.is_dir():
    DATA_DIR = DATA_DIR.parent
if not DATA_DIR.is_dir():
    DATA_DIR = Path.cwd()  # worst case CWD should always exist
assert DATA_DIR.is_dir()  # without a DATA_DIR this package can't run



DF = pd.read_csv(DATA_DIR / 'difficulty_start_stop_step_revised.csv')


def get_countq_params(difficulty=0.01, example_seq_len=3):
    """ Predict the parameters of a quiz question generator based on the desired difficulty

    # FIXME: Test not working (temporarily removed >>>)
    get_countq_params(.01)
    {'difficulty': 0.01, 'start': 1, 'stop ': 6, 'step': 1, 'correct answer': 6, 'stop': 4}
    get_countq_params(.02)
    {'difficulty': 0.02, 'start': 0, 'stop ': 3, 'step': 1, 'correct answer': 3, 'stop': 3}
    get_countq_params(.03)
    {'difficulty': 0.03, 'start': 2, 'stop ': 8, 'step': 2, 'correct answer': 8, 'stop': 8}
    get_countq_params(.05)
    {'difficulty': 0.05, 'start': 10, 'stop ': 13, 'step': 1, 'correct answer': 13, 'stop': 13}
    """
    global DF
    response = DF[
        (DF['difficulty'] > difficulty - .02) & (DF['difficulty'] < difficulty + .02)
    ].sample(1).iloc[0].astype(int).to_dict()
    response['difficulty'] = difficulty
    response['stop'] = response['start'] + response['step'] * example_seq_len
    return response


def generate_countq(start=1, stop=None, step=1, example_seq_len=3, **unused_kwargs):
    """ Generate the question text for a counting quiz question and answer 2-tuple

    >>> generate_countq(start=1, step=1, example_seq_len=3)
    {'question': 'What is the next number after 1, 2, 3?', 'answer': '4'}
    """
    if stop is None:
        stop = start + example_seq_len * step
    return {
        'question': f'What is the next number after {", ".join([str(i) for i in range(start, stop, step)])}?',
        'answer': f'{stop}',
    }


def generate_difficult_countq(difficulty):
    """ Generate the question message (str) and answer (float or str) for a counting quiz question

    # FIXME: Test not working (temporarily removed >>>)
    generate_difficult_countq(.02)
    {'question': 'What is the next number after 0, 1, 2?', 'answer': '3'}
    """
    return generate_countq(**get_countq_params(difficulty))


DF_STUDENTS = pd.DataFrame()
STUDENTS = {}


def set_student_skill(student_id, is_correct=1, question_category='counting'):
    """ Record student's skill level improvement """
    student_record = STUDENTS.get('student_id', dict(student_id=student_id))
    k = question_category + '_num_answered'
    student_record[k] = student_record.get(k, 0) + 1
    k = question_category + '_num_correct'
    student_record[k] = student_record.get(k, 0) + is_correct
    k = question_category + '_skill_score'
    latest_score = student_record[question_category + '_num_correct'] / \
        student_record[question_category + '_num_answered']
    student_record[k] = latest_score

    return student_record
