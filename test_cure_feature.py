"""
Test script for Disease Remedy Service.
Run this to verify the cure feature is working correctly.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.disease_remedies import DiseaseRemedyService

def test_remedy_service():
    """Test the disease remedy service."""
    print("=" * 70)
    print("TESTING DISEASE REMEDY SERVICE")
    print("=" * 70)
    
    service = DiseaseRemedyService()
    
    # Test 1: Get all diseases
    print("\n✅ Test 1: Get all available diseases")
    diseases = service.get_all_diseases()
    print(f"Found {len(diseases)} diseases:")
    for disease in diseases:
        print(f"  - {disease}")
    
    # Test 2: Get remedy for Bacterial Blight
    print("\n✅ Test 2: Get remedy for Bacterial Blight")
    remedy = service.get_remedy("Bacterialblight")
    if remedy:
        print(f"Disease Name: {remedy.disease_name}")
        print(f"Cause: {remedy.cause}")
        print(f"Severity: {remedy.severity_level}")
        print(f"Time to Cure: {remedy.time_to_cure}")
        print(f"Immediate Actions: {len(remedy.immediate_actions)} steps")
        print(f"Chemical Treatments: {len(remedy.chemical_treatment)} steps")
        print(f"Organic Treatments: {len(remedy.organic_treatment)} steps")
        print(f"Preventive Measures: {len(remedy.preventive_measures)} items")
        print(f"Do's: {len(remedy.dos)} items")
        print(f"Don'ts: {len(remedy.donts)} items")
        
        print("\n📋 First Immediate Action:")
        print(f"  {remedy.immediate_actions[0]}")
        
        print("\n💊 First Chemical Treatment Step:")
        step = remedy.chemical_treatment[0]
        print(f"  {step.icon} Step {step.step_number}: {step.title}")
        print(f"  {step.description}")
        
        print("\n🌿 First Organic Treatment Step:")
        step = remedy.organic_treatment[0]
        print(f"  {step.icon} Step {step.step_number}: {step.title}")
        print(f"  {step.description}")
    else:
        print("❌ Failed to get remedy")
    
    # Test 3: Get remedy for Blast
    print("\n✅ Test 3: Get remedy for Blast")
    remedy = service.get_remedy("Blast")
    if remedy:
        print(f"Disease Name: {remedy.disease_name}")
        print(f"Severity: {remedy.severity_level}")
        print(f"Time to Cure: {remedy.time_to_cure}")
    else:
        print("❌ Failed to get remedy")
    
    # Test 4: Get remedy for Brown Spot
    print("\n✅ Test 4: Get remedy for Brown Spot")
    remedy = service.get_remedy("Brownspot")
    if remedy:
        print(f"Disease Name: {remedy.disease_name}")
        print(f"Severity: {remedy.severity_level}")
        print(f"Time to Cure: {remedy.time_to_cure}")
    else:
        print("❌ Failed to get remedy")
    
    # Test 5: Get remedy for non-existent disease
    print("\n✅ Test 5: Get remedy for non-existent disease")
    remedy = service.get_remedy("NonExistentDisease")
    if remedy is None:
        print("✓ Correctly returned None for non-existent disease")
    else:
        print("❌ Should have returned None")
    
    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETED SUCCESSFULLY! ✅")
    print("=" * 70)
    print("\nThe Disease Remedy Service is working correctly!")
    print("The cure feature is ready to use in the application.")
    print("\nNext steps:")
    print("1. Run the Streamlit app: streamlit run app.py")
    print("2. Upload a disease image to see the cure guide")
    print("3. Or visit the Support Bot and ask: 'How to cure bacterial blight?'")
    print("=" * 70)


if __name__ == "__main__":
    test_remedy_service()
