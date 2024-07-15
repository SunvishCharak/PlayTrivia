from tkinter import Tk, Canvas, StringVar, Label, Radiobutton, Button, Frame, messagebox
from quiz_brain import QuizBrain

BACKGROUND_COLOR = "#7289da"  # New background color
QUESTION_COLOR = "#23272a"  # New question color
BUTTON_BG_COLOR = "#99aab5"  # New button background color
BUTTON_TEXT_COLOR = "black"  # Button text color

class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain) -> None:
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("PlayTrivia")
        self.window.geometry("850x600")  # Increased height for more space
        self.window.config(bg=BACKGROUND_COLOR)  # Set new background color

        # Display Title
        self.display_title()

        # Creating a canvas for question text, and display question
        self.canvas = Canvas(width=800, height=250, bg=BACKGROUND_COLOR, highlightthickness=0)  # Set canvas background color
        self.question_text = self.canvas.create_text(
            400, 125,
            text="Question here",
            width=680,
            fill=QUESTION_COLOR,  # Set question color
            font=('poppins', 20, 'bold')  # Font bold and size
        )
        self.canvas.grid(row=2, column=0, columnspan=2, pady=50)
        self.display_question()

        # Declare a StringVar to store user's answer
        self.user_answer = StringVar()

        # Display four options (radio buttons)
        self.opts = self.radio_buttons()
        self.display_options()

        # To show whether the answer is correct or wrong
        self.feedback = Label(self.window, pady=10, font=("poppins", 15, "bold"), bg=BACKGROUND_COLOR)
        self.feedback.place(x=300, y=440)  # Positioning lower in the window

        # Submit, Next, and Quit Buttons
        self.buttons()

        # Mainloop
        self.window.mainloop()

    def display_title(self):
        """To display title"""

        # Title
        title = Label(self.window, text="PlayTrivia",
                      width=20, bg=BACKGROUND_COLOR, fg="Black", font=("poppins", 20, "bold"))

        # place of the title
        title.place(relx=0.5, y=2, anchor='n')

    def display_question(self):
        """To display the question"""

        q_text = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text=q_text)

    def radio_buttons(self):
        """To create four options (radio buttons)"""

        # initialize the list with an empty list of options
        choice_list = []

        # position of the first option
        y_pos = 220

        # adding the options to the list
        while len(choice_list) < 4:

            # setting the radio button properties
            radio_btn = Radiobutton(self.window, text="", variable=self.user_answer,
                                    value='', font=("poppins", 16), bg=BACKGROUND_COLOR, fg="black", anchor='w', justify='left')

            # adding the button to the list
            choice_list.append(radio_btn)

            # placing the button
            radio_btn.place(x=200, y=y_pos, width=450, height=40)  # Ensure equal width and height

            # incrementing the y-axis position by 40
            y_pos += 50

        # return the radio buttons
        return choice_list

    def display_options(self):
        """To display four options"""

        val = 0

        # deselecting the options
        self.user_answer.set(None)

        # looping over the options to be displayed for the
        # text of the radio buttons.
        for option in self.quiz.current_question.choices:
            self.opts[val]['text'] = option
            self.opts[val]['value'] = option
            val += 1

    def submit_btn(self):
        """To show feedback for the selected answer"""

        # Check if the answer is correct
        if self.quiz.check_answer(self.user_answer.get()):
            self.feedback["fg"] = "#006400"
            self.feedback["text"] = 'Correct answer! \U0001F44D'
        else:
            self.feedback['fg'] = "#ff2800"
            self.feedback['text'] = ('\u274E Oops! \n'
                                     f'The right answer is: {self.quiz.current_question.correct_answer}')

    def next_btn(self):
        """To move to the next question"""

        if self.quiz.has_more_questions():
            # Moves to next to display next question and its options
            self.display_question()
            self.display_options()
            self.feedback['text'] = ""
        else:
            # if no more questions, then it displays the score
            self.display_result()

            # destroys the self.window
            self.window.destroy()

    def buttons(self):
        """To show submit, next, and quit buttons"""

        # The first button is the Submit button to submit the answer
        submit_button = Button(self.window, text="Submit", command=self.submit_btn,
                               width=10, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, font=("poppins", 16, "bold"))

        # placing the submit button on the screen
        submit_button.place(x=250, y=510)  # Adjusted y position for lower placement

        # The second button is the Next button to move to the next question
        next_button = Button(self.window, text="Next", command=self.next_btn,
                             width=10, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, font=("poppins", 16, "bold"))

        # placing the next button on the screen
        next_button.place(x=400, y=510)  # Adjusted y position for lower placement

        # This is the third button which is used to Quit the window
        quit_button = Button(self.window, text="Quit", command=self.window.destroy,
                             width=5, bg=BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, font=("poppins", 16, "bold"))

        # placing the Quit button on the screen
        quit_button.place(x=700, y=50)

    def display_result(self):
        """To display the result using messagebox"""
        correct, wrong, score_percent = self.quiz.get_score()

        correct = f"Correct: {correct}"
        wrong = f"Wrong: {wrong}"

        # calculates the percentage of correct answers
        result = f"Score: {score_percent}%"

        # Shows a message box to display the result
        messagebox.showinfo("Result", f"{result}\n{correct}\n{wrong}")

