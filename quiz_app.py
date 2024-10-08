import random
from question import Question

class QuizApp:
    def __init__(self):
        self.questions = []
        self.score = 0
        self.current_question_index = 0

    def add_question(self, question, options, correct_answer):
        self.questions.append(Question(question, options, correct_answer))

    def get_current_question(self):
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    def check_answer(self, answer):
        current_question = self.get_current_question()
        if current_question and current_question.check_answer(answer):
            self.score += 1
            return True
        return False

    def next_question(self):
        self.current_question_index += 1

    def is_finished(self):
        return self.current_question_index >= len(self.questions)

    def reset(self):
        random.shuffle(self.questions)
        self.score = 0
        self.current_question_index = 0