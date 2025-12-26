"""
AI Service for analytics and insights
"""
import openai
import google.generativeai as genai
from anthropic import Anthropic
from typing import Dict, List, Any, Optional
import json


class AIService:
    """AI service for data analysis and insights"""
    
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None):
        """
        Initialize AI service
        
        Args:
            provider: AI provider (openai, gemini, claude)
            api_key: API key for the provider
        """
        self.provider = provider
        self.api_key = api_key
        
        if provider == "openai" and api_key:
            openai.api_key = api_key
        elif provider == "gemini" and api_key:
            genai.configure(api_key=api_key)
        elif provider == "claude" and api_key:
            self.anthropic = Anthropic(api_key=api_key)
    
    def summarize_data(self, data: Dict[str, Any], context: str = "") -> str:
        """
        Generate a summary of the data
        
        Args:
            data: Data to summarize
            context: Additional context for the summary
        
        Returns:
            Summary text
        """
        prompt = f"""
        Please provide a clear and concise summary of the following analytics data:
        
        Context: {context}
        
        Data:
        {json.dumps(data, indent=2)}
        
        Focus on key insights, trends, and actionable recommendations.
        """
        
        return self._generate_response(prompt)
    
    def forecast_trend(self, historical_data: List[Dict[str, Any]], metric: str, periods: int = 7) -> Dict[str, Any]:
        """
        Forecast future trend based on historical data
        
        Args:
            historical_data: Historical data points
            metric: Metric to forecast
            periods: Number of periods to forecast
        
        Returns:
            Forecast data and confidence intervals
        """
        prompt = f"""
        Based on the following historical data, forecast the {metric} for the next {periods} periods.
        
        Historical Data:
        {json.dumps(historical_data, indent=2)}
        
        Provide:
        1. Forecasted values for each period
        2. Confidence interval (upper and lower bounds)
        3. Key factors influencing the forecast
        4. Recommendations based on the trend
        
        Format the response as JSON with keys: forecast, confidence_upper, confidence_lower, factors, recommendations
        """
        
        response_text = self._generate_response(prompt)
        
        try:
            # Try to parse as JSON
            return json.loads(response_text)
        except json.JSONDecodeError:
            # If not valid JSON, return as text
            return {
                'forecast': [],
                'analysis': response_text
            }
    
    def detect_anomalies(self, data: List[Dict[str, Any]], metric: str) -> Dict[str, Any]:
        """
        Detect anomalies in the data
        
        Args:
            data: Data to analyze
            metric: Metric to check for anomalies
        
        Returns:
            Anomaly detection results
        """
        prompt = f"""
        Analyze the following data and detect any anomalies or unusual patterns in the {metric}.
        
        Data:
        {json.dumps(data, indent=2)}
        
        For each anomaly found, provide:
        1. Date/timestamp of the anomaly
        2. Expected value vs actual value
        3. Severity (low, medium, high)
        4. Possible causes
        5. Recommended actions
        
        Format the response as JSON with an array of anomalies.
        """
        
        response_text = self._generate_response(prompt)
        
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            return {
                'anomalies': [],
                'analysis': response_text
            }
    
    def recommend_actions(self, data: Dict[str, Any], goal: str) -> List[str]:
        """
        Recommend actions based on data and goal
        
        Args:
            data: Current data/metrics
            goal: Business goal or objective
        
        Returns:
            List of recommended actions
        """
        prompt = f"""
        Based on the current data and the goal "{goal}", provide specific, actionable recommendations.
        
        Current Data:
        {json.dumps(data, indent=2)}
        
        Provide 5-10 prioritized recommendations that can help achieve the goal.
        Each recommendation should be:
        - Specific and actionable
        - Based on the data
        - Prioritized by potential impact
        
        Format as a JSON array of strings.
        """
        
        response_text = self._generate_response(prompt)
        
        try:
            recommendations = json.loads(response_text)
            if isinstance(recommendations, list):
                return recommendations
            elif isinstance(recommendations, dict) and 'recommendations' in recommendations:
                return recommendations['recommendations']
        except json.JSONDecodeError:
            pass
        
        # If parsing fails, split by lines
        return [line.strip() for line in response_text.split('\n') if line.strip()]
    
    def chat_with_data(self, question: str, data: Dict[str, Any]) -> str:
        """
        Answer questions about the data
        
        Args:
            question: User's question
            data: Available data
        
        Returns:
            Answer to the question
        """
        prompt = f"""
        Answer the following question based on the provided data:
        
        Question: {question}
        
        Available Data:
        {json.dumps(data, indent=2)}
        
        Provide a clear, concise answer. If the data doesn't contain enough information to answer the question, say so.
        """
        
        return self._generate_response(prompt)
    
    def _generate_response(self, prompt: str, max_tokens: int = 2000) -> str:
        """
        Generate AI response based on provider
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens in response
        
        Returns:
            Generated response
        """
        try:
            if self.provider == "openai":
                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a data analyst expert helping with business intelligence insights."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                return response.choices[0].message.content
            
            elif self.provider == "gemini":
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                return response.text
            
            elif self.provider == "claude":
                response = self.anthropic.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=max_tokens,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.content[0].text
            
            else:
                return "AI provider not configured"
        
        except Exception as e:
            return f"Error generating AI response: {str(e)}"
