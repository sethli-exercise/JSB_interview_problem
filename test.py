# This file is to do small tests
import datetime
import time

import ollama
import requests
import streamlit as st

import subprocess
import speech_recognition as sr
import pyaudio

import speechToText
import os

import filetype

__conversation = ["Only respond to the last prompt the rest are the previous prompts. Each prompt is delimited by &&&&**(%."]

def testJoin(string: str):
    __conversation.append(string)
    conversationString = "&&&&**(%".join(entry for entry in __conversation)
    print(conversationString)

def promptOllama(prompt: str, model: str):
    __conversation.append(prompt)
    conversationString = "&&&&**(%".join(entry for entry in __conversation)

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
    print("filetype:")
    # print(detectFileType("E:/codeProjects/JSB_interview_problem/test.py"))


def test4():
    stt = speechToText.SpeechToText()
    print(stt.transcribeFile("E:/codeProjects/JSB_interview_problem/output.wav")) #file has been deleted from repo

def test5():
    start = datetime.datetime.now()
    time.sleep(897/1000)
    end = datetime.datetime.now()
    print(f"{(end - start).total_seconds() * 1000:.3f} milliseconds")

def main():
    # test3()
    # os.environ["PATH"] += os.pathsep + "C:\\ffmpeg\\ffmpeg-7.1-essentials_build\\bin"
    test5()

    # subprocess.run(["ffmpeg", "-version"])

if __name__ == "__main__":
    main()



