import tkinter as tk
from tkinter import messagebox, ttk
from database import save_result, get_results

class QuizGUI:
    def __init__(self, quiz_app):
        self.quiz_app = quiz_app
        self.window = tk.Tk()
        self.window.title("Quiz App")
        self.window.geometry("1024x768")
        self.window.configure(bg="#FEFAE0")

        self.colors = {
            "bg": "#FEFAE0",
            "fg": "#283618",
            "button": "#606C38",
            "button_fg": "#FEFAE0",
            "highlight": "#DDA15E",
            "accent": "#BC6C25",
            "table_bg": "#DDA15E",
            "table_fg": "#283618"
        }

        self.current_frame = None
        self.user_name = ""
        self.create_landing_page()

    def create_landing_page(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.window, bg=self.colors["bg"])
        self.current_frame.pack(expand=True, fill="both")

        title = tk.Label(self.current_frame, text="General Knowledge Quiz", font=("Arial", 40, "bold"), bg=self.colors["bg"], fg=self.colors["fg"])
        title.pack(pady=30)

        subtitle = tk.Label(self.current_frame, text="Test your knowledge with our exciting quiz!", font=("Arial", 24), bg=self.colors["bg"], fg=self.colors["accent"])
        subtitle.pack(pady=20)

        start_button = tk.Button(self.current_frame, text="Start Quiz", command=self.get_user_name, font=("Arial", 20), bg=self.colors["button"], fg=self.colors["button_fg"], padx=20, pady=10)
        start_button.pack(pady=30)

        self.create_results_table()

    def create_results_table(self):
        results_frame = tk.Frame(self.current_frame, bg=self.colors["bg"])
        results_frame.pack(pady=30)

        results_label = tk.Label(results_frame, text="Recent Quiz Results", font=("Arial", 28, "bold"), bg=self.colors["bg"], fg=self.colors["fg"])
        results_label.pack(pady=20)

        columns = ("Name", "Correct", "Wrong", "Score")
        tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=self.colors["table_bg"], foreground=self.colors["table_fg"], rowheight=25, fieldbackground=self.colors["table_bg"])
        style.configure("Treeview.Heading", font=('Arial', 14, 'bold'), background=self.colors["accent"], foreground=self.colors["table_fg"])
        style.map('Treeview', background=[('selected', self.colors["highlight"])])

        tree.tag_configure('oddrow', background=self.colors["table_bg"])
        tree.tag_configure('evenrow', background=self.colors["highlight"])

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=200)

        tree.pack(padx=20, pady=20)

        results = get_results()
        for i, result in enumerate(results):
            tree.insert("", "end", values=(result["user_name"], result["correct_answers"], result["wrong_answers"], f"{result['score']:.2f}%"), tags=('evenrow' if i % 2 == 0 else 'oddrow',))

    def get_user_name(self):
        name_dialog = tk.Toplevel(self.window)
        name_dialog.title("Enter Your Name")
        name_dialog.geometry("400x200")
        name_dialog.configure(bg=self.colors["bg"])

        label = tk.Label(name_dialog, text="Please enter your name:", font=("Arial", 16), bg=self.colors["bg"], fg=self.colors["fg"])
        label.pack(pady=20)

        name_entry = tk.Entry(name_dialog, font=("Arial", 14), width=30)
        name_entry.pack(pady=10)

        def submit_name():
            self.user_name = name_entry.get()
            if self.user_name:
                name_dialog.destroy()
                self.start_quiz()
            else:
                messagebox.showwarning("Warning", "Please enter your name to start the quiz.", parent=name_dialog)

        submit_button = tk.Button(name_dialog, text="Start Quiz", command=submit_name, font=("Arial", 14), bg=self.colors["button"], fg=self.colors["button_fg"], padx=10, pady=5)
        submit_button.pack(pady=20)

    def start_quiz(self):
        self.quiz_app.reset()
        self.create_quiz_page()

    def create_quiz_page(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.window, bg=self.colors["bg"])
        self.current_frame.pack(expand=True, fill="both")

        question_frame = tk.Frame(self.current_frame, bg=self.colors["bg"])
        question_frame.pack(expand=True, fill="both", padx=50, pady=50)

        self.question_label = tk.Label(question_frame, text="", wraplength=900, justify="left", font=("Arial", 24), bg=self.colors["bg"], fg=self.colors["fg"])
        self.question_label.pack(pady=30, anchor="w")

        self.option_buttons = []
        for i in range(4):
            button = tk.Button(question_frame, text="", command=lambda i=i: self.check_answer(i+1), font=("Arial", 18), bg=self.colors["button"], fg=self.colors["button_fg"], width=50, anchor="w", padx=10, pady=5)
            button.pack(pady=10, anchor="w")
            self.option_buttons.append(button)

        self.update_question()

    def update_question(self):
        question = self.quiz_app.get_current_question()
        if question:
            self.question_label.config(text=question.question)
            for i, option in enumerate(question.options):
                self.option_buttons[i].config(text=option, state=tk.NORMAL)
        else:
            self.show_result()

    def check_answer(self, answer):
        self.quiz_app.check_answer(answer)
        self.quiz_app.next_question()
        self.update_question()

    def show_result(self):
        total_questions = len(self.quiz_app.questions)
        correct_answers = self.quiz_app.score
        wrong_answers = total_questions - correct_answers
        score_percentage = (correct_answers / total_questions) * 100

        save_result(self.user_name, correct_answers, wrong_answers, score_percentage)

        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.window, bg=self.colors["bg"])
        self.current_frame.pack(expand=True, fill="both")

        result_message = f"Quiz completed, {self.user_name}!\n\nYour score: {correct_answers}/{total_questions}\nScore: {score_percentage:.2f}%"
        result_label = tk.Label(self.current_frame, text=result_message, font=("Arial", 28), bg=self.colors["bg"], fg=self.colors["fg"], justify="center")
        result_label.pack(pady=50)

        if score_percentage >= 80:
            quote = "Excellent! You're a knowledge master!"
        elif score_percentage >= 60:
            quote = "Great job! You have a good grasp of general knowledge."
        elif score_percentage >= 40:
            quote = "Not bad! There's always room for improvement."
        else:
            quote = "Keep learning! Every day is a new opportunity to grow."

        quote_label = tk.Label(self.current_frame, text=quote, font=("Arial", 22, "italic"), bg=self.colors["bg"], fg=self.colors["accent"], wraplength=800)
        quote_label.pack(pady=30)

        restart_button = tk.Button(self.current_frame, text="Back to Main Menu", command=self.create_landing_page, font=("Arial", 18), bg=self.colors["button"], fg=self.colors["button_fg"], padx=20, pady=10)
        restart_button.pack(pady=30)

    def run(self):
        self.window.mainloop()