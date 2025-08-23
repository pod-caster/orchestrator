import app.scripter.utils.utilities as utils

class EpisodeGenerator:
    def __init__(self,discussion_cards: list , episode_configs: dict):
        self.discussion_cards = discussion_cards
        self.episode_count = episode_configs.get('episode_count', 3)
        self.min_episode_length = episode_configs.get('min_episode_length', 1)

    async def group_cards_by_episode_count(self):
        total_duration = round(sum(utils.estimate_card_minutes(card) for card in self.discussion_cards), 2)
        episode_count = utils.adjust_episode_count(total_duration, self.episode_count, self.min_episode_length)
        ideal_episode_length = total_duration / episode_count

        episodes = []
        current_episode = []
        current_duration = 0

        for card in self.discussion_cards:
            card_duration = utils.estimate_card_minutes(card)
            
            # If adding this card exceeds ideal length and we have episodes left to allocate,
            # close current episode and start a new one.
            if (current_duration + card_duration > ideal_episode_length) and (len(episodes) + 1 < episode_count):
                episode_title = " / ".join(sorted(set(c['theme'] for c in current_episode)))
                episodes.append({
                    "episode_title": episode_title,
                    "cards": current_episode,
                    "estimated_minutes": round(current_duration, 2)
                })
                current_episode = []
                current_duration = 0

            current_episode.append(card)
            current_duration += card_duration

        # Add last episode
        if current_episode:
            episode_title = " / ".join(sorted(set(c['theme'] for c in current_episode)))
            episodes.append({
                "episode_title": episode_title,
                "cards": current_episode,
                "estimated_minutes": round(current_duration, 2)
            })

        return episodes, episode_count, str(total_duration) + " minutes"


# if __name__ == "__main__":
#     cards = []
#     target_episodes = 3
#     min_episode_length = 1  # minutes

#     episodes, final_episode_count, total_duration = group_cards_by_episode_count(cards, target_episodes, min_episode_length)
