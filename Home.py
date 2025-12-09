import streamlit as st
from styles import apply_custom_styles, card

st.set_page_config(
    page_title="AI Detection Hub",
    layout="wide"
)

# Apply global styles
apply_custom_styles()

# Hero Section
st.markdown("""
    <div style="text-align: center; padding: 50px 0;">
        <h1 class="animate-fade-in">AI Detection Hub</h1>
        <p class="animate-fade-in" style="font-size: 1.2rem; color: #cccccc; max-width: 800px; margin: 0 auto;">
            Experience the future of AI forensics. Detect Deepfakes and Predict Software Defects with state-of-the-art machine learning models.
        </p>
    </div>
""", unsafe_allow_html=True)

# Features Grid
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="feature-card-container">', unsafe_allow_html=True)
    st.page_link("pages/Audio_Deepfake.py", label="Audio Deepfake Detection", use_container_width=True)
    st.markdown("""
        <p style="text-align: center; color: #cccccc; margin-top: -10px; padding: 0 20px 20px 20px;">
            Analyze audio files to distinguish between <b>Bonafide (Real)</b> and <b>Deepfake (Spoofed)</b> content.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="feature-card-container">', unsafe_allow_html=True)
    st.page_link("pages/Defect_Prediction.py", label="Software Defect Prediction", use_container_width=True)
    st.markdown("""
        <p style="text-align: center; color: #cccccc; margin-top: -10px; padding: 0 20px 20px 20px;">
            Leverage ML to predict software bugs and classify them based on feature vectors.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <small>Select a module from the sidebar or click a card above to begin.</small>
    </div>
""", unsafe_allow_html=True)

st.sidebar.success("Select a demo above.")
