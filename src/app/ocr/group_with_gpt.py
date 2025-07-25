# src/app/group_with_gpt.py
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()


def get_openai_client():
    """Get Azure OpenAI client"""
    api_key = os.getenv("AZURE_OPENAI_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    if not api_key or not azure_endpoint or not deployment_name:
        raise ValueError(
            "AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, and AZURE_OPENAI_DEPLOYMENT_NAME environment variables must be set"
        )

    return AzureOpenAI(
        api_key=api_key, azure_endpoint=azure_endpoint, api_version="2024-03-01-preview"
    ), deployment_name


def group_lines_with_gpt(ocr_lines: list[str]) -> list[dict]:
    """Group the lines of a menu into items."""

    # Initialize client
    client, deployment_name = get_openai_client()

    prompt = f"""
You are a helpful assistant. The following lines were extracted from a restaurant menu using OCR.

Please extract and group the items. Each item should have:
- name
- description
- price

Handle varying menu formats. Output must be a JSON list of objects with fields 'name', 'price', 'description'.

Text:
{chr(10).join(ocr_lines)}

Return JSON only.
"""

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {
                "role": "system",
                "content": "You extract structured menu data from OCR text.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()
