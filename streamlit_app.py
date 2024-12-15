import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import time

# Function to load system instructions from a file
def load_instructions(file_path):
    with open(file_path, "r") as file:
        return file.read()

# Path to the instructions file
instructions_file = "instructions.txt"

# Load the instructions
system_instructions = load_instructions(instructions_file)

# Retrieve the API key securely from Streamlit Secrets
api_key = st.secrets["GOOGLE_API_KEY"]

# Check if the API key exists
if not api_key:
    st.error("API key not found! Please configure it in the Secrets section of your Streamlit app settings.")
else:
    # Configure the generative AI with the API key
    genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction=system_instructions,
)

# Streamlit app styles
page_bg_color = "#e1e8ed"
st.markdown(
    f"""
    <style>
    body {{
        background-color: {page_bg_color};
    }}
    .bubble {{
        padding: 10px;
        border-radius: 15px;
        margin: 10px 0;
        max-width: 70%;
        display: inline-block;
        word-wrap: break-word; /* Ensures long words or URLs break to the next line */
        white-space: normal;   /* Allows text to wrap properly within the bubble */
    }}
    .user-bubble {{
        background-color: #F0F0F0;
        color: #3d3d3d;
        float: right;
        clear: both;
    }}
    .tutor-bubble {{
        background-color: #DCEEFE;
        color: #3f63f2;
        float: left;
        clear: both;
    }}
    .icon {{
        width: 40px;
        height: 40px;
        margin-right: 10px;
        border-radius: 50%;
        background-size: cover;
        background-position: center;
    }}
    .clear-fix {{
        clear: both;
    }}
    .title {{
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #3f63f2;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.markdown("<div class='title'>AP Environmental Science Tutor</div>", unsafe_allow_html=True)

# Track the last selected topic to avoid duplicate entries
if "last_selected_topic" not in st.session_state:
    st.session_state.last_selected_topic = ""

# Dropdown Box for APES Topics
topics = [
    "Unit 1: The Living World: Ecosystems",
    "Unit 2: The Living World: Biodiversity",
    "Unit 3: Populations",
    "Unit 4: Earth Systems and Resources",
    "Unit 5: Land and Water Use",
    "Unit 6: Energy Resources and Consumption",
    "Unit 7: Atmospheric Pollution",
    "Unit 8: Aquatic and Terrestrial Pollution",
    "Unit 9: Global Change",
]

selected_topic = st.selectbox(
    "Not sure what to study? Click here to see the list of topics!", [""] + topics
)

# Check if the selected topic has changed and only process it once
if selected_topic and selected_topic != st.session_state.last_selected_topic:
    st.session_state.chat_session.history.append({"role": "user", "parts": [{"text": selected_topic}]})
    response = st.session_state.chat_session.send_message(selected_topic)
    st.session_state.chat_session.history.append({"role": "model", "parts": [{"text": response.text}]})
    st.session_state.last_selected_topic = selected_topic  # Update to prevent duplicates

# Set up user icon and tutor icon
user_icon = "https://e7.pngegg.com/pngimages/168/827/png-clipart-computer-icons-user-profile-avatar-profile-woman-desktop-wallpaper-thumbnail.png"  # Placeholder for user icon
tutor_icon = "https://cdn2.iconfinder.com/data/icons/social-media-agency-dazzle-vol-1/256/Bot-512.png"    # Placeholder for tutor icon

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(
        history=[
                {"role": "model", "parts": [{"text": "Good afternoon! I'm here to help with your APES review."}]},
        ]
    )

# Display chat history
chat_placeholder = st.empty()
with chat_placeholder.container():
    for message in st.session_state.chat_session.history:
        if hasattr(message, "role") and message.role == "user":
            st.markdown(
                f"<div class='bubble user-bubble'><div class='icon' style='background-image: url({user_icon});'></div>{message.parts[0].text if message.parts else ''}</div><div class='clear-fix'></div>",
                unsafe_allow_html=True,
            )
        elif hasattr(message, "role") and message.role == "model":
            st.markdown(
                f"<div class='bubble tutor-bubble'><div class='icon' style='background-image: url({tutor_icon});'></div>{message.parts[0].text if message.parts else ''}</div><div class='clear-fix'></div>",
                unsafe_allow_html=True,
            )

# User input with a unique key each time
if "count" not in st.session_state:
    st.session_state.count = 0

input_placeholder = st.empty()
user_input = input_placeholder.text_input(
    "Your message:",
    key=f"user_input_{st.session_state.count}",
    placeholder="Enter your message here..."
)

if st.button("Submit", key=f"submit_button_{st.session_state.count}") or user_input:
    response = st.session_state.chat_session.send_message(user_input)

    # Add user message and response to history
    st.session_state.chat_session.history.append({"role": "user", "parts": [{"text": user_input}]})
    st.session_state.chat_session.history.append({"role": "model", "parts": [{"text": response.text}]})

    # Redisplay chat
    with chat_placeholder.container():
        for message in st.session_state.chat_session.history:
            if hasattr(message, "role") and message.role == "user":
                st.markdown(
                    f"<div class='bubble user-bubble'><div class='icon' style='background-image: url({user_icon});'></div>{message.parts[0].text if message.parts else ''}</div><div class='clear-fix'></div>",
                    unsafe_allow_html=True,
                )
            elif hasattr(message, "role") and message.role == "model":
                st.markdown(
                    f"<div class='bubble tutor-bubble'><div class='icon' style='background-image: url({tutor_icon});'></div>{message.parts[0].text if message.parts else ''}</div><div class='clear-fix'></div>",
                    unsafe_allow_html=True,
                )

    # Reset input field
    st.session_state.count += 1
    input_placeholder.text_input(
        "Your message:",
        value="",
        key=f"user_input_{st.session_state.count}",
        placeholder="Enter your message here..."
    )