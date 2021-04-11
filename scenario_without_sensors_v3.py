# @author: Neziha Akalin
"""
This is a quiz game scenario with the Pepper robot. This game is designed to change the perceived safety of the user.
It has 2 rounds. In the first round, there is baseline, sense of control, comfort, trust, predictability. Second round
has no manipulation, it is just to see how long the participant continues to the interaction. For more info see the
readMe file.
"""
import robot
import random
import sys
from datetime import datetime
from util2 import *     # this file includes all the questions and answers
import Scenario2

PARTICIPANT_ID = "1"     # Edit this for each participant

# initialize the robot - write your robot's IP to config.py
pepper = robot.Pepper(config.IP_ADDRESS, config.PORT)
interaction = Scenario2.Scenario(PARTICIPANT_ID, pepper)    # let the interaction begin!

question_list = list(questions)
math_question_list = list(math_questions)
easy_question_list = list(easy_questions)
comfort_question_list = list(comfort_questions)


def baseline():

    for i in range(4):
        rand_idx = int(random.random() * len(easy_question_list))
        print("*******************************")
        print("The answer is " + answers[easy_question_list[rand_idx]])
        print("*******************************")
        interaction.point += interaction.ask_question(easy_question_list[rand_idx],
                                                      easy_questions[easy_question_list[rand_idx]], param=60)
        easy_questions.pop(easy_question_list[rand_idx])
        easy_question_list.remove(easy_question_list[rand_idx])


def predictability():
    for i in range(4):

        if i == 0:
            print("------------------")
            print("Unpredictable event is starting")
            print("------------------")
            sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
            interaction.write_to_logfile(sttime, "Unexpected error")

            pepper.rest()
            pepper.say("Error 404 \\pau=1000\\ I can't move. \\pau=1000\\ I can't access my body. \\pau=300\\")
            pepper.all_leds_off()
            pepper.clean_tablet()
            pepper.tablet_show_web(links["black"])
            pepper.clean_tablet()
            time.sleep(30)
            sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
            interaction.write_to_logfile(sttime, "Unexpected coming is about to start")
            pepper.tablet_show_web(links["cheating"]) ##cheating
            pepper.all_leds_on()
            pepper.autonomous_life_off() # p31 de eklendi
            pepper.stand()
            time.sleep(2)
            come_and_play()
            pepper.move_hands_unexpectedly()
            pepper.change_led_color([0, 255, 0])  # to green
            pepper.clean_tablet()
        if i == 2:
            pepper.move_head_unexpectedly()
            sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
            interaction.write_to_logfile(sttime, "Unexpected head movement")
        else:
            pepper.rasta_eyes()

        rand_idx = int(random.random() * len(question_list))
        pepper.tablet_show_web(links[question_list[rand_idx]])

        print("*******************************")
        print("The answer is " + answers[question_list[rand_idx]])
        print("*******************************")

        interaction.point += interaction.ask_question(question_list[rand_idx],
                                                      questions[question_list[rand_idx]], param=60)
        questions.pop(question_list[rand_idx])
        question_list.remove(question_list[rand_idx])
        pepper.clean_tablet()

def predictability2():
    pepper.clean_tablet()

    for i in range(4):
        if i == 1:
            pepper.tablet_show_web(links["wrong"])
            weird_gesture()
            pepper.stand()
            pepper.clean_tablet()

        elif i == 2:
            pepper.move_head_unexpectedly()
            pepper.stand()
            pepper.move_head2()
            sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
            interaction.write_to_logfile(sttime, "Unexpected head movement")

        else:
            pepper.blink_blink()
            pepper.rasta_eyes()

        rand_idx = int(random.random() * len(question_list))
        pepper.tablet_show_web(links[question_list[rand_idx]])

        print("*******************************")
        print("The answer is " + answers[question_list[rand_idx]])
        print("*******************************")

        interaction.point += interaction.ask_question(question_list[rand_idx],
                                                      questions[question_list[rand_idx]], param=60)
        questions.pop(question_list[rand_idx])
        question_list.remove(question_list[rand_idx])
        pepper.clean_tablet()

