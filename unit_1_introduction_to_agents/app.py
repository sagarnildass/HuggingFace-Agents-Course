from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, load_tool, tool, VisitWebpageTool
import datetime
import requests
import pytz
import yaml
import os
from tools.final_answer import FinalAnswerTool
from Gradio_UI import GradioUI


# Define a new tool: Weather Information Fetcher
import os
import requests
from smolagents import tool
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

@tool
def get_weather(city: str) -> str:
    """
    Fetches the current weather information for a given city.

    Args:
        city: The name of the city (e.g., 'New York').

    Returns:
        str: A formatted weather report including temperature, humidity, and conditions.
    """
    try:
        # 🔒 Get API key from environment variable (NEVER hardcode it)
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not api_key:
            return "Error: API key is missing. Please set OPENWEATHERMAP_API_KEY as an environment variable."
        
        # 🌍 Build the API request URL
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        # 📡 Fetch data from OpenWeather API
        response = requests.get(url)
        
        # ❌ Handle HTTP request failure
        if response.status_code != 200:
            return f"Error: Unable to fetch weather data. HTTP Status: {response.status_code}"
        
        # 📜 Parse JSON response
        data = response.json()
        
        # ❌ Handle API-level error (e.g., city not found)
        if data.get("cod") != 200:
            return f"Error fetching weather: {data.get('message', 'Unknown error')}"

        # 🌡️ Extract weather details
        weather_desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # 📝 Format the response
        return (
            f"🌍 **Weather in {city}**:\n"
            f"- 🌤 **Condition:** {weather_desc}\n"
            f"- 🌡 **Temperature:** {temp}°C\n"
            f"- 💨 **Wind Speed:** {wind_speed} m/s\n"
            f"- 💧 **Humidity:** {humidity}%\n"
            f"- 🏋 **Pressure:** {pressure} hPa"
        )

    except Exception as e:
        return f"⚠️ Error fetching weather for '{city}': {str(e)}"



# Define a custom tool
@tool
def my_custom_tool(arg1: str, arg2: int) -> str:
    """A tool that does nothing yet 
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build?"


# Define a timezone-aware clock tool
@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        tz = pytz.timezone(timezone)
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"
        
@tool
def calculator(s: str) -> str:
    """A tool that acts as a basic calculator.
    Args:
        s: A string representation of the computation that needs to be executed (e.g., 'What is 3+2*3').
    """
    if len(s) == 0:
        return 0
    
    current_number = 0
    last_number = 0
    result = 0
    sign = '+'
    
    for i in range(len(s)):
        current_char = s[i]
        
        if current_char.isdigit():
            current_number += int(current_char)
            
        if (not current_char.isdigit() and not current_char.isspace()) or i == len(s) - 1:
            if sign == '+' or sign == '-':
                result += last_number
                last_number = current_number if sign == '+' else -current_number
            elif sign == '*':
                last_number *= current_number
            elif sign == '/':
                last_number = int(last_number / current_number)
            
            sign = current_char
            current_number = 0
    result += last_number
    return f"The result is {result}"


# Define web search tool
@tool
def web_search(query: str) -> str:
    """A tool that searches the web using DuckDuckGo.
    Args:
        query: The search query.
    """
    return f"These are the search results: {DuckDuckGoSearchTool().forward(query)}"  # ✅ Correct: Calls `.forward(query)`


# 📌 Define a new tool that calls VisitWebpageTool
@tool
def visit_webpage(url: str) -> str:
    """
    Uses VisitWebpageTool to visit a webpage and extract its content as Markdown.

    Args:
        url: The URL of the webpage to visit.

    Returns:
        str: Extracted content in Markdown format, or an error message.
    """
    return f"This is the content of the website: {VisitWebpageTool().forward(url)}"


# Load final answer tool
final_answer = FinalAnswerTool()

# Hugging Face model setup
model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,
    model_id='deepseek-ai/DeepSeek-R1-Distill-Qwen-32B',
    custom_role_conversions=None,
)

# Import tool from Hugging Face Hub
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

# Load prompt templates
with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)

# Initialize the agent with multiple tools
agent = CodeAgent(
    model=model,
    tools=[
        final_answer,
        calculator,
        web_search,  # Enables web search via DuckDuckGo
        visit_webpage,
        image_generation_tool,  # Enables text-to-image generation
        get_weather,  # Enables weather fetching
        get_current_time_in_timezone,  # Enables timezone-based time retrieval
    ],
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name="Enhanced CodeAgent",
    description="An AI agent with web search, image generation, weather, and timezone utilities.",
    prompt_templates=prompt_templates
)

# Launch Gradio UI
GradioUI(agent).launch()
