# Hacktoberfest 2024 Score Normalizer

This is a simple Python script that normalizes the scores of the Hacktoberfest 2024 participants.

## Instructions

1. Clone the repository
2. Install the required packages (numpy, pandas, scipy, matplotlib, seaborn)
3. Run the script

```bash
python normalize_all.py
```

## Expected Input and Data

There should be panel-wise marksheets in the `marksheets` directory, named `panel01.csv`, `panel02.csv`, etc.

The script expects a CSV file with the following structure

| Team No | Judges | TECHNOLOGY | DESIGN | PRESENTATION | COLLABORATION | IMPLEMENTATION | Total | Collective Total |
|---------|--------|------------|--------|--------------|---------------|----------------|-------|------------------|
| Team Number or blank if same as above row    | Judge Name | score | score | score | score | score | average score | average score from both judges optional |

Example:

```csv
Team No,Judges,TECHNOLOGY,DESIGN,PRESENTATION,COLLABORATION,IMPLEMENTATION,Total,Collective Total
110,Smt. Satya Kiranmai,2,2,2,2,2,2,1.7
, Mr.Madhukar,2,1,2,1,1,1.4,
```

## Output

The script will generate a CSV file with the normalized scores in the `normalized_results/panel{number}/` directory, named `02_normalized_team_scores.csv`, `02_normalized_team_scores.csv`, etc., a CSV file with sorted results `01_normalized_team_scores_sorted`, `02_normalized_team_scores_sorted`, etc., and a plot of the normalized scores in the `normalized_results/panel{number}/` directory, named `01.png`, `02.png`, etc.
