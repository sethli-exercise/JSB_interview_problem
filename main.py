import flask_app
import streamlit_app

def main():
    # backend
    flask_app.main()
    # frontend
    streamlit_app.main()

if __name__ == "__main__":
    main()