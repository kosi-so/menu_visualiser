import json
from src.app.ocr.ocr_pipeline import run_pipeline as run_ocr_pipeline
from src.app.image_gen import generate_images  # You may need to implement this
# from src.app.nlp import ... (if needed)

def full_menu_pipeline(image_path):
    """
    1. Run OCR pipeline to extract and structure menu items.
    2. Generate images for each menu item.
    3. Return structured menu and generated images.
    """
    structured_menu_json = run_ocr_pipeline(image_path)
    
    # Parse the JSON string into a list of dictionaries
    try:
        if isinstance(structured_menu_json, str):
            structured_menu = json.loads(structured_menu_json)
        else:
            # If it's already a list/dict, use it directly
            structured_menu = structured_menu_json
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Raw response: {structured_menu_json}")
        structured_menu = []
    
    # Generate images for each menu item
    images = generate_images(structured_menu)
    
    return {
        "menu": structured_menu,
        "images": images
    }

if __name__ == "__main__":
    result = full_menu_pipeline("src/assets/sample3.jpg")
    print("Pipeline Result:")
    print(f"Menu items: {len(result['menu'])}")
    print(f"Generated images: {len(result['images'])}")
    print("\nMenu items:")
    for item in result['menu']:
        print(f"- {item.get('name', 'Unknown')}: {item.get('price', 'N/A')}")
