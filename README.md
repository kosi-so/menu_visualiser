# Menu Visualiser

A computer vision app that reads a menu and generates images of meals using Azure OCR, OpenAI GPT, and DALL-E3 image generation models.

---

## 🚀 Features

- **OCR Processing:** Extracts text from menu images using Azure Document Intelligence.
- **AI-Powered Structuring:** Uses GPT (via Azure OpenAI) to structure menu items (name, description, price).
- **Image Generation:** Generates images for each menu item using AI.
- **API:** FastAPI-based web service for menu processing.
- **Testing:** Comprehensive test suite with pytest and pre-commit hooks for code quality.

---

## 📦 Project Structure

```
menu_visualiser/
├── main.py                   # Streamlit app entry point
├── src/
│   └── app/
│       ├── pipeline.py       # End-to-end pipeline: OCR → GPT → image_gen
│       ├── image_gen.py      # Image generation logic
│       └── ocr/
│           ├── ocr.py            # OCR extraction
│           ├── group_with_gpt.py # GPT structuring
│           └── ocr_pipeline.py   # OCR pipeline
├── tests/
│   ├── test_ocr.py           # Unit and integration tests
│   └── conftest.py           # Test fixtures
├── pyproject.toml            # Project metadata and dependencies
├── .pre-commit-config.yaml   # Pre-commit hooks (Ruff, formatting)
├── .gitignore
└── README.md
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.12+
- Azure Document Intelligence and Azure OpenAI resources
- [uv](https://github.com/astral-sh/uv) (recommended for fast dependency management)

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd menu_visualiser
   ```

2. **Install dependencies:**
   ```bash
   uv pip install -e ".[dev]"
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```
   AZURE_ENDPOINT=...
   AZURE_KEY=...
   AZURE_OPENAI_KEY=...
   AZURE_OPENAI_ENDPOINT=...
   AZURE_OPENAI_DEPLOYMENT_NAME=...
   ```

4. **(Optional) Set up pre-commit hooks:**
   ```bash
   pre-commit install
   ```

---

## 🚦 Usage

### Run the full pipeline on an image

```bash
python -m src.app.pipeline
```
This will:
- Extract menu items from an image
- Structure them with GPT
- Generate images for each menu item

## 🌐 Streamlit App

You can interactively use the Menu Visualiser via a Streamlit web app. This provides a user-friendly interface for uploading menu images and visualising the generated results.

### Run the Streamlit App

```bash
streamlit run main.py
```

- This will launch the app in your browser at [http://localhost:8501](http://localhost:8501).
- Make sure your environment variables are set (see Installation section).
- The app will guide you through uploading a menu image, extracting items, and viewing generated images.
- **Note:** Images are stored temporarily for the session and are not persisted after the app stops.
- *(Optional)* Add a screenshot or GIF of the Streamlit app here to showcase its functionality.

## 🧪 Testing

Run all tests:
```