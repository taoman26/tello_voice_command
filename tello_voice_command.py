from tello import Tello
import sys
import time
import os
import speech_recognition as sr
import asyncio
import json
from janome.tokenizer import Tokenizer # for japanese

##### MAIN ######
def main():
    tello = Tello()
    # create recognizer and mic instances
    sample_rate = 96000
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=0)
    #recognizer.energy_threshold = 4000
    try:
        flying = 0
        while True:
            print("START RECOGNIZING!")
            VRcommand = recognize_speech_from_mic(recognizer, microphone)
            print("API returns: {}".format(VRcommand["error"]))

            i = 0
            com_list = VRcommand["transcription"]
            command = ""

            for word in (com_list):
                if(com_list[i] == "飛べ" and flying == 1):
                    print("Already Flying!")
                    i=i+1
                elif(com_list[i] == "着陸" and flying == 1):
                    # print("Action command recognized: land")
                    command += "land"
                    flying = 0
                    i=i+1
                    break
                elif((com_list[i] != "飛べ" or com_list[i] != "着陸") and flying == 1):
                    if(com_list[i] == "前" or com_list[i] == "前方" or com_list[i] == "まえ"):
                        # print("Action command recognized: forward")
                        command += "forward 100"
                        i=i+1
                    elif(com_list[i] == "後ろ" or com_list[i] == "後方" or com_list[i] == "うしろ"):
                        # print("Action command recognized: back")
                        command += "back 100"
                        i=i+1
                    elif(com_list[i] == "左" or com_list[i] == "ひだり"):
                        # print("Action command recognized: left")
                        command += "left 100"
                        i=i+1
                    elif(com_list[i] == "右" or com_list[i] == "みぎ"):
                        # print("Action command recognized: right")
                        command += "right 100"
                        i=i+1
                    elif(com_list[i] == "上" or com_list[i] == "上方" or com_list[i] == "上昇" or com_list[i] == "うえ"):
                        # print("Action command recognized: up")
                        command += "up 100"
                        i=i+1
                    elif(com_list[i] == "下" or com_list[i] == "下方" or com_list[i] == "下降" or com_list[i] == "した"):
                        # print("Action command recognized: down")
                        command += "down 100"
                        i=i+1
                    elif(com_list[i] == "旋回" or com_list[i] == "せんかい"):
                        # print("Action command recognized: flip")
                        command += "flip r"
                        i=i+1
                    else:
                        print("Incorrect Command")
                        i=i+1
                elif(com_list[i] == "飛べ" and flying == 0):
                    # print("Action command recognized: takeoff")
                    command += "takeoff"
                    flying = 1
                    i=i+1
                elif(flying == 0):
                    print("Not flying!")
                    i=i+1
                else:
                    print("Debug= "+flying)
                    print("Debug Command = "+com_list[i])
                    command += "land" # emergency landing
                    flying = 0
                    i=i+1

            if(command == "land"):
                print("command = %s" % command)
                tello.send_command(command)
                break
            if(command != "land"):
                print("command = %s" % command)
                tello.send_command(command)
            else:
                print("command not registered")
        exit()

    except SystemExit as e:
        print('exception = "%s"' % e)

##### RECOGNIZE ######
def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.
    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.pause_threshold = 0.8
        recognizer.dynamic_energy_threshold = False
        recognizer.adjust_for_ambient_noise(source)
        recognized = None

        '''LISTINING'''
        try:
            audio = recognizer.listen(source, timeout = 5)
        except sr.WaitTimeoutError:
            print("Timeout...")
            return
        
        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # RECOGNIZING
        try:
            recognized = recognizer.recognize_google(audio, key=None, language='ja')
            print("You said: " + recognized)
            # WAKATI
            t = Tokenizer(wakati=True)
            response["transcription"] = t.tokenize(recognized)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"
        return response

###### ENTRY POINT ######
if __name__ == "__main__":
    main()