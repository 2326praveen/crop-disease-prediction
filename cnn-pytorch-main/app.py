"""
Streamlit App for Crop Disease Prediction System.

REFACTORED following SOLID principles:
- SRP: Separated UI components into focused functions
- OCP: Easy to extend with new pages without modifying existing code
- DIP: Depends on abstractions (Auth, Predictor services)

This application provides:
- User authentication (login/register)
- Image upload functionality
- Disease prediction using trained CNN model
- Results visualization with confidence scores
"""

import streamlit as st
from pathlib import Path
import time

from src.auth import Auth
from src.predictor import Predictor


# =============================================================================
# CONFIGURATION (SRP: Separate configuration from logic)
# =============================================================================

def configure_page():
    """
    Configure page settings.
    
    SRP: Only handles page configuration.
    OCP: Can extend with new config without modifying other parts.
    """
    st.set_page_config(
        page_title="Crop Disease Prediction",
        page_icon="🌾",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def apply_custom_css():
    """
    Apply custom CSS styles.
    
    SRP: Only handles styling.
    OCP: Can extend with new styles without modifying logic.
    """
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
        }
        .prediction-box {
            padding: 1.5rem;
            border-radius: 10px;
            background-color: #f0f2f6;
            margin: 1rem 0;
        }
        .success-box {
            padding: 1rem;
            border-radius: 5px;
            background-color: #d4edda;
            border-left: 5px solid #28a745;
            margin: 1rem 0;
        }
        .warning-box {
            padding: 1rem;
            border-radius: 5px;
            background-color: #fff3cd;
            border-left: 5px solid #ffc107;
            margin: 1rem 0;
        }
        </style>
        """, unsafe_allow_html=True)


# =============================================================================
# NAVIGATION COMPONENT (SRP: Separate navigation rendering)
# =============================================================================

class NavigationComponent:
    """
    Navigation sidebar component.
    
    SOLID Principles:
    - SRP: Only responsible for rendering navigation
    - OCP: Can extend with new pages easily
    - DIP: Depends on Auth abstraction
    """
    
    def __init__(self, auth: Auth):
        """
        Initialize with auth service.
        
        DIP: Depends on Auth abstraction, not concrete implementation.
        """
        self.auth = auth
    
    def render(self) -> str:
        """
        Render navigation sidebar and return selected page.
        
        Returns:
            str: Selected page name
        """
        with st.sidebar:
            st.title("🌾 Navigation")
            st.write(f"**Logged in as:** {self.auth.get_username()}")
            st.markdown("---")
            
            page = st.radio(
                "Go to",
                ["Home", "Upload & Predict", "About"],
                label_visibility="collapsed"
            )
            
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                self.auth.logout()
                st.rerun()
        
        return page


# =============================================================================
# PAGE COMPONENTS (SRP: Each page has its own responsibility)
# =============================================================================

class HomePageComponent:
    """
    Home page component.
    
    SOLID Principles:
    - SRP: Only responsible for rendering home page
    - OCP: Can extend with new sections without modifying existing code
    """
    
    def render(self, username: str):
        """Render home page."""
        st.title("🌾 Welcome to Crop Disease Prediction System")
        st.markdown(f"### Hello, **{username}**!")
        
        self._render_intro()
        self._render_features()
        self._render_diseases()
        st.markdown("---")
        self._render_call_to_action()
        self._render_stats()
    
    def _render_intro(self):
        """Render introduction section."""
        st.markdown("""
        This application helps farmers and agricultural professionals identify rice leaf diseases 
        using advanced deep learning technology.
        """)
    
    def _render_features(self):
        """Render features section."""
        st.markdown("### 🎯 Features")
        st.markdown("""
        - **🔐 Secure Authentication**: Login to access the prediction system
        - **📤 Easy Upload**: Upload rice leaf images for analysis
        - **🤖 AI-Powered Prediction**: Get instant disease predictions
        - **📊 Detailed Results**: View confidence scores and disease information
        - **💡 Treatment Advice**: Get recommendations for disease management
        """)
    
    def _render_diseases(self):
        """Render detectable diseases section."""
        st.markdown("### 🦠 Detectable Diseases")
        st.markdown("Our model can identify the following rice diseases:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### 🔴 Bacterial Blight
            Water-soaked lesions on leaves causing wilting and yellowing.
            """)
        
        with col2:
            st.markdown("""
            #### 🔵 Blast
            Diamond-shaped lesions with gray centers and brown margins.
            """)
        
        with col3:
            st.markdown("""
            #### 🟤 Brown Spot
            Circular or oval brown spots on leaves and grains.
            """)
    
    def _render_call_to_action(self):
        """Render call to action."""
        st.info("👈 Navigate to **Upload & Predict** to start analyzing your rice leaf images!")
    
    def _render_stats(self):
        """Render statistics section."""
        st.markdown("### 📈 Model Performance")
        col1, col2, col3 = st.columns(3)
        col1.metric("Model Accuracy", "66.7%", "")
        col2.metric("Classes", "3", "")
        col3.metric("Parameters", "295K", "")


