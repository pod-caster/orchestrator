import app.scripter.utils.utilities as utils
import pandas as pd
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
                
                episode_title = " / ".join(sorted(set(c.get('theme', '') for c in current_episode)))
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
    
    import pandas as pd

    async def group_cards_by_episode_count_df(self):
        # Step 1: Convert discussion_cards into DataFrame
        df = pd.DataFrame(self.discussion_cards)
        df["card_minutes"] = df.apply(utils.estimate_card_minutes, axis=1)

        # Step 2: Compute totals
        total_duration = round(df["card_minutes"].sum(), 2)
        episode_count = utils.adjust_episode_count(
            total_duration, self.episode_count, self.min_episode_length
        )
        ideal_episode_length = total_duration / episode_count

        # Step 3: Assign cumulative duration
        df["cum_minutes"] = df["card_minutes"].cumsum()

        # Step 4: Assign episode number  
        # Greedy allocation: start new episode when cum > threshold
        thresholds = [ideal_episode_length * i for i in range(1, episode_count)]
        df["episode"] = pd.cut(
            df["cum_minutes"],
            bins=[0] + thresholds + [float("inf")],
            labels=range(1, episode_count + 1),
            include_lowest=True
        ).astype(int)

        # Step 5: Group by episode
        episodes = []
        for ep, group in df.groupby("episode"):
            episode_title = " / ".join(sorted(set(group["theme"].fillna(""))))
            if not episode_title:
                episode_title = f"Episode {ep}"
            if len(group) == 0:
                continue
            episodes.append({
                "episode_title": episode_title,
                "cards": group.to_dict(orient="records"),
                "estimated_minutes": round(group["card_minutes"].sum(), 2)
            })

        return episodes, episode_count, f"{total_duration} minutes"



# if __name__ == "__main__":
#     cards = []
#     target_episodes = 3
#     min_episode_length = 1  # minutes

#     episodes, final_episode_count, total_duration = group_cards_by_episode_count(cards, target_episodes, min_episode_length)
