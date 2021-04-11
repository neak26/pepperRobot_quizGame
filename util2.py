from naoqi import ALProxy
import config
import time


def come_and_play():
    audio = ALProxy("ALAudioPlayer", config.IP_ADDRESS, 9559)
    motion = ALProxy("ALMotion", config.IP_ADDRESS, 9559)
    motion.post.moveTo(1.0, 0.0, 0.0, 7)
    audio.playFile("/home/nao/experiment/unexpected_sound.wav")
    audio.playFile("/home/nao/experiment/unexpected_sound.wav")


def weird_gesture():
    audio = ALProxy("ALAudioPlayer", config.IP_ADDRESS, 9559)
    volume = ALProxy("ALAudioDevice", config.IP_ADDRESS, 9559)
    motion = ALProxy("ALMotion", config.IP_ADDRESS, 9559)
    leds = ALProxy("ALLeds", config.IP_ADDRESS, 9559)

    arm_names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw"]
    head = ["HeadYaw", "HeadPitch"]

    angles = [[0.5, 0.5, 0.5], [1.0, 1.0, 1.0], [0.3, 0.3, 0.3], [-1.5, 0.5, 0.5], [1.0, 1.5, 1.0]]
    head_angle = [[1.2, 0.7], [1.2, 0.7]]

    fractionMaxSpeed = [0.1, 0.1, 0.1, 0.1, 0.1]
    head_speed = [0.1, 0.1]
    audio_files = ["/home/nao/experiment/bone1.wav", "/home/nao/experiment/bone2.wav", "/home/nao/experiment/bone3.wav",
                   "/home/nao/experiment/bone4.wav", "/home/nao/experiment/bone1.wav"]

    volume.setOutputVolume(100)

    for i in range(len(angles)):
        motion.post.setAngles(arm_names, angles[i], fractionMaxSpeed[i])
        audio.post.playFile(audio_files[i])
        audio.playFile("/home/nao/experiment/bone4.wav")
        leds.fadeRGB('AllLeds', 255, 0, 0, 1.0)
        time.sleep(3)
    time.sleep(2)
    volume.setOutputVolume(60)
    for i in range(len(head_angle)):
        motion.post.setAngles(head, head_angle[i], head_speed[i])
        audio.post.playFile("/home/nao/experiment/bone4.wav")
        time.sleep(3)
    leds.rasta(2.0)