class PredictionPageComponent:
    """
    Prediction page component.
    
    SOLID Principles:
    - SRP: Only responsible for prediction page
    - DIP: Depends on Predictor abstraction
    - OCP: Can extend with new features without modifying existing code
    """
    
    def __init__(self, predictor: Predictor):
        """
        Initialize with predictor service.
        
        DIP: Depends on Predictor abstraction.
        """
        self.predictor = predictor
    
    def render(self):
        """Render prediction page."""
        st.title("📤 Upload & Predict")
        st.markdown("Upload rice leaf images to detect diseases")
        
        self._render_upload_section()
    
    def _render_upload_section(self):
        """Render upload section."""
        st.markdown("### 📁 Upload Images")
        uploaded_files = st.file_uploader(
            "Choose rice leaf images (JPG, JPEG, PNG)",
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            help="You can upload multiple images at once"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")
            
            if st.button("🔍 Analyze Images", type="primary", use_container_width=True):
                self._analyze_images(uploaded_files)
        else:
            self._render_tips()
    
    def _render_tips(self):
        """Render tips section."""
        st.info("👆 Please upload one or more images to begin analysis")
        st.markdown("---")
        st.markdown("### 💡 Tips for Best Results")
        st.markdown("""
        - Use clear, well-lit images of rice leaves
        - Ensure the diseased area is visible
        - Avoid blurry or low-quality images
        - Images should show individual leaves or small groups
        """)
    
    def _analyze_images(self, uploaded_files):
        """
        Analyze uploaded images.
        
        SRP: Delegates to prediction service and result renderer.
        """
        st.markdown("---")
        st.markdown("### 🔬 Analysis Results")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = []
        for idx, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Analyzing {uploaded_file.name}...")
            progress_bar.progress((idx + 1) / len(uploaded_files))
            
            try:
                result = self.predictor.predict_image(uploaded_file)
                results.append({'file': uploaded_file, 'result': result})
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")
        
        status_text.empty()
        progress_bar.empty()
        
        if results:
            st.success("✅ Analysis complete!")
            for item in results:
                self._display_result(item['file'], item['result'])
    
    def _display_result(self, uploaded_file, result):
        """
        Display individual prediction result.
        
        SRP: Only responsible for rendering results.
        """
        st.markdown("---")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)
        
        with col2:
            predicted_class = result['predicted_class']
            confidence = result['confidence']
            
            # Prediction header
            if confidence > 50:
                st.markdown(f"### ✅ Detected: **{predicted_class}**")
            else:
                st.markdown(f"### ⚠️ Possible: **{predicted_class}**")
            
            # Confidence score
            st.markdown(f"**Confidence:** {confidence:.2f}%")
            st.progress(confidence / 100)
            
            # All probabilities
            with st.expander("📊 View All Class Probabilities"):
                for class_name, prob in result['all_probabilities'].items():
                    st.write(f"**{class_name}:** {prob:.2f}%")
                    st.progress(prob / 100)
            
            # Disease information
            disease_info = self.predictor.get_disease_info(predicted_class)
            
            st.markdown("### 📖 Disease Information")
            st.markdown(f"**Description:** {disease_info['description']}")
            st.markdown(f"**Symptoms:** {disease_info['symptoms']}")
            
            st.markdown("### 💊 Treatment Recommendations")
            st.markdown(disease_info['treatment'])
            
            # Warning if low confidence
            if confidence < 50:
                st.warning("⚠️ Low confidence prediction. Consider uploading a clearer image or consulting an expert.")


