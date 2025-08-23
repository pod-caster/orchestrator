from .tools import websearch, wikipedia_tool
import logging
logging.basicConfig(format = '%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ResearchAgent:
    def __init__(self, llama_index=None):
        self.web_tool = websearch.WebSearchTool()
        self.wiki_tool = wikipedia_tool.WikipediaTool()
        self.logger = logger

    async def research(self, topic: str, research_flags: dict) -> str:
        output = {}

        if research_flags.get("serp_flag", True):
            self.logger.info("SerpAI search is enabled")
            self.logger.info("Using SerpAI to search")
            web_results = await self.web_tool.search(topic)
            self.logger.info("Done using SerpAI to search")
            output["web_results"] = web_results
        else:
            self.logger.info("SerpAI search is disabled")
            output["web_results"] = []

        if research_flags.get("wiki_flag", True):
            self.logger.info("Using Wikipedia to search")
            wiki_content = self.wiki_tool.get_wiki_topic(topic)
            self.logger.info("Done using Wikipedia to search")
            output["wiki_content"] = wiki_content
        else:
            self.logger.info("Wikipedia search is disabled")
            output["wiki_content"] = ''
        
        if research_flags.get("llama_flag", True):
            self.logger.info("Using LLamaIndex to search")
            llama_response = self.llama_tool.query(topic)
            self.logger.info("Done using LLamaIndex to search")
            output["llama_index_response"] = llama_response
        else:
            self.logger.info("LLamaIndex search is disabled")
            output["llama_index_response"] = ''

        return output
    