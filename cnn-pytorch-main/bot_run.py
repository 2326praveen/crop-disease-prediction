"""
Chatbot Integration for Crop Disease Prediction System.

This module provides a support bot interface with built-in knowledge base
to assist users with questions about disease identification, treatment,
and using the application. Enhanced with comprehensive curing mechanisms.
"""

import streamlit as st
from src.disease_remedies import DiseaseRemedyService


# Knowledge Base for Crop Diseases
KNOWLEDGE_BASE = {
    # Rice Diseases
    "bacterial blight": {
        "keywords": ["bacterial blight", "blight", "xanthomonas", "wilting", "water-soaked"],
        "info": """**Bacterial Blight (Xanthomonas oryzae)**

🔬 **Cause**: Bacteria Xanthomonas oryzae pv. oryzae

🔍 **Symptoms**:
- Water-soaked lesions on leaf margins
- Lesions turn yellow, then grayish-white
- Leaves dry up and wilt
- Milky or opaque dew drops on young lesions

💊 **Treatment**:
1. Use resistant rice varieties (most effective)
2. Apply copper-based bactericides (Copper oxychloride)
3. Avoid excessive nitrogen fertilization
4. Maintain proper water management
5. Remove and destroy infected plant debris

🛡️ **Prevention**:
- Use certified disease-free seeds
- Practice crop rotation
- Avoid field-to-field movement during wet conditions
- Balance fertilizer application"""
    },
    
    "blast": {
        "keywords": ["blast", "magnaporthe", "diamond", "lesion", "fungus", "rice blast"],
        "info": """**Rice Blast Disease (Magnaporthe oryzae)**

🔬 **Cause**: Fungus Magnaporthe oryzae (Pyricularia oryzae)

🔍 **Symptoms**:
- Diamond-shaped lesions with gray/white centers
- Brown or reddish-brown margins on lesions
- Lesions on leaves, nodes, and panicles
- Severe cases cause neck rot and empty grains

💊 **Treatment**:
1. Apply fungicides: Tricyclazole, Isoprothiolane, or Carbendazim
2. Use resistant varieties
3. Split nitrogen application
4. Maintain proper plant spacing

🛡️ **Prevention**:
- Use certified blast-resistant seeds
- Avoid excessive nitrogen
- Ensure proper drainage
- Remove crop residues after harvest
- Practice crop rotation"""
    },
    
    "brown spot": {
        "keywords": ["brown spot", "brownspot", "bipolaris", "helminthosporium", "circular spot"],
        "info": """**Brown Spot Disease (Bipolaris oryzae)**

🔬 **Cause**: Fungus Bipolaris oryzae (Helminthosporium oryzae)

🔍 **Symptoms**:
- Circular to oval brown spots on leaves
- Spots have gray or tan centers with brown margins
- Spots may appear on leaf sheaths and grains
- Severe infection causes seedling blight

💊 **Treatment**:
1. Apply fungicides: Mancozeb, Propiconazole, or Carbendazim
2. Seed treatment with fungicides before planting
3. Foliar spray at disease onset
4. Improve soil fertility (especially potassium)

🛡️ **Prevention**:
- Use healthy, certified seeds
- Treat seeds with fungicide before sowing
- Maintain balanced nutrition (N, P, K)
- Avoid water stress
- Remove infected plant debris"""
    },
    
    "tungro": {
        "keywords": ["tungro", "virus", "yellow", "orange", "stunted", "leafhopper"],
        "info": """**Rice Tungro Disease**

🔬 **Cause**: Rice tungro bacilliform virus (RTBV) + Rice tungro spherical virus (RTSV), transmitted by green leafhoppers

🔍 **Symptoms**:
- Yellow to orange discoloration of leaves
- Stunted plant growth
- Reduced tillering
- Delayed flowering and panicle emergence

💊 **Treatment**:
1. Control leafhopper vectors with insecticides
2. Remove infected plants immediately
3. Use light traps to monitor leafhopper population
4. Apply systemic insecticides

🛡️ **Prevention**:
- Use tungro-resistant varieties
- Synchronous planting in the area
- Control leafhopper population
- Remove weeds that harbor vectors"""
    },
    
    # Black Gram Diseases
    "black gram healthy": {
        "keywords": ["black gram healthy", "healthy black gram", "healthy pulse", "no disease"],
        "info": """**Healthy Black Gram Plant**

✅ Your black gram plant appears healthy!

🌱 **Characteristics of Healthy Plants**:
- Dark green, uniform leaf color
- No spots or lesions
- Normal leaf shape without curling
- Good plant vigor and growth

📋 **Maintenance Tips**:
1. Continue regular watering (avoid waterlogging)
2. Apply balanced fertilizers as needed
3. Monitor regularly for pest and disease signs
4. Maintain proper plant spacing
5. Keep field weed-free"""
    },
    
    "anthracnose": {
        "keywords": ["anthracnose", "colletotrichum", "black gram disease", "pod spots"],
        "info": """**Anthracnose (Colletotrichum species)**

🔬 **Cause**: Fungus Colletotrichum lindemuthianum / C. truncatum

🔍 **Symptoms**:
- Dark brown to black sunken lesions on pods
- Circular spots on leaves with dark margins
- Pink spore masses in humid conditions
- Stem cankers and seedling blight

💊 **Treatment**:
1. Apply fungicides: Carbendazim, Mancozeb, or Chlorothalonil
2. Spray at flowering and pod formation stages
3. Remove infected plant parts
4. Improve air circulation

🛡️ **Prevention**:
- Use disease-free certified seeds
- Treat seeds with fungicide
- Practice 2-3 year crop rotation
- Avoid overhead irrigation"""
    },
    
    "yellow mosaic": {
        "keywords": ["yellow mosaic", "mosaic", "mymv", "whitefly", "yellow patches"],
        "info": """**Yellow Mosaic Virus Disease (MYMV)**

🔬 **Cause**: Mungbean Yellow Mosaic Virus, transmitted by whiteflies

🔍 **Symptoms**:
- Irregular yellow and green patches on leaves
- Mottled appearance (mosaic pattern)
- Stunted growth and reduced pod formation
- Curling and puckering of leaves

💊 **Treatment**:
1. Control whitefly vectors with insecticides (Imidacloprid, Thiamethoxam)
2. Remove and destroy infected plants
3. Use yellow sticky traps for monitoring
4. Apply neem-based products

🛡️ **Prevention**:
- Use MYMV-resistant varieties
- Early sowing to escape peak whitefly population
- Intercropping with non-host crops
- Remove alternate host weeds"""
    },
    
    # Lentil Diseases
    "ascochyta blight": {
        "keywords": ["ascochyta", "lentil blight", "stem lesion", "pod spot"],
        "info": """**Ascochyta Blight of Lentil**

🔬 **Cause**: Fungus Ascochyta lentis

🔍 **Symptoms**:
- Tan to brown lesions on leaves and stems
- Lesions have dark margins
- Pod infection causes seed discoloration
- Severe cases cause plant death

💊 **Treatment**:
1. Apply fungicides: Chlorothalonil, Mancozeb
2. Spray at early flowering stage
3. Remove infected crop debris
4. Improve field drainage

🛡️ **Prevention**:
- Use certified disease-free seeds
- Seed treatment with fungicides
- Crop rotation (3-4 years)
- Avoid dense planting"""
    },
    
    "rust": {
        "keywords": ["rust", "uromyces", "orange pustules", "lentil rust"],
        "info": """**Lentil Rust (Uromyces viciae-fabae)**

🔬 **Cause**: Fungus Uromyces viciae-fabae

🔍 **Symptoms**:
- Orange-brown pustules on leaves (undersides first)
- Pustules turn dark brown with age
- Severe infection causes defoliation
- Reduced pod formation

💊 **Treatment**:
1. Apply fungicides: Mancozeb, Propiconazole, Triadimefon
2. Start spraying at first sign of disease
3. Repeat at 10-14 day intervals
4. Remove severely infected plants

🛡️ **Prevention**:
- Use rust-resistant varieties
- Early sowing
- Balanced fertilization
- Avoid late planting"""
    },
    
    "powdery mildew": {
        "keywords": ["powdery mildew", "white powder", "erysiphe", "white coating"],
        "info": """**Powdery Mildew**

🔬 **Cause**: Fungus Erysiphe species

🔍 **Symptoms**:
- White powdery coating on leaves
- Starts as small white spots
- Spreads to cover entire leaf surface
- Leaves turn yellow and dry

💊 **Treatment**:
1. Apply fungicides: Sulfur, Karathane, Triadimefon
2. Spray at first appearance of symptoms
3. Ensure good coverage of plant surfaces
4. Remove heavily infected leaves

🛡️ **Prevention**:
- Use resistant varieties
- Avoid overcrowding
- Ensure good air circulation
- Balanced nitrogen application"""
    },
}

