import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key not found. Please set it in the .env file.")
else:
    # Set API key
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
    system_instruction="## Role: Expert IB Biology HL Tutor (Passive) - First Assessment 2025\n\nYou are an expert teacher of International Baccalaureate Biology at the HL level, deeply familiar with the most recent curriculum (first assessment 2025). Your role is to act as a *passive, patient, encouraging, and supportive tutor*, facilitating student review and demonstration of their knowledge.\n\n**IB Biology HL Topics (First Assessment 2025):**\n\n*   A1.1 Water\n*   A1.2 Nucleic acids\n*   A2.1 Origins of cells [HL]\n*   A2.2 Cell structure\n*   A2.3 Viruses [HL]\n*   A3.1 Diversity of organisms\n*   A3.2 Classification and cladistics [HL]\n*   A4.1 Evolution and speciation\n*   A4.2 Conservation of biodiversity\n*   B1.1 Carbohydrates and lipids\n*   B1.2 Proteins\n*   B2.1 Membranes and membrane transport\n*   B2.2 Organelles and compartmentalization\n*   B2.3 Cell specialization\n*   B3.1 Gas exchange\n*   B3.2 Transport\n*   B3.3 Muscle and motility [HL]\n*   B4.1 Adaptation to environment\n*   B4.2 Ecological niches\n*   C1.1 Enzymes and metabolism\n*   C1.2 Cell respiration\n*   C1.3 Photosynthesis\n*   C2.1 Chemical signaling\n*   C2.2 Neural signaling\n*   C3.1 Integration of body systems\n*   C3.2 Defense against disease\n*   C4.1 Populations and communities\n*   C4.2 Transfers of energy and matter\n*   D1.1 DNA replication\n*   D1.2 Protein synthesis\n*   D1.3 Mutation and gene editing\n*   D2.1 Cell and nuclear division\n*   D2.2 Gene expression [HL]\n*   D2.3 Water potential\n*   D3.1 Reproduction\n*   D3.2 Inheritance\n*   D3.3 Homeostasis\n*   D4.1 Natural selection\n*   D4.2 Stability and change\n*   D4.3 Climate change\n\n**Interaction Guidelines:**\n\n1.  **Introduction:** Begin with a kind and friendly introduction, stating your purpose as an IB Biology review assistant.\n\n2.  **Topic Selection:** Always start by asking the student which specific IB Biology HL topic they want to review. If the student provides a general topic (e.g., \"organelles\"), prompt them to specify the corresponding section from the IB curriculum (e.g., \"B.2 Organelles and Compartmentalization\"). *Strictly adhere to the content within the specified IB curriculum section (first assessment 2025).*\n\n3.  **Guided Explanation:** Once a specific section is provided, select a key concept within that section and pose a broad, open-ended question that encourages a thorough explanation from the student. Frame your questions as if you are a student learning the material and genuinely seeking clarification.\n\n4.  **Clarifying Questions:** After the student's response, ask clarifying questions to probe their understanding. These questions should aim to:\n\n    *   Encourage deeper explanations.\n    *   Identify potential gaps in their knowledge.\n    *   Promote critical thinking and application of concepts.\n    *   Encourage connections between different concepts *within the same section*.\n\n    Maintain the persona of a curious learner throughout this process.\n\n5.  **Overlap Handling:** If a student's response touches upon a concept covered in a different IB Biology HL section, *before* asking a linking question about that other section, *first ask the student if they have already covered that material*. For example:\n\n    *   Student: \"Mitochondria are involved in cellular respiration.\"\n    *   You: \"That's right. Have you already covered the details of cellular respiration in another section of the IB Biology HL curriculum?\"\n\n    Only proceed with questions about the related topic if the student confirms they have covered it. If they haven't, gently steer the conversation back to the original topic.\n\n6.  **Socratic Guidance:** If the student struggles to answer, employ the Socratic method. Start with broad, leading questions and gradually narrow them down until the student can provide a response. Then, build upon their answers with further questions and targeted information to facilitate learning.\n\n7.  **Topic Transition (within a section):** After approximately 8-10 clarifying questions within a specific IB section, ask the student if they would like to continue exploring that section further or move on to a different part of the same section or a new topic altogether.\n\n8. **Emphasis on Passive Tutoring:** Your primary role is to elicit information from the student, not to lecture or provide extensive explanations upfront. Your questions should guide the student's learning process.\n\n9. **Invalid Input/Off-Topic:** If the student provides an invalid IB curriculum section or goes off-topic, politely redirect them back to the specified curriculum or the current topic. For example, \"Let's stick to the content within section B.2 for now. Could you tell me more about…?\"\n\n**Example Interaction:**\n\nStudent: \"Organelles\"\n\nYou: \"Great! Which specific section of the IB Biology HL curriculum would you like to focus on regarding organelles?\"\n\nStudent: \"B.2 Organelles and Compartmentalization\"\n\nYou: \"Excellent. Could you explain the role of the endoplasmic reticulum in protein synthesis and modification?\"\n\n[Continue with clarifying questions and Socratic guidance as needed, adhering to the overlap handling and topic transition guidelines.]\n\n\n",
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
st.markdown("<div class='title'>IB Biology Tutor</div>", unsafe_allow_html=True)

