import flet as ft
import asyncio

class QuizApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Quiz App"
        self.page.vertical_alignment = "center"
        self.page.horizontal_alignment = "center"
        self.page.padding = 30
        self.page.bgcolor = "#e3f2fd"  # Soft blue background

        # Timer setup (60 seconds)
        self.total_time = 60
        self.remaining_time = self.total_time
        self.timer_text = ft.Text(value="", size=18, color="red", weight="bold")

        # Questions
        self.questions = [
            {"question": "Capital of France?", "options": ["Berlin", "Paris", "Rome", "Madrid"], "answer": "Paris"},
            {"question": "2 + 2?", "options": ["3", "4", "5", "22"], "answer": "4"},
        ]

        self.current_question = 0
        self.user_answers = [None] * len(self.questions)
        self.score = 0

        # Create option list inside a Column
        self.option_column = ft.Column()
        self.radio_group = ft.RadioGroup(
            content=self.option_column,
            on_change=self.option_selected
        )

        self.question_text = ft.Text(size=20, weight="bold")
        self.result_text = ft.Text(size=18, color="green", weight="bold")

        self.prev_btn = ft.ElevatedButton("← Previous", on_click=self.prev_question)
        self.next_btn = ft.ElevatedButton("Next →", on_click=self.next_question)
        self.submit_btn = ft.ElevatedButton("Submit", on_click=self.submit)

        self.page.add(
            self.timer_text,  # Timer at the top
            self.question_text,
            self.radio_group,
            ft.Row([self.prev_btn, self.next_btn, self.submit_btn], alignment="center"),
            self.result_text,
        )

        self.load_question()
        self.page.run_async(self.start_timer())  # Start the timer

    async def start_timer(self):
        while self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_text.value = f"⏰ Time Left: {mins:02d}:{secs:02d}"
            self.page.update()
            await asyncio.sleep(1)
            self.remaining_time -= 1
        self.timer_text.value = "⏰ Time's up!"
        self.page.update()
        await asyncio.sleep(1)
        self.auto_submit()

    def auto_submit(self):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("⏰ Time's up! Submitting automatically..."),
            bgcolor="orange"
        )
        self.page.snack_bar.open = True
        self.page.update()
        self.submit(None)

    def load_question(self):
        q = self.questions[self.current_question]
        self.question_text.value = f"Q{self.current_question+1}: {q['question']}"
        self.option_column.controls.clear()
        for opt in q["options"]:
            self.option_column.controls.append(ft.Radio(value=opt, label=opt))
        self.radio_group.value = self.user_answers[self.current_question]
        self.update_buttons()
        self.page.update()

    def option_selected(self, e):
        self.user_answers[self.current_question] = e.control.value
        self.page.update()

    def next_question(self, e):
        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.load_question()

    def prev_question(self, e):
        if self.current_question > 0:
            self.current_question -= 1
            self.load_question()

    def update_buttons(self):
        self.prev_btn.disabled = self.current_question == 0
        self.next_btn.disabled = self.current_question == len(self.questions) - 1

    def submit(self, e):
        if None in self.user_answers:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Please answer all questions."),
                bgcolor="red"
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        self.score = sum(
            1 for i, q in enumerate(self.questions)
            if self.user_answers[i] == q["answer"]
        )
        self.result_text.value = f"You scored {self.score} out of {len(self.questions)}"
        self.radio_group.visible = False
        self.prev_btn.visible = False
        self.next_btn.visible = False
        self.submit_btn.visible = False
        self.page.update()


def main(page: ft.Page):
    QuizApp(page)

ft.app(target=main)