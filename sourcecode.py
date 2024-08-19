import openai
import random
import json
import datetime

# Set your OpenAI API key here
#You can load it in a more secure way
openai.api_key = "sk****************************"

# Define the list of topics and subtopics
topics = {
    "Beginner": {
        "Data Types and Variables": [
            "Integers, Floats, Strings, Booleans",
            "Type Conversion",
            "Variables and Assignment"
        ],
        "Basic Operators": [
            "Arithmetic Operators",
            "Comparison Operators",
            "Logical Operators"
        ],
        "Control Structures": [
            "Conditional Statements (if, elif, else)",
            "Loops (for, while)",
            "break, continue, and pass"
        ],
        "Basic Data Structures": [
            "Lists",
            "Tuples",
            "Sets",
            "Dictionaries"
        ],
        "Functions": [
            "Defining and Calling Functions",
            "Arguments and Return Values",
            "Local and Global Variables"
        ],
        "Modules and Packages": [
            "Importing Modules",
            "Exploring the Standard Library"
        ]
    },
    "Intermediate": {
        "List Comprehensions": [],
        "Functions (continued)": [
            "Lambda Functions",
            "*args and **kwargs",
            "Decorators",
            "Generators"
        ],
        "File Handling": [
            "Reading and Writing Files",
            "Working with Directories",
            "Exception Handling during I/O"
        ],
        "Error and Exception Handling": [
            "try, except, finally",
            "Custom Exceptions"
        ],
        "Classes and Object-Oriented Programming (OOP)": [
            "Classes and Objects",
            "Inheritance",
            "Polymorphism",
            "Encapsulation"
        ],
        "Intermediate Data Structures": [
            "Stacks, Queues, Linked Lists (using collections module)"
        ],
        "Regular Expressions": [],
        "Working with External Libraries": [
            "pip and Package Management",
            "Common Libraries: requests, numpy, pandas"
        ]
    },
    "Advanced": {
        "Advanced OOP Concepts": [
            "Metaclasses",
            "Decorators in Classes",
            "Abstract Base Classes"
        ],
        "Multithreading and Multiprocessing": [],
        "Networking and APIs": [
            "Building APIs with Flask or Django",
            "Consuming APIs with Python"
        ],
        "Databases": [
            "SQLite, MySQL, PostgreSQL with Python",
            "ORMs like SQLAlchemy"
        ],
        "Advanced Libraries and Frameworks": [
            "Web Development (Django, Flask)",
            "Data Science (SciPy, Matplotlib)",
            "Machine Learning (TensorFlow, Scikit-Learn)"
        ],
        "Memory Management and Optimization": [],
        "Python C Extensions": [],
        "Asynchronous Programming": [
            "Async/Await",
            "Asynchronous Frameworks (e.g., FastAPI)"
        ]
    }
}

#Generating the tutorial using OpenAI 
def generate_tutorial(topic):
    """Generate a tutorial on the given topic."""
    prompt = f"Provide a tutorial on '{topic}' in Python."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a knowledgeable Python programming tutor."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.7
    )

    tutorial_text = response.choices[0].message["content"].strip()
    return tutorial_text

#Generating the respective quizzes
def generate_quiz(topic, subtopics):
    """Generate a detailed quiz with multiple-choice questions and answers on the topic."""
    subtopics_str = ', '.join(subtopics)
    prompt = f"Create a detailed quiz with multiple-choice questions and answers on the topic '{topic}' including the following subtopics: {subtopics_str}."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a knowledgeable Python programming tutor."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )

    quiz = response.choices[0].message["content"].strip()
    return quiz

def parse_quiz(quiz):
    """Parse the generated quiz into questions and answers."""
    lines = quiz.split("\n")
    questions = []
    current_question = None

    for line in lines:
        line = line.strip()
        if line.startswith("Q:"):
            if current_question:
                questions.append(current_question)
            current_question = {"question": line, "options": [], "answer": None}
        elif line and current_question:
            if line[0] in "ABCD" and line[1] == ')':
                current_question["options"].append(line)
            elif line.startswith("Answer:"):
                current_question["answer"] = line.split(":")[1].strip()

    if current_question:
        questions.append(current_question)

    return questions