# Application Usage Knowledge
APP_KNOWLEDGE = {
    "how to use": """**How to Use the Crop Disease Prediction System**

📱 **Step-by-Step Guide**:

1. **Login/Register**: Create an account or login to access features

2. **Upload Images**:
   - Go to 'Upload & Predict' page
   - Click 'Browse files' or drag and drop images
   - Upload clear photos of affected leaves
   - Supports JPG, PNG formats

3. **Get Predictions**:
   - Click 'Analyze Images' button
   - Wait for AI analysis
   - View disease prediction with confidence score

4. **Review Results**:
   - See identified disease name
   - Check confidence percentage
   - Read treatment recommendations

5. **Ask Questions**:
   - Use this Support Bot for additional help
   - Ask about diseases, treatments, or app usage""",
   
    "good image": """**Tips for Capturing Good Leaf Images**

📸 **For Best Prediction Results**:

✅ **DO**:
- Use good natural lighting (avoid harsh shadows)
- Focus clearly on the affected area
- Capture the entire leaf or affected portion
- Use plain background if possible
- Take multiple angles if needed
- Keep camera steady to avoid blur

❌ **DON'T**:
- Use blurry or out-of-focus images
- Take photos in very low light
- Include multiple overlapping leaves
- Use heavily filtered images
- Capture from too far away

📁 **Supported Formats**: JPG, JPEG, PNG
📏 **Recommended**: At least 224x224 pixels""",

    "supported diseases": """**Diseases Detected by This System**

🌾 **Rice Leaf Diseases**:
- Bacterial Blight
- Blast
- Brown Spot
- Tungro

🫘 **Black Gram Diseases**:
- Healthy (no disease)
- Anthracnose
- Yellow Mosaic
- Powdery Mildew
- Leaf Crinkle

🌿 **Lentil Diseases**:
- Ascochyta Blight
- Rust
- Powdery Mildew

The model has been trained on these specific diseases and provides confidence scores for predictions.""",

    "about project": """**About This Project**

🎯 **Crop Disease Prediction System**

This is an AI-powered application that helps farmers and agricultural professionals identify crop diseases from leaf images.

🔬 **Technology**:
- Deep Learning (CNN - Convolutional Neural Network)
- PyTorch framework
- Transfer learning with pre-trained models
- Streamlit web interface

📊 **Features**:
- Image upload and analysis
- Real-time disease prediction
- Confidence scores
- Treatment recommendations
- Support chatbot

👥 **Target Users**:
- Farmers
- Agricultural extension workers
- Researchers
- Students of agriculture"""
}


