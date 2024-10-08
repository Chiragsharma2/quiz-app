from quiz_app import QuizApp
from gui import QuizGUI
from database import init_database, create_tables

def main():
    # Initialize database and create tables
    conn = init_database()
    if conn:
        create_tables(conn)
        conn.close()

    quiz = QuizApp()

    # Add questions to the quiz
    quiz.add_question("What is the capital of France?", ["London", "Berlin", "Paris", "Madrid"], 3)
    quiz.add_question("Which planet is known as the Red Planet?", ["Venus", "Mars", "Jupiter", "Saturn"], 2)
    quiz.add_question("What is the largest mammal in the world?", ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"], 2)
    quiz.add_question("Who painted the Mona Lisa?", ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"], 3)
    quiz.add_question("What is the chemical symbol for gold?", ["Au", "Ag", "Fe", "Cu"], 1)

    # Create and run the GUI
    quiz_gui = QuizGUI(quiz)
    quiz_gui.run()

if __name__ == "__main__":
    main()