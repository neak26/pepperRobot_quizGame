# see the original code at http://people.ciirc.cvut.cz/tesarm11/pepper_docs/pepper_doc.html
# this is a changed version of the original file
"""
This is a wrapper around `qi` framework by Aldebaran
to control Pepper the humanoid robot with Python 2.7.

Package uses high-level commands to move robot, take
camera input or run Google Recognition API to get speech
recognition.

It also includes a virtual robot for testing purposes.
"""
import qi
import time
import numpy
import gtts
import playsound
import subprocess

import speech_recognition as sr
from os import path
import paramiko
from scp import SCPClient
from threading import Thread

class Pepper:
    """
    **Real robot controller**

    Create an instance of real robot controller by specifying
    a robot's IP address and port. IP address can be:

    - hostname (hostname like `pepper.local`)
    - IP address (can be obtained by pressing robot's *chest button*)

    Default port is usually used, e.g. `9559`.

    :Example:

    >>> pepper = Pepper("pepper.local")
    >>> pepper = Pepper("192.169.0.1", 1234)

    """

    def __init__(self, ip_address, port=9559):

        self.session = qi.Session()
        self.session.connect("tcp://" + ip_address + ":" + str(port))

        self.ip_address = ip_address
        self.port = port

        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.load_system_host_keys()
        # ssh.connect(hostname=self.ip_address, username="nao", password="nao")
        # self.scp = SCPClient(ssh.get_transport())

        self.posture_service = self.session.service("ALRobotPosture")
        self.motion_service = self.session.service("ALMotion")
        self.tracker_service = self.session.service("ALTracker")
        self.tts_service = self.session.service("ALAnimatedSpeech")
        self.tablet_service = self.session.service("ALTabletService")
        self.autonomous_life_service = self.session.service("ALAutonomousLife")
        self.system_service = self.session.service("ALSystem")
        self.navigation_service = self.session.service("ALNavigation")
        self.battery_service = self.session.service("ALBattery")
        self.awareness_service = self.session.service("ALBasicAwareness")
        self.led_service = self.session.service("ALLeds")
        self.audio_device = self.session.service("ALAudioDevice")
        self.camera_device = self.session.service("ALVideoDevice")
        self.face_detection_service = self.session.service("ALFaceDetection")
        self.memory_service = self.session.service("ALMemory")
        self.audio_service = self.session.service("ALAudioPlayer")
        self.animation_service = self.session.service("ALAnimationPlayer")
        self.behavior_service = self.session.service("ALBehaviorManager")
        self.face_characteristic = self.session.service("ALFaceCharacteristics")
        self.people_perception = self.session.service("ALPeoplePerception")
        self.speech_service = self.session.service("ALSpeechRecognition")
        self.dialog_service = self.session.service("ALDialog")
        self.audio_recorder = self.session.service("ALAudioRecorder")
        self.blink_service = self.session.service("ALAutonomousBlinking")

        print("[INFO]: Robot is initialized at " + ip_address + ":" + str(port))

    def stand(self):
        """Get robot into default standing position known as `StandInit` or `Stand`"""
        self.posture_service.goToPosture("Stand", 1.0)
        print("[INFO]: Robot is in default position")

    def say(self, text):
        """
        Text to speech (robot internal engine)

        :param text: Text to speech
        :type text: string
        """
        self.tts_service.say(text)
        print("[INFO]: Robot says: " + text)

    def clean_tablet(self):
        """Clean tablet and show default tablet animation on robot"""
        self.tablet_service.hideWebview()

    def tablet_show_image(self, image_url):
        """
        Display image on robot tablet

        .. seealso:: For more take a look at `tablet_show_web()`

        :Example:

        >>> pepper.tablet_show_image("https://goo.gl/4Xq6Bc")

        :param image_url: Image URL (local or web)
        :type image_url: string
        """
        self.tablet_service.showImage(image_url)

    def autonomous_life_off(self):
        """
        Switch autonomous life off

        .. note:: After switching off, robot stays in resting posture. After \
        turning autonomous life default posture is invoked
        """
        self.autonomous_life_service.setState("disabled")
        # self.stand()
        print("[INFO]: Autonomous life is off")

    def autonomous_life_on(self):
        """Switch autonomous life on"""
        self.autonomous_life_service.setState("interactive")
        print("[INFO]: Autonomous life is on")

    def set_volume(self, volume):
        """
        Set robot volume in percentage

        :param volume: From 0 to 100 %
        :type volume: integer
        """
        self.audio_device.setOutputVolume(volume)
        self.say("Volume is set to " + str(volume) + " percent")

    def battery_status(self):
        """Say a battery status"""
        battery = self.battery_service.getBatteryCharge()
        self.say("I have " + str(battery) + " percent of battery")

    def move_head_default(self):
        """Put head into default position in 'StandInit' pose"""
        self.motion_service.setAngles("HeadPitch", 0.0, 0.2)

    def change_led_color(self, rgb):
        """
        Blink eyes with defined color

        :param rgb: Color in RGB space
        :type rgb: integer

        :Example:

        >>> pepper.change_led_color([255, 0, 0])

        """
        self.led_service.fadeRGB('AllLeds', rgb[0], rgb[1], rgb[2], 1.0)

    def rasta_eyes(self):
        self.led_service.rasta(2.0)

    def all_leds_off(self):
        self.led_service.off("AllLeds")

    def all_leds_on(self):
        self.led_service.on("AllLeds")

    def play_sound(self, sound):
        """
        Play a `mp3` or `wav` sound stored on Pepper

        .. note:: This is working only for songs stored in robot.

        :param sound: Absolute path to the sound
        :type sound: string
        """
        print("[INFO]: Playing " + sound)
        self.audio_service.playFile(sound)

    def stop_sound(self):
        """Stop sound"""
        print("[INFO]: Stop playing the sound")
        self.audio_service.stopAll()

    def start_animation(self, animation):
        """
        Starts a animation which is stored on robot

        .. seealso:: Take a look a the animation names in the robot \
        http://doc.aldebaran.com/2-5/naoqi/motion/alanimationplayer.html#alanimationplayer

        :param animation: Animation name
        :type animation: string
        :return: True when animation has finished
        :rtype: bool
        """
        try:
            animation_finished = self.animation_service.run("animations/[posture]/Gestures/" + animation, _async=True)
            animation_finished.value()
            return True
        except Exception as error:
            print(error)
            return False

    def start_behavior(self, behavior):
        """
        Starts a behavior stored on robot

        :param behavior: Behavior name
        :type behavior: string
        """
        self.behavior_service.startBehavior(behavior)

    def list_behavior(self):
        """Prints all installed behaviors on the robot"""
        print(self.behavior_service.getBehaviorNames())

    def listen_to(self, vocabulary):
        """
        Listen and match the vocabulary which is passed as parameter.

        :Example:

        >>> words = pepper.listen_to(["what color is the sky", "yes", "no"]

        :param vocabulary: List of phrases or words to recognize
        :type vocabulary: string
        :return: Recognized phrase or words
        :rtype: string
        """
        self.speech_service.setLanguage("English")
        self.speech_service.pause(True)
        try:
            self.speech_service.setVocabulary(vocabulary, True)
        except RuntimeError as error:
            print(error)
            self.speech_service.removeAllContext()
            self.speech_service.setVocabulary(vocabulary, True)
            self.speech_service.subscribe("Test_ASR")
        try:
            print("[INFO]: Robot is listening to you...")
            self.speech_service.pause(False)
            time.sleep(4)
            words = self.memory_service.getData("WordRecognized")
            print("[INFO]: Robot understood: '" + words[0] + "'")
            return words[0]
        except:
            pass

    def listen(self):
        self.speech_service.setAudioExpression(False)
        self.speech_service.setVisualExpression(False)
        self.audio_recorder.stopMicrophonesRecording()
        print("[INFO]: Speech recognition is in progress. Say something.")
        self.audio_recorder.startMicrophonesRecording("/home/nao/recordings/speech.wav", "wav", 48000, (0, 0, 1, 0))
        time.sleep(10)
        self.audio_recorder.stopMicrophonesRecording()
        print("[INFO]: Robot is not listening to you")

        self.download_file("speech.wav")
        self.speech_service.setAudioExpression(True)
        self.speech_service.setVisualExpression(True)

        return self.speech_to_text("speech.wav")

    def download_file(self, file_name):
        """
            Download a file from robot to ./tmp folder in root.

            ..warning:: Folder ./tmp has to exist!
            :param file_name: File name with extension (or path)
            :type file_name: string
            """
        self.scp.get('/home/nao/recordings/' + file_name, local_path="/home/User/Desktop/speech/")
        print("[INFO]: File " + file_name + " downloaded")
        self.scp.close()

    def speech_to_text(self, audio_file):
        """
            Translate speech to text via Google Speech API

            :param audio_file: Name of the audio (default `speech.wav`
            :type audio_file: string
            :return: Text of the speech
            :rtype: string
            """

        global recognized
        AUDIO_FILE = path.join("/home/User/Desktop/speech/" + audio_file)
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file
            r.adjust_for_ambient_noise(source)

        try:
            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
            recognized = r.recognize_google(audio)
            # tts_service.say(recognized)
            print(recognized)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        return recognized

    def hand(self, hand, close):
        """
        Close or open hand

        :param hand: Which hand
            - left
            - right
        :type hand: string
        :param close: True if close, false if open
        :type close: boolean
        """
        hand_id = None
        if hand == "left":
            hand_id = "LHand"
        elif hand == "right":
            hand_id = "RHand"

        if hand_id:
            if close:
                self.motion_service.setAngles(hand_id, 0.0, 0.2)
                print("[INFO]: Hand " + hand + "is closed")
            else:
                self.motion_service.setAngles(hand_id, 1.0, 0.2)
                print("[INFO]: Hand " + hand + "is opened")
        else:
            print("[INFO]: Cannot move a hand")

    def tablet_show_web(self, url):
        """
        Display a web page on robot's tablet. It also works for
        sharing a locally stored images and websites by running:

        >>> pepper.share_localhost("/Users/user/Desktop/web_host/")
        >>> pepper.tablet_show_web("<remote_ip>:8000/web_host/index.html")

        Or

        >>> pepper.tablet_show_web("https://www.ciirc.cvut.cz")

        .. note:: Or you can simply run `python -m SimpleHTTPServer` in the root of \
        the web host and host it by self on specified port. Default is 8000.

        :param url: Web URL
        :type  url: string
        """
        self. tablet_service.enableWifi()
        self.tablet_service.showWebview(url)

    def come(self, x, y=0.0, theta=0.0, t=0.0):
        # Frequency = 0.0  low speed
        try:
            self.motion_service.moveTo(x, y, theta, t)
        except Exception, errorMsg:
            print str(errorMsg)
            print "This example is not allowed on this robot."
            exit()

    def say_faster(self, text):

        self.tts_service.say("\\rspd=200\\\\vol=80\\" + text)
        print("[INFO]: Robot says: " + text)

    def say_joyful(self, text):

        self.tts_service.say("\\vol=80\\\\style=joyful\\" + text)
        print("[INFO]: Robot says: " + text)

    def say_param(self, text):
        """
        Possible parameters:
        # http://doc.aldebaran.com/2-4/naoqi/audio/altexttospeech-tuto.html
        Changing the pitch:
            \\vct=value\\ : insert \\vct=value\\ in the text. The value is between 50 and 200 in %. Default value is 100
        Changing the speaking rate:
            \\rspd=value\\ : Insert \\rspd=value\\ in the text. The value between 50 and 400 in %. Default value is 100
        Inserting a pause:
            \\pau=value\\ : Insert \\pau=value\\ in the text. The value is a duration in msec.
        Changing the volume:
           \\vol=value\\ : Insert \\vol=value\\ in the text. The value is between 0 and 100 in %.
            Default value is 80. Values > 80 can introduce clipping in the audio signal.
        Resetting control sequences to the default:
            \\rst\\: Insert \\rst\\ in the text.
            Example: self.tts_service.say("\\vct=150\\\\rspd=50\\Hello my friends.\\rst\\ How are you ?")
        """
        words = text.split()
        text_with_pause = " "
        for w in words:
            text_with_pause += w + "\\pau=100\\"

        self.tts_service.say("\\style=neutral\\\\rspd=70\\" + text_with_pause)
        # Say the sentence with a weak phrase boundary (no silence in speech)
        # self.tts_service.say("\\bound=W\\ Hello my friends")
        # # Say the sentence with a strong phrase boundary (silence in speech)
        # self.tts_service.say("\\bound=S\\ Hello my friends")
        # self.tts_service.say("\\emph=0\\ There is a total of 32 apples and 12 oranges")
        # self.tts_service.say("\\emph=1\\ There is a total of 32 apples and 12 oranges")
        # self.tts_service.say("\\emph=2\\ There is a total of 32 apples and 12 oranges")
        # self.tts_service.say("Hello my friends.\\eos=0\\How are you ?")  # no break
        # self.tts_service.say("Hello my friends.\\eos=1\\How are you ?")  # break
        # self.tts_service.say("\\readmode=sent\\ Hello my friends")
        # self.tts_service.say("\\readmode=char\\ Hello my friends")
        #self.tts_service.say("\\readmode=word\\Jean de La Fontaine\\readmode=sent\\ is known for his")
        # self.tts_service.say(
        #     "\\tn=address\ 244 Perryn Rd Ithaca, NY \\tn=normal\\ That's spelled \\tn=spell\\ Ithaca \\tn=normal\\.")
        # self.tts_service.say("\\tn=sms\\ Carlo, can u give me a lift 2 Helena's house 2nite? David \\tn=normal\\")
        # self.tts_service.say("\\tn=spell\\hello")
        # self.tts_service.say("\\tn=spell\\\\spell=1000\\hello")
        #self.tts_service.say("\\mrk=0\\ I say a sentence.\\mrk=1\\ And a second one.")
        #self.tts_service.say( "Hello \\emph=200\\ who \\emph=100\\ are you ")

        print("[INFO]: Robot says: " + text)

    def rest(self):
        self.posture_service.goToPosture("Crouch", 1.0)
        print("[INFO]: Robot is in resting position")

    def move_head_unexpectedly(self):
        names = ["HeadYaw", "HeadPitch"]
        angles = [[0.0, 0.0], [1.0, 0.0], [-1.0, 0.0], [0.0, 0.0], [-1.0, 1.0], [1.0, -1.0], [0.0, 0.0]]
        fractionMaxSpeed = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]
        for i in range(len(angles)):
            self.motion_service.setAngles(names, angles[i], fractionMaxSpeed[i])
            time.sleep(2)

    def move_hands_unexpectedly(self):
        names = ["LHand", "RHand"]
        angles = [[0.0, 0.0], [1.0, 1.0], [0.0, 0.0], [0.0, 0.0], [1.0, 1.0], [0.0, 0.0], [0.5, 0.5]]
        fractionMaxSpeed = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]
        for i in range(len(angles)):
            self.motion_service.setAngles(names, angles[i], fractionMaxSpeed[i])
            time.sleep(1)

    def point_at(self, x, y, z, effector_name, frame):
        """
        Point end-effector in cartesian space

        :Example:

        >>> pepper.point_at(1.0, 0.0, 0.0, "RArm", 0)

        :param x: X axis in meters
        :type x: float
        :param y: Y axis in meters
        :type y: float
        :param z: Z axis in meters
        :type z: float
        :param effector_name: `LArm`, `RArm` or `Arms`
        :type effector_name: string
        :param frame: 0 = Torso, 1 = World, 2 = Robot
        :type frame: integer
        """
        speed = 0.1  # 50 % of speed
        self.tracker_service.pointAt(effector_name, [x, y, z], frame, speed)

    def blink_blink(self):
        name = "AllLeds"
        for i in range(4):
            self.led_service.fade(name, 1.0, 0.3)
            self.led_service.fade(name, 0.0, 0.3)
            self.led_service.fade(name, 1.0, 0.3)
            self.led_service.fade(name, 0.0, 0.3)
            self.led_service.fade(name, 1.0, 0.3)
            self.led_service.fade(name, 0.0, 0.3)
            self.all_leds_on()
            time.sleep(0.5)

    def move_head1(self):
        #2.08 head yaw
        names = ["HeadYaw", "HeadPitch"]
        angles = [[0.000, -0.524], [0.305, -0.393], [0.611, -0.262], [0.916, -0.131], [1.222, 0.000], [0.916, 0.131],
                  [0.611, 0.262], [0.305, 0.393], [-0.305, 0.393], [-0.611, 0.262], [-0.916, 0.131], [-1.222, 0.000],
                  [-0.916, -0.131], [-0.611, -0.262], [-0.305, -0.393], [0.000, 0.524]]

        time.sleep(10)
        self.motion_service.setAngles(names, [0.000, -0.524], 0.1)  # 0.1 is the speed
        time.sleep(1.7)
        self.motion_service.setAngles(names, [0.0, 0.0], 0.1)  # come back to the center
        time.sleep(25)

        # for i in range(len(angles)):
        #     self.motion_service.setAngles(names, angles[i], 0.1)  # 0.1 is the speed
        #     time.sleep(1.7)
        #     self.motion_service.setAngles(names, [0.0, 0.0], 0.1)  # come back to the center
        #     time.sleep(25)

    def move_head2(self):
        #2.08 head yaw
        names = ["HeadYaw", "HeadPitch"]
        angles = [[0.000, -0.524], [0.305, -0.393], [0.611, -0.262], [0.916, -0.131], [1.222, 0.000], [0.916, 0.131]]

        for i in range(len(angles)):
            self.motion_service.setAngles(names, angles[i], 0.1)  # 0.3 is the speed
            time.sleep(2)
            self.motion_service.setAngles(names, [0.0, 0.0], 0.1)  # come back to the center
            time.sleep(3)


