import cycls, os, dotenv , requests, json , google.generativeai as genai
from openai import OpenAI
dotenv.load_dotenv()
CYCLS_API_KEY = os.getenv("CYCLS_API_KEY")
agent = cycls.Agent(api_key=CYCLS_API_KEY, pip=["google-generativeai", "python-dotenv", "openai", "requests", "exa_py"], copy=[".env"])
def generate_cultural_brief(country: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key: return None
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-pro', generation_config={"temperature": 0.9, "top_p": 0.95, "top_k": 40})
    prompt = f"""You are a creative cultural anthropologist. Dive deep into {country}'s culture:
CULTURAL IDENTITY: Write 2-3 paragraphs about what makes {country}'s culture unique. How do people live day-to-day? What values shape their worldview?
DAILY HABITS & RITUALS: Describe 3-4 everyday habits, routines, or social customs locals practice. Include greetings, dining etiquette, daily routines.
WEIRD & WONDERFUL: List 3-4 surprising, quirky facts about {country}'s culture - unusual traditions, superstitions, laws, behaviors that make visitors go "Really?!"
HISTORICAL ROOTS: Share 2-3 key historical events that shaped modern {country} culture. Connect past to present habits.
WHY THIS MATTERS: A reflective paragraph on what we can learn from {country}'s culture.
Be creative, thoughtful, and engaging."""
    response = model.generate_content(prompt)
    return response.text if response and response.text else None
def search_youtube_videos(country: str, query_type: str = "travel") -> dict:
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key: return {"error": "YouTube API key not configured"}
    try:
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={country} {query_type} documentary 4K&type=video&maxResults=5&key={api_key}"
        response = requests.get(url, timeout=10)
        data = response.json()
        if "items" in data:
            videos = [{"title": item["snippet"]["title"], "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}", "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]} for item in data["items"]]
            return {"success": True, "videos": videos}
        return {"error": "No videos found"}
    except Exception as e: return {"error": str(e)}
def search_images(country: str, query_type: str = "culture") -> dict:
    from exa_py import Exa
    api_key = os.getenv("EXA_API_KEY")
    if not api_key: return {"error": "Exa API key not configured"}
    try:
        exa = Exa(api_key=api_key)
        results = exa.search_and_contents(query=f"{country} {query_type} photos images", type="neural", num_results=6, text={"max_characters": 200})
        if results.results and len(results.results) > 0:
            images = [{"url": result.url, "thumb": result.url, "description": result.title or result.text[:100] if result.text else f"{country} {query_type}"} for result in results.results]
            return {"success": True, "images": images}
        return {"error": "No images found"}
    except Exception as e: return {"error": str(e)}
@agent()
async def culture_agent(context):
    import dotenv
    from openai import OpenAI
    dotenv.load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        return "❌ **Error:** OPENAI_API_KEY not configured in environment variables"
    openai_client = OpenAI(api_key=openai_api_key)
    messages = [{"role": "system", "content": """You are a passionate cultural anthropologist exploring world cultures.
Your mission: Help users discover REAL culture - habits, quirks, history, daily life.
- When users mention a country, use get_cultural_brief
- Ask about: cultural habits, unusual traditions, historical influences, weird customs
- Be enthusiastic and curious about culture
- Focus on CULTURE, HABITS, WEIRD FACTS, and HISTORY"""}, *context.messages]
    tools = [
        {"type": "function", "function": {"name": "get_cultural_brief", "description": "Get deep cultural analysis: identity, habits, weird facts, historical roots", "parameters": {"type": "object", "properties": {"country": {"type": "string", "description": "Country name"}}, "required": ["country"]}}},
        {"type": "function", "function": {"name": "get_videos", "description": "Search YouTube videos about country culture/traditions/history", "parameters": {"type": "object", "properties": {"country": {"type": "string"}, "query_type": {"type": "string", "default": "culture"}}, "required": ["country"]}}},
        {"type": "function", "function": {"name": "get_images", "description": "Search images showcasing country culture/traditions", "parameters": {"type": "object", "properties": {"country": {"type": "string"}, "query_type": {"type": "string", "default": "culture"}}, "required": ["country"]}}}
    ]
    completion = openai_client.chat.completions.create(model="gpt-4o", messages=messages, tools=tools, tool_choice="auto", temperature=0.85)
    response_msg = completion.choices[0].message
    if response_msg.tool_calls:
        for tool_call in response_msg.tool_calls:
            args = json.loads(tool_call.function.arguments) 
            if tool_call.function.name == "get_cultural_brief":
                country = args.get("country")
                result = generate_cultural_brief(country)
                if result:
                    return f"""<div style="max-width: 800px; margin: 0 auto; padding: 20px; font-family: system-ui, -apple-system, sans-serif;">
<h2 style="color: #1f2937; margin-bottom: 8px;">🌍 Deep Dive: {country} Culture</h2>
<p style="color: #6b7280; font-size: 14px; margin-bottom: 20px;">Habits • Quirks • History • Daily Life</p>
<div style="background: #f9fafb; padding: 20px; border-radius: 8px; border-left: 4px solid #3b82f6; line-height: 1.6; color: #374151;">{result}</div>
<p style="margin-top: 20px; padding: 16px; background: #eff6ff; border-radius: 8px; border-left: 4px solid #3b82f6; color: #1e40af; font-size: 14px;">
🤔 <strong>What surprised you?</strong> Ask me about: specific habits, weird traditions, historical events, or request <strong>videos/images</strong>!</p></div>"""
                else: return "❌ **Error:** GOOGLE_API_KEY not configured"
            
            elif tool_call.function.name == "get_videos":
                country, query_type = args.get("country"), args.get("query_type", "travel")
                result = search_youtube_videos(country, query_type)
                if result.get("success"):
                    videos_html = f"<h3>🎬 Videos about {country}</h3>"
                    for video in result["videos"]:
                        videos_html += f"""<div style="margin: 12px 0; padding: 12px; border: 1px solid #e1e5e9; border-radius: 8px; background: #f8f9fa;">
<div style="display: flex; align-items: center; gap: 12px;">
<img src="{video['thumbnail']}" style="width: 120px; height: 68px; border-radius: 6px; object-fit: cover;" />
<div><h4 style="margin: 0 0 4px 0; font-size: 14px; font-weight: 600;"><a href="{video['url']}" target="_blank" style="color: #2563eb; text-decoration: none;">{video['title']}</a></h4>
<p style="margin: 0; font-size: 12px; color: #6b7280;">▶️ Watch on YouTube</p></div></div></div>"""
                    return videos_html + "<p style='margin-top: 16px; font-size: 14px; color: #6b7280;'>Want images or more info? Just ask!</p>"
                else: return f"❌ **Error:** {result.get('error', 'Could not fetch videos')}"
            
            elif tool_call.function.name == "get_images":
                country, query_type = args.get("country"), args.get("query_type", "culture")
                result = search_images(country, query_type)
                if result.get("success"):
                    images_html = f"<h3>📸 Photo Collections: {country}</h3><div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin: 16px 0;'>"
                    for idx, img in enumerate(result["images"], 1):
                        desc = img["description"][:60] if img["description"] else f"{country} - Photo {idx}"
                        images_html += f"""<div style="border: 1px solid #e1e5e9; border-radius: 8px; overflow: hidden; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
<a href="{img['url']}" target="_blank" style="text-decoration: none; color: inherit;">
<div style="height: 120px; background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); display: flex; align-items: center; justify-content: center;">
<div style="text-align: center;"><div style="font-size: 32px; margin-bottom: 8px;">📸</div><div style="font-size: 12px; color: #6b7280;">Click to explore</div></div></div>
<div style="padding: 12px;"><p style="margin: 0; font-size: 13px; line-height: 1.4; color: #374151;">{desc}</p></div></a></div>"""
                    return images_html + "</div><p style='margin-top: 16px; font-size: 14px; color: #6b7280;'>Want videos or more info? Just ask!</p>"
                else: return f"❌ **Error:** {result.get('error', 'Could not fetch images')}"
    return response_msg.content or "Hello! 🌍 I'm a cultural anthropologist passionate about the weird, wonderful, and fascinating aspects of world cultures. Which country's daily life, habits, and quirks would you like to explore?"
agent.cycls(prod=True)