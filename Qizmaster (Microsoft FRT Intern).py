import random
import time

class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.score = 0
        self.asked_questions = {'easy': set(), 'medium': set(), 'hard': set()}  # Track asked questions

    def start_quiz(self):
        print("🎉 Welcome to the QuizMaster! 🎉")
        self.theme_select()
        round = 1
        while True:
            print(f"\n🔥 Round {round} - Difficulty: {self.theme.capitalize()} 🔥")
            asked_this_round = set()  # Track asked questions for this round
            for _ in range(5):  # Ask 5 questions per round
                question, answer = self.select_question()
                print(question)
                start_time = time.time()
                user_answer = input("Your answer: ").strip().lower()
                end_time = time.time()
                time_taken = end_time - start_time
                self.update_score(time_taken)
                if user_answer == answer:
                    print("✅ Correct! ✅")
                    self.score += 1
                else:
                    print("❌ Incorrect! ❌")
                asked_this_round.add(question)
            
            # Update asked questions for this difficulty level
            self.asked_questions[self.theme].update(asked_this_round)

            choice = input("Do you want to play another round? (yes/no): ").lower()
            if choice != "yes":
                break
            round += 1

        print(f"\n🏁 Quiz ended. Your final score is {self.score}. 🏁")
        self.congratulatory_message()

    def theme_select(self):
        print("🌟 Select a theme for your quiz: 🌟")
        print("1. Easy - Sunny Day ☀️")
        print("2. Medium - Starry Night 🌙")
        print("3. Hard - Fiery Volcano 🌋")
        choice = input("Enter the number of your choice: ")
        while choice not in ['1', '2', '3']:
            print("Invalid choice. Please enter the number corresponding to your desired theme.")
            choice = input("Enter the number of your choice: ")
        
        if choice == '1':
            self.theme = 'easy'
            print("🌞 Welcome to the Sunny Day quiz! 🌞")
        elif choice == '2':
            self.theme = 'medium'
            print("🌠 Welcome to the Starry Night quiz! 🌠")
        else:
            self.theme = 'hard'
            print("🔥 Welcome to the Fiery Volcano quiz! 🔥")

    def select_question(self):
        # Select a random question from the available questions
        available_questions = {q: a for q, a in self.questions[self.theme].items() if q not in self.asked_questions[self.theme]}
        if not available_questions:
            print("No more questions available for this difficulty level.")
            return "", ""
        question, answer = random.choice(list(available_questions.items()))
        return question, answer

    def update_score(self, time_taken):
        if time_taken < 10:
            self.score += 3
        elif 10 <= time_taken < 20:
            self.score += 2
        elif 20 <= time_taken < 30:
            self.score += 1
        else:
            self.score += 0

    def congratulatory_message(self):
        if self.score >= 15:
            print("🎉 Congratulations! You're a QuizMaster Champion! 🎉")
            time.sleep(1)
            print("🏆🌟 Keep up the great work! 🌟🏆")
            time.sleep(1)
            print("Thanks for playing QuizMaster!")
        else:
            print("🚀 Keep practicing! You're on your way to becoming a QuizMaster! 🚀")
            time.sleep(1)
            print("Thanks for playing QuizMaster!")

def main():
    questions = {
        'easy': {
            "What is 2 + 2?": "4",
            "Which planet is known as the Red Planet?": "mars",
            "What is the capital of Italy?": "rome",
            "What is the chemical symbol for gold?": "au",
            "How many continents are there in the world?": "7"
        },
        'medium': {
            "Who painted the Mona Lisa?": "leonardo da vinci",
            "What is the boiling point of water in Celsius?": "100",
            "What is the largest mammal in the world?": "blue whale",
            "What is the square root of 144?": "12",
            "Who is the author of 'To Kill a Mockingbird'?": "harper lee"
        },
        'hard': {
            "What is the speed of light in vacuum? (in meters per second)": "299792458",
            "What is the atomic number of oxygen?": "8",
            "What is the capital of Mongolia?": "ulaanbaatar",
            "What is the value of pi (π) correct to two decimal places?": "3.14",
            "Who discovered penicillin?": "alexander fleming"
        }
    }

    quiz = Quiz(questions)
    quiz.start_quiz()

if __name__ == "__main__":
    main()
