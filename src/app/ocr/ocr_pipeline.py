# src/app/pipeline.py
from src.app.ocr.ocr import extract_menu_items
from src.app.ocr.group_with_gpt import group_lines_with_gpt

def run_pipeline(image_path):
    print("Running OCR...")
    lines = extract_menu_items(image_path)
    print("Running GPT structuring...")
    structured = group_lines_with_gpt(lines)
    print("Done.")
    return structured

if __name__ == "__main__":
    result = run_pipeline("src/assets/sample3.jpg")
    print(result)
