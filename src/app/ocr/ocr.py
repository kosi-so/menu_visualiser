import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
import re

# Load Azure credentials from .env
load_dotenv()
endpoint = os.getenv("AZURE_ENDPOINT")
key = os.getenv("AZURE_KEY")

# Initialize Azure Document Intelligence client
client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def extract_menu_items(image_path: str) -> list[str]:
    """
    Extracts food items (line-by-line) from a menu image using Azure Document Intelligence Read model.
    Returns a list of cleaned food item lines.
    """
    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id="prebuilt-read",
            body=f,
            content_type="application/octet-stream"
        )
        result = poller.result()

    # Extract lines from OCR result
    raw_lines = [line.content.strip() for page in result.pages for line in page.lines if line.content.strip()]

    # Optional: clean bullet points or stray symbols
    cleaned_lines = []
    for line in raw_lines:
        line = re.sub(r"^[•\-–\d\.\s]*", "", line)  # remove bullets/numbers
        cleaned_lines.append(line.strip())
    return cleaned_lines

# # Example usage
# if __name__ == "__main__":
#     menu_image_path = "src/assets/sample2.jpg"  # Update to your image path
#     items = extract_menu_items(menu_image_path)

#     print("\nExtracted Menu Items:")
#     for item in items:
#         print("-", item)
