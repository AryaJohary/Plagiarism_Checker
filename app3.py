import os
import tkinter as tk
from tkinter import filedialog
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from decimal import Decimal

# Function to check plagiarism
def check_plagiarism():
    student_files = selected_files_with_path.get(0,tk.END)
    student_notes = [open(file, encoding='utf-8').read() for file in student_files]

    def vectorize(Text):
        return TfidfVectorizer().fit_transform(Text).toarray()

    def similarity(doc1, doc2):
        return cosine_similarity([doc1, doc2])

    vectors = vectorize(student_notes)
    print(vectors)
    s_vectors = list(zip(student_files, vectors))
    plagiarism_results = set()

    for student_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((student_a, text_vector_a))
        del new_vectors[current_index]
        for student_b, text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            # print("sim score = ", similarity(text_vector_a, text_vector_b))
            sim_score = round(sim_score*100, 2)
            student_pair = sorted((student_a, student_b))
            score = (student_pair[0], student_pair[1], sim_score)
            plagiarism_results.add(score)
    return plagiarism_results

# Function to browse and select text files
def browse_files():
    enable_boxes()
    file_paths = filedialog.askopenfilenames(filetypes=[("Text Files", "*.txt")])
    if file_paths:
        for path in file_paths:
            selected_files_with_path.insert(tk.END, path)
    disable_boxes()

# Function to check plagiarism for selected files
def check_selected_files():
    enable_boxes()
    selected_files = selected_files_with_path.get(0, tk.END)
    if len(selected_files) < 2:
        result_label.config(text="Select at least two files.")
        result_text.delete(1.0, tk.END)
        return
    plagiarism_results = check_plagiarism()
    result_label.config(text="Plagiarism Check Results:")
    result_text.delete(1.0, tk.END)
    for data in plagiarism_results:
        result_text.insert(tk.END, f"{data[0]}  vs  {data[1]} - \nSimilarity Score: {data[2]}%\n\n")
    disable_boxes()

# Function to clear the browsing window list and result window list
def clear_list():
    enable_boxes()
    selected_files_with_path.delete(0, tk.END)
    result_text.delete(1.0, tk.END)
    disable_boxes()

# Function to disable writing states of text boxes
def disable_boxes():
    selected_files_with_path.configure(state="disabled")
    result_text.configure(state="disabled")

# Function to enable normal states of text boxes
def enable_boxes():
    selected_files_with_path.configure(state="normal")
    result_text.configure(state="normal")

# Main GUI window
root = tk.Tk()
root.title("Assignment Plagiarism Checker - Project by Arya Johary")

# Create and place GUI elements
project_title_label = tk.Label(root, text="Assignment Plagiarism Checker", font=("Arial", 16, "bold"), pady=10)
by_label = tk.Label(root, text="Project 5th Semester", font=("Arial", 12))
college_label = tk.Label(root, text="UEM Jaipur", font=("Arial", 12))
browse_button = tk.Button(root, text="Browse Files", command=browse_files)
selected_files_with_path = tk.Listbox(root, selectmode=tk.MULTIPLE, font=("Arial", 12))
check_button = tk.Button(root, text="Check Plagiarism", command=check_selected_files)
clear_button = tk.Button(root, text="Clear", command=clear_list)
result_label = tk.Label(root, text="")
result_text = tk.Text(root, height=10, width=40, font=("Arial", 12))
disable_boxes()

# Place GUI elements in the window
project_title_label.pack()
by_label.pack()
college_label.pack()
browse_button.pack(pady=10)
selected_files_with_path.pack()
check_button.pack(pady=10)
clear_button.pack()
result_label.pack()     
result_text.pack(padx=10, pady=10)

root.mainloop()


# features to add
# use image to get text using OCR
# then compare text data
# support for pdf files and doc files
# crawl internet to find if text is copied from internet

# let's first use OCR to get data 
