"""
Botpress Chatbot Integration for Crop Disease Prediction System.

This module provides a support bot interface using Botpress webchat
to assist users with questions about disease identification, treatment,
and using the application.
"""

import streamlit as st
import streamlit.components.v1 as components


# Botpress configuration
CONFIG_URL = "https://files.bpcontent.cloud/2025/12/31/05/20251231050750-T56DJWI9.json"


def render_support_bot():
    """
    Render the Botpress support bot interface.
    
    This function creates an embedded chatbot that can:
    - Answer questions about crop diseases
    - Provide guidance on using the application
    - Offer treatment recommendations
    - Assist with troubleshooting
    """
    st.title("🤖 Support Bot")
    
    st.markdown("""
    ### Welcome to the Crop Disease Support Agent
    
    Ask me anything about:
    - 🌾 **Rice diseases**: Bacterial Blight, Blast, Brown Spot
    - 🫘 **Black Gram diseases**: Anthracnose, Yellow Mosaic, Powdery Mildew, Leaf Crinkle
    - 🫘 **Lentil diseases**: Ascochyta Blight, Rust, Powdery Mildew
    - 🔍 How to use the prediction system
    - 💊 Treatment recommendations and disease management
    - 📸 Tips for capturing good leaf images
    - 🌱 Crop management and prevention strategies
    - ❓ General agricultural questions
    """)
    
    st.markdown("---")
    
    # Embed Botpress webchat using direct shareable link
    botpress_url = f"https://cdn.botpress.cloud/webchat/v3.5/shareable.html?configUrl={CONFIG_URL}"
    
    botpress_html = f"""
    <iframe 
        src="{botpress_url}"
        style="width: 100%; height: 650px; border: none; border-radius: 10px;"
        allow="microphone; camera"
    ></iframe>
    """
    
    components.html(botpress_html, height=700, scrolling=False)


def get_bot_training_data():
    """
    Get sample training data for the Botpress bot.
    
    Returns:
        dict: Sample Q&A pairs for bot training
    """
    return {
        "disease_identification": [
            {
                "question": "What is Bacterial Blight?",
                "answer": "Bacterial Blight is a serious rice disease caused by Xanthomonas oryzae. "
                         "It appears as water-soaked lesions on leaves that turn yellow and eventually "
                         "brown, often causing wilting."
            },
            {
                "question": "What is Blast disease?",
                "answer": "Blast is caused by the fungus Magnaporthe oryzae. It creates diamond-shaped "
                         "lesions with gray centers and brown margins on rice leaves. It's one of the "
                         "most destructive rice diseases worldwide."
            },
            {
                "question": "What is Brown Spot?",
                "answer": "Brown Spot is caused by Bipolaris oryzae fungus. It appears as circular or "
                         "oval brown spots on leaves and grains, potentially reducing yield and grain quality."
            }
        ],
        "treatment": [
            {
                "question": "How do I treat Bacterial Blight?",
                "answer": "1. Use resistant varieties\n2. Apply copper-based bactericides\n"
                         "3. Avoid excessive nitrogen fertilizer\n4. Maintain proper water management\n"
                         "5. Remove and destroy infected plants"
            },
            {
                "question": "How do I treat Blast?",
                "answer": "1. Use resistant rice varieties\n2. Apply fungicides like tricyclazole\n"
                         "3. Maintain balanced fertilization\n4. Avoid water stress\n"
                         "5. Practice crop rotation"
            }
        ],
        "usage": [
            {
                "question": "How do I use the prediction system?",
                "answer": "1. Navigate to 'Upload & Predict' page\n2. Upload clear images of rice leaves\n"
                         "3. Click 'Analyze Images'\n4. Review the prediction results with confidence scores\n"
                         "5. Read treatment recommendations"
            },
            {
                "question": "What makes a good image for prediction?",
                "answer": "For best results:\n- Use well-lit images\n- Ensure diseased areas are clearly visible\n"
                         "- Avoid blurry photos\n- Show individual leaves or small groups\n"
                         "- Use JPG or PNG format"
            }
        ]
    }


if __name__ == "__main__":
    # Standalone testing
    st.set_page_config(
        page_title="Support Bot - Crop Disease Prediction",
        page_icon="🤖",
        layout="wide"
    )
    render_support_bot()
