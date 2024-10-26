import numpy as np
import pandas as pd

panels = [2, 3]

team_scores = pd.DataFrame()
for panel in panels:
    panel_scores_normalized = pd.read_csv(
        f"normalized_results/panel{panel:02}/{panel:02}_normalized_team_scores.csv")
    team_scores = pd.concat([team_scores, panel_scores_normalized])

team_scores = team_scores.sort_values(
    "indiv_norm_avg_cdf_scaled", ascending=False)
team_scores.to_csv("merged_results/merged_team_scores.csv", index=False)
print("Merged team scores saved to 'merged_results/merged_team_scores.csv'.")