def run_quiz(quiz):
    """Run the quiz and evaluate user responses."""
    questions = parse_quiz(quiz)
    correct_answers = 0

    for q in questions:
        print(q["question"])
        for option in q["options"]:
            print(option)
        user_answer = input("Your answer (A, B, C, D): ").strip().upper()

        if user_answer and any(user_answer in option for option in q["options"]):
            if any(option.startswith(user_answer) for option in q["options"] if q["answer"] in option):
                print("Correct!")
                correct_answers += 1
            else:
                print(f"Wrong! The correct answer is: {q['answer']}")
        else:
            print("Invalid answer. Skipping question.")

    print(f"\nYou got {correct_answers} out of {len(questions)} questions correct.")

#Chatbot feature - model works in multiple languages
def chatbot_interaction():
    """Interactive chatbot for general Python questions."""
    print("You can ask me any question about Python. Type 'quit' to exit the chatbot.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful Python programming assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )
        print("Bot:", response.choices[0].message["content"].strip())

#streak feature
def save_streak(user_data, user):
    """Save the user's streak data to a file."""
    with open("streaks.json", "w") as file:
        json.dump(user_data, file, indent=4)

def load_streak():
    """Load streak data from a file."""
    try:
        with open("streaks.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def update_streak(user):
    """Update the user's streak information."""
    user_data = load_streak()
    today = datetime.date.today().isoformat()
    
    if user in user_data:
        last_activity = user_data[user]['last_activity']
        if last_activity == today:
            print("You have already practiced today! Keep up the good work.")
        else:
            user_data[user]['last_activity'] = today
            if (datetime.date.fromisoformat(today) - datetime.date.fromisoformat(last_activity)).days == 1:
                user_data[user]['streak'] += 1
            else:
                user_data[user]['streak'] = 1
    else:
        user_data[user] = {'last_activity': today, 'streak': 1}
    
    save_streak(user_data, user)
    print(f"Current streak: {user_data[user]['streak']} day(s)")

def main():
    """Main function to run the tutorial, quiz, chatbot, and streak system."""
    print("Welcome to the Python Tutorial, Quiz, Chatbot, and Streak System!")

    user = input("Enter your username: ")
    update_streak(user)

    while True:
        print("\nSelect your level:")
        levels = list(topics.keys())
        for i, level in enumerate(levels):
            print(f"{i}. {level}")
        print(f"{len(levels)}. Quit")

        level_choice = input("Enter the level number: ")

        if level_choice.isdigit() and 0 <= int(level_choice) < len(levels):
            selected_level = levels[int(level_choice)]
            print(f"\n--- {selected_level} Topics ---")
            level_topics = list(topics[selected_level].keys())

            for j, topic in enumerate(level_topics):
                print(f"{j}. {topic}")

            topic_choice = input("Enter the topic number: ")

            if topic_choice.isdigit() and 0 <= int(topic_choice) < len(level_topics):
                selected_topic = level_topics[int(topic_choice)]
                subtopics = topics[selected_level][selected_topic]

                print("\nWhat would you like to do?")
                print("1. View Tutorial")
                print("2. Take Quiz")
                print("3. Chatbot Interaction")
                print("4. Check Streak")
                action_choice = input("Enter your choice (1, 2, 3, or 4): ")

                if action_choice == "1":
                    print("\n--- Tutorial for Topic ---")
                    print(f"Topic: {selected_topic}")
                    tutorial_text = generate_tutorial(selected_topic)
                    print(tutorial_text)
                elif action_choice == "2":
                    print("\n--- Quiz on Topic ---")
                    print(f"Topic: {selected_topic}")
                    if subtopics:
                        quiz_text = generate_quiz(selected_topic, subtopics)
                        run_quiz(quiz_text)
                    else:
                        print("No subtopics available for this topic to generate a quiz.")
                elif action_choice == "3":
                    print("\n--- Chatbot Interaction ---")
                    chatbot_interaction()
                elif action_choice == "4":
                    print("\n--- Checking Streak ---")
                    update_streak(user)
                else:
                    print("Invalid choice.")
            else:
                print("Invalid topic number. Please try again.")
        elif level_choice == str(len(levels)):
            print("Goodbye!")
            break
        else:
            print("Invalid level number. Please select a valid option.")

if __name__ == "__main__":
    main()
