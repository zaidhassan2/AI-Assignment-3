import streamlit as st
import joblib
import os
import re
import pandas as pd
import numpy as np
from styles import apply_custom_styles

st.set_page_config(page_title="Software Defect Prediction", page_icon="📝", layout="wide")
apply_custom_styles()

st.markdown("""
    <div style="text-align: center; padding-bottom: 20px;">
        <h1 class="animate-fade-in">📝 Software Defect Prediction</h1>
        <p style="color: #cccccc;">Enter a bug report to predict its defect tags (e.g., Bug, High Priority, UI).</p>
    </div>
""", unsafe_allow_html=True)

# Load Models and Vectorizer
@st.cache_resource
def load_resources():
    resources = {}
    model_dir = "Trained Models/Multi-Label Software Defect Prediction"
    
    if not os.path.exists(model_dir):
        return None

    try:
        # Load Models
        resources['SVM'] = joblib.load(os.path.join(model_dir, "text_model_svm.pkl"))
        resources['Logistic Regression'] = joblib.load(os.path.join(model_dir, "text_model_logistic.pkl"))
        resources['Perceptron'] = joblib.load(os.path.join(model_dir, "text_model_perceptron.pkl"))
        resources['DNN'] = joblib.load(os.path.join(model_dir, "text_model_dnn.pkl"))
        
        # Load Vectorizer and Labels
        resources['vectorizer'] = joblib.load(os.path.join(model_dir, "text_vectorizer.pkl"))
        resources['label_columns'] = joblib.load(os.path.join(model_dir, "text_label_columns.pkl"))
    except Exception as e:
        st.error(f"Error loading resources: {e}")
        return None
    
    return resources

resources = load_resources()

if resources is None:
    st.error("Model or vectorizer files not found. Please ensure the 'Trained Models/Multi-Label Software Defect Prediction' directory contains the required .pkl files.")
    st.stop()

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.subheader("Configuration")
    selected_model_name = st.selectbox("Select Model", ["SVM", "Logistic Regression", "Perceptron", "DNN"])
    selected_model = resources[selected_model_name]
    vectorizer = resources['vectorizer']
    label_columns = resources['label_columns']
    st.markdown('</div>', unsafe_allow_html=True)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text) # Remove punctuation
    return text

with col2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.subheader("Bug Report Analysis")
    bug_report = st.text_area("Enter Bug Report", height=150, placeholder="e.g., The system crashes when I click the save button...")
    
    if st.button("Predict Tags"):
        if not bug_report.strip():
            st.warning("Please enter a bug report.")
        else:
            with st.spinner('Analyzing text...'):
                # Preprocess
                cleaned_text = clean_text(bug_report)
                
                # Vectorize
                text_vector = vectorizer.transform([cleaned_text]).toarray()
                
                # Predict
                prediction = selected_model.predict(text_vector)
                
                # Handle prediction format
                if hasattr(prediction, "toarray"):
                    prediction = prediction.toarray()
                
                # Map prediction to labels
                predicted_tags = []
                if isinstance(prediction, np.ndarray) and prediction.ndim > 1:
                     prediction = prediction[0] # Get first sample
                
                for idx, val in enumerate(prediction):
                    if val == 1:
                        predicted_tags.append(label_columns[idx])
                
                # Display Results
                st.markdown("---")
                st.subheader("Prediction Results")
                
                if predicted_tags:
                    st.success("Defect Tags Detected")
                    
                    # Create HTML for badges
                    badges_html = ""
                    colors = ['#00f2ff', '#bc13fe', '#00ff80', '#ff0055', '#ffaa00']
                    for i, tag in enumerate(predicted_tags):
                        color = colors[i % len(colors)]
                        badges_html += f'<span style="background-color: {color}20; border: 1px solid {color}; color: {color}; padding: 5px 15px; border-radius: 20px; margin-right: 10px; margin-bottom: 10px; display: inline-block; font-family: \'Orbitron\', sans-serif; font-size: 0.9rem;">{tag}</span>'
                    
                    st.markdown(f"<div>{badges_html}</div>", unsafe_allow_html=True)
                else:
                    st.info("No specific defect type detected.")
    st.markdown('</div>', unsafe_allow_html=True)