class AboutPageComponent:
    """
    About page component.
    
    SOLID Principles:
    - SRP: Only responsible for rendering about page
    - OCP: Can extend with new sections without modifying existing code
    """
    
    def render(self):
        """Render about page."""
        st.title("ℹ️ About")
        
        self._render_intro()
        self._render_model_details()
        self._render_how_it_works()
        self._render_tech_stack()
        self._render_disclaimer()
        self._render_contact()
        self._render_stats()
    
    def _render_intro(self):
        """Render introduction."""
        st.markdown("""
        ### 🌾 Crop Disease Prediction System
        
        This application uses a Convolutional Neural Network (CNN) trained on rice leaf images 
        to identify common diseases affecting rice crops.
        """)
    
    def _render_model_details(self):
        """Render model details."""
        st.markdown("""
        #### 🤖 Model Details
        
        - **Architecture:** Custom CNN with 295,459 parameters
        - **Training Dataset:** Rice leaf disease images (3 classes)
        - **Classes:** Bacterial Blight, Blast, Brown Spot
        - **Accuracy:** 66.7% on validation set
        - **Training:** 30 epochs with Adam optimizer
        """)
    
    def _render_how_it_works(self):
        """Render how it works section."""
        st.markdown("""
        #### 🎓 How It Works
        
        1. **Upload:** User uploads rice leaf images
        2. **Preprocessing:** Images are resized and normalized
        3. **Prediction:** CNN model analyzes the image
        4. **Results:** System displays predicted disease with confidence scores
        5. **Information:** Treatment recommendations are provided
        """)
    
    def _render_tech_stack(self):
        """Render technology stack."""
        st.markdown("""
        #### 🔬 Technology Stack
        
        - **Deep Learning:** PyTorch
        - **Web Interface:** Streamlit
        - **Database:** SQLite
        - **Image Processing:** PIL, torchvision
        """)
    
    def _render_disclaimer(self):
        """Render disclaimer."""
        st.markdown("""
        #### 📝 Disclaimer
        
        This tool is designed to assist in disease identification but should not replace 
        professional agricultural advice. Always consult with agricultural experts for 
        proper diagnosis and treatment.
        """)
    
    def _render_contact(self):
        """Render contact section."""
        st.markdown("""
        #### 📧 Contact
        
        For questions or feedback, please contact the development team.
        
        ---
        
        Made with ❤️ for farmers and agricultural professionals
        """)
    
    def _render_stats(self):
        """Render system stats."""
        st.markdown("### 📊 System Stats")
        col1, col2, col3 = st.columns(3)
        col1.metric("Version", "1.0.0")
        col2.metric("Model Size", "1.1 MB")
        col3.metric("Supported Formats", "JPG, PNG")


# =============================================================================
# MAIN APPLICATION (SRP: Coordinates components)
# =============================================================================

class Application:
    """
    Main application coordinator.
    
    SOLID Principles:
    - SRP: Only coordinates components, doesn't implement business logic
    - DIP: Depends on Auth and Predictor abstractions
    - OCP: New pages can be added without modifying this class structure
    """
    
    def __init__(self):
        """
        Initialize application.
        
        DIP: Initializes dependencies.
        """
        self.auth = Auth()
        self.predictor = None  # Lazy load predictor
    
    def run(self):
        """
        Run the application.
        
        SRP: Only handles application flow.
        """
        # Check authentication
        if not self.auth.is_logged_in():
            self.auth.login_page()
            return
        
        # Render navigation and get selected page
        nav = NavigationComponent(self.auth)
        page = nav.render()
        
        # Route to appropriate page (OCP: Easy to add new pages)
        if page == "Home":
            home_page = HomePageComponent()
            home_page.render(self.auth.get_username())
        
        elif page == "Upload & Predict":
            # Lazy load predictor
            if self.predictor is None:
                try:
                    if 'predictor' not in st.session_state:
                        with st.spinner("Loading model..."):
                            st.session_state.predictor = Predictor()
                    self.predictor = st.session_state.predictor
                except Exception as e:
                    st.error(f"Error loading model: {str(e)}")
                    st.info("Please ensure the trained model exists at `models/best_model.pth`")
                    return
            
            prediction_page = PredictionPageComponent(self.predictor)
            prediction_page.render()
        
        elif page == "About":
            about_page = AboutPageComponent()
            about_page.render()


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    """
    Application entry point.
    
    SRP: Only initializes and runs the application.
    """
    configure_page()
    apply_custom_css()
    
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
