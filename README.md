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
├── src/
│   └── app/
│       ├── main.py           # FastAPI app
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


## 🧪 Testing

Run all tests:
```bash
pytest
```

Run pre-commit hooks on all files:
```bash
pre-commit run --all-files
```

---

## 📝 Development

- Code is formatted and linted with [Ruff](https://docs.astral.sh/ruff/)
- Pre-commit hooks ensure code quality before every commit.
- Tests use mocks for Azure and OpenAI clients for fast, offline testing.

---

## 📄 License

MIT License

---

## ✨ Contributing

1. Fork the repo and create your branch.
2. Make your changes and add tests.
3. Run `pre-commit run --all-files` and `pytest`.
4. Submit a pull request!

---

## 📬 Contact

Author: Kosi  
Email: kossyfab@gmail.com

---

Let me know if you want to add usage examples, API endpoint details, or deployment instructions!