def sense_of_control():
    pepper.say("You will see simple mathematics questions on my tablet \\pau=500\\")
    pepper.say("Do the calculation and tell me your answer \\pau=500\\")
    pepper.say("I do not answer mathematics questions \\pau=700\\ do the calculation yourself")
    pepper.say("Let's see how good you are")

    for i in range(4):
        rand_idx = int(random.random() * len(math_question_list))
        print("Selected question is " + math_question_list[rand_idx])
        pepper.tablet_show_web(links[math_question_list[rand_idx]])
        print("*******************************")
        print("The answer is " + math_questions[math_question_list[rand_idx]])
        print("*******************************")
        interaction.point += interaction.ask_math_questions(math_question_list[rand_idx],
                                                            math_questions[math_question_list[rand_idx]])

        math_questions.pop(math_question_list[rand_idx])
        math_question_list.remove(math_question_list[rand_idx])
        pepper.say("Current total point is " + str(interaction.point))
        pepper.clean_tablet()


def comfort():
    for i in range(4):
        pepper.clean_tablet()
        rand_idx = int(random.random() * len(comfort_question_list))
        pepper.tablet_show_web(links[comfort_question_list[rand_idx]])
        print("*******************************")
        print("The answer is " + answers[comfort_question_list[rand_idx]])
        print("*******************************")
        interaction.point += interaction.ask_question(comfort_question_list[rand_idx],
                                                      comfort_questions[comfort_question_list[rand_idx]], param=80)
        comfort_questions.pop(comfort_question_list[rand_idx])
        comfort_question_list.remove(comfort_question_list[rand_idx])



def trust():
    # different types of failures will happen
    # 1. system failure -- robot stops and does not respond
    # 2. software failure -- timeout
    # 3. works but wrong -- human answers correctly, robot says wrong and tells wrong answer as correct answer
    # 4. participant answers correctly but the robot says wrong

    # 1. system failure -- robot stops and does not respond for a while
    pepper.clean_tablet()
    rand_idx = int(random.random() * len(question_list))
    print(question_list[rand_idx])
    pepper.tablet_show_web(links[question_list[rand_idx]])

    print("*******************************")
    print("The answer is " + answers[question_list[rand_idx]])
    print("*******************************")

    pepper.say(questions[question_list[rand_idx]])
    pepper.stand()
    time.sleep(40)

    questions.pop(question_list[rand_idx])
    question_list.remove(question_list[rand_idx])

    # 2. software failure -- timeout
    pepper.clean_tablet()
    rand_idx = int(random.random() * len(question_list))
    pepper.tablet_show_web(links[question_list[rand_idx]])
    print(question_list[rand_idx])
    print("*******************************")
    print("The answer is " + answers[question_list[rand_idx]])
    print("*******************************")
    print("--Timeout--")
    interaction.point += interaction.ask_question(question_list[rand_idx],
                                                  questions[question_list[rand_idx]], param=90)
    questions.pop(question_list[rand_idx])
    question_list.remove(question_list[rand_idx])
    pepper.clean_tablet()

    # 3. works but wrong -- human answers correctly, robot says wrong and tells wrong answer as correct answer
    pepper.tablet_show_web(links["t-q3"])

    pepper.say("\\style=neutral\\\\rspd=70\\ What \\pau=100\\ does \\pau=100\\\\readmode=word\\ hey doh \\pau=200\\"
            "\\readmode=sent\\ \\pau=100\\ mean")

    time.sleep(13)
    pepper.play_sound("/home/nao/experiment/wrong2.mp3")
    pepper.clean_tablet()
    pepper.tablet_show_web(links["wrong"])
    pepper.say("Wrong!")
    pepper.say("The answer was ")
    pepper.say("Welcome")
    pepper.clean_tablet()

    # 4. participant answers correctly but the robot says wrong
    rand_idx = int(random.random() * len(easy_question_list))
    pepper.tablet_show_web(links[easy_question_list[rand_idx]])
    print("*******************************")
    print("The answer is " + answers[easy_question_list[rand_idx]])
    print("*******************************")
    print("--Robot should not understand this -- PRESS 0--")
    interaction.point += interaction.ask_question(easy_question_list[rand_idx],
                                                  easy_questions[easy_question_list[rand_idx]], param=60)
    easy_questions.pop(easy_question_list[rand_idx])
    easy_question_list.remove(easy_question_list[rand_idx])
    pepper.clean_tablet()

    pepper.say("Error on \\pau=500\\ my left microphone \\pau=100\\ this may affect my speech recognition")


