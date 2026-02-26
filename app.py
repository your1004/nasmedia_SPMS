import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="나스미디어 Revenue Intelligence v6",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS: Streamlit 기본 여백/헤더 제거
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

html_file = Path(__file__).parent / "nasmedia_v6_4.html"

if html_file.exists():
    html_content = html_file.read_text(encoding="utf-8")
    components.html(html_content, height=900, scrolling=True)
else:
    st.error("HTML 파일을 찾을 수 없습니다: nasmedia_v6_4.html")
