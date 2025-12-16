import os
import csv

# === SETTINGS ===
INPUT_FILENAME = "PAR Report 16-11-2025.csv"  # exact name in Downloads
NUM_COLUMNS = 52                              # how many columns to split

# Get the Downloads folder for the current user
downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")

input_path = os.path.join(downloads_dir, INPUT_FILENAME)
output_dir = os.path.join(downloads_dir, "1-52")

# Make sure output folder exists
os.makedirs(output_dir, exist_ok=True)

# Open the main CSV and split columns
with open(input_path, "r", newline="", encoding="utf-8") as f_in:
    reader = csv.reader(f_in)

    # Read header row (column names)
    header = next(reader)

    if len(header) < NUM_COLUMNS:
        raise ValueError(
            f"CSV has only {len(header)} columns, but NUM_COLUMNS is {NUM_COLUMNS}"
        )

    # Prepare 52 writers, one per output file: 1.csv, 2.csv, ..., 52.csv
    writers = []
    out_files = []
    for i in range(NUM_COLUMNS):
        col_number = i + 1  # 1-based index for file names
        output_path = os.path.join(output_dir, f"{col_number}.csv")

        f_out = open(output_path, "w", newline="", encoding="utf-8")
        out_files.append(f_out)

        writer = csv.writer(f_out)
        # Write header for just this column
        writer.writerow([header[i]])
        writers.append(writer)

    # Now write each row's column value into its respective file
    for row in reader:
        # Make sure the row has at least NUM_COLUMNS cells
        # (if shorter, fill missing cells as empty strings)
        if len(row) < NUM_COLUMNS:
            row = list(row) + [""] * (NUM_COLUMNS - len(row))

        for i, writer in enumerate(writers):
            writer.writerow([row[i]])

# Close all output files
for f_out in out_files:
    f_out.close()

print(f"Done! Created folder '1-52' in {downloads_dir} with 1.csv to 52.csv.")
