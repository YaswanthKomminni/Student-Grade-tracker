import tkinter as tk
from tkinter import messagebox, ttk

# Function to calculate grade based on marks
def calculate_grade(obtained, maximum):
    """Calculate the grade based on obtained marks and maximum marks."""
    percentage = (obtained / maximum) * 100
    if percentage >= 95:
        return 'O'
    elif percentage >= 90:
        return 'A+'
    elif percentage >= 85:
        return 'A'
    elif percentage >= 80:
        return 'B+'
    elif percentage >= 75:
        return 'B'
    elif percentage >= 70:
        return 'c+'
    elif percentage >= 65:
        return 'c'
    elif percentage >= 60:
        return 'D+'
    elif percentage >= 60:
        return 'D'
    else:
        return 'F'

# Function to add subject details to the table
def add_subject():
    """Add a subject to the grade table."""
    try:
        subject_name = entry_subject.get()
        obtained_marks = int(entry_obtained.get())
        max_marks = int(entry_max.get())
        
        # Calculate grade and add to tree view
        grade = calculate_grade(obtained_marks, max_marks)
        subject_data = (subject_name, obtained_marks, max_marks, grade)
        subject_tree.insert("", "end", values=subject_data)
        
        # Clear input fields
        entry_subject.delete(0, tk.END)
        entry_obtained.delete(0, tk.END)
        entry_max.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid marks")

# Function to remove selected subject
def remove_subject():
    """Remove the selected subject from the grade table."""
    selected_item = subject_tree.selection()
    if selected_item:
        subject_tree.delete(selected_item)
    else:
        messagebox.showwarning("Selection Error", "Please select a subject to remove.")

# Function to display results in a new window
def display_results():
    """Display the student's grade report in a new window and save to file."""
    student_name = entry_name.get()
    if not student_name:
        messagebox.showerror("Input Error", "Please enter the student name")
        return
    
    result_window = tk.Toplevel(root)
    result_window.title("Student Grade Report")
    result_window.geometry("400x300")
    
    tk.Label(result_window, text=f"Student Name: {student_name}", font=("Arial", 12, "bold")).pack(pady=10)
    
    # Calculate overall grade
    total_obtained = total_max = 0
    for row in subject_tree.get_children():
        values = subject_tree.item(row)["values"]
        total_obtained += values[1]
        total_max += values[2]
        
    overall_grade = calculate_grade(total_obtained, total_max) if total_max > 0 else "N/A"
    
    # Display each subject and overall grade
    for row in subject_tree.get_children():
        values = subject_tree.item(row)["values"]
        subject = f"{values[0]}: {values[3]} (Marks: {values[1]}/{values[2]})"
        tk.Label(result_window, text=subject, font=("Arial", 10)).pack()
    
    tk.Label(result_window, text=f"\nOverall Grade: {overall_grade}", font=("Arial", 12, "bold")).pack(pady=10)

    # Save to file
    save_to_file(student_name, overall_grade)

# Function to save data to a file
def save_to_file(student_name, overall_grade):
    """Save student data to a file."""
    with open("student_grades.txt", "a") as file:
        file.write(f"Student Name: {student_name}\n")
        file.write("Subject Grades:\n")
        for row in subject_tree.get_children():
            values = subject_tree.item(row)["values"]
            file.write(f"{values[0]}: {values[3]} (Marks: {values[1]}/{values[2]})\n")
        file.write(f"Overall Grade: {overall_grade}\n")
        file.write("--------------\n")
    messagebox.showinfo("Success", "Student data saved to student_grades.txt.")

# Function to initialize default subjects and prompt for marks
def initialize_default_subjects():
    """Initialize with default subjects and prompt for marks."""
    default_subjects = [("Math", 100), ("Science", 100), ("English", 100), ("History", 100), ("Geography", 100), ("Computer", 100)]
    for subject, max_marks in default_subjects:
        obtained_marks = int(input(f"Enter obtained marks for {subject}: "))
        
        grade = calculate_grade(obtained_marks, max_marks)
        subject_tree.insert("", "end", values=(subject, obtained_marks, max_marks, grade))

# Function to show all students' data from file
def show_all_students():
    """Display all students' data saved in the file."""
    try:
        with open("student_grades.txt", "r") as file:
            all_data = file.read()

        # Display in a new window
        all_students_window = tk.Toplevel(root)
        all_students_window.title("All Students Data")
        all_students_window.geometry("500x400")

        text_widget = tk.Text(all_students_window, wrap="word", font=("Arial", 10))
        text_widget.insert("1.0", all_data)
        text_widget.config(state="disabled")  # Make it read-only
        text_widget.pack(expand=True, fill="both")
    except FileNotFoundError:
        messagebox.showerror("File Not Found", "No student data found. Please save some records first.")

# Function to add a new student and clear the current student data
def add_new_student():
    """Clear current student data and allow entry for a new student."""
    entry_name.delete(0, tk.END)
    for row in subject_tree.get_children():
        subject_tree.delete(row)

# Main window setup
root = tk.Tk()
root.title("Student Grade Database")
root.geometry("700x500")

# Student Name
tk.Label(root, text="Student Name:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_name = tk.Entry(root, font=("Arial", 12))
entry_name.grid(row=0, column=1, padx=10, pady=10)

# Subject Input
tk.Label(root, text="Subject Name:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_subject = tk.Entry(root, font=("Arial", 12))
entry_subject.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Marks Obtained:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_obtained = tk.Entry(root, font=("Arial", 12))
entry_obtained.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Maximum Marks:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_max = tk.Entry(root, font=("Arial", 12))
entry_max.grid(row=3, column=1, padx=10, pady=5)

# Buttons
btn_add = tk.Button(root, text="Add Subject", command=add_subject, font=("Arial", 12), bg="#4CAF50", fg="white")
btn_add.grid(row=4, column=0, columnspan=2, pady=10)

btn_remove = tk.Button(root, text="Remove Subject", command=remove_subject, font=("Arial", 12), bg="#f44336", fg="white")
btn_remove.grid(row=5, column=0, columnspan=2, pady=10)

btn_display = tk.Button(root, text="Display Results", command=display_results, font=("Arial", 12), bg="#2196F3", fg="white")
btn_display.grid(row=6, column=0, columnspan=2, pady=10)

btn_show_all = tk.Button(root, text="Show All Students", command=show_all_students, font=("Arial", 12), bg="#FF9800", fg="white")
btn_show_all.grid(row=7, column=0, columnspan=2, pady=10)

# New Student Button (Side by Side)
btn_new_student = tk.Button(root, text="Add New Student", command=add_new_student, font=("Arial", 12), bg="#9C27B0", fg="white")
btn_new_student.grid(row=8, column=0, padx=10, pady=10)

# Treeview Table for Subjects and Grades
subject_tree = ttk.Treeview(root, columns=("Subject", "Obtained", "Maximum", "Grade"), show="headings", height=10)
subject_tree.heading("Subject", text="Subject")
subject_tree.heading("Obtained", text="Obtained Marks")
subject_tree.heading("Maximum", text="Max Marks")
subject_tree.heading("Grade", text="Grade")
subject_tree.column("Subject", width=150)
subject_tree.column("Obtained", width=100)
subject_tree.column("Maximum", width=100)
subject_tree.column("Grade", width=80)
subject_tree.grid(row=1, column=2, rowspan=7, padx=20, pady=10)

root.mainloop()
