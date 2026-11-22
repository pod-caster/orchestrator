import logging
import app.constant as constant
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()    
logger.setLevel(logging.INFO)




def prepare_input_for_research(input_dict):
    """
    Prepare input for research service.

    Parameters
    ----------
    input_dict : dict
        Input dictionary containing topic, scraper mode, user content, episode configs, and speaker details.

    Returns
    -------
    research_json : dict
        JSON object to be passed to the research service.
    links: list
        user uploaded links
    content : list
        List of user-provided content.
    to_use_research : bool
        Whether to use the research service or not.
    to_scrape: bool
        Whether to scrape in case user uploaded links

    Raises
    ------
    ValueError
        If the 'user' mode is selected but no user content is provided, or if neither 'links' nor 'content' is provided in the user content.
    """
    # Determine whether to use the research service or not
    to_use_research = True
    to_scrape = False
    # Initialize the research JSON object
    research_json = {}
    links = []
    # Get the user-provided content
    content = []
    mode = input_dict.get("scraper_mode")
    supported_modes = constant.config.get("modes")
    if mode not in supported_modes:
        logger.warning(f"Unsupported mode '{mode}' provided. Defaulting to 'research' mode.")
        mode = "researcher"

    if mode == "researcher":
        research_configs = constant.research_config
        research_json['topic'] = input_dict.get("topic")
        research_json['research_configs'] = research_configs

    else:
        # Check if the user content is provided
        user_content_dict = input_dict.get("user_content", {})
        if len(user_content_dict) == 0:
            raise ValueError("User content is required for 'user' mode.")
        
        # Get the links and content from the user content
        links = user_content_dict.get("links", [])
        content = user_content_dict.get("content", [])
        
        # Check if either links or content is provided
        if len(links) == 0 and len(content) == 0:
            raise ValueError("At least one of 'links' or 'content' must be provided in 'user_content'.")
        
        # If links are provided, set to_use_research to False
        if len(links) > 0:
            to_use_research = False
            to_scrape = True
        # If the mode is 'researcher', set the research configs
    
    
        
    # Return the research JSON object, user-provided content, and whether to use the research service or not
    return research_json, links, content, to_use_research, to_scrape

        


def get_content_from_research(research_output, user_provided_content= []):
    user_content_info = []
    status = research_output.get("status")
    if len(user_provided_content) > 0:
        user_content_info = [{"link": f"link_{idx}", "content": item_content} for idx, item_content in enumerate(user_provided_content, start=1)]

    if status != "Success":
        if len(user_content_info) == 0:
            raise ValueError("Research service failed to fetch content and there is no user given content.")
    
    content = research_output.get("output", [])
    if len(user_provided_content) > 0:
        final_content = content + user_content_info
    else:
        final_content = content
    return final_content