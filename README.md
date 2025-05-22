# AI Code Review Assistant

An intelligent code review system that leverages Large Language Models (LLMs) to analyze code, suggest improvements, and detect potential bugs. Built with Streamlit for a simple and intuitive user interface.

<img width="1704" alt="Screenshot 2025-05-21 at 5 30 10 PM" src="https://github.com/user-attachments/assets/37101fa0-a9b8-48f5-a875-e7050700913c" />

## Features

- 🤖 AI-powered code analysis and suggestions
- 📊 Code quality metrics visualization
- 🔄 Automated code review suggestions
- 🧪 A/B testing of different prompt strategies
- 📱 Simple and intuitive web interface

## Setup Instructions

1. Clone the repository
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)
2. Paste your code in the input area
3. Select the programming language
4. (Optional) Add any additional context
5. Click "Review Code" to get AI-powered feedback

## MLOps Integration

The project can be integrated with MLOps tools:

- MLflow for experiment tracking
- DVC for data versioning
- Prometheus/Grafana for monitoring

## Team Members and Contributions

### Roshini Joga:
- Led traditional ML pipeline, Preprocessing and feature engineering, documentation.
### Shruti Goyal:
- Led transformer model integration, tokenization, model comparison.
### Siri Batchu:
- Led Streamlit UI development, metrics visualization, API integration.
### All members contributed to design, testing, and reporting.

## License

MIT License

## Contact

[To be filled with contact information] 
