import streamlit as st
import speech_recognition as sr


# Load the content of the book.txt file with proper encoding
def load_book(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            book_content = file.read()
        return book_content
    except Exception as e:
        return f"Error loading book: {e}"


# Basic keyword matching function for chatbot responses
def get_chatbot_response(user_input, book_content):
    # Simple keyword matching (you can improve this logic)
    user_input = user_input.lower()

    # Search for keywords in the book content
    if "hero" in user_input:
        return "The hero is a central character in the book, often facing challenges."
    elif "villain" in user_input:
        return "The villain is the antagonist who causes conflict for the hero."
    elif "love" in user_input:
        return "Love plays a significant role in the development of the characters."
    elif "end" in user_input:
        return "The ending of the book is where all loose ends are tied up."
    else:
        return "I am not sure about that, but here's something from the book: \n" + book_content[
                                                                                    :500]  # Show first 500 characters of the book content


# Function to recognize speech and convert to text
def transcribe_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Please speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            # Use Google's speech recognition API to transcribe the audio to text
            text = recognizer.recognize_google(audio)
            st.write("You said: " + text)
            return text
        except sr.UnknownValueError:
            st.write("Sorry, I could not understand the audio.")
            return ""
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
            return ""


# Streamlit app UI
st.title("Book Chatbot with Speech Recognition")

# Load the book content (assuming 'book.txt' is in the same directory)
book_content = load_book('book.txt')

if book_content:
    # Option to use text input or speech input
    user_input_type = st.radio("How would you like to provide input?", ("Text", "Speech"), key="input_choice")

    if user_input_type == "Text":
        user_input = st.text_input("Ask a question about the book:")

        if user_input:
            # Get chatbot response based on user input
            response = get_chatbot_response(user_input, book_content)
            st.write(f"Chatbot response: {response}")

    elif user_input_type == "Speech":
        if st.button("Start Speech Recognition", key="speech_button"):
            # Transcribe speech and get the chatbot response
            speech_input = transcribe_speech()
            if speech_input:
                response = get_chatbot_response(speech_input, book_content)
                st.write(f"Chatbot response: {response}")
else:
    st.write("Failed to load the book. Please check the file path.")
