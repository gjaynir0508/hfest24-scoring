import os
from normalize import normalize_and_save_results

panels = [2, 3]

for panel in panels:
    # make sure marksheets folder exists with panel csv files
    marksheets_folder = "marksheets"
    marksheet_file = f"{marksheets_folder}/panel{panel:02}.csv"
    if not os.path.exists(marksheet_file):
        raise FileNotFoundError(f"File '{marksheet_file}' not found")

    normalize_and_save_results(panel)
    print(f"Panel {panel} normalization completed.")
