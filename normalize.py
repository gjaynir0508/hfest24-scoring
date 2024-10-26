# %% [markdown]
# # Hacktoberfest 2024 Hackathon Score Normalization

# %%
from IPython.display import display_html
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import colormaps
import scipy.stats as stats


def normalize_and_save_results(panel_number: int):
    # %%
    panel_scores_csv_path = f"marksheets/panel{panel_number:02}.csv"
    panel_scores = pd.read_csv(panel_scores_csv_path)
    panel_scores = panel_scores.dropna(how="all").reset_index(drop=True)
    # rename columns to lowercase, trimmed
    panel_scores.columns = panel_scores.columns.str.strip().str.lower()
    panel_scores = panel_scores.ffill()
    panel_scores

    # %%
    raw_team_scores = panel_scores.groupby(
        "team no")["total"].mean().reset_index()
    raw_team_scores = raw_team_scores.rename(columns={"total": "raw_avg"})
    raw_team_scores

    # %%
    # Normalize the scores for each metric and then calculate the average score for each panelist
    panel_scores_normalized = panel_scores.groupby("judges")[
        ["technology", "design", "presentation",
            "collaboration", "implementation", "total"]
    ].transform(lambda x: stats.zscore(x))
    panel_scores_normalized.columns += "_norm"
    panel_scores_normalized["raw_avg_norm"] = panel_scores_normalized["total_norm"]
    panel_scores_normalized.drop(columns="total_norm", inplace=True)
    panel_scores_normalized["indiv_norm_avg"] = panel_scores_normalized.mean(
        axis=1)
    panel_scores_normalized["judges"] = panel_scores["judges"]
    panel_scores_normalized["team no"] = panel_scores["team no"].astype(int)
    panel_scores_normalized

    # %%
    # Overall average score for each team
    team_scores = panel_scores_normalized.groupby(
        "team no")[["raw_avg_norm", "indiv_norm_avg"]].mean().reset_index()
    team_scores

    # %%
    team_scores["raw_avg_norm_cdf_scaled"] = stats.norm.cdf(
        team_scores["raw_avg_norm"]) * 5
    team_scores["indiv_norm_avg_cdf_scaled"] = stats.norm.cdf(
        team_scores["indiv_norm_avg"]) * 5
    team_scores["raw_avg"] = raw_team_scores["raw_avg"]
    team_scores

    # %%
    team_scores_sorted_by_ran = team_scores.sort_values(
        "raw_avg_norm", ascending=False)[["team no", "raw_avg_norm", "raw_avg_norm_cdf_scaled"]]
    team_scores_sorted_by_ina = team_scores.sort_values(
        "indiv_norm_avg", ascending=False)[["team no", "indiv_norm_avg", "indiv_norm_avg_cdf_scaled"]]

    # display both sorted dataframes side by side
    ran_styler = team_scores_sorted_by_ran.style.set_table_attributes(
        "style='display:inline; margin-right: 3rem'").set_caption("Sorted by raw_avg_norm")
    ina_styler = team_scores_sorted_by_ina.style.set_table_attributes(
        "style='display:inline'").set_caption("Sorted by indiv_norm_avg")
    # display_html(ran_styler._repr_html_() + ina_styler._repr_html_(), raw=True)

    team_scores_sorted_by_ran_cdf = team_scores_sorted_by_ran.sort_values(
        "raw_avg_norm_cdf_scaled", ascending=False)
    team_scores_sorted_by_ina_cdf = team_scores_sorted_by_ina.sort_values(
        "indiv_norm_avg_cdf_scaled", ascending=False)

    # display both sorted dataframes side by side
    ran_cdf_styler = team_scores_sorted_by_ran_cdf.style.set_table_attributes(
        "style='display:inline; margin-right: 3rem'").set_caption("Sorted by raw_avg_norm_cdf_scaled")
    ina_cdf_styler = team_scores_sorted_by_ina_cdf.style.set_table_attributes(
        "style='display:inline'").set_caption("Sorted by indiv_norm_avg_cdf_scaled")
    # display_html(ran_cdf_styler._repr_html_() +
    #  ina_cdf_styler._repr_html_(), raw = True)

    # %% [markdown]
    # ## Vizualization of the score normalization process

    # %%
    # Melting the dataframe for seaborn
    team_scores_melted = pd.melt(
        team_scores, id_vars=["team no"], value_vars=["raw_avg_norm_cdf_scaled", "indiv_norm_avg_cdf_scaled", "raw_avg"])

    # %%
    # draw a normal curve using sns
    sns.set_theme()
    fig, ax = plt.subplots(2, 2, figsize=(30, 15))
    sns.barplot(data=team_scores_melted, x="team no",
                y="value", hue="variable", ax=ax[0, 0])
    # Normal curve
    m = team_scores["raw_avg"].mean()
    s = team_scores["raw_avg"].std()
    l = m - 3 * s
    u = m + 3 * s
    sns.lineplot(x=np.linspace(l, u, 1000), y=stats.norm.pdf(
        np.linspace(l, u, 1000), m, s), ax=ax[0, 1])
    for row in team_scores.itertuples():
        # draw a vertical line at the raw_avg colored by team no
        ax[0, 1].axvline(row.raw_avg, linestyle="--", label=row._1, alpha=0.3,
                         color=colormaps['viridis'](row.Index/len(team_scores)))
        ax[0, 1].axvline(row.raw_avg_norm_cdf_scaled, alpha=0.5,
                         color=colormaps['viridis'](row.Index/len(team_scores)))
    ax[0, 0].set_title("Barplot of team scores")
    ax[0, 1].set_title("Normal curve and team scores")
    ax[0, 1].legend(title="Team no")
    # Heatmap of team scores
    sns.heatmap(team_scores[["raw_avg_norm", "indiv_norm_avg"]],
                annot=True, ax=ax[1, 0])
    # Heatmap of parameter-wise scores for each team
    sns.heatmap(panel_scores_normalized.groupby("team no")[
                ["technology_norm", "design_norm", "presentation_norm", "collaboration_norm", "implementation_norm"]].mean(), annot=True, ax=ax[1, 1])
    ax[1, 0].set_title("Heatmap of team scores")
    ax[1, 1].set_title("Heatmap of parameter-wise scores")
    plt.tight_layout()
    fig.savefig(
        f"normalized_results/panel{panel_number:02}/{panel_number:02}.png")

    # %% [markdown]
    # ## Export results to a CSV file

    # %%
    # export the dataframes
    team_scores_path = f"normalized_results/panel{panel_number:02}/{panel_number:02}_normalized_team_scores.csv"
    team_scores.to_csv(team_scores_path, index=False)
    team_scores_sorted_path = f"normalized_results/panel{panel_number:02}/{panel_number:02}_normalized_team_scores_sorted.csv"
    team_scores_sorted = team_scores.sort_values(
        "indiv_norm_avg_cdf_scaled", ascending=False)
    team_scores_sorted.to_csv(team_scores_sorted_path, index=False)
