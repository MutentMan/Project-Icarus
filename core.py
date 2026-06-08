
import asyncio
import re
import argparse
import sys
import yaml
import json
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

# Import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from modules import email_search, phone_search, social_search, web_search, ai_analyst

console = Console()

class IcarusCore:
    def __init__(self, config_path="config.yaml"):
        self.config = self.load_config(config_path)
        self.results = []
        self.seen_entities = set()
        self.queue = [] 

    def load_config(self, path):
        try:
            with open(path, 'r') as f: return yaml.safe_load(f)
        except: return {}

    def detect_type(self, input_str):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(email_regex, input_str): return "email"
        phone_regex = r'^\+?[0-9\-\(\)\s]{7,15}$'
        if re.match(phone_regex, input_str): return "phone"
        url_regex = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        if re.match(url_regex, input_str): return "url"
        return "handle"

    async def process_entity(self, entity, entity_type, depth, max_depth, progress_callback=None):
        if entity in self.seen_entities or depth > max_depth: return None
        self.seen_entities.add(entity)
        
        if progress_callback:
            progress_callback(f"Investigating {entity} ({entity_type})...")
        
        results = {"entity": entity, "type": entity_type, "depth": depth}

        try:
            if entity_type == "email":
                res = await email_search.search_email(entity, self.config)
                results["data"] = res
                handle = entity.split('@')[0]
                if handle not in self.seen_entities:
                     self.queue.append((handle, "handle", depth + 1))

            elif entity_type == "phone":
                res = await phone_search.search_phone(entity, self.config)
                results["data"] = res
            
            elif entity_type == "handle":
                res = await social_search.search_social(entity, self.config)
                results["data"] = res

            elif entity_type == "url":
                handle = entity.rstrip('/').split('/')[-1]
                res = await social_search.search_social(handle, self.config)
                results["data"] = res

            # Document Search (for initial entity)
            if depth == 0:
                docs = web_search.search_documents(entity, self.config)
                results["documents"] = docs
            
        except Exception as e:
            results["error"] = str(e)
        
        return results

    async def run_investigation(self, start_input, max_depth=1, progress_callback=None):
        self.results = []
        self.seen_entities = set()
        self.queue = []
        
        start_type = self.detect_type(start_input)
        self.queue.append((start_input, start_type, 0))

        while self.queue:
            current_entity, current_type, current_depth = self.queue.pop(0)
            if current_depth > max_depth: continue
            
            result = await self.process_entity(current_entity, current_type, current_depth, max_depth, progress_callback)
            if result:
                self.results.append(result)

        # AI Analysis
        if self.config.get('ai_engine', {}).get('enabled'):
             if progress_callback: progress_callback("Running AI Analysis...")
             ai_summary = await ai_analyst.analyze_report(start_input, self.results, self.config)
             if ai_summary:
                 self.results.append({"type": "ai_summary", "data": ai_summary})

        self.save_reports(start_input)
        return self.results

    def display_identity_graph(self):
        console.print(Panel("[bold]Identity Graph Analysis[/bold]", style="magenta"))
        
        tree = Tree("Target Identity")
        
        social_branch = tree.add("Social Media & Networks")
        blog_branch = tree.add("Blogs & Mentions")
        doc_branch = tree.add("Found Documents")
        other_branch = tree.add("Other Linked Accounts")

        for item in self.results:
            data = item.get('data', {})
            # Docs
            if 'documents' in item:
                for doc in item['documents']:
                     doc_branch.add(f"[yellow]{doc['title']}[/yellow]: {doc['href']}")

            # Process Email Sources
            if item['type'] == 'email':
                for conn in data.get('social_media_connections', []):
                    social_branch.add(f"[blue]{conn['platform']}[/blue]: {conn['url']}")
                mx = data.get('mx_records', [])
                if mx:
                    other_branch.add(f"Email Provider: {mx[0].get('exchange')}")
            
            # Process Phone
            if item['type'] == 'phone':
                 mentions = data.get('web_mentions', [])
                 for m in mentions:
                     blog_branch.add(f"[green]Web Mention[/green]: {m['title']} ({m['href']})")

            # Process Handles
            if item['type'] == 'handle':
                if isinstance(data, list):
                    for profile in data:
                        if profile.get('exists'):
                            social_branch.add(f"[cyan]{profile['site']}[/cyan]: {profile['url']} ({profile.get('title', '')})")

        console.print(tree)

    def save_reports(self, input_str):
        sanitized = "".join(x for x in input_str if x.isalnum())
        with open(f"investigation_{sanitized}.json", 'w') as f:
            json.dump(self.results, f, indent=4, default=str)
        console.print(f"[bold green]Full Report saved to investigation_{sanitized}.json[/bold green]")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--depth", "-d", type=int, default=1)
    args = parser.parse_args()

    icarus = IcarusCore()
    # For CLI, we can use a simple print as progress_callback if we want, or just leave None
    await icarus.run_investigation(args.input, args.depth)
    icarus.display_identity_graph()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