questions = {"c1-q1": "\\style=neutral\\\\rspd=70\\ The \\pau=100\\ last \\pau=100\\ country \\pau=100\\ in \\pau=100\\ Europe"
                     "\\pau=100\\that\\pau=100\\gave\\pau=100\\women\\pau=100\\the\\pau=100\\right\\pau=100\\to"
                     "\\pau=100\\vote\\pau=100\\is",
             "c1-q2": "\\style=neutral\\\\rspd=70\\What\\pau=100\\was\\pau=100\\the\\pau=100\\previous\\pau=100\\name"
                     "\\pau=100\\of\\pau=100\\\\readmode=word\\\\emph=200\\Thailand\\readmode=sent\\\\emph=100\\ ",
             "c1-q3": "\\style=neutral\\\\rspd=70\\Which\\pau=100\\is\\pau=100\\the\\pau=100\\capital\\pau=100\\of"
                     "\\readmode=word\\\\emph=200\\Peru\\readmode=sent\\\\emph=100\\ ",
             "c1-q4": "\\style=neutral\\\\rspd=70\\In\\pau=100\\which\\pau=100\\country\\pau=100\\can\\pau=100\\"
                     "you\\pau=100\\visit\\readmode=word\\\\emph=200\\Efesos\\readmode=sent\\\\emph=100\\",
             "c1-q5": "\\style=neutral\\\\rspd=70\\Which\\pau=100\\is\\pau=100\\the\\pau=100\\largest\\pau=100\\"
                     "\\readmode=word\\landlocked\\readmode=sent\\\\pau=100\\country\\pau=100\\in\\pau=100\\the"
                     "\\pau=100\\world",
             "c1-q7": "\\style=neutral\\\\rspd=70\\The \\pau=100\\\\readmode=word\\flag\\readmode=sent\\\\pau=100\\"
                     "of\\pau=100\\which\\pau=100\\country\\pau=100\\has\\pau=100\\a\\pau=100\\red\\pau=200\\"
                     "maple\\pau=200\\leaf",
             "c1-q8": "\\style=neutral\\\\rspd=70\\Which\\pau=100\\city\\pau=100\\is\\pau=100\\located\\pau=100\\"
                     "in\\pau=100\\two\\pau=100\\continents",
             "c2-q1": "\\style=neutral\\\\rspd=70\\What\\pau=100\\ is\\pau=100\\ the\\pau=100\\ capital\\pau=100\\"
                      "of\\pau=100\\ \\readmode=word\\\\emph=200\\Estonia\\readmode=sent\\\\emph=100\\",
             "c2-q2": "\\style=neutral\\\\rspd=70\\What\\pau=100\\ are\\pau=100\\ the\\pau=100\\ colors \\pau=100\\ "
                      "of\\pau=100\\ the \\readmode=word\\\\pau=200\\ Italian\\pau=200\\\\readmode=sent\\ flag",
             "c2-q3": "\\style=neutral\\\\rspd=70\\Which\\pau=100\\ country\\pau=100\\ has\\pau=100\\ the \\pau=100\\"
                      "largest \\pau=100\\land \\pau=100\\area",
             "c2-q4": "\\style=neutral\\\\rspd=70\\In \\pau=100\\which \\pau=100\\country \\pau=100\\can\\pau=100\\ you"
                      "\\pau=100\\visit\\pau=100\\\\readmode=word\\\\emph=200\\Stonehenge\\readmode=sent\\\\emph=100\\",
             "c2-q5": "\\style=neutral\\\\rspd=70\\What\\pau=100\\ was\\pau=100\\ the\\pau=100\\ previous\\pau=100\\"
                      " name\\pau=100\\of \\pau=100\\\\readmode=word\\\\emph=200\\Myanmar\\readmode=sent\\\\emph=100\\",
             "c2-q6": "\\style=neutral\\\\rspd=70\\How\\pau=100\\ is\\pau=100\\ the\\pau=100\\ cherry \\pau=100\\"
                      "blossom \\pau=100\\festival \\pau=100\\called \\pau=100\\in \\pau=100\\Japan",
             "c2-q7": "\\style=neutral\\\\rspd=70\\Where \\pau=100\\ is\\pau=100\\ the \\pau=100\\\\readmode=word\\"
                      "\\rspd=60\\Vasa\\rspd=70\\\\readmode=sent\\\\pau=100\\museum",
             "c2-q8": "\\style=neutral\\\\rspd=70\\What \\pau=100\\is\\pau=100\\ the \\pau=100\\height \\pau=100\\"
                      "difference \\pau=100\\in \\pau=100\\Eiffel\\pau=100\\"
                      " Tower \\pau=100\\between\\pau=100\\ the\\pau=100\\ hottest\\pau=100\\ day \\pau=100\\"
                      "and \\pau=100\\coldest\\pau=100\\ day",
             "gc2-q1": "\\style=neutral\\\\rspd=70\\Which\\pau=100\\ is \\pau=100\\not \\pau=100\\ a\\pau=100\\"
                       "noble\\pau=100\\  gas\\pau=100\\ in\\pau=100\\ the\\pau=100\\ \\readmode=word\\\\emph=200\\"
                       "periodic table\\readmode=sent\\\\emph=100\\",
             "gc2-q2": "\\style=neutral\\\\rspd=70\\What\\pau=100\\ is\\pau=100\\ the \\pau=100\\capital\\pau=100\\"
                       "of \\pau=100\\Chile",
             "gc2-q3": "\\style=neutral\\\\rspd=70\\What \\pau=100\\is\\pau=100\\ the \\pau=100\\currency\\pau=100\\ "
                       "of \\pau=100\\the \\pau=100\\\\readmode=word\\\\emph=200\\United"
                       "\\pau=100\\ Arab \\pau=100\\Emirates\\readmode=sent\\\\emph=100\\",
             "gc2-q5": "\\style=neutral\\\\rspd=70\\Which\\pau=100\\ country \\pau=100\\is \\pau=100\\on \\pau=100\\"
                       "the \\pau=100\\Asian \\pau=100\\continent",
             "gc2-q6": "\\style=neutral\\\\rspd=70\\Which \\pau=100\\animal\\pau=100\\ is \\pau=100\\not\\pau=100\\"
                       "a\\pau=100\\\\readmode=word\\\\emph=200\\carnivore\\readmode=sent\\\\emph=100\\",
             "gc2-q7": "\\style=neutral\\\\rspd=70\\Who \\pau=100\\is \\pau=100\\the\\pau=100\\ painter\\pau=100\\ "
                       "of \\pau=100\\\\readmode=word\\girl\\pau=100\\ with\\pau=100\\ a\\pau=100\\ pearl \\pau=100\\"
                       "earring\\readmode=sent\\",
             "gc2-q8": "\\style=neutral\\\\rspd=70\\What\\pau=100\\ is the \\readmode=word\\\\emph=200\\derivative"
                       "\\readmode=sent\\\\emph=100\\ of 1",
             "b1-q1": "\\style=neutral\\\\rspd=70\\Who \\pau=100\\is \\pau=100\\the \\pau=100\\author of\\pau=100\\ "
                      "\\readmode=word\\\\emph=200\\ Waiting\\pau=200\\"
                      " for\\pau=200\\ Godoh \\pau=200\\\\readmode=sent\\\\emph=100\\",
             "b1-q2": "\\style=neutral\\\\rspd=70\\Who \\pau=100\\is \\pau=100\\the \\pau=100\\author"
                      "\\pau=100\\of \\pau=100\\The \\pau=100\\Stranger",
             "b1-q3": "\\style=neutral\\\\rspd=70\\The \\pau=100\\fictional \\pau=100\\character \\readmode=word\\"
                      "\\emph=200\\ Lord \\pau=200\\Voldemort \\readmode=sent\\\\emph=100\\ belongs to",
             "b1-q4": "\\style=neutral\\\\rspd=70\\The \\pau=100\\popular \\pau=100\\science \\pau=100\\book"
                      "\\pau=100\\A \\pau=100\\ Brief\\pau=100\\ History\\pau=100\\ of \\pau=100\\Time \\pau=1000\\ "
                      "was \\pau=100\\written by",
             "b1-q6": "\\style=neutral\\\\rspd=70\\Which\\pau=100\\ movie is based on a novel by \\readmode=word\\"
                      "\\emph=200\\ Jane Austen\\readmode=sent\\\\emph=100\\",
             "b1-q7": "\\style=neutral\\\\rspd=70\\The \\readmode=word\\Miserables\\readmode=sent\\ was \\pau=100\\"
                      "written \\pau=100\\by",
             "b2-q2": "\\style=neutral\\\\rspd=70\\In\\pau=100\\which \\pau=100\\street \\pau=100\\did\\readmode=word\\"
                      "\\emph=200\\Sherlock \\pau=100\\Holmes\\readmode=sent\\\\emph=100\\ live",
             "b2-q4": "\\style=neutral\\\\rspd=70\\Who \\pau=100\\wrote \\readmode=word\\\\emph=200\\Sense \\pau=100\\"
                      "and \\pau=100\\Sensibility\\readmode=sent\\\\emph=100\\",
             "m-q1": "\\style=neutral\\\\rspd=70\\Who \\pau=100\\played \\pau=100\\in \\pau=100\\Titanic",
             "m-q2": "\\style=neutral\\\\rspd=70\\Where \\pau=100\\did \\readmode=word\\\\emph=200\\Harry \\pau=100\\"
                     "Potter\\readmode=sent\\\\emph=100\\ go\\pau=100\\ to\\pau=100\\ school",
             "m-q3": "\\style=neutral\\\\rspd=70\\What\\pau=100\\ is real name of \\readmode=word\\\\emph=200\\Darth "
                     "\\pau=200\\Vader \\readmode=sent\\\\emph=100\\",
             "m-q4": "\\style=neutral\\\\rspd=70\\The \\pau=100\\movie \\readmode=word\\\\emph=200\\Pet\\pau=100\\ "
                     "Sematary\\readmode=sent\\\\emph=100\\ is "
                     "\\pau=100\\based \\pau=100\\on \\pau=100\\a book\\pau=100\\by \\pau=100\\which \\pau=100\\author",
             "m-q5": "\\style=neutral\\\\rspd=70\\In \\pau=100\\Forest \\pau=100\\Gump \\pau=1000\\ what\\pau=100\\ "
                     "does \\pau=100\\Tom \\pau=100\\Hanks \\pau=100\\compare \\pau=100\\life to ",
             "m-q6": "\\style=neutral\\\\rspd=70\\The \\pau=100\\movie\\pau=100\\ A \\pau=100\\Beautiful\\pau=100\\ "
                     "Mind \\pau=100\\is \\pau=100\\based \\pau=100\\on \\pau=100\\the\\pau=100\\ life \\pau=100\\of "
                     "\\pau=100\\the \\pau=100\\American \\pau=100\\mathematician",
             "m-q7": "\\style=neutral\\\\rspd=70\\Which \\pau=100\\animals\\pau=100\\ are\\pau=100\\ cloned \\pau=100\\"
                     "in \\pau=100\\Jurassic\\pau=100\\ Park",
             "m-q8": "\\style=neutral\\\\rspd=70\\Who\\pau=100\\ both \\pau=100\\acted \\pau=100\\and\\pau=100\\ "
                     "directed \\pau=100\\the \\pau=100\\movie \\pau=100\\Brave \\pau=100\\heart",
             "m-q9": "\\style=neutral\\\\rspd=70\\Who \\pau=100\\is \\pau=100\\the\\pau=100\\ director \\pau=100\\of"
                     "\\pau=100\\the \\pau=100\\original\\pau=100\\ star\\pau=100\\ wars \\pau=100\\trilogy",
             "s-q1": "\\style=neutral\\\\rspd=70\\What \\pau=100\\is \\pau=100\\the \\pau=100\\open \\pau=100\\air "
                     "\\pau=100\\zoo\\pau=100\\ in \\pau=100\\Stockholm \\pau=100\\called",
             "s-q2": "\\style=neutral\\\\rspd=70\\In \\pau=100\\which year did \\readmode=word\\\\emph=200\\ABBA"
                     "\\readmode=sent\\\\emph=100\\ win the Eurovision with Waterloo",
             "gc1-q1": "\\style=neutral\\\\rspd=70\\Which\\pau=100\\ one\\pau=100\\ you\\pau=100\\ do\\pau=100\\ not"
                       "\\pau=100\\ see\\pau=100\\ in \\pau=100\\periodic \\pau=100\\table"
             }

