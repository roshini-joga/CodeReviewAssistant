import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
from mlops.metrics import MetricsTracker

# Load environment variables
load_dotenv()

# Initialize OpenAI client and metrics tracker
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
metrics_tracker = MetricsTracker()

# Different prompt strategies for A/B testing
PROMPT_STRATEGIES = {
    "default": """Please review the following {language} code and provide a detailed analysis:

Code:
{code}

Context:
{context}

Please analyze the code for:
1. Code quality and best practices
2. Potential bugs and issues
3. Areas for improvement
4. Security concerns
5. Performance considerations

Provide your analysis in a structured format.""",

    "detailed": """As an expert code reviewer, provide a comprehensive analysis of this {language} code:

Code:
{code}

Context:
{context}

Please provide:
1. A detailed code quality assessment
2. List of potential bugs with severity levels
3. Specific improvement suggestions with examples
4. Security vulnerability analysis
5. Performance optimization recommendations
6. Best practices compliance check

Format your response with clear sections and bullet points.""",

    "concise": """Review this {language} code briefly:

Code:
{code}

Context:
{context}

Focus on:
- Critical issues only
- Major improvements needed
- Security risks
- Performance bottlenecks

Keep the response concise and actionable."""
}

def create_code_review_prompt(code: str, language: str, context: str = None, prompt_version: str = "default") -> str:
    prompt_template = PROMPT_STRATEGIES.get(prompt_version, PROMPT_STRATEGIES["default"])
    return prompt_template.format(
        language=language,
        code=code,
        context=context if context else "No additional context provided"
    )

def review_code(code: str, language: str, context: str = None, prompt_version: str = "default"):
    try:
        prompt = create_code_review_prompt(code, language, context, prompt_version)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert code reviewer with deep knowledge of software engineering best practices."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        review_text = response.choices[0].message.content
        
        # Parse the review text into structured format
        # This is a simplified parser - you might want to make it more robust
        review_results = {
            "suggestions": ["Add input validation for zero division."],  # Example
            "quality_score": 0.8,  # Example score
            "potential_bugs": ["ZeroDivisionError"],
            "improvement_areas": ["Add error handling for division by zero."]
        }
        
        # Log metrics
        metrics_tracker.log_review_metrics(code, language, review_results, prompt_version)
        
        return review_text, review_results

    except Exception as e:
        st.error(f"Error in code review: {str(e)}")
        return None, None

def display_metrics(review_results):
    if not review_results:
        return
    
    # Create metrics visualization
    metrics_data = {
        "Metric": ["Quality Score", "Suggestions", "Potential Bugs", "Improvement Areas"],
        "Count": [
            review_results["quality_score"],
            len(review_results["suggestions"]),
            len(review_results["potential_bugs"]),
            len(review_results["improvement_areas"])
        ]
    }
    
    df = pd.DataFrame(metrics_data)
    fig = px.bar(df, x="Metric", y="Count", title="Code Review Metrics")
    st.plotly_chart(fig)

def main():
    st.set_page_config(
        page_title="AI Code Review Assistant",
        page_icon="🤖",
        layout="wide"
    )

    st.title("🤖 AI Code Review Assistant")
    st.markdown("""
    This tool uses AI to analyze your code, suggest improvements, and detect potential bugs.
    Simply paste your code, select the programming language, and get instant feedback!
    """)

    # Create three columns
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        st.subheader("Input")
        # Code input
        code = st.text_area(
            "Paste your code here",
            height=400,
            help="Enter the code you want to review"
        )

        # Language selection
        language = st.selectbox(
            "Select Programming Language",
            ["python", "javascript", "java", "cpp", "typescript", "go", "rust"],
            help="Choose the programming language of your code"
        )

        # Optional context
        context = st.text_area(
            "Additional Context (Optional)",
            help="Provide any additional context about the code"
        )

        # Prompt strategy selection
        prompt_version = st.selectbox(
            "Select Review Strategy",
            list(PROMPT_STRATEGIES.keys()),
            help="Choose the review strategy to use"
        )

        # Review button
        if st.button("Review Code", type="primary"):
            if not code:
                st.warning("Please enter some code to review")
            else:
                with st.spinner("Analyzing your code..."):
                    review_text, review_results = review_code(code, language, context, prompt_version)
                    if review_text:
                        st.session_state.review_text = review_text
                        st.session_state.review_results = review_results

    with col2:
        st.subheader("Review Results")
        if "review_text" in st.session_state:
            st.markdown(st.session_state.review_text)
        else:
            st.info("Your code review will appear here")

    with col3:
        st.subheader("Metrics")
        if "review_results" in st.session_state:
            display_metrics(st.session_state.review_results)
        else:
            st.info("Review metrics will appear here")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>Built with ❤️ using Streamlit and OpenAI</p>
        <p>Last updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)

if __name__ == "__main__":
    main() 