# gradebook.py
# Author: [vikash rawat]
# Date: November 22, 2025
# Title: GradeBook Analyzer - Mini Project
# Description: CLI tool for analyzing and reporting student grades from manual input or CSV.

import csv
import sys

# --- Core Statistical Functions (Task 3) ---

def calculate_average(marks_dict):
    """Calculates the mean (average) score."""
    if not marks_dict:
        return 0.0
    # Use values() to get all marks, then sum and divide by the count
    total_marks = sum(marks_dict.values())
    count = len(marks_dict)
    return total_marks / count

def calculate_median(marks_dict):
    """Calculates the median score."""
    if not marks_dict:
        return 0.0
    
    # 1. Get all marks and convert to a sorted list
    sorted_marks = sorted(marks_dict.values())
    n = len(sorted_marks)
    
    # 2. Find the middle index
    middle_index = n // 2
    
    if n % 2 == 1:
        # Odd number of students: return the middle element
        return sorted_marks[middle_index]
    else:
        # Even number of students: return the average of the two middle elements
        return (sorted_marks[middle_index - 1] + sorted_marks[middle_index]) / 2

def find_max_score(marks_dict):
    """Finds the highest score."""
    if not marks_dict:
        return 0
    return max(marks_dict.values())

def find_min_score(marks_dict):
    """Finds the lowest score."""
    if not marks_dict:
        return 0
    return min(marks_dict.values())

# --- Grade Assignment (Task 4) ---

def assign_grade(score):
    """Assigns a letter grade based on the score."""
    # Grading scheme: A: 90+, B: 80-89, C: 70-79, D: 60-69, F: <60 [cite: 50]
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

def calculate_grades_and_distribution(marks_dict):
    """Calculates grades for all students and their distribution."""
    grades_dict = {}
    grade_distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}

    for student, mark in marks_dict.items():
        grade = assign_grade(mark)
        grades_dict[student] = grade
        grade_distribution[grade] += 1
    
    return grades_dict, grade_distribution

# --- Data Entry Methods (Task 2) ---

def manual_data_entry():
    """Allows manual entry of student names and marks."""
    print("\n--- Manual Data Entry ---")
    marks = {}
    while True:
        name = input("Enter student name (or type 'done' to finish): ").strip()
        if name.lower() == 'done':
            break
        if not name:
            continue
            
        while True:
            try:
                mark = int(input(f"Enter mark for {name} (0-100): "))
                if 0 <= mark <= 100:
                    marks[name] = mark
                    break
                else:
                    print("Mark must be between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a whole number for the mark.")
    
    return marks

def load_data_from_csv(filename):
    """Loads student names and marks from a specified CSV file."""
    marks = {}
    try:
        # 'r' for read mode, newline='' for consistent line ending handling
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader) # Skip the header row (assuming: Name, Mark)
            for row in reader:
                if len(row) >= 2:
                    student_name = row[0].strip()
                    try:
                        mark = int(row[1].strip())
                        if 0 <= mark <= 100:
                            marks[student_name] = mark
                        else:
                            print(f"Skipping {student_name}: Mark {mark} out of range.")
                    except ValueError:
                        print(f"Skipping {student_name}: Invalid mark value.")
                else:
                    print(f"Skipping row: Not enough data: {row}")

        print(f"\nSuccessfully loaded {len(marks)} student records from {filename}.")
    except FileNotFoundError:
        print(f"\nERROR: File '{filename}' not found. Please check the path and try again.")
        return None
    except Exception as e:
        print(f"\nAn unexpected error occurred during CSV loading: {e}")
        return None
        
    return marks

# --- Analysis and Reporting (Task 5 & 6) ---

def print_analysis_summary(marks_dict):
    """Displays the key statistical analysis results."""
    print("\n" + "="*40)
    print("      📊 Statistical Analysis Summary")
    print("="*40)
    
    if not marks_dict:
        print("No student data available to analyze.")
        return

    # Calculate statistics
    avg = calculate_average(marks_dict)
    median = calculate_median(marks_dict)
    maximum = find_max_score(marks_dict)
    minimum = find_min_score(marks_dict)

    print(f"Total Students: {len(marks_dict)}")
    print(f"Average Score:  {avg:.2f}")
    print(f"Median Score:   {median:.2f}")
    print(f"Highest Score:  {maximum}")
    print(f"Lowest Score:   {minimum}")
    print("="*40)

