import sys
import time

import streamlit as st
import requests
import signal


def sigterm_handler(signum, frame):
    sys.exit(0)


# signal.signal(signal.SIGTERM, sigterm_handler)

def fetch_messages():
    try:
        response = requests.get('http://localhost:5000/get_messages')
        if response.status_code == 200:
            return response.json()["messages"]
        else:
            return []
    except Exception as e:
        st.error(f"Failed to fetch messages: {str(e)}")
        return []

def send_message(message: str):
    url = 'http://localhost:5000/send_message'
    data = {
        "msg": message
    }

    try:
        response = requests.post(url, json = data)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()["messages"]
    except Exception as e:
        st.error(f"failed to send message: {str(e)}")
        return []


def display_messages(messages):
    for message in messages:
        st.markdown(message[0])
        st.info(message[1])
        st.divider()




def main():
    st.title('Fantastic Hallucinations from LLMs')

    # st.markdown("<span style='color: blue;'>This text is blue!</span>", unsafe_allow_html=True)

    displayed_messages = []
    while True:
        # time.sleep(1000)
        messages = fetch_messages()
        new_messages = [msg for msg in messages if msg not in displayed_messages]

        if new_messages:
            display_messages(new_messages)
            displayed_messages.extend(new_messages)
        st.rerun()

if __name__ == "__main__":
    main()