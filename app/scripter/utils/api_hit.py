import asyncio
import time
import aiohttp

import logging
logging.basicConfig(format = '%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# import tiktoken
# encoding = tiktoken.encoding_for_model("gpt-4o-mini")

# @backoff.on_exception(backoff.expo, (socket.error, ConnectionResetError))
async def fetch_response(endpoint, headers, session, semaphore, payload, timeout):
    try:
        data = {}
        start = time.time()
        async with semaphore:
            async with session.post(endpoint, headers=headers, json=payload, timeout=timeout) as response:
                if response.status == 200: # Check if the request was successful
                    data = await response.json() # Parse JSON response data
                else:
                    print(response.headers)
                    response.raise_for_status()
        end = time.time()
        logger.info(f"Request took {round((end - start),2)} seconds")
  
        return data
    except Exception as e:
        print(e)
        time.sleep(3)
        return {}

async def make_concurrent_requests(payloads, endpoint, headers = None, concurrent_count=20, timeout = 1000, llm_provider="openai"):
    # headers = {'Query-Type': 'application/json'}

    if headers is None:
        headers = {
    'Content-Type': 'application/json'
    }

    semaphore = asyncio.Semaphore(concurrent_count)
    async with aiohttp.ClientSession() as session:
        await session.__aenter__() # start the session
        if not isinstance(payloads, list):
            result = await fetch_response(endpoint, headers, session, semaphore, payloads, timeout)
        else:
            if llm_provider == "openai":
            
                tasks = [fetch_response(endpoint, payload[1], session, semaphore, payload[0], timeout) for payload in payloads]
                result = await asyncio.gather(*tasks)
            else:
                endpoint_list = [endpoint]*len(payloads)
                tasks = [fetch_response(endpoint.replace("{{api_key}}",payload[2]), payload[1], session, semaphore, payload[0], timeout) for endpoint,payload in zip(endpoint_list,payloads)]
                result = await asyncio.gather(*tasks)
            tasks.clear()
        await session.__aexit__(None, None, None) # end the session
    return result


async def make_single_request(payload, endpoint, headers = None, concurrent_count=20, timeout = 1000):
    # headers = {'Query-Type': 'application/json'}

    if headers is None:
        headers = {
    'Content-Type': 'application/json'
    }
    
    semaphore = asyncio.Semaphore(concurrent_count)
    async with aiohttp.ClientSession() as session:
        await session.__aenter__() # start the session
        result = await fetch_response(endpoint, headers, session, semaphore, payload, timeout)
        await session.__aexit__(None, None, None) # end the session
    return result