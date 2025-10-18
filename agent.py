import cycls, os, dotenv, requests, json, google.generativeai as genai, asyncio
from openai import OpenAI
dotenv.load_dotenv(".env")
agent = cycls.Agent(api_key=os.getenv("CYCLS_API_KEY"), pip=["google-generativeai", "python-dotenv", "openai", "requests", "exa_py"], copy=[".env"])

def get_brief(country):
    if not (key := os.getenv("GOOGLE_API_KEY")): return None
    genai.configure(api_key=key)
    prompt = f"Analyze {country} culture: IDENTITY (2-3 para unique traits, values), HABITS (3-4 daily customs), WEIRD FACTS (3-4 quirky traditions), HISTORY (2-3 key events), WHY IT MATTERS. Be engaging."
    return genai.GenerativeModel('gemini-2.5-flash', generation_config={"temperature": 0.9}).generate_content(prompt).text

def get_videos(country, qtype="culture"):
    if not (key := os.getenv("YOUTUBE_API_KEY")): return {"error": "No YouTube key"}
    try:
        data = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={country} {qtype} documentary&type=video&maxResults=5&key={key}", timeout=10).json()
        return {"success": True, "videos": [{"title": i["snippet"]["title"], "url": f"https://www.youtube.com/watch?v={i['id']['videoId']}"} for i in data.get("items", [])]} if "items" in data else {"error": "No videos"}
    except: return {"error": "API failed"}

def get_images(country, qtype="culture"):
    from exa_py import Exa
    if not (key := os.getenv("EXA_API_KEY")): return {"error": "No Exa key"}
    try:
        results = Exa(key).search_and_contents(f"{country} {qtype} photos", type="neural", num_results=6, text={"max_characters": 200})
        return {"success": True, "images": [{"url": r.url, "desc": (r.title or r.text[:60]) if r.text or r.title else f"{country}"} for r in results.results]} if results.results else {"error": "No images"}
    except: return {"error": "API failed"}

