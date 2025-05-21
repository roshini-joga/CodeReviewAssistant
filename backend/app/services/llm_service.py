import os
from openai import OpenAI
from typing import List, Dict, Any
import json

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4"  # or "gpt-3.5-turbo" based on requirements

    def _create_code_review_prompt(self, code: str, language: str, context: str = None) -> str:
        return f"""Please review the following {language} code and provide a detailed analysis:

Code:
{code}

Context:
{context if context else 'No additional context provided'}

Please analyze the code for:
1. Code quality and best practices
2. Potential bugs and issues
3. Areas for improvement
4. Security concerns
5. Performance considerations

Provide your analysis in a structured format."""

    async def review_code(self, code: str, language: str, context: str = None) -> Dict[str, Any]:
        try:
            prompt = self._create_code_review_prompt(code, language, context)
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer with deep knowledge of software engineering best practices."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            # Parse the response and structure it
            review_text = response.choices[0].message.content
            
            # TODO: Implement proper parsing of the LLM response
            # This is a placeholder implementation
            return {
                "suggestions": [
                    "Consider adding type hints",
                    "Add docstring to function"
                ],
                "quality_score": 0.85,
                "potential_bugs": [
                    "Possible null reference in line 15"
                ],
                "improvement_areas": [
                    "Code organization",
                    "Error handling"
                ]
            }

        except Exception as e:
            raise Exception(f"Error in code review: {str(e)}")

    async def evaluate_code_quality(self, code: str, language: str) -> float:
        try:
            prompt = f"""Rate the quality of this {language} code on a scale of 0 to 1:

{code}

Consider:
- Code organization
- Naming conventions
- Error handling
- Documentation
- Best practices

Provide only a number between 0 and 1."""

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=10
            )

            score = float(response.choices[0].message.content.strip())
            return min(max(score, 0), 1)  # Ensure score is between 0 and 1

        except Exception as e:
            raise Exception(f"Error in quality evaluation: {str(e)}") 