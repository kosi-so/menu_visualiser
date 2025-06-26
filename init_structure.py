import os
from pathlib import Path

# Define subdirectories to create
subdirs = [
    "app",
    "frontend",
    "azure",
    ".github/workflows"
]

# Define files to create
files = {
    "app": ["ocr.py", "nlp.py", "image_gen.py", "main.py"],
    "azure": ["model_deployment.yml"],
    ".github/workflows": ["ci-cd.yml"],
    ".": [".gitignore", "requirements.txt", "pyproject.toml", "README.md"]
}

# Create subdirectories
for subdir in subdirs:
    Path(subdir).mkdir(parents=True, exist_ok=True)

# Create files
for folder, file_list in files.items():
    for filename in file_list:
        file_path = Path(folder) / filename
        file_path.touch(exist_ok=True)
        print(f"Created: {file_path}")

print("\n✅ Subfolders and files created inside 'menu-visualiser'.")
