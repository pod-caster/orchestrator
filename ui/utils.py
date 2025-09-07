from better_profanity import profanity

profanity.load_censor_words()

def check_topic(topic: str) -> bool:
    return profanity.contains_profanity(topic)

# # Example
# topic = "sex and drugs"
# if check_topic(topic):
#     print("🚫 Topic flagged for profanity/explicit content")
# else:
#     print("✅ Topic is safe")
