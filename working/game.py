import tkinter as tk
import json
from tkinter import font, scrolledtext


class QuizApp:
    def __init__(self, root):
        self.next_button = None
        self.quiz_data = None
        self.question_label = None
        self.question_topic_numb = None
        self.answer_buttons = None
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("1000x600")
        self.current_question_index = 0
        self.load_quiz_data()
        self.create_widgets()

    def load_quiz_data(self):
        # Load quiz data from a JSON file
        with open("questions_data_output.json", "r") as file:
            self.quiz_data = json.load(file)

    def create_widgets(self):
        label_font = font.Font(size=16)
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill="both")

        # Check if the current question contains "HOTSPOT -" or "DRAG DROP -"
        question_text = self.quiz_data[self.current_question_index]["Question"]

        question_number = self.quiz_data[self.current_question_index]["Question Number"]
        topic_number = self.quiz_data[self.current_question_index]["Topic Number"]

        self.next_button = tk.Button(self.root, text="Next Question", state=tk.DISABLED, command=self.next_question)
        self.next_button.pack(side=tk.RIGHT)

        self.question_topic_numb = tk.Label(frame, text="Question #" + question_number + " Topic #" + topic_number,
                                       anchor="center", justify="center", wraplength=400, font=label_font)
        self.question_topic_numb.pack(pady=(10, 10))

        self.question_label = tk.Label(frame, text=question_text, anchor="center", justify="center", wraplength=400,
                                       font=label_font)
        self.question_label.pack(pady=(20, 10))

        self.answer_buttons = []
        for i, answer in enumerate(self.quiz_data[self.current_question_index]["Answers"]):
            button = tk.Button(self.root, text=answer,anchor="center", justify="center", command=lambda ans=i: self.check_answer(ans))
            self.answer_buttons.append(button)
            button.pack()

    def check_answer(self, selected_index):
        if self.quiz_data[self.current_question_index]["Community Vote Distribution"] is None:
            correct_answers = self.quiz_data[self.current_question_index]["Correct Answer"]
        else:
            correct_answers = self.quiz_data[self.current_question_index]["Community Vote Distribution"]

        selected_answer = self.quiz_data[self.current_question_index]["Answers"][selected_index]

        isTrue = False
        for answer in correct_answers:
            if answer in selected_answer:
                isTrue = True
                break

        if isTrue:
            self.answer_buttons[selected_index].configure(bg="green")
        else:
            self.answer_buttons[selected_index].configure(bg="red")

        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index < len(self.quiz_data):
            self.question_label.config(text=self.quiz_data[self.current_question_index]["Question"])

            question_number = self.quiz_data[self.current_question_index]["Question Number"]
            topic_number = self.quiz_data[self.current_question_index]["Topic Number"]

            self.question_topic_numb.config(text="Question #" + question_number + " Topic #" + topic_number)

            for button in self.answer_buttons:
                button.destroy()
            self.answer_buttons = []
            for i, answer in enumerate(self.quiz_data[self.current_question_index]["Answers"]):
                button = tk.Button(self.root, text=answer,anchor="center", justify="center", command=lambda ans=i: self.check_answer(ans))
                self.answer_buttons.append(button)
                button.pack()
            self.next_button.config(state=tk.DISABLED)
        else:
            self.question_label.config(text="Quiz Completed!")


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
