
import random  # Imports the random module to generate random numbers for quiz questions
import tkinter as tk  # Imports the tkinter module and assigns it the alias 'tk' for creating GUI windows
from tkinter import messagebox  # Imports the messagebox module from tkinter to show pop-up alerts
from PIL import ImageTk, Image  # Imports PIL modules: ImageTk to display images in Tkinter, Image to open and manipulate images

root = tk.Tk()
root.title("Math Quiz")
root.geometry("500x350")  # Set window size

# Load and display background image
bg_image = Image.open("mathquiz.jpg")  # Open image file
bg_image = bg_image.resize((500, 350))  # Resize to fit window
bg_photo = ImageTk.PhotoImage(bg_image)  # Convert to Tkinter image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place image to fill window
bg_label.lower()  # Keep background behind widgets

# Global variables to track quiz state
difficulty = 1  # Stores difficulty level selected by user
current_question = 0  # Current question number (0-9)
score = 0  # Total score
attempt = 1  # Track whether user is on first or second try
answer_entry = None  # Tkinter Entry widget to get user's answer

# Clear all widgets except background
def clear_frame():
    for widget in root.winfo_children():
        if widget != bg_label:
            widget.destroy()  # Remove widget from window

# Display main menu with difficulty options
def displayMenu():
    clear_frame()  # Remove previous widgets
    tk.Label(root, text="Choose Difficulty Level", font=("Arial", 16), bg="#ffffff").pack(pady=10)
    tk.Button(root, text="Easy (Single digits)", width=30, command=lambda: startQuiz(1)).pack(pady=5)
    tk.Button(root, text="Moderate (Double digits)", width=30, command=lambda: startQuiz(2)).pack(pady=5)
    tk.Button(root, text="Advanced (Four digits)", width=30, command=lambda: startQuiz(3)).pack(pady=5)
    tk.Label(root, text="Try to answer correctly on the first attempt for full points.", font=("Arial", 10), bg="#ffffff").pack(pady=10)

# Generate random number based on difficulty
def randomInt(level):
    if level == 1:
        return random.randint(1, 9)  # Easy: 1-9
    elif level == 2:
        return random.randint(10, 99)  # Moderate: 10-99
    else:
        return random.randint(1000, 9999)  # Advanced: 1000-9999

# Randomly choose an operation
def decideOperation():
    return random.choice(['+', '-'])  # Return '+' or '-'

# Display math problem for user to solve
def displayProblem(num1, num2, op):
    global answer_entry
    clear_frame()  # Remove old widgets
    tk.Label(root, text=f"Question {current_question+1} of 10", font=("Arial", 14), bg="#ffffff").pack(pady=5)
    tk.Label(root, text=f"Current score: {score}/100", font=("Arial", 12), bg="#ffffff").pack(pady=5)
    tk.Label(root, text=f"What is {num1} {op} {num2}?", font=("Arial", 18), bg="#ffffff").pack(pady=10)
    answer_entry = tk.Entry(root, font=("Arial", 14))  # Input box for answer
    answer_entry.pack(pady=5)
    answer_entry.focus()  # Automatically focus cursor
    tk.Button(root, text="Submit Answer", command=checkAnswer).pack(pady=10)  # Button to submit answer

# Check if user's answer is correct
def isCorrect(user_ans, correct_ans):
    return user_ans == correct_ans  # Return True if correct, False otherwise

# Display final results and feedback
def displayResults():
    clear_frame()  # Remove previous widgets
    grade = "F"  # Default grade
    if score >= 90: grade = "A+"
    elif score >= 80: grade = "A"
    elif score >= 70: grade = "B"
    elif score >= 60: grade = "C"
    elif score >= 50: grade = "D"

    tk.Label(root, text="Quiz Complete", font=("Arial", 16), bg="#ffffff").pack(pady=10)
    tk.Label(root, text=f"Your final score: {score}/100", font=("Arial", 14), bg="#ffffff").pack(pady=5)
    tk.Label(root, text=f"Your grade: {grade}", font=("Arial", 14), bg="#ffffff").pack(pady=5)

    # Friendly feedback based on score
    if score >= 80:
        tk.Label(root, text="Great job! You did very well.", font=("Arial", 12), bg="#ffffff").pack(pady=5)
    elif score >= 50:
        tk.Label(root, text="Good effort! Keep practicing to improve.", font=("Arial", 12), bg="#ffffff").pack(pady=5)
    else:
        tk.Label(root, text="Don't worry, try again and you'll get better.", font=("Arial", 12), bg="#ffffff").pack(pady=5)

    # Buttons to play again or exit
    tk.Button(root, text="Play Again", width=20, command=displayMenu).pack(pady=5)
    tk.Button(root, text="Exit", width=20, command=root.quit).pack(pady=5)

# Start quiz with selected difficulty
def startQuiz(level):
    global difficulty, current_question, score, attempt
    difficulty = level  # Set selected difficulty
    current_question = 0  # Reset question counter
    score = 0  # Reset score
    attempt = 1  # Reset attempt count
    nextQuestion()  # Display first question

# Generate next question
def nextQuestion():
    global num1, num2, op, correct_ans, attempt, current_question
    if current_question >= 10:  # End of quiz
        displayResults()
        return
    num1 = randomInt(difficulty)  # Generate first number
    num2 = randomInt(difficulty)  # Generate second number
    op = decideOperation()  # Choose operation
    correct_ans = num1 + num2 if op == '+' else num1 - num2  # Compute correct answer
    attempt = 1  # Reset attempt for new question
    displayProblem(num1, num2, op)  # Show problem

# Handle answer submission
def checkAnswer():
    global score, attempt, current_question
    try:
        user_ans = int(answer_entry.get())  # Read user input
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a valid number.")  # Not a number
        return

    if isCorrect(user_ans, correct_ans):  # Correct answer
        points = 10 if attempt == 1 else 5  # Full points first attempt, half second attempt
        score += points
        messagebox.showinfo("Correct!", f"Good job! You earned {points} points.")
        current_question += 1
        nextQuestion()  # Move to next question
    else:  # Incorrect answer
        if attempt == 1:  # First try wrong
            attempt += 1
            messagebox.showinfo("Try Again", "Not quite right. Try once more.")
            answer_entry.delete(0, tk.END)  # Clear input
        else:  # Second try wrong
            current_question += 1
            messagebox.showinfo("Incorrect", f"The correct answer was {correct_ans}. Let's move to the next question.")
            nextQuestion()  # Move to next question

# Start program by displaying the menu
displayMenu()
root.mainloop()
