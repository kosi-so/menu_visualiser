from openai import AzureOpenAI
import argparse
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
import openai
import re

load_dotenv()

def sanitize_filename(name):
    """Convert menu item name to a valid filename."""
    # Replace forward slashes and other invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    # Convert to lowercase
    sanitized = sanitized.lower()
    # Remove multiple underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    return sanitized

# ---- Configuration ----
def get_openai_client():
    """Get Azure OpenAI client"""
    api_key = os.getenv("DALLE_3_KEY")
    azure_endpoint = os.getenv("DALLE_3_ENDPOINT")
    deployment_name = os.getenv("DALLE_3_DEPLOYMENT_NAME")
    
    if not api_key or not azure_endpoint or not deployment_name:
        raise ValueError(
            "DALLE_3_KEY, DALLE_3_ENDPOINT, and DALLE_3_DEPLOYMENT_NAME environment variables must be set"
        )

    client = AzureOpenAI(
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version="2024-03-01-preview"
    )
    return client, deployment_name


def build_prompt(name: str, description: str = None) -> str:
    """Build a prompt for the image generation"""

    base = f"A realistic, appetizing photo of {name}."
    if description:
        base += f" The dish is described as: {description}."
    base += " The photo should be in a restaurant menu style."
    return base

# ---- Image Generation ----
def generate_image(client, deployment_name: str, prompt: str, name: str, save_path: Path) -> None:
    print(f"[INFO] Generating image for: {name}")
    response = client.images.generate(
        prompt=prompt,
        model=deployment_name,   # now using the correct deployment name!
        n=1,
        size="1024x1024",
        quality="standard",
        response_format="url"
    )
    image_url = response.data[0].url
    # print(f"[INFO] Image URL: {image_url}")

    # Download image
    img_data = requests.get(image_url).content
    with open(save_path, "wb") as f:
        f.write(img_data)
    print(f"[SUCCESS] Image saved to {save_path}")

def generate_images(menu_items: list[dict]):
    """
    Accepts a list of menu item dicts and returns a list of image paths or image data.
    """
    client, deployment_name = get_openai_client()
    output_dir = Path("src/assets/menu2")
    output_dir.mkdir(parents=True, exist_ok=True)
    list_of_images = []
    for item in menu_items:
        prompt = build_prompt(item["name"], item["description"])
        clean_name = sanitize_filename(item["name"])
        image_path = output_dir / f"{clean_name}.jpg"
        try:
            generate_image(client, deployment_name, prompt, item["name"], image_path)
            list_of_images.append(image_path)
        except openai.BadRequestError as e:
            if "content_policy_violation" in str(e):
                print(f"[WARNING] Skipping {item['name']} due to content policy")
                continue
            else:
                raise

    return list_of_images




