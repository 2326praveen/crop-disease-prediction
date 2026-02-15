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
from src.disease_remedies import DiseaseRemedyService, RemedyStep
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
        /* Professional White/Green Theme */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .main {
            padding: 2rem 3rem;
            background-color: #ffffff;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .stApp {
            background: linear-gradient(to bottom, #f8fffe 0%, #ffffff 100%);
        }
        
        /* Text Color Fix for Visibility */
        p, span, div, label {
            color: #212529 !important;
        }
        
        .stMarkdown {
            color: #212529;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #fafbfc;
            border-right: 1px solid #e1e4e8;
            box-shadow: 2px 0 10px rgba(0,0,0,0.02);
        }
        
        [data-testid="stSidebar"] h1 {
            color: #1b5e20;
            font-weight: 700;
            font-size: 1.5rem;
            padding: 0.5rem 0;
        }
        
        /* Button Styling */
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            border: none;
            font-weight: 600;
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(76, 175, 80, 0.2);
            letter-spacing: 0.3px;
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #45a049 0%, #388e3c 100%);
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
            transform: translateY(-1px);
        }
        
        .stButton>button:active {
            transform: translateY(0);
        }
        
        /* Card Boxes */
        .prediction-box {
            padding: 2rem;
            border-radius: 12px;
            background-color: #ffffff;
            margin: 1.5rem 0;
            border: 1px solid #e8f5e9;
            box-shadow: 0 2px 12px rgba(0,0,0,0.04);
            transition: box-shadow 0.3s ease;
        }
        
        .prediction-box:hover {
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }
        
        .success-box {
            padding: 1.2rem 1.5rem;
            border-radius: 10px;
            background-color: #f1fdf4;
            border: 1px solid #c3e6cb;
            border-left: 4px solid #28a745;
            margin: 1rem 0;
        }
        
        .warning-box {
            padding: 1.2rem 1.5rem;
            border-radius: 10px;
            background-color: #fffbf0;
            border: 1px solid #ffeaa7;
            border-left: 4px solid #ffc107;
            margin: 1rem 0;
        }
        
        /* Farm Assist Box */
        .farm-assist-box {
            background: linear-gradient(135deg, #f8fffe 0%, #ffffff 100%);
            padding: 1.2rem;
            border-radius: 12px;
            border: 2px solid #4CAF50;
            margin: 1rem 0;
            box-shadow: 0 4px 20px rgba(76, 175, 80, 0.15);
            max-height: 70vh;
            overflow-y: auto;
            overflow-x: hidden;
        }
        
        .farm-assist-box h3 {
            color: #1b5e20;
            font-weight: 700;
            font-size: 1.1rem;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 0.6rem;
            margin-bottom: 0.8rem;
        }
        
        .farm-assist-box .stButton>button {
            padding: 0.4rem 0.8rem;
            font-size: 0.85rem;
        }
        
        .farm-assist-box .stChatMessage {
            font-size: 0.88rem;
            padding: 0.7rem;
            margin: 0.5rem 0;
            border-radius: 8px;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        
        .farm-assist-box .stChatInput {
            margin-top: 0.5rem;
        }
        
        /* Custom scrollbar for chat box */
        .farm-assist-box::-webkit-scrollbar {
            width: 8px;
        }
        
        .farm-assist-box::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        .farm-assist-box::-webkit-scrollbar-thumb {
            background: #4CAF50;
            border-radius: 4px;
        }
        
        .farm-assist-box::-webkit-scrollbar-thumb:hover {
            background: #388e3c;
        }
        
        /* Typography */
        h1 {
            color: #1b5e20;
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 1rem;
            letter-spacing: -0.5px;
        }
        
        h2 {
            color: #2e7d32;
            font-weight: 600;
            font-size: 1.8rem;
            margin-top: 1.5rem;
        }
        
        h3 {
            color: #388e3c;
            font-weight: 600;
            font-size: 1.3rem;
        }
        
        /* Chat Messages */
        .stChatMessage {
            background-color: #ffffff;
            border: 1px solid #e8eaed;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        .stChatMessage p, .stChatMessage div, .stChatMessage span {
            color: #212529 !important;
        }
        
        .stChatMessage[data-testid="user-message"] {
            background: linear-gradient(135deg, #e8f5e9 0%, #f1f8f4 100%);
            border-color: #c8e6c9;
        }
        
        .stChatMessage[data-testid="user-message"] p,
        .stChatMessage[data-testid="user-message"] div,
        .stChatMessage[data-testid="user-message"] span {
            color: #212529 !important;
        }
        
        .stChatMessage[data-testid="assistant-message"] {
            background-color: #ffffff;
        }
        
        .stChatMessage[data-testid="assistant-message"] p,
        .stChatMessage[data-testid="assistant-message"] div,
        .stChatMessage[data-testid="assistant-message"] span {
            color: #212529 !important;
        }
        
        /* Progress Bars */
        .stProgress > div > div {
            background: linear-gradient(90deg, #66bb6a 0%, #4CAF50 100%);
            border-radius: 10px;
        }
        
        [data-testid="stProgress"] > div {
            background-color: #e8f5e9;
            border-radius: 10px;
        }
        
        /* Metrics */
        .stMetric {
            background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #e8f5e9;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }
        
        .stMetric label {
            color: #2e7d32 !important;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stMetric [data-testid="stMetricValue"] {
            color: #1b5e20;
            font-weight: 700;
        }
        
        /* Info/Warning/Success Boxes */
        .stInfo {
            background-color: #f3e5f5;
            border: 1px solid #ce93d8;
            border-left: 4px solid #9c27b0;
            border-radius: 8px;
            padding: 1rem 1.2rem;
        }
        
        .stInfo p, .stInfo div, .stInfo span {
            color: #4a148c !important;
        }
        
        .stSuccess {
            background-color: #e8f5e9;
            border: 1px solid #a5d6a7;
            border-left: 4px solid #4CAF50;
            border-radius: 8px;
        }
        
        .stSuccess p, .stSuccess div, .stSuccess span {
            color: #1b5e20 !important;
        }
        
        .stWarning {
            background-color: #fff8e1;
            border: 1px solid #ffe082;
            border-left: 4px solid #ffc107;
            border-radius: 8px;
        }
        
        .stWarning p, .stWarning div, .stWarning span {
            color: #f57f17 !important;
        }
        
        .stError {
            background-color: #ffebee;
            border: 1px solid #ef9a9a;
            border-left: 4px solid #f44336;
            border-radius: 8px;
        }
        
        .stError p, .stError div, .stError span {
            color: #b71c1c !important;
        }
        
        /* Dividers */
        hr {
            border: none;
            border-top: 2px solid #e8f5e9;
            margin: 2rem 0;
        }
        
        /* Keyframe animations */
        @keyframes pulse {
            0%, 100% {
                box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
            }
            50% {
                box-shadow: 0 6px 30px rgba(255, 107, 107, 0.6);
            }
        }
        
        /* File Uploader */
        [data-testid="stFileUploadDropzone"] {
            border: 3px dashed #7dd87d !important;
            border-radius: 16px !important;
            background: linear-gradient(135deg, #e8ffe8 0%, #f7fff7 100%) !important;
            padding: 2rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(125, 216, 125, 0.2) !important;
        }
        
        [data-testid="stFileUploadDropzone"]:hover {
            border-color: #51cf66 !important;
            background: linear-gradient(135deg, #d0ffd0 0%, #ecffe8 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(81, 207, 102, 0.25) !important;
        }
        
        [data-testid="stFileUploadDropzone"] p,
        [data-testid="stFileUploadDropzone"] span {
            color: #2f9e44 !important;
            font-weight: 700 !important;
            font-size: 1.15rem !important;
        }
        
        [data-testid="stFileUploadDropzone"] small {
            color: #2f9e44 !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }
        
        [data-testid="stFileUploadDropzone"] button {
            background: linear-gradient(135deg, #51cf66 0%, #37b24d 100%) !important;
            color: #ffffff !important;
            border: 2px solid #2f9e44 !important;
            padding: 1rem 3rem !important;
            border-radius: 12px !important;
            font-weight: 800 !important;
            font-size: 1.2rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            box-shadow: 0 6px 20px rgba(81, 207, 102, 0.4) !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
            margin: 1rem 0 !important;
            animation: pulse 2s ease-in-out infinite !important;
        }
        
        [data-testid="stFileUploadDropzone"] button:hover {
            background: linear-gradient(135deg, #40c057 0%, #2f9e44 100%) !important;
            transform: translateY(-3px) scale(1.05) !important;
            box-shadow: 0 8px 25px rgba(81, 207, 102, 0.5) !important;
            border-color: #2b8a3e !important;
        }
        
        [data-testid="stFileUploadDropzone"] button:active {
            transform: translateY(-1px) scale(1.02) !important;
            box-shadow: 0 4px 15px rgba(81, 207, 102, 0.3) !important;
        }
        
        [data-testid="stFileUploadDropzone"] svg {
            color: #51cf66 !important;
            width: 48px !important;
            height: 48px !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px 8px 0 0;
            padding: 0.8rem 1.5rem;
            font-weight: 600;
            color: #666;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #4CAF50;
            color: white;
            border-color: #4CAF50;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: #f8fffe;
            border: 1px solid #e8f5e9;
            border-radius: 8px;
            font-weight: 600;
            color: #2e7d32 !important;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: #e8f5e9;
        }
        
        .streamlit-expanderContent {
            background-color: #ffffff;
            color: #212529 !important;
        }
        
        .streamlit-expanderContent p,
        .streamlit-expanderContent div,
        .streamlit-expanderContent span {
            color: #212529 !important;
        }
        
        /* Input Fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            color: #212529 !important;
            background-color: #ffffff !important;
        }
        
        .stTextInput > div > div > input::placeholder,
        .stTextArea > div > div > textarea::placeholder {
            color: #6c757d !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
            color: #212529 !important;
            background-color: #ffffff !important;
        }
        
        .stTextInput label, .stTextArea label, .stSelectbox label, 
        .stMultiselect label, .stNumberInput label, .stFileUploader label {
            color: #212529 !important;
            font-weight: 500;
        }
        
        /* Password Input */
        input[type="password"] {
            color: #212529 !important;
            background-color: #ffffff !important;
        }
        
        /* Radio Buttons */
        [data-testid="stSidebar"] .stRadio > label {
            font-weight: 500;
            color: #2e7d32 !important;
        }
        
        [data-testid="stSidebar"] .stRadio label {
            color: #212529 !important;
        }
        
        [data-testid="stSidebar"] [data-baseweb="radio"] label {
            color: #212529 !important;
        }
        
        /* General text visibility */
        .stMarkdown p, .stMarkdown li, .stMarkdown span {
            color: #212529 !important;
        }
        
        .element-container p, .element-container span, .element-container div {
            color: #212529 !important;
        }
        
        /* All input elements */
        input, textarea, select {
            color: #212529 !important;
            background-color: #ffffff !important;
        }
        
        input::placeholder, textarea::placeholder {
            color: #6c757d !important;
        }
        
        /* Chat input placeholder */
        .stChatInput input::placeholder {
            color: #6c757d !important;
        }
        
        .stChatInput input {
            color: #212529 !important;
            background-color: #ffffff !important;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #c8e6c9;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #a5d6a7;
        }
        
        /* Clean spacing */
        .element-container {
            margin-bottom: 0.5rem;
        }
        
        .row-widget {
            margin-top: 0.5rem;
        }
        
        /* Login/Register Form Styling */
        [data-testid="stForm"] {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        }
        
        [data-testid="stForm"] input {
            color: #212529 !important;
            background-color: #ffffff !important;
            border: 1px solid #ced4da !important;
        }
        
        [data-testid="stForm"] input:focus {
            border-color: #4CAF50 !important;
            background-color: #ffffff !important;
        }
        
        [data-testid="stForm"] label {
            color: #212529 !important;
            font-weight: 500;
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
    Sidebar component with chatbot only.
    
    SOLID Principles:
    - SRP: Only responsible for rendering sidebar chatbot
    - DIP: Depends on Auth abstraction
    """
    
    def __init__(self, auth: Auth):
        """
        Initialize with auth service.
        
        DIP: Depends on Auth abstraction, not concrete implementation.
        """
        self.auth = auth
    
    def render(self):
        """
        Render sidebar with chatbot and logout.
        """
        with st.sidebar:
            st.title("🤖 Farm Assist")
            st.write(f"**Logged in as:** {self.auth.get_username()}")
            st.markdown("---")
            
            # Farm Assist Chatbot in styled box
            st.markdown('<div class="farm-assist-box">', unsafe_allow_html=True)
            render_support_bot(compact=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                self.auth.logout()
                st.rerun()


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
        self._render_cure_information()
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
        - **🌾 Farm Assist**: 24/7 AI assistant to answer your questions
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
    
    def _render_cure_information(self):
        """Render disease cure and treatment information section."""
        st.markdown("### 🏥 Disease Cure & Treatment Information")
        st.markdown("""
        <p style='font-size: 1.05rem; color: #555; line-height: 1.6; margin-bottom: 1.5rem;'>
        Browse comprehensive cure guides and treatment recommendations for all rice diseases in the <strong>Cure Guide</strong> tab.
        </p>
        """, unsafe_allow_html=True)
        
        st.info("👉 Visit the **Cure Guide** tab above to view detailed treatment plans, preventive measures, and step-by-step cure instructions for each disease.")
    
    def _render_call_to_action(self):
        """Render call to action."""
        st.info("� Navigate to **Upload & Predict** to analyze your rice leaf images!")
        st.success("🏥 Visit **Cure Guide** for detailed disease treatment information!")
        st.info("🤖 Use the **Farm Assist Chatbot** in the sidebar to ask questions anytime!")
    
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
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1 style='color: #1b5e20; font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;'>
                📸 Upload & Predict
            </h1>
            <p style='color: #555; font-size: 1.2rem; margin: 0;'>
                Upload rice leaf images to detect diseases instantly
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        self._render_upload_section()
    
    def _render_upload_section(self):
        """Render upload section."""
        # Prominent upload header with styling
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4CAF50 0%, #66bb6a 100%); 
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;
                    box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);'>
            <h2 style='color: #ffffff; margin: 0; text-align: center; font-weight: 700;'>
                📁 Upload Your Rice Leaf Images
            </h2>
            <p style='color: #f1f8f4; margin: 0.5rem 0 0 0; text-align: center; font-size: 1.05rem;'>
                Drag and drop or click to browse • Supports JPG, JPEG, PNG • Multiple files allowed
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader(
            "Choose rice leaf images (JPG, JPEG, PNG)",
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            help="You can upload multiple images at once",
            label_visibility="collapsed"
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
        Display individual prediction result with comprehensive cure information.
        
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
        
        # Warning if low confidence
        if confidence < 50:
            st.warning("⚠️ Low confidence prediction. Consider uploading a clearer image or consulting an expert.")
        
        # Comprehensive Disease & Remedy Information Section
        st.markdown("---")
        st.markdown("## 🏥 Complete Disease Treatment & Cure Guide")
        
        # Get remedy information
        remedy_service = DiseaseRemedyService()
        remedy = remedy_service.get_remedy(predicted_class)
        
        if remedy:
            # Severity Alert
            st.markdown(
                f"""
                <div style='background-color: #fff3cd; padding: 15px; border-radius: 8px; border-left: 5px solid #ffc107; margin: 10px 0;'>
                    <h3 style='color: #856404; margin-top: 0;'>⚠️ Disease Severity</h3>
                    <p style='margin: 5px 0;'><strong>Level:</strong> {remedy.severity_level}</p>
                    <p style='margin: 5px 0;'><strong>Expected Recovery Time:</strong> {remedy.time_to_cure}</p>
                    <p style='margin: 5px 0;'><strong>Cause:</strong> {remedy.cause}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Immediate Actions
            st.markdown("### 🚨 IMMEDIATE ACTIONS - DO THIS NOW!")
            st.markdown(
                """
                <div style='background-color: #f8d7da; padding: 15px; border-radius: 8px; border-left: 5px solid #dc3545;'>
                """,
                unsafe_allow_html=True
            )
            for action in remedy.immediate_actions:
                st.markdown(f"- {action}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Treatment Options Tabs
            tab1, tab2, tab3 = st.tabs(["💊 Chemical Treatment", "🌿 Organic Treatment", "🛡️ Prevention"])
            
            with tab1:
                st.markdown("### Chemical Treatment Steps")
                st.info("Follow these steps in order for best results. Always read product labels and follow safety instructions.")
                
                for step in remedy.chemical_treatment:
                    with st.expander(f"{step.icon} Step {step.step_number}: {step.title}", expanded=True):
                        st.markdown(f"**Instructions:** {step.description}")
                        st.success("✓ Check off when completed")
            
            with tab2:
                st.markdown("### Organic & Natural Treatment Options")
                st.info("Eco-friendly alternatives that are safer for the environment. May take longer but have no chemical residue.")
                
                for step in remedy.organic_treatment:
                    with st.expander(f"{step.icon} Step {step.step_number}: {step.title}", expanded=True):
                        st.markdown(f"**Instructions:** {step.description}")
                        st.success("✓ Check off when completed")
            
            with tab3:
                st.markdown("### Preventive Measures")
                st.info("Apply these measures to prevent future outbreaks and maintain healthy crops.")
                
                for measure in remedy.preventive_measures:
                    st.markdown(f"- {measure}")
            
            # Do's and Don'ts
            st.markdown("### ✅ Do's and ❌ Don'ts")
            col_do, col_dont = st.columns(2)
            
            with col_do:
                st.markdown(
                    """
                    <div style='background-color: #d4edda; padding: 15px; border-radius: 8px; border-left: 5px solid #28a745;'>
                        <h4 style='color: #155724; margin-top: 0;'>✅ DO THESE</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                for do_item in remedy.dos:
                    st.markdown(f"{do_item}")
            
            with col_dont:
                st.markdown(
                    """
                    <div style='background-color: #f8d7da; padding: 15px; border-radius: 8px; border-left: 5px solid #dc3545;'>
                        <h4 style='color: #721c24; margin-top: 0;'>❌ DON'T DO THESE</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                for dont_item in remedy.donts:
                    st.markdown(f"{dont_item}")
            
            # Emergency Contact
            if remedy.emergency_contact:
                st.markdown(
                    f"""
                    <div style='background-color: #d1ecf1; padding: 15px; border-radius: 8px; border-left: 5px solid #0c5460; margin: 15px 0;'>
                        <h4 style='color: #0c5460; margin-top: 0;'>📞 Emergency Contact</h4>
                        <p>{remedy.emergency_contact}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            # Fallback to basic disease info if remedy not available
            disease_info = self.predictor.get_disease_info(predicted_class)
            
            st.markdown("### 📖 Disease Information")
            st.markdown(f"**Description:** {disease_info['description']}")
            st.markdown(f"**Symptoms:** {disease_info['symptoms']}")
            
            st.markdown("### 💊 Treatment Recommendations")
            st.markdown(disease_info['treatment'])


class CureGuidePageComponent:
    """
    Cure Guide page component - Browse all disease treatments.
    
    SOLID Principles:
    - SRP: Only responsible for rendering cure guide page
    - OCP: Can extend with new diseases without modifying existing code
    """
    
    def render(self):
        """Render dedicated cure guide page with comprehensive disease information."""
        st.title("🏥 Disease Cure & Treatment Guide")
        
        st.markdown("""
        <p style='font-size: 1.1rem; color: #555; line-height: 1.6; margin-bottom: 2rem;'>
        Browse comprehensive cure guides and treatment recommendations for all rice diseases. 
        Select a disease to view detailed treatment plans, preventive measures, and best practices.
        </p>
        """, unsafe_allow_html=True)
        
        # Disease Selection
        st.markdown("### 🔍 Select a Disease")
        
        remedy_service = DiseaseRemedyService()
        available_diseases = remedy_service.get_all_diseases()
        
        if not available_diseases:
            st.info("No disease information available at this time.")
            return
        
        # Disease selection cards
        disease_col1, disease_col2, disease_col3 = st.columns(3)
        
        with disease_col1:
            if st.button("🦠 Bacterial Blight", use_container_width=True, key="btn_bb"):
                st.session_state['selected_disease'] = "Bacterialblight"
                st.rerun()
        
        with disease_col2:
            if st.button("💨 Blast", use_container_width=True, key="btn_blast"):
                st.session_state['selected_disease'] = "Blast"
                st.rerun()
        
        with disease_col3:
            if st.button("🟤 Brown Spot", use_container_width=True, key="btn_bs"):
                st.session_state['selected_disease'] = "Brownspot"
                st.rerun()
        
        st.markdown("---")
        
        # Display selected disease information
        if 'selected_disease' in st.session_state:
            selected_disease = st.session_state['selected_disease']
            remedy = remedy_service.get_remedy(selected_disease)
            
            if remedy:
                self._display_disease_cure(remedy)
            else:
                st.warning(f"Cure information for {selected_disease} is not available.")
        else:
            # Show overview when no disease selected
            self._show_overview()
    
    def _show_overview(self):
        """Show overview when no disease is selected."""
        st.markdown("### 📊 Disease Overview")
        st.info("👆 Click on a disease button above to view detailed cure information and treatment plans.")
        
        # Feature Highlights
        st.markdown("### ✨ What You'll Find")
        
        col_x, col_y = st.columns(2)
        
        with col_x:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 100%); 
                        padding: 1.5rem; border-radius: 12px; border: 1px solid #c8e6c9; 
                        margin-bottom: 1rem;'>
                <h4 style='color: #1b5e20; margin-top: 0;'>💊 Treatment Plans</h4>
                <p style='color: #555; line-height: 1.6;'>
                Step-by-step cure guides with both chemical and organic treatment options, 
                including exact dosages and application methods.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style='background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 100%); 
                        padding: 1.5rem; border-radius: 12px; border: 1px solid #c8e6c9; 
                        margin-bottom: 1rem;'>
                <h4 style='color: #1b5e20; margin-top: 0;'>🚨 Immediate Actions</h4>
                <p style='color: #555; line-height: 1.6;'>
                Urgent steps to take immediately when disease is detected to prevent 
                spread and minimize crop damage.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_y:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 100%); 
                        padding: 1.5rem; border-radius: 12px; border: 1px solid #c8e6c9; 
                        margin-bottom: 1rem;'>
                <h4 style='color: #1b5e20; margin-top: 0;'>🛡️ Prevention Tips</h4>
                <p style='color: #555; line-height: 1.6;'>
                Learn best practices to prevent diseases before they occur, including 
                crop rotation, water management, and field hygiene.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style='background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 100%); 
                        padding: 1.5rem; border-radius: 12px; border: 1px solid #c8e6c9; 
                        margin-bottom: 1rem;'>
                <h4 style='color: #1b5e20; margin-top: 0;'>✅ Do's & Don'ts</h4>
                <p style='color: #555; line-height: 1.6;'>
                Clear guidance on what to do and what to avoid during treatment for 
                maximum effectiveness.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    def _display_disease_cure(self, remedy):
        """Display complete cure information for a disease."""
        st.markdown(f"## 🏥 {remedy.disease_name} - Complete Treatment Guide")
        
        # Severity Alert
        st.markdown(
            f"""
            <div style='background-color: #fff3cd; padding: 15px; border-radius: 8px; border-left: 5px solid #ffc107; margin: 10px 0;'>
                <h3 style='color: #856404; margin-top: 0;'>⚠️ Disease Severity</h3>
                <p style='margin: 5px 0;'><strong>Level:</strong> {remedy.severity_level}</p>
                <p style='margin: 5px 0;'><strong>Expected Recovery Time:</strong> {remedy.time_to_cure}</p>
                <p style='margin: 5px 0;'><strong>Cause:</strong> {remedy.cause}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Immediate Actions
        st.markdown("### 🚨 IMMEDIATE ACTIONS - DO THIS NOW!")
        st.markdown(
            """
            <div style='background-color: #f8d7da; padding: 15px; border-radius: 8px; border-left: 5px solid #dc3545;'>
            """,
            unsafe_allow_html=True
        )
        for i, action in enumerate(remedy.immediate_actions, 1):
            st.markdown(f"{i}. {action}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Treatment Options Tabs
        tab1, tab2, tab3 = st.tabs(["💊 Chemical Treatment", "🌿 Organic Treatment", "🛡️ Prevention"])
        
        with tab1:
            st.markdown("### Chemical Treatment Steps")
            st.info("Follow these steps in order for best results. Always read product labels and follow safety instructions.")
            
            for step in remedy.chemical_treatment:
                with st.expander(f"{step.icon} Step {step.step_number}: {step.title}", expanded=False):
                    st.markdown(f"**Instructions:** {step.description}")
        
        with tab2:
            st.markdown("### Organic & Natural Treatment Options")
            st.info("Eco-friendly alternatives that are safer for the environment. May take longer but have no chemical residue.")
            
            for step in remedy.organic_treatment:
                with st.expander(f"{step.icon} Step {step.step_number}: {step.title}", expanded=False):
                    st.markdown(f"**Instructions:** {step.description}")
        
        with tab3:
            st.markdown("### Preventive Measures")
            st.info("Apply these measures to prevent future outbreaks and maintain healthy crops.")
            
            for i, measure in enumerate(remedy.preventive_measures, 1):
                st.markdown(f"{i}. {measure}")
        
        st.markdown("---")
        
        # Do's and Don'ts
        st.markdown("### ✅ Do's and ❌ Don'ts")
        col_do, col_dont = st.columns(2)
        
        with col_do:
            st.markdown(
                """
                <div style='background-color: #d4edda; padding: 15px; border-radius: 8px; border-left: 5px solid #28a745;'>
                    <h4 style='color: #155724; margin-top: 0;'>✅ DO THESE</h4>
                </div>
                """,
                unsafe_allow_html=True
            )
            for do_item in remedy.dos:
                st.markdown(f"- {do_item}")
        
        with col_dont:
            st.markdown(
                """
                <div style='background-color: #f8d7da; padding: 15px; border-radius: 8px; border-left: 5px solid #dc3545;'>
                    <h4 style='color: #721c24; margin-top: 0;'>❌ DON'T DO THESE</h4>
                </div>
                """,
                unsafe_allow_html=True
            )
            for dont_item in remedy.donts:
                st.markdown(f"- {dont_item}")
        
        # Emergency Contact
        if remedy.emergency_contact:
            st.markdown("---")
            st.markdown(
                f"""
                <div style='background-color: #d1ecf1; padding: 15px; border-radius: 8px; border-left: 5px solid #0c5460; margin: 15px 0;'>
                    <h4 style='color: #0c5460; margin-top: 0;'>📞 Emergency Contact</h4>
                    <p>{remedy.emergency_contact}</p>
                </div>
                """,
                unsafe_allow_html=True
            )


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
        
        # Render sidebar with chatbot
        nav = NavigationComponent(self.auth)
        nav.render()
        
        # Main content navigation using tabs
        tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📸 Upload & Predict", "🏥 Cure Guide", "ℹ️ About"])
        
        with tab1:
            home_page = HomePageComponent()
            home_page.render(self.auth.get_username())
        
        with tab2:
            # Lazy load predictor
            if self.predictor is None:
                try:
                    if 'predictor' not in st.session_state:
                        with st.spinner("Loading model..."):
                            st.session_state.predictor = Predictor()
                    self.predictor = st.session_state.predictor
                    
                    prediction_page = PredictionPageComponent(self.predictor)
                    prediction_page.render()
                except Exception as e:
                    st.error(f"Error loading model: {str(e)}")
                    st.info("Please ensure the trained model exists at `models/best_model.pth`")
                    st.warning("💡 You can still use the Cure Guide and chatbot features!")
            else:
                prediction_page = PredictionPageComponent(self.predictor)
                prediction_page.render()
        
        with tab3:
            cure_page = CureGuidePageComponent()
            cure_page.render()
        
        with tab4:
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