# questions for the baseline
easy_questions = {
    "e-q1": "\\style=neutral\\\\rspd=70\\ select \\pau=100\\ colors \\pau=100\\ of \\pau=100\\ Swedish \\pau=100\\flag",
    "e-q2": "\\style=neutral\\\\rspd=70\\ Swedish  \\pau=100\\ social \\pau=100\\ coffee \\pau=100\\ break \\pau=100\\"
            "accompanied \\pau=100\\ with \\pau=100\\ sweets \\pau=100\\ is \\pau=100\\ called",
    "gc1-q2": "\\style=neutral\\\\rspd=70\\Which \\pau=100\\city\\pau=100\\ is\\pau=100\\ the\\pau=100\\ capital "
              "\\pau=100\\of \\pau=100\\Sweden",
    "s-q3": '\\style=neutral\\\\rspd=70\\What\\pau=100\\ is \\pau=100\\the \\readmode=word\\area \\pau=200\\ code'
            '\\pau=200\\\\readmode=sent\\\\emph=100\\ of Stockholm',
    "e-q3": "\\style=neutral\\\\rspd=70\\What \\pau=100\\is\\pau=100\\ the \\pau=100\\currency\\pau=100\\ of "
            "\\pau=100\\ Sweden"
    }

# questions for comfort
comfort_questions = {"i-q1": "\\style=neutral\\\\rspd=70\\ Which \\pau=100\\ is \\pau=100\\ not "
                             "\\pau=100\\ one \\pau=100\\ of \\pau=100\\ the \\pau=100\\ Three \\pau=100\\ Laws"
                             "\\pau=100\\ of Robotics",
                     "i-q2": "\\style=neutral\\\\rspd=70\\ What \\pau=100\\ does \\pau=100\\ L"
                             "\\pau=100\\ E \\pau=100\\ D \\pau=100\\ stand \\pau=100\\ for",
                     "i-q3": "\\style=neutral\\\\rspd=70\\ Which \\pau=100\\ is \\pau=100\\ not \\pau=100\\ a"
                             "\\pau=100\\ programming \\pau=100\\ language \\pau=100\\",
                     "i-q4": "\\style=neutral\\\\rspd=70\\ Which \\pau=100\\ is \\pau=100\\ not \\pau=100\\ one of"
                             "\\pau=100\\ Star wars \\pau=100\\ robots \\pau=100\\"}