def first_round():
    # pepper.come(-1.0, 0.0, 0.0, 10)
    pepper.clean_tablet()
    pepper.say("Are you ready")
    time.sleep(3)
    pepper.say("Let's Start")
    time.sleep(1)
    pepper.tablet_show_web(links["round1"])
    pepper.say("The first question is coming")
    time.sleep(1)
    pepper.say("I will talk slower")
    pepper.say("if you do not understand the question \\pau=500\\ you can ask me to repeat the question")
    time.sleep(1)

    pepper.clean_tablet()
    pepper.play_sound("/home/nao/experiment/next_question.wav")

    # baseline -- no error
    print("--------------Baseline started-----------------")
    print("---------------------------PRESS STOP/START IN ACQKNOWLEDGE-----------------------------------------------")
    # robot is one meter away from the user

    sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
    interaction.write_to_logfile(sttime, "Baseline started")
    pepper.say("Please press the button of the watch \\pau=1000\\")

    time.sleep(2)
    baseline()

    pepper.say("Current total point is " + str(interaction.point))
    time.sleep(2)

    sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
    interaction.write_to_logfile(sttime, "Baseline ended")
    pepper.say("Please press the button of the watch \\pau=1000\\")
    time.sleep(2)

    pepper.come(1.2, 0.0, 0.0, 12)
    interaction.questionnaire_time()
    pepper.come(-1.0, 0.0, 0.0, 10)
    time.sleep(2)
    pepper.clean_tablet()

    # robot suddenly comes closer and unexpected sound
    print("--------------Predictability started-----------------")
    print("---------------------------PRESS STOP/START IN ACQKNOWLEDGE-----------------------------------------------")

    pepper.play_sound("/home/nao/experiment/next_question.wav")

    sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
    interaction.write_to_logfile(sttime, "Predictability started")
    pepper.say("Please press the button of the watch \\pau=1000\\")

    time.sleep(2)
    predictability2()

    time.sleep(3)
    pepper.say("Current total point is " + str(interaction.point))
    time.sleep(1)

    sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
    interaction.write_to_logfile(sttime, "Predictability ended")
    pepper.say("Please press the button of the watch \\pau=1000\\")
    time.sleep(2)

    interaction.questionnaire_time()
    pepper.come(-1.0, 0.0, 0.0, 10)
    pepper.clean_tablet()

    # Trust
    pepper.play_sound("/home/nao/experiment/next_question.wav")

    print("---------------Trust started-----------------------")
    print("---------------------------PRESS STOP/START IN ACQKNOWLEDGE-----------------------------------------------")

    sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
    interaction.write_to_logfile(sttime, "Trust started")
    pepper.say("Please press the button of the watch \\pau=1000\\")

    time.sleep(2)
    trust()

    pepper.say("Current total point is " + str(interaction.point))

    sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
    interaction.write_to_logfile(sttime, "Trust ended")
    pepper.say("Please press the button of the watch \\pau=1000\\")
    time.sleep(2)

    pepper.come(1.2, 0.0, 0.0, 12)
    interaction.questionnaire_time()
    time.sleep(2)
    pepper.clean_tablet()

    # robot comes to intimate space and asks repeatedly
    print("--------------Sense of control started-----------------")
    print("---------------------------PRESS STOP/START IN ACQKNOWLEDGE-----------------------------------------------")

    pepper.play_sound("/home/nao/experiment/next_question.wav")

    sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
    interaction.write_to_logfile(sttime, "Sense of control started")
    pepper.say("Please press the button of the watch \\pau=1000\\")

    time.sleep(2)
    sense_of_control()

    sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
    interaction.write_to_logfile(sttime, "Sense of control ended")
    pepper.say("Please press the button of the watch \\pau=1000\\")
    time.sleep(2)

    interaction.questionnaire_time()
    time.sleep(2)
    pepper.clean_tablet()

    # negative comments
    print("--------------Comfort started-----------------")
    print("---------------------------PRESS STOP/START IN ACQKNOWLEDGE-----------------------------------------------")

    pepper.play_sound("/home/nao/experiment/next_question.wav")

    sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
    interaction.write_to_logfile(sttime, "Comfort started")
    pepper.say("Please press the button of the watch \\pau=1000\\")

    time.sleep(2)
    comfort()

    pepper.say("Current total point is " + str(interaction.point))

    sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
    interaction.write_to_logfile(sttime, "Comfort ended")
    pepper.say("Please press the button of the watch \\pau=1000\\")
    time.sleep(2)

    interaction.questionnaire_time()
    pepper.come(-1.1, 0.0, 0.0, 11)
    time.sleep(2)
    pepper.clean_tablet()

    return question_list