@agent()
async def culture_agent(context):
    import dotenv
    dotenv.load_dotenv(".env")
    if not (key := os.getenv("OPENAI_API_KEY")): yield "❌ OPENAI_API_KEY missing"; return
    client = OpenAI(api_key=key)
    tools = [{"type": "function", "function": {"name": n, "description": d, "parameters": {"type": "object", "properties": {"country": {"type": "string"}}, "required": ["country"]}}} for n, d in [("get_cultural_brief", "Get cultural analysis"), ("get_videos", "Search videos"), ("get_images", "Search images")]]
    resp = client.chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": "Cultural anthropologist. Use get_cultural_brief for countries. Focus on habits, quirks, history."}, *context.messages], tools=tools, tool_choice="auto", temperature=0.85).choices[0].message
    
    if resp.tool_calls:
        for tc in resp.tool_calls:
            args, fn = json.loads(tc.function.arguments), tc.function.name
            country = args.get("country")
            
            if fn == "get_cultural_brief":
                yield f'<div style="max-width:800px;margin:0 auto;padding:40px 20px;text-align:center"><div style="display:inline-block;padding:30px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);border-radius:16px;box-shadow:0 10px 40px rgba(102,126,234,0.4)"><div style="font-size:48px;margin-bottom:16px;animation:bounce 1s infinite">🌍</div><h3 style="color:white;margin:0 0 8px 0;font-size:20px">Exploring {country} Culture</h3><p style="color:rgba(255,255,255,0.9);margin:0;font-size:14px">Gathering insights...</p><div style="margin-top:20px;display:flex;justify-content:center;gap:8px"><div style="width:12px;height:12px;background:white;border-radius:50%;animation:pulse 1.4s ease-in-out infinite"></div><div style="width:12px;height:12px;background:white;border-radius:50%;animation:pulse 1.4s ease-in-out 0.2s infinite"></div><div style="width:12px;height:12px;background:white;border-radius:50%;animation:pulse 1.4s ease-in-out 0.4s infinite"></div></div></div><style>@keyframes bounce{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-10px)}}}}@keyframes pulse{{0%,100%{{opacity:0.4;transform:scale(0.8)}}50%{{opacity:1;transform:scale(1.2)}}}}</style></div>'
                await asyncio.sleep(0.5)
                
                result = get_brief(country)
                if not result: yield "❌ GOOGLE_API_KEY missing"; return
                
                vid_html = ""
                if (vr := get_videos(country, "culture")).get("success") and vr.get("videos"):
                    v = vr["videos"][0]
                    vid = v['url'].split('v=')[1].split('&')[0]
                    vid_html = f'<div style="margin:24px 0;padding:16px;border:1px solid #e1e5e9;border-radius:12px;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,0.08)"><h3 style="margin:0 0 12px 0;font-size:16px">🎬 Experience {country} Culture</h3><div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px"><iframe src="https://www.youtube.com/embed/{vid}" style="position:absolute;top:0;left:0;width:100%;height:100%;border:none" allowfullscreen allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture"></iframe></div><p style="margin:8px 0 0 0;font-size:13px;color:#6b7280">{v["title"]}</p></div>'
                
                yield f'<div style="max-width:800px;margin:0 auto;padding:20px"><h2 style="color:#1f2937;margin-bottom:8px">🌍 Deep Dive: {country} Culture</h2><p style="color:#6b7280;font-size:14px;margin-bottom:20px">Habits • Quirks • History • Daily Life</p>{vid_html}<div style="background:#f9fafb;padding:20px;border-radius:8px;border-left:4px solid #3b82f6;line-height:1.6;color:#374151">{result}</div><p style="margin-top:20px;padding:16px;background:#eff6ff;border-radius:8px;border-left:4px solid #3b82f6;color:#1e40af;font-size:14px">🤔 <strong>What surprised you?</strong> Ask about specific habits, traditions, or request <strong>videos/images</strong>!</p></div>'
                return
            
            elif fn == "get_videos":
                vr = get_videos(country, args.get("query_type", "travel"))
                if not vr.get("success"): yield f"❌ {vr.get('error')}"; return
                html = f"<div style='max-width:900px;margin:0 auto'><h3 style='color:#1f2937;margin-bottom:16px'>🎬 Videos: {country}</h3>"
                for v in vr["videos"]:
                    vid = v['url'].split('v=')[1].split('&')[0]
                    html += f'<div style="margin:20px 0;padding:16px;border:1px solid #e1e5e9;border-radius:12px;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,0.08)"><h4 style="margin:0 0 12px 0;font-size:15px">{v["title"]}</h4><div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px"><iframe src="https://www.youtube.com/embed/{vid}" style="position:absolute;top:0;left:0;width:100%;height:100%;border:none" allowfullscreen allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture"></iframe></div></div>'
                yield html + "<p style='margin-top:16px;font-size:14px;color:#6b7280'>Want images or more info? Just ask!</p></div>"
                return
            
            elif fn == "get_images":
                ir = get_images(country, args.get("query_type", "culture"))
                if not ir.get("success"): yield f"❌ {ir.get('error')}"; return
                html = f"<h3>📸 Photo Collections: {country}</h3><div style='display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:16px 0'>"
                for idx, img in enumerate(ir["images"], 1):
                    html += f'<div style="border:1px solid #e1e5e9;border-radius:8px;overflow:hidden;background:white;box-shadow:0 2px 4px rgba(0,0,0,0.1)"><a href="{img["url"]}" target="_blank" style="text-decoration:none;color:inherit"><div style="height:120px;background:linear-gradient(135deg,#f3f4f6 0%,#e5e7eb 100%);display:flex;align-items:center;justify-content:center"><div style="text-align:center"><div style="font-size:32px;margin-bottom:8px">📸</div><div style="font-size:12px;color:#6b7280">Click to explore</div></div></div><div style="padding:12px"><p style="margin:0;font-size:13px;line-height:1.4;color:#374151">{img["desc"][:60]}</p></div></a></div>'
                yield html + "</div><p style='margin-top:16px;font-size:14px;color:#6b7280'>Want videos or more info? Just ask!</p>"
                return
    
    yield resp.content or "Hello! 🌍 I'm a cultural anthropologist. Which country's culture would you like to explore?"

agent.cycls(prod=True)
