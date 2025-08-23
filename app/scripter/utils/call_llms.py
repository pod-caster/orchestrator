import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import app.scripter.utils.constant as constant
from ..utils.api_hit import make_concurrent_requests

async def call_llms(prompt_list,llm_provider):
    if llm_provider == 'openai':
        logger.info(f"Using OpenAI model: {constant.OPENAI_MODEL}")
        payloads = [({"model": constant.OPENAI_MODEL,"messages": [{"role": "user","content": i[0]}]},{'Content-Type': 'application/json','Authorization': f'Bearer {i[1]}','Cookie': '__cf_bm=W3t8NXJeqs6LUDqzTDEl2FEzcCf66r1JFxn1l.u3z3s-1729689442-1.0.1.1-U515eDgUoGEzboTX.qKrqd.7mjFZJUCWeBb9tPqDCRSlRJ_MQmGarFQBTbe7SJztQ4rgHHPPV5CReTnejPdVAg; _cfuvid=vWhXPNMzKv2F06Emzeav2FHai8MZPZCpxB5RVXCq6Ys-1729689442491-0.0.1.1-604800000'}) for i in prompt_list]
        results = await make_concurrent_requests(payloads, constant.OPENAI_URL, concurrent_count=constant.OPENAI_CONCURRENCY_LIMIT,llm_provider=llm_provider)
    else:
        logger.info(f"Using Gemini model: {constant.GEMINI_MODEL}")
        payloads = [({"contents":[{"parts":[{"text":i[0]}]}]},{'Content-Type': 'application/json'},i[1]) for i in prompt_list]
        results = await make_concurrent_requests(payloads, constant.GEMINI_URL.replace("{{model}}",constant.GEMINI_MODEL), concurrent_count=constant.GEMINI_CONCURRENCY_LIMIT,llm_provider=llm_provider)
    return results