def get_detailed_cure_response(disease_name):
    """Get detailed cure response for a specific disease."""
    remedy_service = DiseaseRemedyService()
    remedy = remedy_service.get_remedy(disease_name)
    
    if not remedy:
        return None
    
    response = f"""**🏥 Complete Cure Guide for {remedy.disease_name}**

⚠️ **SEVERITY**: {remedy.severity_level}
⏱️ **Recovery Time**: {remedy.time_to_cure}
🔬 **Cause**: {remedy.cause}

---

🚨 **IMMEDIATE ACTIONS - Do This Now!**
"""
    
    for idx, action in enumerate(remedy.immediate_actions, 1):
        response += f"\n{idx}. {action}"
    
    response += "\n\n---\n\n💊 **CHEMICAL TREATMENT STEPS**\n"
    for step in remedy.chemical_treatment:
        response += f"\n{step.icon} **{step.title}**\n   {step.description}\n"
    
    response += "\n---\n\n🌿 **ORGANIC TREATMENT OPTIONS**\n"
    for step in remedy.organic_treatment:
        response += f"\n{step.icon} **{step.title}**\n   {step.description}\n"
    
    response += "\n---\n\n✅ **DO's**\n"
    for do_item in remedy.dos[:5]:  # Show first 5
        response += f"\n{do_item}"
    
    response += "\n\n❌ **DON'Ts**\n"
    for dont_item in remedy.donts[:5]:  # Show first 5
        response += f"\n{dont_item}"
    
    if remedy.emergency_contact:
        response += f"\n\n📞 **Emergency**: {remedy.emergency_contact}"
    
    response += "\n\n💡 **Tip**: Upload an image for prediction to see complete step-by-step treatment instructions!"
    
    return response


