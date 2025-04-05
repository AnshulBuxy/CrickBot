import streamlit as st
from backend import CricketAPI, ChatAgent

st.set_page_config(page_title="Cricket ChatBot", layout="wide")
cricket_api = CricketAPI()

# Sidebar setup
st.sidebar.title("🏏 Cricket ChatBot")

selected_match_id = None
selected_match_name = None
match_type = None

menu = st.sidebar.selectbox("Select Category", ["Live Matches", "Past Matches", "General Questions"], key="menu")

# Match selection logic based on category
if menu == "Live Matches":
    match_type = "Live"
    live_matches = cricket_api.fetch_live_matches()
    selected_match = st.sidebar.selectbox("Select a Live Match", [match['title'] for match in live_matches['matches']], key="live_match")
    if selected_match:
        for match in live_matches['matches']:
            if match['title'] == selected_match:
                selected_match_id = match['id']
                selected_match_name = match['title']
                st.session_state['selected_match_id'] = selected_match_id
                st.session_state['selected_match_name'] = selected_match_name
                st.session_state['match_type'] = match_type

elif menu == "Past Matches":
    match_type = "Past"
    past_matches = cricket_api.fetch_past_matches()
    selected_match = st.sidebar.selectbox("Select a Past Match", [match['teams'] for match in past_matches['match']], key="past_match")
    if selected_match:
        for match in past_matches['match']:
            if match['teams'] == selected_match:
                selected_match_id = match['match_id']
                selected_match_name = match['teams']
                st.session_state['selected_match_id'] = selected_match_id
                st.session_state['selected_match_name'] = selected_match_name
                st.session_state['match_type'] = match_type

elif menu == "General Questions":
    match_type = "General"
    st.session_state['selected_match_id'] = 'N/A'
    st.session_state['selected_match_name'] = 'General Inquiry'
    st.session_state['match_type'] = match_type

# Main Chatbox Interface
if st.session_state.get("selected_match_id") or menu == "General Questions":
    match_id = st.session_state.get('selected_match_id', "N/A")
    match_name = st.session_state.get('selected_match_name', "General Inquiry")
    match_type = st.session_state.get('match_type', "General")
    
    st.subheader(f"Chat about: {match_name} ({match_type})")
    
    # Initialize chat history if not already present
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    
    # Display chat history (this will display previous user/assistant messages)
    for chat_history in st.session_state["chat_history"]:
        with st.chat_message(chat_history["role"]):
            st.markdown(chat_history["content"])
    
    # User input for asking questions
    user_input = st.text_input("Ask a question:", "")
    
    if st.button("Ask"):
        # Add user question to history
        user_message = {"role": "user", "content": f'Answer the following: \n{user_input}'}
        st.session_state["chat_history"].append(user_message)
        
        # Initialize ChatAgent
        chat_agent = ChatAgent(user_input=user_input, match_type=match_type, match_id=match_id)
        response = chat_agent.get_response(match_type=match_type, match_id=match_id, user_input=f"Match Type: {match_type}, Match ID: {match_id}, Query: {user_input}")
        
        # Append assistant response to history
        assistant_message = {"role": "assistant", "content": response}
        st.session_state["chat_history"].append(assistant_message)
    
        # Display the assistant response
        with st.chat_message("assistant"):
            st.markdown(response)

    # Keep the chat input box at the bottom by adding some spacing
    st.markdown('<br><br><br><br>', unsafe_allow_html=True)
