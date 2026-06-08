
import requests
import json
import asyncio
from rich.console import Console
from rich.panel import Panel

console = Console()

async def analyze_report(target: str, findings: list, config: dict) -> str:
    ai_config = config.get('ai_engine', {})
    if not ai_config.get('enabled', False):
        return None

    provider = ai_config.get('provider', 'ollama')
    base_url = ai_config.get('base_url', 'http://localhost:11434/v1').rstrip('/')
    api_key = ai_config.get('api_key', 'ollama')
    model = ai_config.get('model', 'llama3')
    
    # Simplify findings to text
    findings_str = json.dumps(findings, default=str)
    
    template = ai_config.get('prompt_template', 
                           "Analyze the following OSINT data. Summarize key findings, risks, and potential connections for target: {target}.\nData: {data}")
    
    final_prompt = template.replace("{target}", target).replace("{data}", findings_str) 
    
    # Combined prompt for models that don't like system role or prefer merged context
    combined_prompt = f"System: You are a professional intelligence analyst.\n\nUser: {final_prompt}"

    # AI Settings from config
    max_tokens = ai_config.get('max_tokens', 4096)
    temperature = ai_config.get('temperature', 1.0)
    top_p = ai_config.get('top_p', 0.95)
    
    # Call API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": combined_prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "stream": False,
        "chat_template_kwargs": {"enable_thinking": True}
    }

    try:
        loop = asyncio.get_event_loop()
        url = f"{base_url}/chat/completions"
        # Increased timeout for cloud models
        response = await loop.run_in_executor(None, lambda: requests.post(url, headers=headers, json=payload, timeout=90))
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"AI Error ({provider}): API returned {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"AI Connection Failed ({provider}): {str(e)}"

if __name__ == "__main__":
    pass
