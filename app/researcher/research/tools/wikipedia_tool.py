import wikipedia
import wikipediaapi
from urllib.parse import quote

class WikipediaTool:
    def __init__(self, language: str = "en", user_agent: str = "AI-Podcast-Generator/1.0"):
        self.wiki = wikipediaapi.Wikipedia(language=language, user_agent=user_agent)
        self.base_url = f"https://{language}.wikipedia.org/wiki/"

    def resolve_title(self, topic: str) -> str:
        """Search for best matching title."""
        try:
            search_results = wikipedia.search(topic)
            if search_results:
                return search_results[0]
        except Exception as e:
            print(f"[WikipediaTool][resolve_title] Error: {e}")
        return topic  # fallback

    def get_content_and_link(self, topic: str, summary_only: bool = False, length: int = 800) -> dict:
        """Fetch resolved content and link for a topic."""
        resolved_title = self.resolve_title(topic)
        page = self.wiki.page(resolved_title)

        if not page.exists():
            return {"link": None, "content": None}

        content = page.summary[:length] if summary_only else page.text
        link = self.base_url + quote(page.title.replace(" ", "_"))
        return {"link": link, "content": content}

    def get_batch(self, topics: list[str], summary_only: bool = False, length: int = 800) -> list[dict]:
        """Fetch multiple Wikipedia entries."""
        return [self.get_content_and_link(topic, summary_only=summary_only, length=length) for topic in topics]
    
    def get_wiki_topic(self, topic:str, summary_only:bool = False, length:int = 800) -> list[dict]:
        return [self.get_content_and_link(topic, summary_only=summary_only, length=length)]