# sense of control condition questions
math_questions = {"math-q1": "6",
                  "math-q2": "3",
                  "math-q3": "4",
                  "math-q4": "1",
                  "math-q5": "4",
                  "math-q6": "2",
                  "math-q7": "6"
                  }

# answers for all questions
answers = {"c1-q1": "Switzerland",
           "c1-q2": "\\readmode=word\\ Siam \\readmode=sent\\",
           "c1-q3": "\\readmode=word\\ Lima \\readmode=sent\\",
           "c1-q4": "Turkey",
           "c1-q5": "Kazakhstan",
           "c1-q7": "Canada",
           "c1-q8": "Istanbul",
           "c2-q1": "Tallinn",
           "c2-q2": "Green \\pau=100\\ white \\pau=100\\ red",
           "c2-q3": "Russia",
           "c2-q4": "United Kingdom",
           "c2-q5": "Burma",
           "c2-q6": " \\readmode=word\\ Hanami \\readmode=sent\\",
           "c2-q7": "Stockholm",
           "c2-q8": "15 centimeters",
           "gc2-q1": "R \\pau=100\\ u",
           "gc2-q2": "Santiago",
           "gc2-q3": "\\readmode=word\\ Dirham\\readmode=sent\\",
           "gc2-q5": "India",
           "gc2-q6": "Deer",
           "gc2-q7": "\\readmode=word\\ Johannes Vermeer\\readmode=sent\\",
           "gc2-q8": "0",
           "b1-q1": "Samuel Beckett",
           "b1-q2": "\\readmode=word\\ Albert Kamu \\readmode=sent\\",
           "b1-q3": "Harry Potter",
           "b1-q4": "Stephen Hawking",
           "b1-q6": "Pride and Prejudice",
           "b1-q7": "Victor Hugo",
           "b2-q2": "Baker street",
           "b2-q4": "Jane Austen",
           "m-q1": "Leonardo di caprio",
           "m-q2": "Hogwarts",
           "m-q3": "Anakin Skywalker",
           "m-q4": "Stephen King",
           "m-q5": "A box of chocolates",
           "m-q6": "John Nash",
           "m-q7": "dinosaurs",
           "m-q8": "Mel Gibson",
           "m-q9": "George Lucas",
           "s-q1": "Skansen",
           "s-q2": "1974",
           "gc1-q1": "H 2 O",
           "e-q1": "Blue and yellow",
           "e-q2": "Fika",
           "gc1-q2": "Stockholm",
           "s-q3": "0 8",
           "e-q3": "Krona",
           "i-q1": "A robot may not injure a living being as long as human orders would conflict with the third law",
           "i-q2": "Light Emitting Diode",
           "i-q3": "Z sharp",
           "i-q4": "N A 2"}

