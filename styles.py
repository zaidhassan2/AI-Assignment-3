import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@300;400;700&display=swap');

        /* Global Variables */
        :root {
            --primary-color: #00f2ff; /* Cyan Neon */
            --secondary-color: #bc13fe; /* Purple Neon */
            --bg-color: #0e1117; /* Dark Background */
            --text-color: #ffffff;
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
        }

        /* General Body Styling */
        .stApp {
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(188, 19, 254, 0.1) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(0, 242, 255, 0.1) 0%, transparent 20%);
            background-attachment: fixed;
            font-family: 'Roboto', sans-serif;
            color: var(--text-color);
        }

        /* Headings */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Orbitron', sans-serif;
            color: var(--text-color);
            text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
        }
        
        h1 {
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem !important;
            padding-bottom: 1rem;
        }

        /* Glassmorphism Containers (Static) */
        .glass-container {
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        }

        /* Feature Card Containers (Interactive feel for Home page) */
        .feature-card-container {
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border);
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .feature-card-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(0, 242, 255, 0.2);
            border-color: var(--primary-color);
        }
        
        /* Style Streamlit Page Links to look like buttons/cards */
        .stPageLink > a {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        
        .stPageLink > a:hover {
            background: transparent !important;
        }
        
        /* Make the label inside page link look like a header */
        .stPageLink p {
            font-family: 'Orbitron', sans-serif !important;
            font-size: 1.5rem !important;
            font-weight: bold !important;
            text-align: center !important;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Custom Buttons */
        .stButton > button {
            background: linear-gradient(45deg, var(--secondary-color), var(--primary-color));
            color: white;
            border: none;
            border-radius: 25px;
            padding: 10px 25px;
            font-family: 'Orbitron', sans-serif;
            font-weight: bold;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 0 0 15px rgba(188, 19, 254, 0.5);
        }

        .stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 25px rgba(0, 242, 255, 0.8);
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: rgba(14, 17, 23, 0.95);
            border-right: 1px solid var(--glass-border);
        }

        /* Inputs and Selectboxes */
        .stTextInput > div > div > input, .stSelectbox > div > div > div {
            background-color: rgba(255, 255, 255, 0.05);
            color: white;
            border: 1px solid var(--glass-border);
            border-radius: 10px;
        }

        .stTextInput > div > div > input:focus, .stSelectbox > div > div > div:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 10px rgba(0, 242, 255, 0.3);
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .animate-fade-in {
            animation: fadeIn 0.8s ease-out forwards;
        }
        
        /* Custom Classes for specific elements */
        .feature-card {
            text-align: center;
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 10px;
        }

        .result-card-success {
            background: rgba(0, 255, 128, 0.1);
            border: 1px solid #00ff80;
            color: #00ff80;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            font-family: 'Orbitron', sans-serif;
            animation: fadeIn 0.5s ease-out;
        }

        .result-card-error {
            background: rgba(255, 0, 85, 0.1);
            border: 1px solid #ff0055;
            color: #ff0055;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            font-family: 'Orbitron', sans-serif;
            animation: fadeIn 0.5s ease-out;
        }

        </style>
    """, unsafe_allow_html=True)

def card(title, content, icon="✨"):
    st.markdown(f"""
        <div class="glass-container animate-fade-in feature-card">
            <div class="feature-icon">{icon}</div>
            <h3>{title}</h3>
            <p>{content}</p>
        </div>
    """, unsafe_allow_html=True)
