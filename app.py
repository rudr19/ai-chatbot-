import streamlit as st
import google.generativeai as gai
from PIL import Image
from datetime import datetime

# Initialize Google Generative AI with API key
gai.configure(api_key='AIzaSyDgXMq9ebip97UpTcjGiLLIlPHvEpK4FDM')

# Custom CSS for Instagram-like chat bubbles and buttons
st.markdown("""
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .chat-bubble {
            padding: 10px;
            border-radius: 20px;
            margin-bottom: 10px;
            width: fit-content;
        }
        .user-bubble {
            background-color: #daf8e3;
            text-align: left;
            margin-left: auto;
            max-width: 70%;
        }
        .ai-bubble {
            background-color: #f0f0f5;
            text-align: left;
            max-width: 70%;
        }
        .header {
            text-align: center;
        }
        .logo {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100px;
        }
        .footer {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            text-align: center;
            font-size: 12px;
            padding: 10px;
            width: 100%;
            background-color: #f1f1f1;
            color: black;
        }
        .send-button {
            background-color: #fc5c65;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
        }
        .send-button:hover {
            background-color: #eb3b5a;
        }
        .file-upload {
            background-color: #3867d6;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
        }
        .file-upload:hover {
            background-color: #4b7bec;
        }
    </style>
""", unsafe_allow_html=True)

# Display logo at the top
logo_url = "https://path-to-your-logo-image.png"  # Replace with your logo path
st.image(logo_url, width=150, use_column_width=True)

# Set up the Streamlit app layout
st.title("AI Image and Text Interaction App")
st.write("Upload an image, ask a question, and interact with Google's Generative AI.")

# Create session state for storing chat history
if 'history' not in st.session_state:
    st.session_state.history = []

# Upload an image with a custom button
uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Check if an image has been uploaded
if uploaded_image is not None:
    img = Image.open(uploaded_image)
    st.image(img, caption="Uploaded Image", use_column_width=True)

# Input text prompt
prompt = st.text_input("Enter your prompt here", placeholder="Type your question here...")

# Function to generate AI response
def generate_response(prompt, img):
    model = gai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt, img])
    return response.text

# API response section
if st.button("Send", key='send', help='Send your prompt', use_container_width=True):
    if uploaded_image is not None:
        if prompt:
            response_text = generate_response(prompt, img)
            # Add user prompt and AI response to chat history with timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            st.session_state.history.insert(0, {"user": prompt, "response": response_text, "time": timestamp})  # Insert at the beginning
            # Clear the prompt after sending
            st.experimental_rerun()
        else:
            st.warning("Please enter a prompt.")
    else:
        st.warning("Please upload an image before asking a question.")

# Display ongoing chat history with newest at the top
if st.session_state.history:
    st.write("### Chat History")
    for chat in st.session_state.history:
        # Display user input
        st.markdown(f"""
        <div class='chat-bubble user-bubble'>
            <strong>You:</strong> {chat['user']} <br>
            <small>{chat['time']}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Display AI response
        st.markdown(f"""
        <div class='chat-bubble ai-bubble'>
            <strong>AI:</strong> {chat['response']}
        </div>
        """, unsafe_allow_html=True)

# Add footer text
st.markdown("""
    <div class="footer">
        Made With Love ❤️
    </div>
""", unsafe_allow_html=True)
