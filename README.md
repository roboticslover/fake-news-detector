# Real-Time Multilingual Fake News Detector

A Streamlit-based application that uses AI to analyze and verify news content in multiple languages, helping users identify potential fake news in real-time.

## 📋 Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Project Submission Notes](#project-submission-notes)
- [License](#license)

## ✨ Features

- **Real-time Analysis**: Get immediate feedback on the authenticity of news content
- **Multilingual Support**: Analyze content in multiple languages
- **Web Search Integration**: Utilizes DuckDuckGo search to verify claims against online sources
- **Wikipedia Integration**: Cross-references information with Wikipedia for additional verification
- **User-friendly Interface**: Clean and intuitive Streamlit interface
- **Detailed Analysis**: Provides explanation of the verification process and verdict

## 📦 Requirements

- Python 3.8 or higher
- OpenAI API key
- Internet connection for web searches and API calls

## 💻 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/roboticslover/fake-news-detector.git
   cd fake-news-detector
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a `.env` file** in the project root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🚀 Usage

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

2. **Access the application**:
   Open your web browser and navigate to `http://localhost:8501`

3. **Enter news text to verify**:
   - Paste the news content or claim that you want to fact-check
   - Click the "Verify Text" button

4. **Review the results**:
   - The system will show a verdict (REAL, FAKE, or UNCERTAIN)
   - A detailed explanation of the verification process is provided
   - Any red flags or inconsistencies will be highlighted

## ⚙️ Configuration

### API Keys
- The application uses the OpenAI API key for analysis
- You can provide your API key in two ways:
  1. Set it as an environment variable (recommended for production)
  2. Enter it in the sidebar when running the application (convenient for testing)

### Model Selection
- The application allows you to select from different OpenAI models:
  - GPT-4o (recommended for best results)
  - GPT-4-turbo
  - GPT-3.5-turbo

## 🔧 Troubleshooting

### Missing DuckDuckGo Search Package
If you see a warning about missing DuckDuckGo search functionality:
```bash
pip install -U duckduckgo-search
```

### OpenAI API Key Issues
- Ensure your API key is valid and has sufficient credits
- Check that the key is correctly set in your `.env` file or entered in the sidebar

### Connection Problems
- Check your internet connection
- Ensure that your network allows connections to OpenAI's API endpoints

## 📝 Project Submission Notes

For B.Tech final year project submission:

1. **Required Files**:
   - `app.py`: Main application code
   - `requirements.txt`: List of required packages (see below)
   - `.env`: Environment variables file (do not include your actual API key when submitting)
   - `README.md`: This documentation file

2. **Create a `requirements.txt` file** with the following content:
   ```
   streamlit>=1.32.0
   langchain>=0.1.0
   langchain-openai>=0.0.2
   langchain-community>=0.0.10
   python-dotenv>=1.0.0
   openai>=1.10.0
   duckduckgo-search>=4.1.0
   Pillow>=10.0.0
   wikipedia>=1.4.0
   ```

3. **Preparation for Demonstration**:
   - Test the application on different computers before submission
   - Prepare sample news articles (both real and fake) to demonstrate functionality
   - Create a short presentation explaining the architecture and functionality
   - Be prepared to explain how the AI models and search engines integrate to verify information

4. **Documentation**:
   - Include comments in your code
   - Prepare a short report explaining the methodology and technologies used
   - Document any limitations and future improvements

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.