def print_grade_distribution(distribution):
    """Prints the count of students per letter grade."""
    print("\n--- Grade Distribution (A-F) ---")
    
    # Use f-strings and \t (tabs) for clean, columnar formatting
    print(f"Grade\t| Count")
    print("-" * 15)
    for grade, count in distribution.items():
        print(f"{grade}\t| {count}")
    print("-" * 15)
    
def print_pass_fail_summary(marks_dict):
    """Uses list comprehension to filter and print pass/fail students (Pass threshold: 40)."""
    
    # List Comprehension (Task 5)
    # Get a list of (student_name, score) tuples for easy filtering
    student_score_list = list(marks_dict.items())
    
    # Filter for passed students (score >= 40)
    passed_students = [(name, score) for name, score in student_score_list if score >= 40] # [cite: 57]
    
    # Filter for failed students (score < 40)
    failed_students = [(name, score) for name, score in student_score_list if score < 40] # [cite: 59]
    
    print("\n--- Pass/Fail Analysis (Threshold >= 40) ---")
    print(f"✅ Total Passed Students: {len(passed_students)}")
    print(f"❌ Total Failed Students: {len(failed_students)}")

    # Print names of failed students
    if failed_students:
        print("\nFailed Students (Name | Score):")
        for name, score in failed_students:
            print(f"\t- {name} ({score})")
    
    
def print_results_table(marks_dict, grades_dict):
    """Prints the final, formatted results table (Task 6)."""
    if not marks_dict:
        return
        
    print("\n" + "="*45)
    print("         📑 Final Student GradeBook")
    print("="*45)
    
    # Define column widths for consistent spacing
    NAME_WIDTH = 15
    MARK_WIDTH = 10
    GRADE_WIDTH = 10

    # Print Header
    header = f"{'Name':<{NAME_WIDTH}} {'Marks':<{MARK_WIDTH}} {'Grade':<{GRADE_WIDTH}}"
    print(header)
    print("-" * 45)

    # Print Data
    for student, mark in marks_dict.items():
        grade = grades_dict.get(student, 'N/A')
        # Use f-strings for clean formatting (Task 6)
        print(f"{student:<{NAME_WIDTH}} {mark:<{MARK_WIDTH}} {grade:<{GRADE_WIDTH}}")

    print("="*45)


# --- Main CLI Loop (Task 6) ---

def main():
    """Main application loop for the GradeBook Analyzer CLI."""
    # Task 1: Print welcome message and basic usage menu
    print("\n******************************************")
    print("  👋 Welcome to the GradeBook Analyzer CLI")
    print("******************************************")
    
    while True: # CLI Loop (Task 6)
        print("\n--- Main Menu ---")
        print("1. Enter marks manually")
        print("2. Load marks from CSV file")
        print("3. Exit program")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            marks_data = manual_data_entry()
        elif choice == '2':
            # Note: For testing, create a file named 'grades.csv' in the project folder
            csv_file = input("Enter the CSV filename (e.g., grades.csv): ").strip()
            marks_data = load_data_from_csv(csv_file)
        elif choice == '3':
            print("\nGoodbye! Happy analyzing.")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue
            
        # Proceed only if we have data to analyze
        if marks_data:
            if not marks_data:
                print("\nNo data was entered or loaded. Returning to menu.")
                continue
                
            # Task 4: Calculate grades and distribution
            student_grades, grade_counts = calculate_grades_and_distribution(marks_data)
            
            # Print Analysis and Reports
            print_analysis_summary(marks_data) # Task 3
            print_grade_distribution(grade_counts) # Task 4
            print_pass_fail_summary(marks_data) # Task 5
            print_results_table(marks_data, student_grades) # Task 6
            
            # Loop continues, allowing the user to repeat analysis (Task 6)
            
if __name__ == "__main__":
    main()