import streamlit as st
from pathlib import Path
from datetime import datetime

def get_character_logo_path(role):
    BASE_DIR = Path("/Users/alexandrelavalleeperso/Desktop/code/LLM-as-a-judge-realtime/ai-court-simulator")
    logo_map = {
        "Judge": "judge.png",
        "Depp's Attorney": "defendant_lawyer.png",
        "Heard's Attorney": "prosecutor_lawyer.png",
        "Witness": "witness.png"
    }
    return BASE_DIR / "frontend/components/character_logo" / logo_map.get(role, "default.png")

def setup_page_config():
    st.set_page_config(
        page_title="AI Court Simulator",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .speaking {
            border-left: 4px solid #00ff00;
            background-color: rgba(0, 255, 0, 0.1);
            padding: 10px;
        }
        .waiting {
            border-left: 4px solid #808080;
            padding: 10px;
        }
        .participant-card {
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
            background-color: #f0f2f6;
            display: flex;
            align-items: center;
        }
        .dialogue-box {
            margin: 10px 0;
            padding: 15px;
            border-radius: 10px;
            background-color: #ffffff;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .character-logo {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            margin-right: 15px;
        }
        .participant-info {
            flex-grow: 1;
        }
        .header-img {
            max-width: 150px;
            margin: 10px;
        }
        .stButton button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

def display_participant(name, role, status):
    color = "#00ff00" if status == "speaking" else "#808080"
    icon = "🗣️" if status == "speaking" else "⏳"
    
    # Get logo path
    logo_path = get_character_logo_path(role)
    
    # Create columns for layout
    cols = st.columns([1, 4])
    
    with cols[0]:
        if logo_path.exists():
            st.image(str(logo_path), width=60)
    
    with cols[1]:
        st.markdown(f"""
            <div class="participant-card {status}">
                <div class="participant-info">
                    <h3>{icon} {name}</h3>
                    <p>Role: {role}</p>
                    <p>Status: {status}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

def display_dialogue(speaker, text, timestamp):
    # Get role based on speaker
    role = "Judge" if "Judge" in speaker else \
           "Depp's Attorney" if "Chew" in speaker else \
           "Heard's Attorney" if "Rottenborn" in speaker else \
           "Witness" if "Dembrowski" in speaker else None
    
    logo_path = get_character_logo_path(role) if role else None
    
    cols = st.columns([1, 6])
    
    with cols[0]:
        if logo_path and logo_path.exists():
            st.image(str(logo_path), width=50)
    
    with cols[1]:
        st.markdown(f"""
            <div class="dialogue-box">
                <strong>{speaker}</strong> <small>{timestamp}</small>
                <p>{text}</p>
            </div>
        """, unsafe_allow_html=True)

def initialize_session_state():
    if 'session_active' not in st.session_state:
        st.session_state.session_active = False
    if 'dialogue_history' not in st.session_state:
        st.session_state.dialogue_history = []
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None

def main():
    setup_page_config()
    initialize_session_state()
    
    # Load images
    BASE_DIR = Path("/Users/alexandrelavalleeperso/Desktop/code/LLM-as-a-judge-realtime/ai-court-simulator")
    amber_depp_logo_path = BASE_DIR / "frontend/components/reporting_amber_heard.png"
    openai_build_lab_logo_path = BASE_DIR / "frontend/components/openAI_builder_lab.png"

    # Header with logos
    st.markdown("<div style='display: flex; justify-content: space-around;'>", unsafe_allow_html=True)
    if amber_depp_logo_path.exists():
        st.image(str(amber_depp_logo_path), caption='Amber vs Depp Trial', width=150)
    if openai_build_lab_logo_path.exists():
        st.image(str(openai_build_lab_logo_path), caption='OpenAI Build Lab', width=150)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.title("🏛️ AI Court Simulator")
    
    # Main layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("Ongoing Proceedings")
        
        # Session control
        if not st.session_state.session_active:
            if st.button("▶️ Start New Session"):
                st.session_state.session_active = True
                st.session_state.start_time = datetime.now()
                # Add initial dialogue
                st.session_state.dialogue_history = [
                    {
                        "speaker": "Judge Penney Azcarate",
                        "text": "Court is now in session. We are here today for the case of Depp vs Heard.",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    }
                ]
                st.experimental_rerun()
        
        # Display dialogue history
        with st.container():
            if st.session_state.session_active:
                for dialogue in st.session_state.dialogue_history:
                    display_dialogue(
                        dialogue["speaker"],
                        dialogue["text"],
                        dialogue["timestamp"]
                    )
            else:
                st.info("Press 'Start New Session' to begin the court simulation")
            
        # Control buttons
        if st.session_state.session_active:
            st.divider()
            cols = st.columns(4)
            with cols[0]:
                if st.button("⏯️ Pause/Resume"):
                    new_dialogue = {
                        "speaker": "System",
                        "text": "Session paused",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    }
                    st.session_state.dialogue_history.append(new_dialogue)

            with cols[1]:
                if st.button("⏭️ Next Phase"):
                    new_dialogue = {
                        "speaker": "Judge Penney Azcarate",
                        "text": "Let's proceed to the next phase.",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    }
                    st.session_state.dialogue_history.append(new_dialogue)

            with cols[2]:
                if st.button("👤 Call Witness"):
                    new_dialogue = {
                        "speaker": "Court Clerk",
                        "text": "Calling Christi Dembrowski to the stand.",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    }
                    st.session_state.dialogue_history.append(new_dialogue)

            with cols[3]:
                if st.button("❌ End Session"):
                    st.session_state.session_active = False
                    st.session_state.dialogue_history = []
                    st.session_state.start_time = None
                    st.experimental_rerun()
            
    with col2:
        st.header("Participants")
        
        if st.session_state.session_active:
            display_participant("Judge Penney Azcarate", "Judge", "speaking")
            display_participant("Ben Chew", "Depp's Attorney", "waiting")
            display_participant("Ben Rottenborn", "Heard's Attorney", "waiting")
            display_participant("Christi Dembrowski", "Witness", "waiting")
            
            st.divider()
            elapsed_time = "00:00"
            if st.session_state.start_time:
                elapsed = datetime.now() - st.session_state.start_time
                minutes, seconds = divmod(elapsed.seconds, 60)
                elapsed_time = f"{minutes:02d}:{seconds:02d}"
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Elapsed Time", elapsed_time)
            with col2:
                st.metric("Participants", "4/6")
        else:
            st.info("Session not started")
        
        st.divider()
        st.subheader("Session Settings")
        st.selectbox("Case Type", ["Defamation", "Libel"], 
                    disabled=st.session_state.session_active)
        st.number_input("Est. Duration (min)", 
                       min_value=15, 
                       max_value=120, 
                       value=60,
                       disabled=st.session_state.session_active)
    
    st.markdown("""
        <div style='text-align: center; margin-top: 20px;'>
            <p>Project built at Station F for the OpenAI Build Lab!</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()