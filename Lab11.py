import os
import matplotlib.pyplot as plt

def load_students():
    students = {}
    with open('students.txt', 'r') as f:
        for line in f:
            id, name = line[:3], line[3:].strip()
            students[name] = id
    return students
def load_assignments():
    assignments = {}
    with open('assignments.txt', 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 3):
            name = lines[i].strip()
            id = lines[i + 1].strip()
            points = int(lines[i + 2].strip())
            assignments[name] = {'id': id, 'points': points}
    return assignments
def load_submissions():
    submissions = {}
    for filename in os.listdir('submissions'):
        if filename.endswith('.txt'):
            with open(os.path.join('submissions', filename), 'r') as f:
                for line in f:
                    student_id, assignment_id, score = line.strip().split('|')
                    if student_id not in submissions:
                        submissions[student_id] = {}
                    submissions[student_id][assignment_id] = float(score)
    return submissions

def calculate_student_grade(name, students, assignments, submissions):
    if name not in students:
        return "Student not found"
    student_id = students[name]
    total_score = 0
    total_points = 0
    for assignment, details in assignments.items():
        if details['id'] in submissions[student_id]:
            score = submissions[student_id][details['id']]
            total_score += score * details['points'] / 100
            total_points += details['points']
    return f"{round((total_score / total_points) * 100)}%"
def calculate_assignment_stats(name, assignments, submissions):
    if name not in assignments:
        return "Assignment not found"
    assignment_id = assignments[name]['id']
    scores = [submissions[student][assignment_id] for student in submissions if assignment_id in submissions[student]]

    total = sum(scores)
    count = len(scores)
    avg = int(total / count)

    return f"Min: {min(scores):.0f}%\nAvg: {avg}%\nMax: {max(scores):.0f}%"

def assignment_histogram(assignment_name, assignments, submissions):
    if assignment_name not in assignments:
        print("Assignment not found")
        return

    assignment_id = assignments[assignment_name]['id']
    scores = [
        submissions[student][assignment_id]
        for student in submissions
        if assignment_id in submissions[student]
    ]
    if not scores:
        print("No scores available for this assignment")
        return

    bins = [i for i in range(40, 101, 10)]
    plt.hist(scores, bins=bins, edgecolor='black', color='skyblue')
    plt.title({assignment_name})
    plt.xlabel("Score Range (%)")
    plt.ylabel("###")
    plt.xticks(bins)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlim(40, 100)
    plt.show()

def main():
    students = load_students()
    assignments = load_assignments()
    submissions = load_submissions()
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    print()
    choice = input("Enter your selection: ")
    if choice == '1':
        name = input("What is the student's name: ")
        print(calculate_student_grade(name, students, assignments, submissions))
    elif choice == '2':
        name = input("What is the assignment name: ")
        print(calculate_assignment_stats(name, assignments, submissions))
    elif choice == '3':
        name = input("What is the assignment name: ")
        assignment_histogram(name, assignments, submissions)


if __name__ == "__main__":
    main()