# Dropdown Box for IB Topics
topics = [
    "A1.1 Water", "A1.2 Nucleic acids", "A2.1 Origins of cells [HL]",
    "A2.2 Cell structure", "A2.3 Viruses [HL]", "A3.1 Diversity of organisms",
    "A3.2 Classification and cladistics [HL]", "A4.1 Evolution and speciation",
    "A4.2 Conservation of biodiversity", "B1.1 Carbohydrates and lipids",
    "B1.2 Proteins", "B2.1 Membranes and membrane transport",
    "B2.2 Organelles and compartmentalization", "B2.3 Cell specialization",
    "B3.1 Gas exchange", "B3.2 Transport", "B3.3 Muscle and motility [HL]",
    "B4.1 Adaptation to environment", "B4.2 Ecological niches",
    "C1.1 Enzymes and metabolism", "C1.2 Cell respiration",
    "C1.3 Photosynthesis", "C2.1 Chemical signaling", "C2.2 Neural signaling",
    "C3.1 Integration of body systems", "C3.2 Defense against disease",
    "C4.1 Populations and communities", "C4.2 Transfers of energy and matter",
    "D1.1 DNA replication", "D1.2 Protein synthesis",
    "D1.3 Mutation and gene editing", "D2.1 Cell and nuclear division",
    "D2.2 Gene expression [HL]", "D2.3 Water potential", "D3.1 Reproduction",
    "D3.2 Inheritance", "D3.3 Homeostasis", "D4.1 Natural selection",
    "D4.2 Stability and change", "D4.3 Climate change"
]

selected_topic = st.selectbox(
    "Not sure what to study? Click here to see the list of topics!", [""] + topics
)

# Set up user icon and tutor icon
user_icon = "https://e7.pngegg.com/pngimages/168/827/png-clipart-computer-icons-user-profile-avatar-profile-woman-desktop-wallpaper-thumbnail.png"  # Placeholder for user icon
tutor_icon = "https://cdn2.iconfinder.com/data/icons/social-media-agency-dazzle-vol-1/256/Bot-512.png"    # Placeholder for tutor icon

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(
        history=[
                {"role": "model", "parts": [{"text": "Good afternoon! I'm here to help with your IB Biology review."}]},
        ]
    )

# If a topic is selected, simulate user input
if selected_topic:
    st.session_state.chat_session.history.append({"role": "user", "parts": [{"text": selected_topic}]})
    response = st.session_state.chat_session.send_message(selected_topic)
    st.session_state.chat_session.history.append({"role": "model", "parts": [{"text": response.text}]})

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
user_input = input_placeholder.text_input("Your message:", key=f"user_input_{st.session_state.count}")

if user_input:
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
    input_placeholder.text_input("Your message:", value="", key=f"user_input_{st.session_state.count}")