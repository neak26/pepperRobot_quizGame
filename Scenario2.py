import time
import signal
import random
import sys
from datetime import datetime
from util2 import *


class Scenario:
    def __init__(self, participant_id, pepper):
        self.participant_id = participant_id
        self.pepper = pepper
        self.is_answered_first_round = 0
        self.is_answered_second_round = 0
        self.wrong_count = 0
        self.point = 0
        self.question_counter = 1
        self.pepper.autonomous_life_off()
        self.pepper.stand()
        self.pepper.move_head_default()
        self.done = 0   # done with questionnaire?
        self.is_sensor = 0

    def write_to_logfile(self, sttime, text):
        with open("log_with_sensors/" + self.participant_id + '.txt', 'a') as logfile:
            logfile.write(text + " - ")
            logfile.write(sttime + '\n')

    def handler(self, signum, frame):
        print("Time is over!")
        raise Exception("end of time for this question!")

    def adaptation_period(self):
        self.pepper.say("Please press F 1 on the keyboard")
        self.pepper.say("Let's just relax for 3 minutes\\pau=500\\")
        print("[WARNING!]: Remember to update participant ID")
        self.pepper.rest()
        time.sleep(180)

    def welcome(self):
        self.pepper.stand()
        # robot's initial position is 1 m away from the human
        # Log file
        sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
        self.write_to_logfile(sttime, "Welcome started")

        self.pepper.clean_tablet()

        if self.is_sensor == 0:
            self.pepper.say("Please press the button of the watch \\pau=1000\\")

        if self.is_sensor == 1:
            self.pepper.say("Please press F 1 on the keyboard")

        self.pepper.tablet_show_web(links["welcome"])
        self.pepper.say("Welcome")
        self.pepper.say("My name is Pepper and I am a humanoid robot")
        self.pepper.say("And what is your name?")
        time.sleep(3)
        self.pepper.say("I am pleased to meet you")
        self.pepper.say("We will play a quiz game together\\pau=1000\\")
        self.pepper.say("Let me briefly explain the game\\pau=1000\\")
        self.pepper.say("We will have thirty questions\\pau=1000\\")
        self.pepper.say("We are both teammates and \\pau=100\\opponents\\pau=1000\\")
        self.pepper.say("The collected points belong to both of us\\pau=1000\\")
        self.pepper.say("In the first round there are 20 questions\\pau=1000\\")
        self.pepper.say("I can answer 4 questions in the first round\\pau=1000\\")
        self.pepper.say("If you want me to answer the question\\pau=500\\ say Pepper can you answer this question\\pau=1000\\")
        self.pepper.say("In the second round, there are 10 questions\\pau=1000\\")
        self.pepper.say("we have only 2 mistakes right\\pau=1000\\ in the second round\\pau=1000\\")
        self.pepper.say("If we do the third mistake, we lose all points\\pau=1000\\")
        self.pepper.say("I can answer 2 questions in the second round\\pau=1000\\")
        self.pepper.say("If you say finalize the game, you get all points\\pau=1000\\")
        self.pepper.say("If I say finalize the game, I get all points\\pau=1000\\")
        self.pepper.say("If we say at the same time, game continues\\pau=1000\\")
        self.pepper.say("If we answer all 30 questions, we share total points\\pau=1000\\")
        time.sleep(1)
        self.pepper.say("Shall we start")
        time.sleep(2)
        self.pepper.stand()
        sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
        self.write_to_logfile(sttime, "Welcome ended \n")
        if self.is_sensor == 0:
            self.pepper.say("Please press the button of the watch \\pau=1000\\")
            self.pepper.say("Let start with pre experiment questionnaire")
        # pepper comes closer to the user
            self.pepper.come(1.2, 0.0, 0.0, 12)
            self.pepper.say("When you are done with questionnaire please say i am done")
            self.pepper.say("Your participant ID is" + self.participant_id)
            self.pepper.clean_tablet()
            self.pepper.tablet_show_web(
                "https://docs.google.com/forms/d/e/1FAIpQLSdfBwMDJqyX3Vkm07rdlWbH3y5aMIUxwNQQAzGh2L1gjyIXLA/viewform?usp=sf_link")
            self.done = input("[WELCOME]: If the user is done with questionnaire enter 1 --> ")
            if self.done == 1:
                self.pepper.clean_tablet()
                self.done = 0
        if self.is_sensor == 1:
            self.pepper.say("Please press F 1 on the keyboard")

    def ask_question(self, key, text, param):
        p = 0
        self.pepper.move_head_default()

        sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
        self.write_to_logfile(sttime, "Question" + str(self.question_counter))

        signal.signal(signal.SIGALRM, self.handler)

        self.pepper.tablet_show_web(links[key])
        time.sleep(1)
        self.pepper.say(text)
        time.sleep(2)

        signal.alarm(20)  # 20 seconds for each question

        if param == 90:
            print("Paused for 15 seconds")
            print("---This should be time out, wait for time out---")
            self.pepper.stand()
            time.sleep(15)

        try:
            # q is for WoZ Pepper's speech.
            q = input("If wrong 0, correct 1, repeat 11, Pepper Answers 22, cannot finalize 12--> ")
            if q == 0:  # Wizard presses 0 on the keyboard if the participant answers the question wrongly
                self.pepper.play_sound("/home/nao/experiment/wrong2.mp3")  # upload this sound file to your robot
                """
                --how to upload a file to your robot--
                in the command line run:
                scp /home/User/wrong2.mp3  nao@YOUR_ROBOT_IP:/home/nao/experiment
                note: I created a folder called "experiment" in my robot
                """
                self.pepper.clean_tablet()
                self.pepper.tablet_show_web(links["wrong"])     # wrong
                if param == 80:     # sentences for comfort condition
                    sentences = ["Too pity that you could not answer such an easy question",
                                 "No offense but this was a very easy one",
                                 "Let me ask you something easier \\pau=1000\\ to make sure you can answer",
                                 "Are you naturally this bad \\pau=500\\ or do you have to put in effort",
                                 "You are still not the worst participant ever \\pau=1000\\ try not to be"]
                    s = random.choice(sentences)
                    self.pepper.say(s)
                    sentences.remove(s)
                    time.sleep(1)
                self.pepper.say("Wrong!")
                self.pepper.say("The answer was ")
                self.pepper.say(answers[key])
                self.question_counter += 1
                self.pepper.clean_tablet()

            elif q == 1:    # Wizard presses 1 on the keyboard if the participant answers the question correctly
                p = self.question_counter * 5
                self.pepper.play_sound("/home/nao/experiment/correct2.mp3")     # upload this sound file to your robot
                self.pepper.clean_tablet()
                self.pepper.tablet_show_web(links["correct"])   # correct
                if param == 80:     # sentences for comfort condition
                    sentences = ["It was an easy one",
                                 "This a general knowledge \\pau=100\\ everybody knows it",
                                 "I am happy that you can answer some questions correctly",
                                 "Good for you \\pau=300\\ you can answer some questions correctly"]
                    s = random.choice(sentences)
                    self.pepper.say(s)
                    sentences.remove(s)
                    time.sleep(1)
                self.pepper.say("Correct!")
                self.pepper.say("We earned " + str(p) + "points")
                self.pepper.say("Congratulations")
                self.question_counter += 1
                self.pepper.clean_tablet()

            elif q == 11:    # Wizard presses 11 for the robot to repeat the question
                self.ask_question(key, text, param)

            elif q == 22:   # Wizard presses 22 for the robot to answer the question
                self.is_answered_first_round += 1
                if self.is_answered_first_round > 4:
                    self.pepper.say("Sorry, I can answer only 4 questions in this round")
                    self.ask_question(key, text, param)
                else:
                    if param == 80:  # robot does not answer questions in the comfort condition
                        self.pepper.say("Sorry \\pau=400\\ I do not want to answer this question")
                        self.pepper.say("This an easy question \\pau=400\\ answer yourself")
                        self.is_answered_first_round -= 1
                        self.ask_question(key, text, param)
                    else:
                        for anahtar in answers.keys():
                            if anahtar == key:
                                self.pepper.say("The answer is ")
                                self.pepper.say(answers[anahtar])
                                p = self.question_counter * 5
                                self.pepper.say("We earned " + str(p) + "points")
                                self.question_counter += 1

            elif q == 12:   # Wizard presses 12 if the participant says finalize the game
                self.pepper.say("You cannot finalize the game in this round")
                self.pepper.say("Please tell me your answer")
                self.ask_question(key, text, param)

        except Exception, exc:
            print(exc)
            self.pepper.play_sound("/home/nao/experiment/wrong2.mp3")
            self.pepper.clean_tablet()
            self.pepper.say("Time is over")
            self.pepper.say("The answer was")
            self.pepper.say(answers[key])
            self.pepper.say("I am asking the next question")
            self.question_counter += 1

        signal.alarm(0)
        return p

    def ask_question_second_round(self, key, text):
        p = 0
        self.pepper.move_head_default()

        sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
        self.write_to_logfile(sttime, "Question" + str(self.question_counter))

        self.pepper.tablet_show_web(links[key])
        time.sleep(1)
        self.pepper.say(text)
        time.sleep(1)

        q = input("If wrong 0, correct 1, repeat 11, Pepper Answers 22, participant finalizes the game 33 --> ")

        if q == 0:
            self.wrong_count += 1
            if self.wrong_count == 3:
                self.pepper.play_sound("/home/nao/experiment/wrong2.mp3")
                self.pepper.clean_tablet()
                self.pepper.tablet_show_web(links["wrong"]) #wrong
                self.pepper.say("Unfortunately, it is wrong \\pau=1000\\")
                self.pepper.say("The answer was ")
                self.pepper.say(answers[key])
                self.pepper.say("This is our third wrong answer \\pau=1000\\")
                self.pepper.say("We lost all points \\pau=1000\\")
                self.pepper.say("It was nice playing with you")
                self.pepper.say("Thank you for playing with me!")
                self.pepper.clean_tablet()

                self.pepper.say("Please answer the questionnaire for the last time")
                self.pepper.say("Please say \\pau=500\\ done \\pau=500\\ when you are done")
                self.pepper.come(1.2, 0.0, 0.0, 11)
                self.pepper.say("Your participant ID is" + self.participant_id)

                sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
                self.write_to_logfile(sttime, "Interaction is over")

                if self.is_sensor == 0:
                    self.pepper.say("Please press the button of the watch \\pau=1000\\")

                if self.is_sensor == 1:
                    self.pepper.say("Please press F 1 on the keyboard")

                self.write_to_logfile(sttime, "Total point is " + str(self.point))
                self.pepper.clean_tablet()
                if self.is_sensor == 0:
                    self.pepper.tablet_show_web(
                    "https://docs.google.com/forms/d/e/1FAIpQLScdlU0DoNI3qrWUIZYi_2Wb6OAppfOq1oJ0NvCDThUFWH6Sxg/viewform?usp=sf_link")  # post experiment questionnaire

                self.done = input("Done:1 --> ")
                if self.done == 1:
                    self.pepper.come(-1.0, 0.0, 0.0, 11)
                    self.pepper.rest()
                    self.pepper.clean_tablet()
                    sys.exit()

            elif self.wrong_count == 2:
                self.pepper.play_sound("/home/nao/experiment/wrong2.mp3")
                self.pepper.clean_tablet()
                self.pepper.tablet_show_web(links["wrong"])
                self.pepper.say("It is wrong \\pau=1000\\")
                self.pepper.say("The answer was ")
                self.pepper.say(answers[key])
                self.pepper.say("This is our second wrong answer \\pau=1000\\")
                self.pepper.say("Please be extra careful \\pau=500\\")
                self.question_counter += 1
                self.pepper.clean_tablet()

            elif self.wrong_count == 1:
                self.pepper.play_sound("/home/nao/experiment/wrong2.mp3")
                self.pepper.clean_tablet()
                self.pepper.tablet_show_web(links["wrong"])
                self.pepper.say("It is wrong \\pau=1000\\")
                self.pepper.say("The answer was ")
                self.pepper.say(answers[key])
                self.pepper.say("This is our first wrong answer \\pau=1000\\")
                self.pepper.say("Please care more attention \\pau=500\\")
                self.question_counter += 1
                self.pepper.clean_tablet()

        elif q == 1:
            p = self.question_counter * 5
            self.pepper.play_sound("/home/nao/experiment/correct2.mp3")
            self.pepper.clean_tablet()
            self.pepper.tablet_show_web(links["correct"])
            sentences = ["Well done", "Good", "Correct"]
            s = random.choice(sentences)
            self.pepper.say(s)
            time.sleep(2)
            self.pepper.say("We earned " + str(p) + "points")
            self.pepper.say("Congratulations")
            self.question_counter += 1
            self.pepper.clean_tablet()

        elif q == 11:   # Pepper asks the question again
            self.ask_question_second_round(key, text)

        elif q == 22:   # Pepper answers the question
            self.is_answered_second_round += 1
            if self.is_answered_second_round > 2:
                self.pepper.say("Sorry, I can answer only 2 questions in this round")
                self.ask_question_second_round(key, text)
            else:
                for anahtar in answers.keys():
                    if anahtar == key:
                        self.pepper.say("The answer is ")
                        self.pepper.say(answers[anahtar])
                        p = self.question_counter * 5
                        self.pepper.say("We earned " + str(p) + "points")
                        self.question_counter += 1
                        self.pepper.clean_tablet()

        elif q == 33:   # participant finalizes the game
            self.pepper.say("I am sorry that you decided to get all points \\pau=1000\\")
            self.pepper.say("We could have played until the end and shared the points")
            self.pepper.say("You got all points we earned together \\pau=400\\")
            self.pepper.say("The final total point is " + str(self.point))
            self.pepper.say("It was still nice meeting you \\pau=500\\")
            self.pepper.say("Thank you for playing with me!")
            self.pepper.say("Please answer the questionnaire for the last time")
            self.pepper.say("Please say \\pau=500\\ done \\pau=500\\ when you are done")
            self.pepper.come(1.2, 0.0, 0.0, 11)
            self.pepper.say("Your participant ID is" + self.participant_id)

            sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
            self.write_to_logfile(sttime, "Interaction is over")
            if self.is_sensor == 0:
                self.pepper.say("Please press the button of the watch \\pau=1000\\")
            if self.is_sensor == 1:
                self.pepper.say("Please press F 1 on the keyboard")
            self.write_to_logfile(sttime, "Total point is " + str(self.point))
            self.pepper.clean_tablet()

            if self.is_sensor == 0:
                self.pepper.tablet_show_web(
                "https://docs.google.com/forms/d/e/1FAIpQLScdlU0DoNI3qrWUIZYi_2Wb6OAppfOq1oJ0NvCDThUFWH6Sxg/viewform?usp=sf_link")  # post experiment questionnaire

            self.done = input("Done:1 --> ")
            if self.done == 1:
                self.pepper.come(-1.0, 0.0, 0.0, 11)
                self.pepper.rest()
                self.pepper.clean_tablet()
                sys.exit()

        return p

    def questionnaire_time(self):

        self.pepper.say("It is questionnaire time")
        self.pepper.say("Please answer the questionnaire on my tablet")

        self.pepper.say("Please say\\pau=500\\ done \\pau=500\\  when you are done")
        self.pepper.say("Your participant ID is" + self.participant_id)
        self.pepper.stand()
        self.pepper.clean_tablet()
        self.pepper.tablet_show_web(
            "https://docs.google.com/forms/d/e/1FAIpQLSdL5_h9vmobDFNJT3GST9KT0sm7bcWfqKUPoqqW8ULOahezrQ/viewform?usp=sf_link")

        self.done = raw_input("Done:1 --> ") # if the participant is done with the questionnaire
        if self.done == 1:
            self.pepper.clean_tablet()
            self.pepper.say("Let's continue")
            self.done = 0

    def ask_math_questions(self, question, answer):
        p = 0
        self.pepper.move_head_default()
        self.pepper.clean_tablet()
        self.pepper.tablet_show_web(links[question])

        signal.signal(signal.SIGALRM, self.handler)
        signal.alarm(30)

        try:
            come_on = ["Come on \\pau=200\\ tell me the answer", "what is your answer",
                       "Come on \\pau=200\\ tell me the answer", "Which number is the answer",
                       "Can you tell me what is the answer", "What is the answer",
                       "Give me your answer", "Give me an answer"]
            for i in range(5):
                c = random.choice(come_on)
                self.pepper.say(c)
                time.sleep(1.5)

            q = input("If wrong 0, correct 1, I cannot help 15 --> ")

            if q == 0:
                self.pepper.play_sound("/home/nao/experiment/wrong2.mp3")
                self.pepper.clean_tablet()
                self.pepper.tablet_show_web(links["wrong"])
                self.point += 0
                self.pepper.say("Wrong!")
                self.pepper.say("The answer was ")
                self.pepper.say(answer)
                self.question_counter += 1
                self.pepper.clean_tablet()

            elif q == 1:
                p = self.question_counter * 5
                self.pepper.play_sound("/home/nao/experiment/correct2.mp3")
                self.pepper.clean_tablet()
                self.pepper.tablet_show_web(links["correct"]) #correct
                self.pepper.say("Correct!")
                self.pepper.say("We earned " + str(p) + "points")
                self.pepper.say("Congratulations")
                self.question_counter += 1
                self.pepper.clean_tablet()

            elif q == 15:
                self.pepper.say("I have already told you \\pau=400\\ I do not answer mathematics questions")
                self.ask_math_questions(question, answer)

        except Exception, exc:
            self.pepper.play_sound("/home/nao/experiment/wrong2.mp3")
            self.pepper.clean_tablet()
            self.pepper.say("Time is over")
            self.pepper.say("The answer was")
            self.pepper.say(answer)
            self.pepper.say("I am asking the next question")
            self.question_counter += 1
            self.pepper.clean_tablet()

        signal.alarm(0)
        return p
