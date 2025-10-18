# Culture Agent

An AI agent that delivers immersive, multimedia deep dives into the culture of any country.

**Live Demo:** `https://culture-agent-280879789566.me-central1.run.app/`

---

## 🎯 About The Project

This AI agent acts as a cultural anthropologist, providing rich reports on any country. It understands user requests using **GPT-4o**, which then orchestrates a set of tools to gather information: **Google Gemini** generates the core cultural analysis, the **YouTube API** finds relevant documentary videos, and the **Exa API** sources collections of cultural photos. The final output is a beautifully formatted HTML report combining text, video, and images for an engaging experience.

## 🛠️ Tech Stack

-   **Framework**: [Cycls](https://cycls.com/)
-   **Language**: Python
-   **APIs**:
    -   **OpenAI API (GPT-4o)**: For conversational logic and tool orchestration.
    -   **Google Gemini API**: For generating detailed cultural briefs.
    -   **YouTube API**: For sourcing relevant videos.
    -   **Exa API**: For semantic search to find photo collections.

## 🚀 Getting Started

To run this project locally, clone the repository, create a `.env` file with your API keys, install dependencies, and run the agent.

```bash
# 1. Clone the repository
git clone [https://github.com/your-username/Culture-Agent.git](https://github.com/your-username/Culture-Agent.git)
cd Culture_Agent

# 2. Create and populate your .env file with all required keys
# Example: echo "OPENAI_API_KEY=sk-..." > .env
# Required keys: CYCLS_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY, YOUTUBE_API_KEY, EXA_API_KEY
```
## Make the AI you love, Cycls does the rest.
