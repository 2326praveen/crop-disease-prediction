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
from datetime import datetime
import io

from src.auth import Auth
from src.predictor import Predictor
from bot_run import render_support_bot

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
    from reportlab.lib import colors
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


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


def get_disease_information(disease_name):
    """Get detailed disease information."""
    disease_data = {
        'Bacterialblight': {
            'description': 'Bacterial blight is a serious disease affecting rice crops caused by Xanthomonas oryzae bacteria.',
            'symptoms': 'Water-soaked lesions on leaves, wilting, yellowing, and eventual drying of leaves.',
            'treatment': 'Use resistant rice varieties, apply copper-based bactericides (Copper oxychloride), avoid excessive nitrogen fertilization, maintain proper water management, and remove infected plant debris.'
        },
        'Blast': {
            'description': 'Rice blast is caused by the fungal pathogen Magnaporthe oryzae and is one of the most destructive rice diseases worldwide.',
            'symptoms': 'Diamond-shaped lesions with gray or white centers and brown or reddish-brown margins on leaves, nodes, and panicles. Severe cases cause neck rot and empty grains.',
            'treatment': 'Apply fungicides such as Tricyclazole, Isoprothiolane, or Carbendazim. Use blast-resistant varieties, split nitrogen application, maintain proper plant spacing, and ensure good drainage.'
        },
        'Brownspot': {
            'description': 'Brown spot is a fungal disease caused by Bipolaris oryzae (Helminthosporium oryzae) that affects rice plants.',
            'symptoms': 'Circular to oval brown spots on leaves with gray or tan centers and brown margins. Spots may also appear on leaf sheaths and grains.',
            'treatment': 'Apply fungicides like Mancozeb, Propiconazole, or Carbendazim. Treat seeds with fungicide before planting, improve soil fertility (especially potassium), and remove infected plant debris.'
        }
    }
    return disease_data.get(disease_name, {
        'description': 'Disease information not available.',
        'symptoms': 'Please consult an agricultural expert for detailed symptoms.',
        'treatment': 'Please consult an agricultural expert for proper treatment recommendations.'
    })


def generate_pdf_report(results_data, username):
    """
    Generate a PDF report for prediction results.
    
    Args:
        results_data: List of dicts containing file info and prediction results
        username: Username of the current user
    
    Returns:
        BytesIO: PDF file in memory
    """
    if not PDF_AVAILABLE:
        return None
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c5aa0'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    story.append(Paragraph("🌾 Crop Disease Prediction Report", title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Report info
    report_info = [
        ["Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        ["User:", username],
        ["Total Images Analyzed:", str(len(results_data))]
    ]
    
    info_table = Table(report_info, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#555555')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.3 * inch))
    
    # Results for each image
    for idx, item in enumerate(results_data, 1):
        result = item['result']
        filename = item.get('filename', f'Image {idx}')
        
        # Section header
        story.append(Paragraph(f"Result #{idx}: {filename}", heading_style))
        
        # Prediction details
        predicted_class = result['predicted_class']
        confidence = result['confidence']
        
        prediction_data = [
            ["Predicted Disease:", predicted_class],
            ["Confidence:", f"{confidence:.2f}%"],
            ["Status:", "High Confidence" if confidence > 50 else "Low Confidence - Verify Needed"]
        ]
        
        pred_table = Table(prediction_data, colWidths=[2*inch, 4*inch])
        pred_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#555555')),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f5f5f5')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        story.append(pred_table)
        story.append(Spacer(1, 0.15 * inch))
        
        # All probabilities
        story.append(Paragraph("<b>Class Probabilities:</b>", styles['Normal']))
        story.append(Spacer(1, 0.05 * inch))
        
        prob_data = [["Class", "Probability"]]
        for class_name, prob in result['all_probabilities'].items():
            prob_data.append([class_name, f"{prob:.2f}%"])
        
        prob_table = Table(prob_data, colWidths=[3*inch, 2*inch])
        prob_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ]))
        story.append(prob_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Disease Information Section with better structure
        disease_info = get_disease_information(predicted_class)
        
        # Disease Info Box
        info_heading_style = ParagraphStyle(
            'InfoHeading',
            parent=styles['Heading3'],
            fontSize=14,
            textColor=colors.white,
            spaceAfter=0,
            spaceBefore=0,
            alignment=0
        )
        
        section_heading_style = ParagraphStyle(
            'SectionHeading',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#1f4788'),
            fontName='Helvetica-Bold',
            spaceAfter=6,
            spaceBefore=10
        )
        
        body_style = ParagraphStyle(
            'BodyText',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            leftIndent=15,
            rightIndent=10,
            spaceAfter=8
        )
        
        # Main heading with background
        heading_data = [[Paragraph("Disease Information & Treatment Recommendations", info_heading_style)]]
        heading_table = Table(heading_data, colWidths=[6.5*inch])
        heading_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ]))
        story.append(heading_table)
        
        # Create a bordered box for disease information
        info_data = [
            [Paragraph("📋 Description:", section_heading_style)],
            [Paragraph(disease_info['description'], body_style)],
            [Paragraph("🔍 Symptoms:", section_heading_style)],
            [Paragraph(disease_info['symptoms'], body_style)],
            [Paragraph("💊 Treatment & Remedy:", section_heading_style)],
            [Paragraph(disease_info['treatment'], body_style)]
        ]
        
        info_table = Table(info_data, colWidths=[6.5*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#2c5aa0')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.2 * inch))
        
        # Add page break between results (except for last one)
        if idx < len(results_data):
            story.append(Spacer(1, 0.3 * inch))
    
    # Footer
    story.append(Spacer(1, 0.5 * inch))
    footer_text = """<i>Note: This report is generated by an AI-powered system. 
    Please consult agricultural experts for professional diagnosis and treatment.</i>"""
    story.append(Paragraph(footer_text, styles['Italic']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


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
                ["Home", "Upload & Predict", "Support Bot", "About"],
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
        - **🤖 Support Bot**: 24/7 AI assistant to answer your questions
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
            
            # Store results in session state for PDF generation
            st.session_state['latest_results'] = [
                {
                    'filename': item['file'].name,
                    'result': item['result']
                }
                for item in results
            ]
            
            # PDF Download Button
            if PDF_AVAILABLE:
                try:
                    username = "User"
                    # Try to get actual username from session state
                    if 'username' in st.session_state:
                        username = st.session_state['username']
                    
                    pdf_buffer = generate_pdf_report(st.session_state['latest_results'], username)
                    if pdf_buffer:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        col1, col2, col3 = st.columns([1, 1, 1])
                        with col2:
                            st.download_button(
                                label="📥 Download PDF Report",
                                data=pdf_buffer,
                                file_name=f"crop_disease_report_{timestamp}.pdf",
                                mime="application/pdf",
                                type="primary",
                                use_container_width=True
                            )
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
            else:
                st.info("📦 Install 'reportlab' package to enable PDF downloads: pip install reportlab")
            
            st.markdown("---")
            
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


class SupportBotPageComponent:
    """
    Support Bot page component.
    
    SOLID Principles:
    - SRP: Only responsible for rendering support bot page
    - OCP: Can extend with new features without modifying existing code
    """
    
    def render(self):
        """Render support bot page."""
        render_support_bot()


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
        
        elif page == "Support Bot":
            support_bot_page = SupportBotPageComponent()
            support_bot_page.render()
        
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
