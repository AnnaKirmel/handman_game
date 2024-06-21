import tkinter as tk
import random
import winsound
import time
import pygame
from PIL import Image, ImageTk

class HangmanGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Виселица")
        self.root.geometry("1100x550")

        # Adding background image
        self.bg_image = Image.open("C:\\Users\\Professional\\PycharmProjects\\game2\\venv\\Scripts\\i.png")
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        self.canvas = tk.Canvas(self.root, width=200, height=250, bg="white")
        self.canvas.place(x=50, y=50)
        self.hangman_stages = [
            self.canvas.create_line(20, 230, 180, 230, width=2),  # base
            self.canvas.create_line(50, 230, 50, 20, width=2),    # pole
            self.canvas.create_line(50, 20, 150, 20, width=2),    # top bar
            self.canvas.create_line(150, 20, 150, 40, width=2),   # rope
            self.canvas.create_oval(140, 40, 160, 60, width=2),   # head
            self.canvas.create_line(150, 60, 150, 120, width=2),  # body
            self.canvas.create_line(150, 80, 130, 100, width=2),  # left arm
            self.canvas.create_line(150, 80, 170, 100, width=2),  # right arm
            self.canvas.create_line(150, 120, 130, 160, width=2), # left leg
            self.canvas.create_line(150, 120, 170, 160, width=2), # right leg
            self.canvas.create_line(150, 120, 130, 200, width=2), # left leg extension
            self.canvas.create_line(150, 120, 170, 200, width=2)  # right leg extension
        ]
        for part in self.hangman_stages:
            self.canvas.itemconfig(part, state="hidden")

        self.words = ["яблоко", "банан", "вишня", "финик", "клюква", "малина", "черника", "груша", "слива", "персик",
                      "абрикос", "виноград", "гранат", "киви", "манго", "папайя", "ананас", "инжир", "лайм", "лимон",
                      "апельсин", "мандарин", "карамбола", "личи", "маракуйя", "гуава", "дуриан", "питайя", "черешня",
                      "ежевика", "клубника", "голубика", "арония", "барбарис", "облепиха", "рябина", "смородина", "брусника"]
        self.word_to_guess = random.choice(self.words)
        self.guessed_letters = ["_"] * len(self.word_to_guess)
        self.lives = 10

        self.label_word = tk.Label(self.root, text=" ".join(self.guessed_letters), font=("Arial", 24, "bold"), fg="blue", bg="yellow")
        self.label_word.place(x=300, y=300)

        self.entry_letter = tk.Entry(self.root, width=20, font=("Arial", 18))
        self.entry_letter.place(x=300, y=350)

        self.button_guess = tk.Button(self.root, text="Угадать", command=self.guess_letter, font=("Arial", 18, "bold"), fg="green", bg="lightgray")
        self.button_guess.place(x=300, y=400)

        self.button_next = tk.Button(self.root, text="Далее", command=self.next_word)
        self.button_next.place(x=300, y=450)
        self.button_next.pack_forget()  # hide the "Next" button initially

        self.label_lives = tk.Label(self.root, text="Жизней: " + str(self.lives), font=("Arial", 18))
        self.label_lives.place(x=300, y=250)

        self.timer_label = tk.Label(self.root, text="Time: 0 seconds", font=("Arial", 18))
        self.timer_label.place(x=300, y=200)

        self.alphabet_label = tk.Label(self.root, text="Алфавит: а, б, в, г, д, е, ё, ж, з, и, й, к, л, м, н, о, п, р, с, т, у, ф, х, ц, ч, ш, щ, ъ, ы, ь, э, ю, я", font=("Arial", 18), wraplength=500)
        self.alphabet_label.place(x=300, y=100)

        self.checked_letters_label = tk.Label(self.root, text="Проверенные буквы: ", font=("Arial", 18))
        self.checked_letters_label.place(x=300, y=50)

        self.checked_letters = []

        self.timer = 0
        def update_timer():
            self.timer += 1
            self.timer_label.config(text="Time: " + str(self.timer) + " seconds")
            self.root.after(1000, update_timer)  # update every 1 second
        update_timer()

        self.root.bind("<Return>", lambda event: self.button_guess.invoke())

        pygame.mixer.init()

        self.root.mainloop()

    def guess_letter(self):
        letter = self.entry_letter.get()
        self.entry_letter.delete(0, tk.END)

        if letter in self.word_to_guess:
            winsound.Beep(250, 100)  # play a short beep sound
            for i in range(len(self.word_to_guess)):
                if self.word_to_guess[i] == letter:
                    self.guessed_letters[i] = letter
            self.label_word.config(text=" ".join(self.guessed_letters))
        else:
            winsound.Beep(500, 200)  # play a longer beep sound
            self.lives -= 1
            self.label_lives.config(text="Жизней: " + str(self.lives))
            self.canvas.itemconfig(self.hangman_stages[10 - self.lives], state="normal")  # show next hangman part

        self.checked_letters.append(letter)
        self.checked_letters_label.config(text="Проверенные буквы: " + ", ".join(self.checked_letters))

        alphabet_text = "Алфавит: "
        for char in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
            if char in self.checked_letters:
                alphabet_text += char + u'\u0336' + ", "
            else:
                alphabet_text += char + ", "
        self.alphabet_label.config(text=alphabet_text[:-2])  # remove trailing comma and space

        if "_" not in self.guessed_letters:
            self.label_word.config(text="Поздравляем! Вы угадали слово: " + self.word_to_guess)
            self.button_guess.config(state="disabled")
            self.button_next.pack()  # show the "Next" button
            pygame.mixer.music.load("C:\\Users\\Professional\\Downloads\\salutwav.mp3")
            pygame.mixer.music.play()
            self.fireworks()  # call fireworks animation
        elif self.lives == 0:
            self.label_word.config(text="Игра окончена! Слово было: " + self.word_to_guess)
            self.button_guess.config(state="disabled")
            self.button_next.pack()  # show the "Next" button

    def fireworks(self):
        canvas = tk.Canvas(self.root, width=400, height=300)
        canvas.pack()
        colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        for i in range(50):  # increase the number of fireworks
            x = random.randint(0, 400)
            y = random.randint(0, 300)
            radius = random.randint(5, 20)  # vary the size of the fireworks
            color = random.choice(colors)  # choose a random color
            canvas.create_oval(x, y, x + radius, y + radius, fill=color)
            canvas.update()
            time.sleep(0.05)  # decrease the sleep time to make it faster
        for i in range(20):  # add some extra explosions
            x = random.randint(0, 400)
            y = random.randint(0, 300)
            radius = random.randint(10, 30)
            color = random.choice(colors)
            canvas.create_oval(x, y, x + radius, y + radius, fill=color)
            canvas.update()
            time.sleep(0.05)
        canvas.delete("all")
        canvas.pack_forget()

    def next_word(self):
        pygame.mixer.music.stop()  # stop the music when "Next" is clicked
        self.button_next.pack_forget()  # hide the "Next" button
        self.word_to_guess = random.choice(self.words)
        self.guessed_letters = ["_"] * len(self.word_to_guess)
        self.lives = 10
        for part in self.hangman_stages:
            self.canvas.itemconfig(part, state="hidden")  # hide all hangman parts
        self.timer = 0  # reset the timer
        self.label_word.config(text=" ".join(self.guessed_letters))
        self.label_lives.config(text="Жизней: " + str(self.lives))
        self.entry_letter.delete(0, tk.END)
        self.button_guess.config(state="normal")  # enable the "Guess" button
        self.checked_letters = []
        self.checked_letters_label.config(text="Проверенные буквы: ")
        self.alphabet_label.config(text="Алфавит: а, б, в, г, д, е, ё, ж, з, и, й, к, л, м, н, о, п, р, с, т, у, ф, х, ц, ч, ш, щ, ъ, ы, ь, э, ю, я")

if __name__ == "__main__":
    game = HangmanGame()