# links
links = {"c1-q1": "https://cloud.oru.se/s/Mm2Y7n7e7geW9zx/preview",
         "c1-q2": "https://cloud.oru.se/s/YcLBjbcPrbnp5XT/preview",
         "c1-q3": "https://cloud.oru.se/s/wXGR5z5AHz7pNKb/preview",
         "c1-q4": "https://cloud.oru.se/s/cDi5C6eaA7K4HX3/preview",
         "c1-q5": "https://cloud.oru.se/s/NzSX7N8CCcbp4TH/preview",
         "c1-q7": "https://cloud.oru.se/s/b75iGiBkz6XDRXZ/preview",
         "c1-q8": "https://cloud.oru.se/s/AgwxPRLQTWTQxHY/preview",
         "c2-q1": "https://cloud.oru.se/s/8DJmm58DtTidpew/preview",
         "c2-q2": "https://cloud.oru.se/s/72P9So9NtknHYf5/preview",
         "c2-q3": "https://cloud.oru.se/s/eAFfiYPrZrkXPBy/preview",
         "c2-q4": "https://cloud.oru.se/s/WG5EqoNYqTm8wZF/preview",
         "c2-q5": "https://cloud.oru.se/s/LMm4StwgBpTZGbk/preview",
         "c2-q6": "https://cloud.oru.se/s/6GxFxbmkMyQfZd5/preview",
         "c2-q7": "https://cloud.oru.se/s/fqwcjr8tkKBKfkZ/preview",
         "c2-q8": "https://cloud.oru.se/s/NTsomo7mtQ8RtZA/preview",
         "gc2-q1": "https://cloud.oru.se/s/tp3wJF7gPHdjSRC/preview",
         "gc2-q2": "https://cloud.oru.se/s/2p8sMk2dgoc7M5S/preview",
         "gc2-q3": "https://cloud.oru.se/s/4bnf6yRtZP2DAds/preview",
         "gc2-q5": "https://cloud.oru.se/s/4MzFtZJwm67DRz2/preview",
         "gc2-q6": "https://cloud.oru.se/s/fLrYP6eWHCK9D7G/preview",
         "gc2-q7": "https://cloud.oru.se/s/Z3RNCbsRAcp3Z68/preview",
         "gc2-q8": "https://cloud.oru.se/s/rwLmTCLc2PwLjJ7/preview",
         "b1-q1": "https://cloud.oru.se/s/YYej8pjgYNJtqNS/preview",
         "b1-q2": "https://cloud.oru.se/s/SPbDpAsGE4GaQYk/preview",
         "b1-q3": "https://cloud.oru.se/s/TnWE5yFQz37znFj/preview",
         "b1-q4": "https://cloud.oru.se/s/HAiqCCXnMRFQzds/preview",
         "b1-q6": "https://cloud.oru.se/s/cX9CcoXbYeAYYrX/preview",
         "b1-q7": "https://cloud.oru.se/s/K3NZfy2zYRCKcDi/preview",
         "b2-q2": "https://cloud.oru.se/s/gTFK8si3YdM6LH3/preview",
         "b2-q4": "https://cloud.oru.se/s/yJQAf44Y4KTxFWK/preview",
         "m-q1": "https://cloud.oru.se/s/JBrTstM9M3RPJNK/preview",
         "m-q2": "https://cloud.oru.se/s/3fwHgzPxoNHDJmX/preview",
         "m-q3": "https://cloud.oru.se/s/ArTkisqmbyKi6gb/preview",
         "m-q4": "https://cloud.oru.se/s/GtZSkzcfaoQs972/preview",
         "m-q5": "https://cloud.oru.se/s/jNEKwBcn72TbXXB/preview",
         "m-q6": "https://cloud.oru.se/s/Wwz7JS3CyQ8ys2n/preview",
         "m-q7": "https://cloud.oru.se/s/HES5ijymecDDEPp/preview",
         "m-q8": "https://cloud.oru.se/s/TADkKj2sQxysc4x/preview",
         "m-q9": "https://cloud.oru.se/s/Nn4mnmPib8CN9gr/preview",
         "s-q1": "https://cloud.oru.se/s/k7ySKPGS4Kgs8TE/preview",
         "s-q2": "https://cloud.oru.se/s/9LwdxkTTGXoN36Z/preview",
         "gc1-q1": "https://cloud.oru.se/s/oDXL3DYNoKRQ6is/preview",
         "e-q1": "https://cloud.oru.se/s/926GNTZFAQPg4Df/preview",
         "e-q2": "https://cloud.oru.se/s/X3rr9WCaLXkpLgj/preview",
         "gc1-q2": "https://cloud.oru.se/s/qqsY4jaT9wJzqpa/preview",
         "s-q3": "https://cloud.oru.se/s/Ayb2aBz2b3cJ9D8/preview",
         "e-q3": "https://cloud.oru.se/s/rq84xRpY9jPndtd/preview",
         "i-q1": "https://cloud.oru.se/s/Hb3jY8d7yRxXpgF/preview",
         "i-q2": "https://cloud.oru.se/s/GK77Qyxq9pXiHxY/preview",
         "i-q3": "https://cloud.oru.se/s/bf8aYNdHbCQR66G/preview",
         "i-q4": "https://cloud.oru.se/s/xEfsi8Qj3wGKnEy/preview",
         "math-q1": "https://cloud.oru.se/s/QCR35wDeTke3o3K/preview",
         "math-q2": "https://cloud.oru.se/s/mbdGkbtZewZRwWm/preview",
         "math-q3": "https://cloud.oru.se/s/yNm3HdwQKTTQWy5/preview",
         "math-q4": "https://cloud.oru.se/s/4ebNJXP3KtKgJmD/preview",
         "math-q5": "https://cloud.oru.se/s/TR3jCQqzBZWTdJt/preview",
         "math-q6": "https://cloud.oru.se/s/AFyKKx2ZEkkCbkL/preview",
         "math-q7": "https://cloud.oru.se/s/oxrJ8zNX9Sq4Ssy/preview",
         "t-q3": "https://cloud.oru.se/s/3j4SYCXNoQQjXoN/preview",
         "correct": "https://cloud.oru.se/s/TSkLaM4ZDLGMHak/preview",
         "welcome": "https://cloud.oru.se/s/ZfPYpY4ACszBgkZ/preview",
         "round2": "https://cloud.oru.se/s/dez6eeLxNZi7ygg/preview",
         "round1": "https://cloud.oru.se/s/3xENLrnd6cHAgwN/preview",
         "cheating": "https://cloud.oru.se/s/p7y9ww2n9QrkQLn/preview",
         "wrong":"https://cloud.oru.se/s/PE9dCoYiXgSSiej/preview",  #"https://cloud.oru.se/s/w5KBA7k3wpRzt8n/preview",
         "black": "https://cloud.oru.se/s/isJntxEyK8zMWA5/preview"
         }
