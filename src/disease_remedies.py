"""
Disease Remedies and Curing Information Module.

This module provides comprehensive curing and treatment information for crop diseases,
following SOLID principles with a clear interface for remedy retrieval.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class RemedyStep:
    """Represents a single step in the treatment process."""
    step_number: int
    title: str
    description: str
    icon: str = "📌"


@dataclass
class DiseaseRemedy:
    """Complete remedy information for a disease."""
    disease_name: str
    cause: str
    immediate_actions: List[str]
    chemical_treatment: List[RemedyStep]
    organic_treatment: List[RemedyStep]
    preventive_measures: List[str]
    dos: List[str]
    donts: List[str]
    time_to_cure: str
    severity_level: str
    emergency_contact: Optional[str] = None


class DiseaseRemedyService:
    """
    Service for retrieving disease remedy information.
    
    SOLID Principles:
    - SRP: Only responsible for managing remedy data
    - OCP: Easy to extend with new diseases
    - DIP: Returns abstract disease remedy objects
    """
    
    def __init__(self):
        """Initialize with comprehensive remedy database."""
        self._remedies = self._load_remedies()
    
    def get_remedy(self, disease_name: str) -> Optional[DiseaseRemedy]:
        """
        Get remedy information for a specific disease.
        
        Args:
            disease_name: Name of the disease
            
        Returns:
            DiseaseRemedy object or None if not found
        """
        return self._remedies.get(disease_name)
    
    def get_all_diseases(self) -> List[str]:
        """Get list of all diseases with remedy information."""
        return list(self._remedies.keys())
    
    def _load_remedies(self) -> Dict[str, DiseaseRemedy]:
        """Load all remedy information."""
        return {
            "Bacterialblight": DiseaseRemedy(
                disease_name="Bacterial Blight",
                cause="Bacteria Xanthomonas oryzae pv. oryzae",
                immediate_actions=[
                    "🚨 Isolate infected plants immediately to prevent spread",
                    "💧 Drain excess water from the field - bacteria thrives in waterlogged conditions",
                    "🔍 Mark and tag all infected areas for targeted treatment",
                    "✂️ Remove severely infected leaves using sterilized tools",
                    "🧤 Always wear gloves when handling infected plants"
                ],
                chemical_treatment=[
                    RemedyStep(
                        1,
                        "Apply Copper-Based Bactericide",
                        "Spray Copper Oxychloride (50% WP) at 2.5g per liter of water. Apply thoroughly on both sides of leaves. Repeat every 7-10 days for 3 weeks.",
                        "💊"
                    ),
                    RemedyStep(
                        2,
                        "Use Streptocycline",
                        "Mix Streptocycline (100 ppm) with Copper Oxychloride for enhanced effect. Apply during early morning or late evening.",
                        "💉"
                    ),
                    RemedyStep(
                        3,
                        "Apply Systemic Treatment",
                        "Use Validamycin 3% SL at 2ml per liter for systemic action. This helps plants fight bacterial invasion from within.",
                        "🔬"
                    )
                ],
                organic_treatment=[
                    RemedyStep(
                        1,
                        "Neem Oil Application",
                        "Mix 5ml neem oil with 1 liter water and a few drops of liquid soap (emulsifier). Spray weekly on affected plants.",
                        "🌿"
                    ),
                    RemedyStep(
                        2,
                        "Garlic-Chili Solution",
                        "Blend 100g garlic + 50g chili in 1L water. Ferment for 24 hours, strain, and dilute 1:10. Spray on plants.",
                        "🧄"
                    ),
                    RemedyStep(
                        3,
                        "Pseudomonas Treatment",
                        "Apply Pseudomonas fluorescens (bio-fungicide) at 10g per liter as a foliar spray and soil drench.",
                        "🦠"
                    ),
                    RemedyStep(
                        4,
                        "Turmeric Paste",
                        "Mix turmeric powder with water to form paste. Apply on visible lesions to prevent bacterial spread.",
                        "🟡"
                    )
                ],
                preventive_measures=[
                    "🌾 Plant resistant varieties: Use varieties like IR64, Swarna, and other certified resistant cultivars",
                    "🌱 Seed treatment: Soak seeds in Streptocycline solution (100 ppm) for 12 hours before planting",
                    "💧 Water management: Maintain 2-3 inches water depth, avoid continuous flooding",
                    "🚜 Field sanitation: Remove and burn all infected plant debris after harvest",
                    "📏 Proper spacing: Maintain 20x15cm spacing for better air circulation",
                    "🌡️ Balanced nutrition: Avoid excessive nitrogen fertilizer which makes plants susceptible",
                    "🔄 Crop rotation: Rotate with non-host crops for at least one season",
                    "🚫 Movement control: Avoid moving between fields during wet weather or early morning dew"
                ],
                dos=[
                    "✅ Use certified disease-free seeds from authorized dealers",
                    "✅ Apply copper fungicide preventively before disease appears",
                    "✅ Monitor fields regularly (at least twice weekly) for early detection",
                    "✅ Drain field water before applying any treatment",
                    "✅ Sterilize all farm tools with 10% bleach solution between uses",
                    "✅ Maintain field hygiene and remove weeds regularly",
                    "✅ Apply potassium fertilizers to strengthen plant immunity"
                ],
                donts=[
                    "❌ Don't apply nitrogen fertilizer during infection period",
                    "❌ Don't spray during rain or when rain is expected within 4 hours",
                    "❌ Don't use contaminated irrigation water from infected fields",
                    "❌ Don't walk through infected areas when plants are wet",
                    "❌ Don't compost infected plant material - burn it instead",
                    "❌ Don't ignore early symptoms - they spread rapidly",
                    "❌ Don't use same tools across healthy and infected plants without sterilization"
                ],
                time_to_cure="2-4 weeks with consistent treatment",
                severity_level="High - Can cause 20-50% yield loss if untreated",
                emergency_contact="Contact local agricultural extension officer immediately for severe outbreaks"
            ),
            
            "Blast": DiseaseRemedy(
                disease_name="Rice Blast",
                cause="Fungus Magnaporthe oryzae (Pyricularia oryzae)",
                immediate_actions=[
                    "🚨 Identify blast type: leaf blast, neck blast, or node blast for targeted treatment",
                    "✂️ Remove heavily infected leaves and destroy by burning",
                    "💧 Reduce water stress - maintain consistent moisture levels",
                    "🌾 Inspect entire field and mark severity zones for treatment priority",
                    "📊 Record weather conditions - blast worsens in cool, humid weather"
                ],
                chemical_treatment=[
                    RemedyStep(
                        1,
                        "Apply Tricyclazole Fungicide",
                        "Use Tricyclazole 75% WP at 0.6g per liter. This is the most effective fungicide for blast. Spray at tillering and booting stages.",
                        "💊"
                    ),
                    RemedyStep(
                        2,
                        "Carbendazim Treatment",
                        "Apply Carbendazim 50% WP at 1g per liter for systemic control. Use when disease is in early stages.",
                        "🧪"
                    ),
                    RemedyStep(
                        3,
                        "Isoprothiolane Application",
                        "Use Isoprothiolane 40% EC at 1.5ml per liter water. Highly effective for neck blast. Apply during heading stage.",
                        "💉"
                    ),
                    RemedyStep(
                        4,
                        "Combination Spray",
                        "Mix Tricyclazole + Hexaconazole for enhanced protection. Apply every 10-12 days during favorable disease conditions.",
                        "🔬"
                    )
                ],
                organic_treatment=[
                    RemedyStep(
                        1,
                        "Neem-Based Treatment",
                        "Apply Neem oil (Azadirachtin 1%) at 5ml per liter. Add Tween-20 as spreader. Spray weekly.",
                        "🌿"
                    ),
                    RemedyStep(
                        2,
                        "Trichoderma Application",
                        "Mix Trichoderma viride (2 x 10^8 spores/g) at 5g per liter for foliar spray and 10kg per hectare for soil application.",
                        "🦠"
                    ),
                    RemedyStep(
                        3,
                        "Silicon Treatment",
                        "Apply Silicon fertilizer (Potassium Silicate) to strengthen cell walls. Use 2ml per liter as foliar spray.",
                        "⚗️"
                    ),
                    RemedyStep(
                        4,
                        "Cow Urine Solution",
                        "Ferment cow urine for 15 days, dilute 1:10 with water. Add neem leaves. Spray every 7 days.",
                        "🐄"
                    )
                ],
                preventive_measures=[
                    "🌾 Use resistant varieties: Plant varieties like Tetep, Carreon, Pi-ta, Pi-54 gene varieties",
                    "🌱 Seed treatment: Treat seeds with Tricyclazole @ 2g per kg of seeds before sowing",
                    "💊 Prophylactic spray: Apply Tricyclazole at tillering stage as preventive measure",
                    "🌿 Split nitrogen: Apply nitrogen in 3-4 splits instead of bulk application",
                    "💧 Water management: Avoid water stress during critical growth stages",
                    "📏 Optimal spacing: Use 20x20cm spacing for better air flow and reduced humidity",
                    "🍂 Remove stubble: Clean field thoroughly after harvest - fungus survives in crop residue",
                    "🌡️ Monitor weather: Be extra vigilant during cool (20-25°C) and humid conditions"
                ],
                dos=[
                    "✅ Spray fungicides during early morning or evening for better absorption",
                    "✅ Use spreader-sticker with fungicides for improved coverage",
                    "✅ Rotate fungicides to prevent resistance development",
                    "✅ Apply potassium and silicon fertilizers to strengthen plants",
                    "✅ Monitor disease severity regularly using assessment scales",
                    "✅ Adjust spray frequency based on weather conditions",
                    "✅ Ensure complete coverage of leaves, especially undersides"
                ],
                donts=[
                    "❌ Don't apply excessive nitrogen - it increases blast susceptibility",
                    "❌ Don't skip prophylactic sprays in blast-prone areas",
                    "❌ Don't use only one fungicide repeatedly - rotate chemicals",
                    "❌ Don't ignore neck blast - it causes severe yield loss",
                    "❌ Don't spray when rain is imminent",
                    "❌ Don't use contaminated irrigation water",
                    "❌ Don't let infected stubble remain in field after harvest"
                ],
                time_to_cure="3-5 weeks with intensive fungicide schedule",
                severity_level="Very High - Can cause up to 70% yield loss, especially neck blast",
                emergency_contact="Consult plant pathologist or agricultural officer for severe neck blast outbreaks"
            ),
            
            "Brownspot": DiseaseRemedy(
                disease_name="Brown Spot",
                cause="Fungus Bipolaris oryzae (Helminthosporium oryzae)",
                immediate_actions=[
                    "🔍 Check soil nutrients - brown spot indicates nutrient deficiency",
                    "🌾 Collect infected leaves for confirmation - spots should be circular with brown margins",
                    "💧 Improve water management - ensure adequate but not excessive irrigation",
                    "🌱 Assess seedling vigor - poor vigor indicates susceptibility",
                    "📝 Document spot distribution - helps identify nutrient deficiency patterns"
                ],
                chemical_treatment=[
                    RemedyStep(
                        1,
                        "Mancozeb Fungicide",
                        "Apply Mancozeb 75% WP at 2g per liter. Best broad-spectrum fungicide for brown spot. Spray at 10-day intervals.",
                        "💊"
                    ),
                    RemedyStep(
                        2,
                        "Propiconazole Application",
                        "Use Propiconazole 25% EC at 1ml per liter for systemic control. Effective for moderate to severe infections.",
                        "💉"
                    ),
                    RemedyStep(
                        3,
                        "Carbendazim + Mancozeb",
                        "Combination spray: Mix Carbendazim 12% + Mancozeb 63% WP at 2g per liter for enhanced control.",
                        "🔬"
                    ),
                    RemedyStep(
                        4,
                        "Seed Treatment",
                        "Treat seeds with Carbendazim 50% WP at 2g per kg before planting to prevent seedling infection.",
                        "🌱"
                    )
                ],
                organic_treatment=[
                    RemedyStep(
                        1,
                        "Neem Oil Spray",
                        "Mix neem oil 5ml per liter with liquid soap. Spray weekly on infected plants for fungal control.",
                        "🌿"
                    ),
                    RemedyStep(
                        2,
                        "Trichoderma Treatment",
                        "Apply Trichoderma harzianum at 5g per liter as foliar spray. Also mix in soil at 5kg per hectare.",
                        "🦠"
                    ),
                    RemedyStep(
                        3,
                        "Panchagavya Application",
                        "Spray Panchagavya (fermented cow products) at 3% solution to boost plant immunity and disease resistance.",
                        "🐄"
                    ),
                    RemedyStep(
                        4,
                        "Baking Soda Solution",
                        "Mix 1 tablespoon baking soda + few drops vegetable oil in 1 liter water. Spray to change leaf surface pH.",
                        "🧂"
                    )
                ],
                preventive_measures=[
                    "🌾 Use healthy seeds: Source certified seeds from disease-free areas",
                    "🌱 Seed treatment mandatory: Treat all seeds with Carbendazim or Thiram before planting",
                    "🌿 Balanced nutrition: Apply NPK fertilizers as per soil test - especially focus on potassium",
                    "📊 Soil testing: Conduct soil tests and correct nutrient deficiencies before planting",
                    "💧 Avoid water stress: Maintain consistent moisture - water stress increases susceptibility",
                    "🌡️ Proper nutrition timing: Apply potassium at tillering and panicle initiation stages",
                    "🍂 Field sanitation: Remove and destroy infected stubble and plant debris",
                    "🌾 Use resistant varieties: Choose varieties with moderate resistance to brown spot"
                ],
                dos=[
                    "✅ Apply potassium sulfate or muriate of potash to strengthen plants",
                    "✅ Maintain soil pH between 5.5-6.5 for optimal nutrient availability",
                    "✅ Apply organic matter to improve soil health",
                    "✅ Use balanced fertilization - avoid nitrogen excess",
                    "✅ Treat seeds before every planting season",
                    "✅ Monitor seedlings closely - early detection is key",
                    "✅ Apply foliar zinc and iron if deficiency symptoms appear"
                ],
                donts=[
                    "❌ Don't plant in nutrient-deficient soils without correction",
                    "❌ Don't use seeds from infected crops",
                    "❌ Don't over-apply nitrogen fertilizer",
                    "❌ Don't ignore soil testing - brown spot loves poor soils",
                    "❌ Don't allow water stress during critical stages",
                    "❌ Don't use untreated seeds - seed infection is common",
                    "❌ Don't skip potassium application - it's crucial for resistance"
                ],
                time_to_cure="2-3 weeks with proper fungicide and nutrition management",
                severity_level="Medium - Causes 10-20% yield loss, more severe in nutrient-poor soils",
                emergency_contact="Contact soil testing lab and agricultural extension for nutrient management advice"
            )
        }


def get_remedy_html(disease_name: str) -> str:
    """
    Generate HTML formatted remedy information for display.
    
    Args:
        disease_name: Name of the disease
        
    Returns:
        HTML string with formatted remedy information
    """
    service = DiseaseRemedyService()
    remedy = service.get_remedy(disease_name)
    
    if not remedy:
        return "<p>No remedy information available for this disease.</p>"
    
    html = f"""
    <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #28a745;'>
        <h3 style='color: #28a745; margin-top: 0;'>🏥 Complete Cure & Treatment Guide</h3>
        
        <div style='background-color: white; padding: 15px; border-radius: 5px; margin: 10px 0;'>
            <h4 style='color: #dc3545;'>⚠️ Severity: {remedy.severity_level}</h4>
            <p><strong>⏱️ Expected Recovery Time:</strong> {remedy.time_to_cure}</p>
            <p><strong>🔬 Cause:</strong> {remedy.cause}</p>
        </div>
        
        <div style='background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #ffc107;'>
            <h4 style='color: #856404; margin-top: 0;'>🚨 IMMEDIATE ACTIONS REQUIRED</h4>
            <ul style='margin: 10px 0;'>
                {''.join(f"<li>{action}</li>" for action in remedy.immediate_actions)}
            </ul>
        </div>
    </div>
    """
    
    return html


if __name__ == "__main__":
    # Test the module
    service = DiseaseRemedyService()
    print("Available diseases:", service.get_all_diseases())
    
    remedy = service.get_remedy("Bacterialblight")
    if remedy:
        print(f"\nRemedy for {remedy.disease_name}:")
        print(f"Cause: {remedy.cause}")
        print(f"Time to cure: {remedy.time_to_cure}")
        print(f"Number of chemical treatment steps: {len(remedy.chemical_treatment)}")
        print(f"Number of organic treatment steps: {len(remedy.organic_treatment)}")