def find_best_response(user_input):
    """Find the best matching response from knowledge base."""
    user_input_lower = user_input.lower()
    
    # Check for specific cure/treatment requests
    cure_keywords = ["cure", "treat", "remedy", "fix", "heal", "how to cure", "treatment for"]
    disease_map = {
        "bacterial blight": "Bacterialblight",
        "bacterialblight": "Bacterialblight",
        "blight": "Bacterialblight",
        "blast": "Blast",
        "brown spot": "Brownspot",
        "brownspot": "Brownspot"
    }
    
    if any(kw in user_input_lower for kw in cure_keywords):
        for disease_key, disease_name in disease_map.items():
            if disease_key in user_input_lower:
                cure_response = get_detailed_cure_response(disease_name)
                if cure_response:
                    return cure_response
        
        # If cure keyword found but no specific disease
        return """**🏥 Treatment & Cure Information**

I can provide detailed treatment plans for:

🌾 **Rice Diseases**:
- **Bacterial Blight** - Ask: "How to cure bacterial blight?"
- **Blast** - Ask: "Treatment for blast disease"
- **Brown Spot** - Ask: "How to treat brown spot?"

Just specify which disease you need treatment for, and I'll provide:
✅ Immediate actions
✅ Chemical treatment steps
✅ Organic alternatives
✅ Prevention measures
✅ Do's and Don'ts

**Example**: "How to cure blast disease?"
"""
    
    # Check for greetings
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "hii", "hiii"]
    if any(greet in user_input_lower for greet in greetings):
        return "Hello! 👋 I'm your Crop Disease Support Assistant. How can I help you today? You can ask me about:\n- Rice diseases (Bacterial Blight, Blast, Brown Spot, Tungro)\n- **Complete cure guides** - Ask: 'How to cure bacterial blight?'\n- Treatment recommendations\n- How to use this application\n- Image upload tips"
    
    # Check for thanks
    thanks = ["thank", "thanks", "thx", "appreciate"]
    if any(t in user_input_lower for t in thanks):
        return "You're welcome! 😊 Feel free to ask if you have more questions about crop diseases or using this application."
    
    # Check for app usage questions
    app_keywords = {
        "how to use": ["how to use", "how do i use", "usage", "guide", "tutorial", "help me use"],
        "good image": ["good image", "photo tip", "capture", "take photo", "image quality", "picture"],
        "supported diseases": ["what disease", "which disease", "supported", "detect", "identify", "list of disease"],
        "about project": ["about", "what is this", "project", "application", "app", "system"]
    }
    
    for key, keywords in app_keywords.items():
        if any(kw in user_input_lower for kw in keywords):
            return APP_KNOWLEDGE[key]
    
    # Check disease knowledge base
    best_match = None
    best_score = 0
    
    for disease, data in KNOWLEDGE_BASE.items():
        score = 0
        for keyword in data["keywords"]:
            if keyword in user_input_lower:
                score += len(keyword)  # Longer keyword matches score higher
        
        if score > best_score:
            best_score = score
            best_match = data["info"]
    
    if best_match:
        return best_match
    
    # Check for treatment questions
    if "treat" in user_input_lower or "cure" in user_input_lower or "remedy" in user_input_lower:
        return """**Treatment Information**

Please specify which disease you want treatment information for:
- Bacterial Blight
- Blast
- Brown Spot
- Tungro
- Anthracnose
- Yellow Mosaic
- Powdery Mildew
- Ascochyta Blight
- Rust

Just type the disease name and I'll provide detailed treatment recommendations!"""
    
    # Check for prevention questions
    if "prevent" in user_input_lower or "avoid" in user_input_lower:
        return """**General Disease Prevention Tips**

🛡️ **For All Crops**:
1. Use certified, disease-free seeds
2. Practice crop rotation (2-3 years)
3. Maintain proper plant spacing
4. Balanced fertilization
5. Proper water management
6. Remove infected plant debris
7. Control insect vectors
8. Regular field monitoring

Ask about a specific disease for detailed prevention methods!"""

    # Check for rice specific questions
    if "rice" in user_input_lower and ("disease" in user_input_lower or "problem" in user_input_lower or "leaf" in user_input_lower or "plant" in user_input_lower):
        return """**Rice Leaf Diseases**

This system can detect the following rice diseases:

1. **Bacterial Blight** - Water-soaked lesions, wilting
   - Caused by Xanthomonas oryzae bacteria

2. **Blast** - Diamond-shaped lesions with gray centers
   - Caused by Magnaporthe oryzae fungus

3. **Brown Spot** - Circular brown spots on leaves
   - Caused by Bipolaris oryzae fungus

4. **Tungro** - Yellow-orange discoloration, stunting
   - Caused by virus, spread by leafhoppers

Type any disease name to learn more about symptoms, treatment, and prevention!"""

    # Check for black gram questions
    if "black gram" in user_input_lower or "pulse" in user_input_lower:
        return """**Black Gram Diseases**

This system can detect:

1. **Anthracnose** - Dark sunken lesions on pods
2. **Yellow Mosaic (MYMV)** - Yellow-green mosaic pattern on leaves
3. **Powdery Mildew** - White powdery coating on leaves
4. **Leaf Crinkle** - Curling and crinkling of leaves

Type any disease name for detailed information!"""

    # Check for lentil questions
    if "lentil" in user_input_lower:
        return """**Lentil Diseases**

This system can detect:

1. **Ascochyta Blight** - Tan-brown lesions with dark margins
2. **Rust** - Orange-brown pustules on leaves
3. **Powdery Mildew** - White powdery coating

Type any disease name for detailed information!"""
    
    # Default response
    return """I can help you with information about crop diseases! Here's what I know:

🌾 **Rice Diseases**: Bacterial Blight, Blast, Brown Spot, Tungro
🫘 **Black Gram**: Anthracnose, Yellow Mosaic, Powdery Mildew
🌿 **Lentil**: Ascochyta Blight, Rust, Powdery Mildew

📱 **App Help**: Ask "How to use", "Image tips", or "Supported diseases"

**Try asking**:
- "What is Bacterial Blight?"
- "How to treat Blast disease?"
- "What are rice diseases?"
- "How to use this app?"

Just type your question!"""