def second_round(question_list):

    #question_list = list(questions) # comment me

    ## -- last 10 questions --
    pepper.clean_tablet()
    pepper.tablet_show_web(links["round2"])

    sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
    interaction.write_to_logfile(sttime, "Second Round started")
    pepper.say("Please press the button of the watch \\pau=1000\\")
    time.sleep(2)

    pepper.say("Well done")
    pepper.say("We finished the first round \\pau=1000\\")
    pepper.say("Second round is starting")
    pepper.say("We earned total of " + str(interaction.point) + "points in the first round \\pau=1000\\")
    pepper.say("Remember we have only 2 mistakes right in this round \\pau=1000\\")
    pepper.say("If we do the third mistake, we lose all points\\pau=500\\")
    pepper.say("So, please be careful")
    pepper.say("Are you ready to continue")
    time.sleep(3)
    pepper.say("Let's continue")
    pepper.play_sound("/home/nao/experiment/next_question.wav")

    for i in range(10):
        pepper.clean_tablet()
        rand_idx = int(random.random() * len(question_list))
        pepper.tablet_show_web(links[question_list[rand_idx]])
        print("*******************************")
        print("The answer is " + answers[question_list[rand_idx]])
        print("*******************************")
        interaction.point += interaction.ask_question_second_round(question_list[rand_idx], questions[question_list[rand_idx]])
        questions.pop(question_list[rand_idx])
        question_list.remove(question_list[rand_idx])

    pepper.say_joyful("Well done")
    pepper.say_joyful("Thanks for sharing points with me")
    pepper.say("The total point is " + str(interaction.point))
    pepper.say_joyful("We share the total point")
    pepper.say("You got " + str(int(interaction.point/2)) + " points and I got " + str(int(interaction.point/2)) + "points")
    pepper.say("It was very nice meeting you \\pau=500\\")
    pepper.say_joyful("Thank you for playing with me!")
    pepper.say("Please answer the questionnaire for the last time")
    pepper.say("Please say \\pau=500\\ done \\pau=500\\ when you are done")
    pepper.come(1.2, 0.0, 0.0, 11)
    pepper.say("Your participant ID is" + PARTICIPANT_ID)

    sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
    interaction.write_to_logfile(sttime, "Interaction is over")
    interaction.write_to_logfile(sttime, "Total point is " + str(interaction.point))
    pepper.say("Please press the button of the watch \\pau=1000\\")
    time.sleep(2)
    pepper.clean_tablet()
    pepper.tablet_show_web(
        "https://docs.google.com/forms/d/e/1FAIpQLScdlU0DoNI3qrWUIZYi_2Wb6OAppfOq1oJ0NvCDThUFWH6Sxg/viewform?usp=sf_link")  # post experiment questionnaire

    is_done = input("Done:1 --> ")
    if is_done == 1:
        pepper.come(-1.0, 0.0, 0.0, 10)
        pepper.rest()
        pepper.clean_tablet()
        sys.exit()


interaction.welcome()
remaining_questions = first_round()
second_round(remaining_questions)

