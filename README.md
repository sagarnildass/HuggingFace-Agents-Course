Unit 1: Introduction to Agents 🤖
=================================

Overview
--------

Link to course: https://huggingface.co/learn/agents-course/

This unit introduces a powerful AI agent built with the smolagents framework, capable of performing various tasks through a user-friendly Gradio interface. The agent combines multiple tools including web search, weather information, timezone utilities, and image generation capabilities.

Features 🌟🌟
-----------

-   Web Search: Search the internet using DuckDuckGo

-   Weather Information: Get real-time weather data for any city

-   Time Zone Utilities: Check current time in different time zones

-   Basic Calculator: Perform mathematical calculations

-   Webpage Content Extraction: Visit and extract content from webpages

-   Image Generation: Create images from text descriptions

-   Interactive UI: User-friendly Gradio interface

Installation 🛠️
----------------

-   Clone the repository

-   Install the required dependencies:

```
pip install smolagents[gradio] duckduckgo-search markdownify requests pytz python-dotenv
```

-   Set up environment variables:

Create a .env file in the root directory and add your OpenWeatherMap API key:

```
OPENWEATHERMAP_API_KEY=your_api_key_here
```
Usage 🚀
--------

-   Run the application:

```
python app.py
```
-   Open your browser and navigate to the local URL provided by Gradio (typically http://localhost:7860)

-   Start interacting with the agent through the chat interface

Architecture 🏗️
----------------

The application is built using:

-   smolagents: Core framework for agent functionality

-   Gradio: Web interface for user interaction

-   HuggingFace Models: Powered by DeepSeek-R1-Distill-Qwen-32B

-   External APIs: OpenWeatherMap for weather data

Configuration ⚙️
----------------

The agent is configured with:

-   Max tokens: 2096

-   Temperature: 0.5

-   Maximum steps: 6

-   Model: deepseek-ai/DeepSeek-R1-Distill-Qwen-32B