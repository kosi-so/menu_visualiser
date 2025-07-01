import argparse
from pathlib import Path

from src.app.image_gen import build_prompt, generate_image, get_openai_client



# ---- Main CLI ----
def main():
    parser = argparse.ArgumentParser(description="Generate a realistic food image using Azure DALL·E 3.")
    parser.add_argument("--name", required=True, help="Name of the meal (e.g., Beef Rendang)")
    parser.add_argument("--description", help="Optional description of the meal")
    parser.add_argument("--output_dir", default="src/assets", help="Directory to save generated images")

    args = parser.parse_args()
    prompt = build_prompt(args.name, args.description)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = args.name.lower().replace(" ", "_") + ".jpg"
    save_path = output_dir / filename

    client, deployment_name = get_openai_client()
    generate_image(client, deployment_name, prompt, args.name, save_path)

if __name__ == "__main__":
    main()