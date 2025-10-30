

import tkinter as tk # Tkinter is used to create GUI windows, buttons, labels, etc.
from tkinter import ttk, messagebox, simpledialog
# ttk      - provides modern-looking Tkinter widgets like Combobox, Button, etc.
# messagebox - used to show pop-up messages (information, warnings, or errors)
# simpledialog - used to ask the user for text input through a small pop-up box
import os                           # The os module helps check if a file exists and handle file paths
from PIL import ImageTk, Image # For loading and resizing images

root = tk.Tk()
root.title("Student Manager")
root.geometry("600x420")
root.configure(bg="#333333")

# ========================
# STUDENT CLASS
# ========================
class Student:
    def __init__(self, code, name, m1, m2, m3, exam):
        # store the student details
        self.code = code
        self.name = name
        self.coursework = [int(m1), int(m2), int(m3)]
        self.exam = int(exam)

    def total_coursework(self):
        # adds up all coursework marks
        return sum(self.coursework)

    def overall_percentage(self):
        # total mark out of 160 (120 coursework + 40 exam)
        total = self.total_coursework() + self.exam
        percent = (total / 160) * 100
        return round(percent, 2)

    def grade(self):
        # return grade based on percentage
        p = self.overall_percentage()
        if p >= 70:
            return "A"
        elif p >= 60:
            return "B"
        elif p >= 50:
            return "C"
        elif p >= 40:
            return "D"
        else:
            return "F"

# ========================
# FILE HANDLING
# ========================

FILENAME = "studentMarks.txt"  # name of file used to save data

def load_students():
    # read all student records from the file
    lst = []
    if not os.path.exists(FILENAME):
        return lst
    with open(FILENAME, "r") as f:
        lines = f.read().splitlines()
    for line in lines[1:]:  # skip header line
        parts = line.split(",")
        if len(parts) == 6:
            code, name, m1, m2, m3, exam = parts
            lst.append(Student(code, name, m1, m2, m3, exam))
    return lst

def save_students():
    # write all student data back to the file
    with open(FILENAME, "w") as f:
        f.write("Code,Name,CW1,CW2,CW3,Exam\n")
        for s in students:
            f.write(f"{s.code},{s.name},{s.coursework[0]},{s.coursework[1]},"
                    f"{s.coursework[2]},{s.exam}\n")

# ========================
# GUI FUNCTIONS
# ========================

def refresh_dropdown():
    # refresh combobox with student list
    dropdown['values'] = [f"{s.name} ({s.code})" for s in students]

def show_all_records():
    # display all student data in textbox
    output_text.delete("1.0", tk.END)
    if not students:
        output_text.insert(tk.END, "No student records found.\n")
        return
    for s in students:
        output_text.insert(tk.END, f"Name: {s.name}\n")
        output_text.insert(tk.END, f"Code: {s.code}\n")
        output_text.insert(tk.END, f"Coursework Total: {s.total_coursework()}\n")
        output_text.insert(tk.END, f"Exam: {s.exam}\n")
        output_text.insert(tk.END,
            f"Overall %: {s.overall_percentage()} | Grade: {s.grade()}\n")
        output_text.insert(tk.END, "-" * 40 + "\n")

def show_highest_score():
    # find and show student with highest percentage
    if not students:
        messagebox.showinfo("Info", "No records available.")
        return
    s = max(students, key=lambda x: x.overall_percentage())
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END,
        f"Highest Scorer:\n{s.name} ({s.code}) - {s.overall_percentage()}% ({s.grade()})\n")

def show_lowest_score():
    # find and show student with lowest percentage
    if not students:
        messagebox.showinfo("Info", "No records available.")
        return
    s = min(students, key=lambda x: x.overall_percentage())
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END,
        f"Lowest Scorer:\n{s.name} ({s.code}) - {s.overall_percentage()}% ({s.grade()})\n")

def show_individual_record():
    # show details for one student selected in dropdown
    sel = dropdown.get()
    if not sel:
        messagebox.showwarning("Warning", "Please select a student.")
        return
    code = sel.split("(")[-1][:-1]  # get code inside brackets
    for s in students:
        if s.code == code:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, f"Name: {s.name}\n")
            output_text.insert(tk.END, f"Code: {s.code}\n")
            output_text.insert(tk.END, f"Coursework Total: {s.total_coursework()}\n")
            output_text.insert(tk.END, f"Exam: {s.exam}\n")
            output_text.insert(tk.END,
                f"Overall %: {s.overall_percentage()} | Grade: {s.grade()}\n")
            break

def add_new_student():
    # simple way to add a student manually
    code = simpledialog.askstring("Input", "Enter student code:")
    name = simpledialog.askstring("Input", "Enter student name:")
    m1 = simpledialog.askstring("Input", "Enter coursework 1 mark:")
    m2 = simpledialog.askstring("Input", "Enter coursework 2 mark:")
    m3 = simpledialog.askstring("Input", "Enter coursework 3 mark:")
    exam = simpledialog.askstring("Input", "Enter exam mark:")

    if not (code and name and m1 and m2 and m3 and exam):
        messagebox.showwarning("Warning", "All fields are required.")
        return

    try:
        new_s = Student(code, name, m1, m2, m3, exam)
        students.append(new_s)
        save_students()
        refresh_dropdown()
        messagebox.showinfo("Success", f"Record for {name} added.")
    except ValueError:
        messagebox.showerror("Error", "Please enter numbers for marks only.")

# ========================
# MAIN GUI WINDOW
# ========================

students = load_students()  # read from file

# --- Title ---
title_label = tk.Label(root, text="Student Manager", font=("Arial", 16, "bold"), bg="#E7F2EF")
title_label.pack(pady=10)

# --- Buttons section ---
top_frame = tk.Frame(root, bg="#E7F2EF")
top_frame.pack(pady=5)

tk.Button(top_frame, text="View All Records", width=18, bg ="lightblue", command=show_all_records).grid(row=0, column=0, padx=5)
tk.Button(top_frame, text="Highest Score", width=15, bg = "lightblue", command=show_highest_score).grid(row=0, column=1, padx=5)
tk.Button(top_frame, text="Lowest Score", bg = "lightblue", width=15, command=show_lowest_score).grid(row=0, column=2, padx=5)
tk.Button(top_frame, text="Add Student", bg = "lightblue", width=15, command=add_new_student).grid(row=0, column=3, padx=5)

# --- Individual student selection ---
ind_frame = tk.Frame(root, bg="#E7F2EF")
ind_frame.pack(pady=10)

tk.Label(ind_frame, text="Select Student:", bg="lightblue").grid(row=0, column=0, padx=5)
dropdown = ttk.Combobox(ind_frame, width=25)
dropdown.grid(row=0, column=1, padx=5)
tk.Button(ind_frame, text="View Record", bg="lightblue", command=show_individual_record).grid(row=0, column=2, padx=5)

refresh_dropdown()

# --- Output box ---
output_text = tk.Text(root, width=70, height=15, bg="lightblue")
output_text.pack(pady=10)

root.mainloop()

