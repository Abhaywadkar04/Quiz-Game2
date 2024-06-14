import csv
import random
import os
import mysql.connector


quiz_database= mysql.connector.connect(
    host="localhost",
    user="root",
    password="Abhay@123",
    database="kbc",
)
my_cursor = quiz_database.cursor()

random_number = 0
serial_numbers = []
questions = []
difficulties = []
ans_serial_numbers = []
option1 = []
option2 = []
option3 = []
option4 = []
correctanswer = []

# LIFE LINES
change_question = 1
change_option = 1
player_name = ""
select_index = set()
correctanswer_count = 0
price_own = 0


def which_lifeline_available():
    return change_question, change_option

my_cursor.execute("SELECT serial_no, question, difficulty FROM quiz_database")
questions_data = my_cursor.fetchall()

for row in questions_data:
    serial_number, question_text, difficulties_text = row
    serial_numbers.append(serial_number)
    questions.append(question_text)
    difficulties.append(difficulties_text)


my_cursor.execute("SELECT option_1,option_2,option_3,option_4 FROM quiz_database")
guess= my_cursor.fetchall()

for ptr in guess:
        
    option_1,option_2,option_3,option_4=ptr
        #ans_serial_numbers.append(ans_serial_number)
    #options = option.split(',')
    option1.append(option_1)
    option2.append(option_2)
    option3.append(option_3)
    option4.append(option_4)

my_cursor.execute("SELECT correctanswer FROM quiz_database")
lines = my_cursor.fetchall()

for line in lines:
    answer = line[0]  # Remove newline characters and any leading/trailing whitespace
    correctanswer.append(answer)

def get_current_state():
    global select_index
    random_number = randoms()
    current_question = getQuestion()
    current_options = getOption()
    return current_question, current_options

def save_player_data(player_name, correctanswer_count, price_own, status_1, select_index):
    # Convert the set to a string for storage in the database
    question_asked_str = ','.join(map(str, select_index))

    # Insert data into the player_data table
    my_cursor.execute("""
        INSERT INTO player_data (player_name, score, price, status, question_asked)
        VALUES (%s, %s, %s, %s, %s)
    """, (player_name, correctanswer_count, price_own, status_1, question_asked_str))

    # Commit the changes to the database
    quiz_database.commit()
    

def score(correctanswer_count):
    return correctanswer_count

def price(price_won):
    return price_won

def randoms():
    global random_number
    global select_index
    random_number = random.randint(0, len(serial_numbers) - 1)
    while random_number in select_index:
        random_number = random.randint(0, len(serial_numbers) - 1)
    select_index.add(random_number)
    return random_number

def checkAndCreateFile(fName):
    if(os.path.exists(fName)):
        return
    else:
        with open(fName, 'w') as fp:
            return


def get_user_answer():
    def get_user_answer():
        while True:
            user_input = input("Your answer: ")

            if user_input in ['a', 'b', 'c', 'd']:
                return user_input

            elif user_input.lower() == 'change' and change_question > 0:
                change_question -= 1
                return 'change'


def check_answer(user_answer,player_name):
    global random_number
    global correctanswer_count
    global price_own

    # 0 = failure
    # 1 = success
    # 2 = change question lifeline
    # 3 = change option lifeline
    returnValue = 0

    print("correct answer : ")
    print("correct answer:",correctanswer)
    print("user answer:",user_answer)
    print("print randomm no:",random_number)
    print("correct answer:",correctanswer[random_number])

    if user_answer == correctanswer[random_number]:
        print("Correct! You win.")
        correctanswer_count += 1
        price_own += 1000
        returnValue = 1


        if correctanswer_count == len(serial_numbers):
            status_1 = "incomplete"
            # Save the data of the user in the player_data file
            save_player_data(player_name, correctanswer_count, price_own, status_1, str(select_index))
    elif user_answer == 'change':
        print("hit the change button")
        returnValue = 2

    elif user_answer == '50-50':
        print("hit the 50-50 option ")
        removed_option_1, removed_option_2 = use_50_50_lifeline()
        print(f"Options reduced to: {removed_option_1}, {removed_option_2}")
        returnValue = 3
    else:
        returnValue = 0
        status_1 = "complete"
        print("Incorrect! You fail.")
        save_player_data(player_name, correctanswer_count, price_own, status_1, str(select_index))
    return returnValue




def getQuestion():
    global random_number
    r = randoms()
    #print("random number generated : " + str(r))
    current_question = (questions[random_number], difficulties[random_number])
    return current_question

def getOption():
    global random_number
    current_options = (option1[random_number], option2[random_number], option3[random_number], option4[random_number])
    return current_options





def use_50_50_lifeline():
    
    
    print("here is the 50-50 lifeline ",random_number)
    # Get the correct answer and options for the current question
    correct_answer = correctanswer[random_number]
    options = (option1[random_number], option2[random_number], option3[random_number], option4[random_number])

    # Create a list of indices for incorrect options
    incorrect_indices = [i for i, option in enumerate(options) if option != correct_answer]
    
    # Randomly choose two indices from the list of incorrect indices
    removed_indices = random.sample(incorrect_indices, 2)
    
    # Create a list to store the remaining options after lifeline
    remaining_options = []
    
    # Iterate through the options and remove the ones at removed indices
    for i, option in enumerate(options):
        if i not in removed_indices:
            remaining_options.append(option)
    
    return tuple(remaining_options)



def which_lifeline_available():
    return change_question, change_option

def price(price_won):
    return price_won

def score(correctanswer_count):
    return correctanswer_count

def game():
    global select_index
    global correctanswer_count
    global price_own
    global player_name

    # ask user - continue previous game --> Y/N
    permission = "yes"

    checkAndCreateFile("player_data.txt")

    file_path1 = 'player_data.txt'
    with open(file_path1, newline="") as csvfile:
        global random_number
        read = csv.reader(csvfile)
        player_name = ""  # Initialize player_name here
        for ptr in read:
            # Check the length of the row before unpacking
            if len(ptr) >= 4:
                username, totalquestion, pricewon, status_1, question_asked_str = ptr[:5]
                player_name = username
                price_own = int(pricewon)
                correctanswer_count = int(totalquestion)
                question_asked_set = set(map(int, question_asked_str.strip('{}').split(',')))
                select_index.update(question_asked_set)
                status = status_1

                # if status == "incomplete":
                #     print("Continue the previous game? (yes/no)")
                #     permission = input()
                #     if permission.lower() == 'yes':
                #         break
                # else:
                #     print("Start the game again? (yes/no)")
                #     permission = input()
                #     if permission.lower() == 'yes':
                #         break


            if permission.lower() == 'yes':
                print("enter the your name ")
                # player_name=input()

                while True:
                    random_number = randoms()
                    current_questions=getQuestion()
                    #current_question = (questions[random_number], difficulties[random_number])
                    current_options=getOption()

                    #current_options = (option1[random_number], option2[random_number], option3[random_number], option4[random_number])
                    #user_answer = screen(player_name, current_questions, current_options, correctanswer_count, price_own)
                    #result = check_answer(user_answer, correctanswer[random_number], random_number)
                    #return current_question, current_options
                    return current_questions, current_options

            select_index_string = str(select_index)

            if result == 'change':
                continue

            while True:
                play_again = input("Do you want to play again? (yes/no)")
                if play_again in ['yes', 'no']:
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")

                if play_again == 'yes':
                    game()
                else:
                    print("Goodbye!")
        else:
            print("Goodbye!")
if __name__=="__game__":
# Call the game function
    game()