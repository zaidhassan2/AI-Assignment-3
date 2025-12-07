import streamlit as st
import librosa
import numpy as np
import joblib
import os
from styles import apply_custom_styles

st.set_page_config(page_title="Audio Deepfake Detection",  layout="wide")
apply_custom_styles()

st.markdown("""
    <div style="text-align: center; padding-bottom: 20px;">
        <h1 class="animate-fade-in"> Audio Deepfake Detection</h1>
        <p style="color: #cccccc;">Upload an audio file to detect if it's <b>Bonafide (Real)</b> or <b>Deepfake (Spoofed)</b>.</p>
    </div>
""", unsafe_allow_html=True)

# Load Models
@st.cache_resource
def load_models():
    models = {}
    model_dir = "Trained Models/Urdu Deepfake Audio Detection/"
    # Ensure directory exists to avoid hard crash if path is wrong
    if not os.path.exists(model_dir):
         return None
         
    try:
        models['SVM'] = joblib.load(os.path.join(model_dir, "model_svm.pkl"))
        models['Logistic Regression'] = joblib.load(os.path.join(model_dir, "model_logistic_regression.pkl"))
        models['Perceptron'] = joblib.load(os.path.join(model_dir, "model_perceptron.pkl"))
        models['DNN'] = joblib.load(os.path.join(model_dir, "model_dnn.pkl"))
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None
    return models

models = load_models()

if models is None:
    st.error("Model files not found. Please ensure the 'Trained Models/Urdu Deepfake Audio Detection/' directory contains the required .pkl files.")
    st.stop()

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.subheader("Configuration")
    selected_model_name = st.selectbox("Select Model", list(models.keys()))
    selected_model = models[selected_model_name]
    
    uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])
    st.markdown('</div>', unsafe_allow_html=True)

def extract_features(audio_path):
    try:
        # Load audio (3 seconds fixed duration)
        y, sr = librosa.load(audio_path, sr=22050, duration=3.0)
        
        # Pad if shorter than 3 seconds
        expected_length = 22050 * 3
        if len(y) < expected_length:
            y = np.pad(y, (0, expected_length - len(y)))
        else:
            y = y[:expected_length]
            
        # Extract MFCCs
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        mfcc = np.mean(mfcc.T, axis=0)
        return mfcc
    except Exception as e:
        st.error(f"Error processing audio: {e}")
        return None

with col2:
    if uploaded_file is not None:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.subheader("Analysis")
        st.audio(uploaded_file, format='audio/wav')
        
        if st.button("Analyze Audio"):
            with st.spinner('Extracting features and analyzing...'):
                # Save temp file
                with open("temp_audio.wav", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Extract features
                features = extract_features("temp_audio.wav")
                
                if features is not None:
                    # Reshape for prediction
                    features = features.reshape(1, -1)
                    
                    # Predict
                    prediction = selected_model.predict(features)[0]
                    
                    # Get probability if available
                    confidence = 0.0
                    if hasattr(selected_model, "predict_proba"):
                        try:
                            proba = selected_model.predict_proba(features)[0]
                            confidence = np.max(proba) * 100
                        except:
                            pass
                    elif hasattr(selected_model, "decision_function"):
                        try:
                            # Normalize decision function roughly for display if needed, or just ignore
                            confidence = 0.0 
                        except:
                            pass

                    # Display Result
                    # Logic: 0 = Bonafide, 1 = Deepfake (Standard convention, adjusting if needed based on user feedback)
                    # If prediction is string, use it directly.
                    
                    is_deepfake = False
                    result_text = ""
                    
                    if isinstance(prediction, str):
                        result_text = prediction
                        if "fake" in result_text.lower() or "spoof" in result_text.lower():
                            is_deepfake = True
                    else:
                        # Numeric prediction
                        if prediction == 1:
                            result_text = "Deepfake (Spoofed)"
                            is_deepfake = True
                        else:
                            result_text = "Bonafide (Real)"
                            is_deepfake = False

                    st.markdown("---")
                    
                    if is_deepfake:
                        st.markdown(f"""
                            <div class="result-card-error">
                                <h2>⚠️ DETECTED: {result_text.upper()}</h2>
                                <p>The model has flagged this audio as potentially manipulated.</p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="result-card-success">
                                <h2>✅ RESULT: {result_text.upper()}</h2>
                                <p>The model has classified this audio as authentic.</p>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    if confidence > 0:
                        st.markdown(f"""
                            <div style="margin-top: 20px;">
                                <p>Confidence Score</p>
                                <div style="background-color: #333; border-radius: 10px; height: 20px; width: 100%;">
                                    <div style="background-color: {'#ff0055' if is_deepfake else '#00ff80'}; width: {confidence}%; height: 100%; border-radius: 10px;"></div>
                                </div>
                                <p style="text-align: right; font-size: 0.8rem;">{confidence:.2f}%</p>
                            </div>
                        """, unsafe_allow_html=True)