def render_support_bot():
    """
    Render the support bot interface with built-in knowledge base and cure mechanisms.
    """
    st.title("🤖 Support Bot - AI Health Assistant")
    
    st.markdown("""
    ### Welcome to the Crop Disease Support & Cure Agent
    
    I can help you with comprehensive cure information! Ask me about:
    - 🏥 **Complete cure guides** - Ask: "How to cure bacterial blight?"
    - 💊 **Step-by-step treatment plans** for all diseases
    - 🌾 **Rice diseases**: Bacterial Blight, Blast, Brown Spot, Tungro
    - 🧪 **Chemical & organic treatments**
    - 🛡️ **Prevention strategies**
    - 🔍 How to use the prediction system
    - 📸 Tips for capturing good leaf images
    
    **Example questions**:
    - "How to cure blast disease?"
    - "What is the treatment for bacterial blight?"
    - "How do I treat brown spot organically?"
    """)
    
    st.markdown("---")
    
    # Quick Action Buttons
    st.markdown("### 🎯 Quick Cure Guides")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🦠 Cure Bacterial Blight", use_container_width=True):
            cure_response = get_detailed_cure_response("Bacterialblight")
            if cure_response:
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                st.session_state.messages.append({"role": "user", "content": "How to cure bacterial blight?"})
                st.session_state.messages.append({"role": "assistant", "content": cure_response})
                st.rerun()
    
    with col2:
        if st.button("🍃 Cure Blast Disease", use_container_width=True):
            cure_response = get_detailed_cure_response("Blast")
            if cure_response:
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                st.session_state.messages.append({"role": "user", "content": "How to cure blast?"})
                st.session_state.messages.append({"role": "assistant", "content": cure_response})
                st.rerun()
    
    with col3:
        if st.button("🟤 Cure Brown Spot", use_container_width=True):
            cure_response = get_detailed_cure_response("Brownspot")
            if cure_response:
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                st.session_state.messages.append({"role": "user", "content": "How to cure brown spot?"})
                st.session_state.messages.append({"role": "assistant", "content": cure_response})
                st.rerun()
    
    st.markdown("---")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! 👋 I'm your Crop Disease Support & Cure Assistant. Ask me for complete cure guides - try: 'How to cure bacterial blight?'"}
        ]
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me how to cure any disease..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        response = find_best_response(prompt)
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)


if __name__ == "__main__":
    # Standalone testing
    st.set_page_config(
        page_title="Support Bot - Crop Disease Prediction",
        page_icon="🤖",
        layout="wide"
    )
    render_support_bot()
