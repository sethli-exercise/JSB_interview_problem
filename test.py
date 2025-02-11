# This file is to do small tests

import ollama
import requests
import streamlit as st

import subprocess
import speech_recognition as sr
import pyaudio

import listener
import speechToText
import os


class LLMInterface():

    sendPromptUrl = "http://localhost:5000/prompt/send"
    getResponseUrl = "http://localhost:5000/response/get"

    def __init__(self):
        self.displayedMessages = []

    # send a prompt to the LLM
    # returns true if the prompt was successfully sent
    # returns false if the prompt was not succ
    def sendPrompt(self, prompt: str):

        # where and what to send
        url = LLMInterface.sendPromptUrl
        data = {
            "prompt" : prompt
        }

        try:
            response = requests.post(url)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            st.error(f"failed to send prompt\nERROR:{e}")
            return False

    def getAllResponses(self):
        url = LLMInterface.getResponseUrl
        try:
            response = requests.post(url)
        except Exception as e:
            st.error(f"failed to get all responses\nERROR:{e}")
            return []

    def getLastResponse(self):
        url = LLMInterface.getResponseUrl
        try:
            response = requests.post(url)
        except Exception as e:
            st.error(f"failed to get last response\nERROR:{e}")
            return []

conversation = ["Only respond to the last prompt the rest are the previous prompts. Each prompt is delimited by &&&&**(%."]

def testJoin(string: str):
    conversation.append(string)
    conversationString = "&&&&**(%".join(entry for entry in conversation)
    print(conversationString)

def promptOllama(prompt: str, model: str):
    conversation.append(prompt)
    conversationString = "&&&&**(%".join(entry for entry in conversation)

    response = ollama.chat(
        model = model,
        messages = [
            {'role': 'user',
             'content': conversationString
             }
        ]
    )
    return response

def test1():
    modelVersion = "llama3.3"
    # modelOutput = flask_app.run_ollama("How many parameters do you have?")
    modelOutput = promptOllama("write bananas", modelVersion)
    print(modelOutput['message']['content'])

    modelOutput = promptOllama("what is the last prompt you were given", modelVersion)
    print(modelOutput['message']['content'])
    return

def test2():
    testJoin("message 1")
    testJoin("message 2")

def test3():
    recorder = listener.AudioRecorder()
    recorder.record()

def test4():
    stt = speechToText.SpeechToText()
    print(stt.transcribeFile("E:/codeProjects/JSB_interview_problem/output.wav"))


def main():
    test3()
    # os.environ["PATH"] += os.pathsep + "C:\\ffmpeg\\ffmpeg-7.1-essentials_build\\bin"
    test4()

    # subprocess.run(["ffmpeg", "-version"])

if __name__ == "__main__":
    main()



