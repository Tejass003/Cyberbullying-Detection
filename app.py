import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
from predict_function import predict_cyberbullying

# Page configuration
st.set_page_config(
    page_title="Cyberbullying Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Main title styling */
    .main-title {
        text-align: center;
        color: #1e3a8a;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    /* Result card styling */
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 2rem 0;
        text-align: center;
    }

    .result-safe {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }

    .result-danger {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
    }

    .result-label {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .confidence-text {
        color: white;
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }

    /* Info boxes */
    .info-box {
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }

    /* Sidebar styling */
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e3a8a;
        margin-bottom: 1rem;
    }

    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #64748b;
        font-size: 0.9rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 3rem;
    }

    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animated {
        animation: fadeIn 0.6s ease-out;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Header section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="main-title">🛡️ Cyberbullying Detection System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Advanced AI-powered content safety analysis</p>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.markdown('<p class="sidebar-header">📝 Message Analysis</p>', unsafe_allow_html=True)

    user_input = st.text_area(
        "Enter your text here:",
        height=200,
        placeholder="Type or paste the message you want to analyze...",
        help="Enter any text to check for potential cyberbullying content"
    )

    analyze = st.button("🔍 Analyze Message", use_container_width=True, type="primary")

    st.markdown("---")

    # Information section in sidebar
    with st.expander("ℹ️ About This Tool"):
        st.write("""
        This tool uses advanced Natural Language Processing to detect 
        potential cyberbullying content in text messages.

        **Features:**
        - Real-time analysis
        - Confidence scoring
        - Multi-language support
        - XLM-RoBERTa model
        """)

    with st.expander("📊 How to Interpret Results"):
        st.write("""
        - **Safe Content**: No cyberbullying detected
        - **Cyberbullying**: Potentially harmful content identified
        - **Confidence Score**: Model's certainty (0-100%)
        """)

# Main content area
if analyze:
    if user_input.strip():
        with st.spinner("🔄 Analyzing text..."):
            label, confidence, bully_prob = predict_cyberbullying(user_input)

        # Results section with custom styling
        st.markdown('<div class="animated">', unsafe_allow_html=True)

        # Create result display
        if label == "CYBERBULLYING":
            result_class = "result-danger"
            icon = "🚫"
            result_text = "CYBERBULLYING DETECTED"
        else:
            result_class = "result-safe"
            icon = "✅"
            result_text = "SAFE CONTENT"

        # Display result card
        st.markdown(f"""
            <div class="result-card {result_class}">
                <div class="result-label">{icon} {result_text}</div>
                <div class="confidence-text">Confidence: {confidence:.2f}%</div>
            </div>
        """, unsafe_allow_html=True)

        # Detailed metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Prediction",
                value=label,
                delta="High Risk" if label == "CYBERBULLYING" else "Low Risk"
            )

        with col2:
            st.metric(
                label="Confidence Score",
                value=f"{confidence:.1f}%"
            )

        with col3:
            st.metric(
                label="Bullying Probability",
                value=f"{bully_prob:.1f}%"
            )

        # Progress bar
        st.markdown("### Analysis Breakdown")
        st.progress(float(bully_prob) / 100)
        st.caption(f"Cyberbullying probability: {bully_prob:.2f}%")

        # Additional context
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        if label == "CYBERBULLYING":
            st.warning(
                "⚠️ **Action Recommended**: This message contains potential cyberbullying content. Consider reviewing the context and taking appropriate action.")
        else:
            st.info("✨ **All Clear**: No concerning content detected. The message appears to be safe.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("⚠️ Please enter some text to analyze.")
else:
    # Welcome screen when no analysis has been run
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class="info-box" style="text-align: center; border-left: none; border: 2px solid #3b82f6;">
                <h3>👋 Welcome!</h3>
                <p>Enter a message in the sidebar and click "Analyze Message" to begin.</p>
                <p style="margin-top: 1rem;">Our AI model will analyze the text and provide instant feedback on potential cyberbullying content.</p>
            </div>
        """, unsafe_allow_html=True)

        # Feature highlights
        st.markdown("### ✨ Key Features")

        feature_col1, feature_col2, feature_col3 = st.columns(3)

        with feature_col1:
            st.markdown("""
                <div style="text-align: center; padding: 1rem;">
                    <h2>⚡</h2>
                    <h4>Fast Analysis</h4>
                    <p>Get results in seconds</p>
                </div>
            """, unsafe_allow_html=True)

        with feature_col2:
            st.markdown("""
                <div style="text-align: center; padding: 1rem;">
                    <h2>🎯</h2>
                    <h4>Accurate Detection</h4>
                    <p>Powered by XLM-RoBERTa</p>
                </div>
            """, unsafe_allow_html=True)

        with feature_col3:
            st.markdown("""
                <div style="text-align: center; padding: 1rem;">
                    <h2>🌐</h2>
                    <h4>Multi-Language</h4>
                    <p>Supports multiple languages</p>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div class="footer">
        <p><strong>Cyberbullying Detection System</strong></p>
        <p>Powered by XLM-RoBERTa | Built with Streamlit & PyTorch</p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem;">
            This tool is designed to assist in content moderation and should be used alongside human judgment.
        </p>
    </div>
""", unsafe_allow_html=True)