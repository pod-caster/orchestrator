import app.scripter.utils.utilities as utils
import pandas as pd
class EpisodeGenerator:
    def __init__(self, discussion_cards: list, episode_configs: dict):
        self.discussion_cards = discussion_cards
        self.episode_count = episode_configs.get('episode_count', 3)

    async def group_cards_by_episode_count_df(self):
        total_duration = round(sum(utils.estimate_card_minutes(card) for card in self.discussion_cards), 2)
        total_cards = len(self.discussion_cards)

        # Compute how many cards go in each episode
        base_size = total_cards // self.episode_count
        remainder = total_cards % self.episode_count

        episodes = []
        start = 0
        for i in range(self.episode_count):
            # Distribute the remainder so the split is even
            end = start + base_size + (1 if i < remainder else 0)
            current_episode = self.discussion_cards[start:end]
            current_duration = sum(utils.estimate_card_minutes(c) for c in current_episode)

            if current_episode:  # never create an empty episode
                episode_title = " / ".join(sorted(set(c['theme'] for c in current_episode)))
                episodes.append({
                    "episode_title": episode_title,
                    "cards": current_episode,
                    "estimated_minutes": round(current_duration, 2)
                })

            start = end

        return episodes, self.episode_count, str(total_duration) + " minutes"