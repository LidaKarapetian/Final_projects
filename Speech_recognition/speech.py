#!/usr/bin/python

"""
Speech Recognition - create a script which will help you to implement a lot of voice commands.
"""
import importlib.util
import subprocess
from commands_dict import COMMANDS

def check_module_and_install(module_name):
    """
    This function checks if the module is installed.
    If not, it attempts to install the module using the 'pip' command.
    """
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        try:
            subprocess.run(["pip", "install", module_name], check=True)
            print(f"Successfully installed the '{module_name}' module.")
        except subprocess.CalledProcessError as error:
            print(f"Error installing the '{module_name}' module: {error}")
            return False
    else:
        print(f"The '{module_name}' module is already installed.")
    return True

try:
    import speech_recognition
except ModuleNotFoundError:
    print("The 'speech_recognition' module is not installed.")
    check_module_and_install("speech_recognition")
    import speech_recognition

def get_audio_command(sr):
    """
    Get the audio command using the speech recognition module.
    """
    try:
        with speech_recognition.Microphone() as mic:
            print("Listening...")
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            command = sr.recognize_google(audio_data=audio, language='en-US').lower()
        return command
    except speech_recognition.UnknownValueError:
        return  "Couldn't understand what you said."
    except speech_recognition.RequestError as e:
        return f"Failed to connect. Please check your internet connection. {e}"

def execute_command(command):
    """
    Execute the recognized command.
    """
    try:
        if command in COMMANDS:
            print(f"Executing command: {command}")
            subprocess.Popen(COMMANDS[command], shell=True)
        else:
            print("Command not found.")
    except Exception as error:
        print(f"An error occurred while executing the command: {error}")

def main():
    """
    The main function that controls the execution flow of the program.
    """
    sr = speech_recognition.Recognizer()
    print("""Hi, these are commands that you can say:
          list files, print working directory, open terminal, open code, open firefox, 
          shutdown computer, make directory, create file, open calculator, restart computer,
          take a screenshot, open calendar, open music player.""")
    while True:
        command = get_audio_command(sr)
        execute_command(command)

if __name__ == "__main__":
    main()
