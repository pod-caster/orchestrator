import sys
import os
import constant
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dummy import dummy
import streamlit as st
from app.handler import Orchestrator
from app.model.request_model import PodcasterInput
from utils import check_topic

import asyncio

st.set_page_config(page_title="Podcaster Studio", layout="wide")

# ---- CSS for cards, inputs, and episode counter ----
st.markdown("""
<style>
body { background: #f6f9ff; }
.block-container { padding-top:1.25rem; padding-bottom:2rem; }
.title { color:#1a2b6d; font-size:1.9rem; font-weight:800; line-height:1.1; }
.subtitle { color:#5b6b8a; font-size:0.98rem; margin-top:4px; }
/* Card style containers in main/side columns */
section.main .stContainer, section[data-testid="stSidebar"] .stContainer {
    background: #fff;
    border-radius: 16px;
    padding: 22px 20px;
    margin-bottom: 18px;
    box-shadow: 0 4px 14px rgba(31,38,135,0.08);
    border: 1px solid #eef2ff;
}
.stTextInput > div > div > input { border-radius: 10px; border: 1px solid #dbe1f1; font-size: 1rem; }
.stTextArea textarea { border-radius: 10px !important; border: 1px solid #dbe1f1 !important; }
.stTextArea textarea:focus, .stTextInput > div > div > input:focus { border-color:#275efe !important; box-shadow:none !important; }
.stSelectbox > div > div { border-radius: 10px; border: 1px solid #dbe1f1; }
.stRadio > div { gap: 18px; }
.stSlider [data-baseweb="slider"] { margin-top: 6px; }
.link-pill {
    background:#f3f6ff; border:1px solid #e1e8ff; border-radius:10px;
    padding: 8px 12px; font-size: 0.92rem; overflow-wrap: anywhere;
}
.header-container {
    margin-top: 30px;
    margin-bottom: 20px;
}
/* Episode stepper buttons */
.stButton.episode-btn>button {
    background: #fff !important;
    color: #275efe !important;
    border: 2px solid #eef2ff !important;
    border-radius: 10px !important;
    font-size: 1.5rem !important;
    width: 44px !important;
    height: 44px !important;
    box-shadow: none !important;
    font-weight: 700 !important;
    margin: 0 !important;
}
.stButton.episode-btn>button:hover {
    background: #e6edfb !important;
    color: #1f49d5 !important;
}
.episode-value-holder {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 44px;
}
.episode-value-text {
    font-size: 1.1rem;
    font-weight: 600;
    color: #263876;
    text-align: center;
    padding: 0 15px;
}
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown("""
<div style='width:98%; display:flex; justify-content:center;margin-top:30px; margin-bottom:55px;transform: scale(2);'>
  <div class="header-container" style='display:flex; align-items:center; gap:1px;'>
    <img src='https://img.icons8.com/?size=100&id=UygLWuKwvqkC&format=png&color=000000' width='58'/>
    <div style='text-align:left;'>
      <div class='title'>Podcaster Studio</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


main_col, sidebar = st.columns([3.5, 1], gap="large")


# --------- SIDEBAR ---------
with sidebar:
    with st.container():
        st.markdown("### 🎤 Speaker & Host Setup")
        
        host = st.radio("Choose the Host", constant.speakers, key="host_radio")

        st.markdown("#### ➕ Add More Speakers")
        
        if constant.more_than_one_guest:
            ############# Multiple Additional Speakers
            speaker_checks = []
            for sp in constant.speakers:
                if sp != host:
                    checked = st.checkbox(f"Include {sp}", key=f"incl_{sp}")
                    speaker_checks.append((sp, checked))
            guests = [sp for sp, checked in speaker_checks if checked]
            selected_speakers = [host] + guests
        else :
            ############# Single Additional Speaker
            additional_speaker = st.radio(
                "Choose one guest speaker",
                options=[sp for sp in constant.speakers if sp != host],
                index=0,
                key="additional_speaker_radio"
            )
            guests = [additional_speaker] if additional_speaker else []
            selected_speakers = [host] + guests


    st.markdown("#### 🎼 Select Speaker Tones")
    speaker_tones = {}
    for sp in selected_speakers:
        speaker_tones[sp] = st.selectbox(
            f"Select tone for {sp}",
            constant.SPEAKER_TONES,
            index=0,
            key=f"tone_{sp}"
        )

    with st.container():
        st.markdown(
            "<span style='font-size:1.25rem; font-weight:700; display:flex; align-items:center;'>"
            "<img src='https://img.icons8.com/?size=28&id=bKkGcH7iCgGs&format=png&color=FFFFFF' style='margin-right:7px; margin-bottom:-7px;'/> Current Cast</span>",
            unsafe_allow_html=True
        )
        st.markdown(f"- 🏆 <b>Host:</b> <span style='color:#275efe'>{host}</span>", unsafe_allow_html=True)
        if guests:
            st.markdown(
                "- 🎙️ <b>Guests:</b> " + ", ".join([f"<span style='color:#667085'>{g}</span>" for g in guests]),
                unsafe_allow_html=True
            )
        else:
            st.markdown("- 🎙️ <b>Guests:</b> <span style='color:#667085'>None selected</span>", unsafe_allow_html=True)


# ------------------- MAIN CONTENT -------------------
with main_col:
    with st.container():

        label_col_head, text_col_head = st.columns([.8, 3.23], gap="small", vertical_alignment="center")
        with label_col_head:
            st.markdown(
        "<span style='display: flex; align-items: center; gap:6px; margin-bottom:0;'>"
        "<img src='https://img.icons8.com/?size=40&id=scnic4OL3EMo&format=png&color=000000' style='margin: 0 0px 0 0;'/>"
        "<span style='font-size:1.7rem; font-weight:600; color:#000768'>Topic :</span>"
        "</span>",
        unsafe_allow_html=True
    )


        with text_col_head:
            topic = st.text_input(
                "Enter your podcast topic",
                placeholder="E.g., Artificial Intelligence in Healthcare",
                key="podcast_topic",
                label_visibility="collapsed"
            )
            # Profanity check right after topic input
            topic_valid = True
            if topic:
                if check_topic(topic):
                    st.warning("⚠️ Profanity detected! Please choose a different topic.")
                    topic_valid = False

    st.markdown("<div style='margin-top:35px;'></div>", unsafe_allow_html=True)
    # Content Source container
    with st.container():
        label_col_content, radio_col= st.columns([2, 8], gap="small", vertical_alignment="center")
        with label_col_content:
            st.markdown(
        "<span style='display: flex; align-items: center; gap:6px; margin-bottom:0;'>"
        "<img src='https://img.icons8.com/?size=35&id=TTC1PmevMuGY&format=png&color=FFFFFF' style='margin: 0 0px 0 0;'/>"
        "<span style='font-size:1.56rem; font-weight:600; color:#000768'>Content Source :</span>"
        "</span>",
        unsafe_allow_html=True
    )


        with radio_col:
            content_mode = st.radio(
                "a",
                ["Use Podcaster Researcher", "Use my own content"],
                index=0,
                horizontal=True,
                label_visibility="collapsed"
            )


        if content_mode == "Use my own content":
            if "links" not in st.session_state:
                st.session_state.links = []
            if "pasted_texts" not in st.session_state:
                st.session_state.pasted_texts = []
            st.markdown("<div style='margin-top:35px;'></div>", unsafe_allow_html=True)
            col_links, col_paste = st.columns(2, vertical_alignment="top")

            with col_links:
                st.markdown("#### 🔗 Add Reference Links")
                with st.form("add_link_form", clear_on_submit=True):
                    new_link = st.text_area("Add Link", placeholder="https://example.com/article", height=50)
                    add_clicked = st.form_submit_button("➕ Add Link")
                if add_clicked and new_link and new_link not in st.session_state.links:
                    st.session_state.links.append(new_link)

                def delete_link(idx):
                    st.session_state.links.pop(idx)

                for i, link in enumerate(st.session_state.links):
                    c1, c2 = st.columns([9, 1])
                    with c1:
                        st.markdown(f"<div class='link-pill'><a href='{link}' target='_blank'>{link}</a></div>", unsafe_allow_html=True)
                    with c2:
                        st.button("❌", key=f"del_link_{i}", on_click=delete_link, args=(i,))

            with col_paste:
                st.markdown("#### 📝 Paste Supporting Text")
                with st.form("add_pasted_text_form", clear_on_submit=True):
                    new_text = st.text_area("Paste text here", height=50, placeholder="Paste any content, article excerpts, or notes you'd like to incorporate.")
                    add_text_clicked = st.form_submit_button("➕ Add Text")
                if add_text_clicked and new_text.strip():
                    st.session_state.pasted_texts.append(new_text.strip())

                def delete_pasted_text(idx):
                    st.session_state.pasted_texts.pop(idx)

                for i, full_text in enumerate(st.session_state.pasted_texts):
                    preview = " ".join(full_text.split()[:6]) + ("..." if len(full_text.split()) > 6 else "")
                    c1, c2 = st.columns([9, 1])
                    with c1:
                        st.markdown(f"<div class='link-pill'>{preview}</div>", unsafe_allow_html=True)
                    with c2:
                        st.button("❌", key=f"del_text_{i}", on_click=delete_pasted_text, args=(i,))

        else:
            st.info("Podcaster will research your topic and generate content automatically.")
            links = []
            pasted_texts = []
    st.markdown("<div style='margin-top:35px;'></div>", unsafe_allow_html=True)
    with st.container():
        st.markdown(
            "<span style='font-size:1.25rem; font-weight:700; display:flex; align-items:center;'>"
            "<img src='https://img.icons8.com/?size=45&id=zQOo2lqkRswL&format=png&color=000000' style='margin-right:7px; margin-bottom:-7px;'/> Customize Podcast</span>",
            unsafe_allow_html=True
        )
        if "num_episodes" not in st.session_state:
            st.session_state.num_episodes = 1

        def increment_episodes():
            if st.session_state.num_episodes < 5:
                st.session_state.num_episodes += 1

        def decrement_episodes():
            if st.session_state.num_episodes > 1:
                st.session_state.num_episodes -= 1

        col_minus, col_count, col_plus, col_label, col_slider, col_tone = st.columns([1,3,1,3,4, 5], gap="small",vertical_alignment="center")
        with col_minus:
            st.button("➖", on_click=decrement_episodes, key="minus_btn", help="Decrease", type="secondary")
        with col_count:
            st.markdown(
                f"<span style='font-size:1.1rem; font-weight:600; margin-left:10px;'>Count of Episodes: {st.session_state.num_episodes}</span>"
                "</div>", unsafe_allow_html=True)
        with col_plus:
            st.button("➕", on_click=increment_episodes, key="plus_btn", help="Increase", type="secondary")

        with col_label:
            st.markdown(
                "<span style='font-size:1rem; font-weight:600; margin-left:10px;'>Episode Duration (minutes) :</span>",
                unsafe_allow_html=True
            )

        with col_slider:
            dur = st.slider(
                "Episode Duration (minutes)",
                1, 10, 3, step=1,
                key="episode_duration",
                label_visibility="collapsed"
            )

        with col_tone:
            tone = st.selectbox(
                "**Select Episode Tone**",
                constant.episode_tones,
                index=0,
                key="episode_tone"
            )
        st.markdown("<div style='margin-top:35px;'></div>", unsafe_allow_html=True)
        st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
        submitted = st.button("🎬 Generate Podcast", use_container_width=True)

    if submitted:
        if not topic:
            st.error("Please provide a podcast topic.")
        elif not topic_valid:
            st.error("Please change the topic to remove profanity.")
        elif (content_mode == "Use my own content") and not (st.session_state.links or st.session_state.pasted_texts):
            st.error("Provide at least links or some supporting text.")
        else:
            # Build JSON output
            mode = "user" if content_mode == "Use my own content" else "researcher"
            user_content = {
                "content": st.session_state.pasted_texts if mode == "user" else [],
                "links": st.session_state.links if mode == "user" else []
            }
            episode_configs = {
                "episode_count": st.session_state.num_episodes,
                "min_episode_length": dur,
                "tone": st.session_state.episode_tone
            }

            speaker_details = []
            for sp in selected_speakers:
                profile = constant.SPEAKER_PROFILES.get(sp, {"voice": "Unknown"})
                speaker_details.append({
                    "speaker_name": sp,
                    "is_host": sp == st.session_state["host_radio"],
                    "speaker_voice": profile["voice"],
                    "speaker_tone": speaker_tones[sp]
                })

            final_json = {
                "topic": topic,
                "scraper_mode": mode,
                "user_content": user_content,
                "episode_configs": episode_configs,
                "speaker_details": speaker_details
            }
            print(final_json)
            # Use your function to generate episode WAV metadata

            with st.spinner('Generating podcast episodes...'):
                orchestrator = Orchestrator()
                final_output = asyncio.run(orchestrator.generate_podcast(PodcasterInput(**final_json)))
                # final_output = dummy(final_json)

            episode_outputs = final_output.get('tts_output_path', [])
            if len(episode_outputs) == 0:
                st.error(final_output.get('error_message', 'Failed to generate podcast episodes.'))
            else : 
                st.success("Podcast generated! See your episodes below.")

            # episode_outputs = dummy(final_json)

            st.markdown("### 📂 Episodes")
            for epi in episode_outputs:
                st.markdown(f"**{epi['episode_name']}**")
                st.audio(epi["episode_path"], format="audio/wav")

