# 0) Setup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from google.colab import files
uploaded = files.upload()  # pick your CSV file

# 1) Load & Clean
file_name = list(uploaded.keys())[0]
df_raw = pd.read_csv(file_name)

# Rename the 5 main numbers if they came in as "Winning Numbers" + unnamed columns
rename_map = {
    'Winning Numbers': 'Num1',
    'Unnamed: 2': 'Num2',
    'Unnamed: 3': 'Num3',
    'Unnamed: 4': 'Num4',
    'Unnamed: 5': 'Num5',
}
df = df_raw.rename(columns=rename_map)

# Keep only what we need
keep_cols = ['Draw Date', 'Num1', 'Num2', 'Num3', 'Num4', 'Num5', 'Powerball']
df = df[keep_cols].copy()

# Types
df['Draw Date'] = pd.to_datetime(df['Draw Date'], errors='coerce')
for c in ['Num1','Num2','Num3','Num4','Num5','Powerball']:
    df[c] = pd.to_numeric(df[c], errors='coerce').astype('Int64')

# Drop incomplete rows and sort oldest -> newest
df = df.dropna(subset=['Draw Date','Num1','Num2','Num3','Num4','Num5','Powerball'])
df = df.sort_values('Draw Date').reset_index(drop=True)

print(f"Rows after cleaning: {len(df)}")
display(df.head())

# 2) Frequency Analysis
# Combine all main numbers into a single Series
all_main = pd.concat([df['Num1'], df['Num2'], df['Num3'], df['Num4'], df['Num5']])
freq_main = all_main.value_counts().sort_index()
freq_pb   = df['Powerball'].value_counts().sort_index()

# Quick table: top hot/cold numbers
hot_main = freq_main.sort_values(ascending=False).head(10)
cold_main = freq_main.sort_values(ascending=True).head(10)

print("\nTop 10 hot main numbers:\n")
display(hot_main.to_frame('count'))

print("\nTop 10 cold main numbers:\n")
display(cold_main.to_frame('count'))

print("\nPowerball frequency (full table):\n")
display(freq_pb.to_frame('count'))

# 3) Plots
plt.figure(figsize=(12,5))
freq_main.plot(kind='bar')
plt.title("Frequency of Main Numbers")
plt.xlabel("Number")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,4))
freq_pb.plot(kind='bar')
plt.title("Frequency of Powerball Numbers")
plt.xlabel("Powerball Number")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# 4) Recent-window option (bias toward recent history)
def windowed_frequencies(df, last_n_draws=None):
    """
    If last_n_draws is provided (e.g., 200), restricts analysis to most recent N draws.
    Otherwise uses entire dataset.
    """
    if last_n_draws is not None and last_n_draws > 0:
        data = df.tail(last_n_draws).copy()
    else:
        data = df.copy()

    all_main_w = pd.concat([data['Num1'], data['Num2'], data['Num3'], data['Num4'], data['Num5']])
    freq_main_w = all_main_w.value_counts().sort_index()
    freq_pb_w = data['Powerball'].value_counts().sort_index()
    return freq_main_w, freq_pb_w

# Example: last 200 draws
freq_main_recent, freq_pb_recent = windowed_frequencies(df, last_n_draws=200)
print("\nRecent-window (last 200 draws) — top 10 hot main numbers:\n")
display(freq_main_recent.sort_values(ascending=False).head(10).to_frame('count'))

# 5) Weighted Picks
def sample_without_replacement(values, weights, k):
    """np.random.choice with replace=False and weights (safe wrapper)."""
    values = np.array(values)
    weights = np.array(weights, dtype=float)
    weights = weights / weights.sum()
    # If there aren't enough distinct values with nonzero weight, backstop to uniform
    nonzero = (weights > 0)
    if nonzero.sum() < k:
        weights = np.ones_like(weights) / len(weights)
    return np.random.choice(values, size=k, replace=False, p=weights)

def build_weighted_picks(freq_main_src, freq_pb_src, k_main=5, rng_seed=None):
    """
    Pick 5 main numbers + 1 Powerball using frequency weights.
    Set rng_seed for reproducibility.
    """
    if rng_seed is not None:
        np.random.seed(rng_seed)

    # Main numbers
    main_vals = list(freq_main_src.index)
    main_wts  = freq_main_src.values
    main_pick = sample_without_replacement(main_vals, main_wts, k=k_main)

    # Powerball
    pb_vals = list(freq_pb_src.index)
    pb_wts  = freq_pb_src.values
    pb_pick = np.random.choice(pb_vals, p=(pb_wts / pb_wts.sum()))

    return sorted(main_pick.tolist()), int(pb_pick)

# 6) Generate example picks
# Option A: full-history weighted
main_full, pb_full = build_weighted_picks(freq_main, freq_pb, rng_seed=42)
print("\nFull-history weighted pick:")
print("Main:", main_full, "| Powerball:", pb_full)

# Option B: recent-window weighted (e.g., last 200 draws)
main_recent, pb_recent = build_weighted_picks(freq_main_recent, freq_pb_recent, rng_seed=42)
print("\nRecent-window (last 200) weighted pick:")
print("Main:", main_recent, "| Powerball:", pb_recent)

# 7) Generate multiple tickets
def generate_tickets(freq_main_src, freq_pb_src, n=10, rng_seed=None):
    if rng_seed is not None:
        np.random.seed(rng_seed)
    tickets = []
    for _ in range(n):
        m, p = build_weighted_picks(freq_main_src, freq_pb_src)
        tickets.append((m, p))
    return tickets

tickets_full = generate_tickets(freq_main, freq_pb, n=5, rng_seed=7)
print("\n5 tickets (full-history weighted):")
for i, (m, p) in enumerate(tickets_full, 1):
    print(f"{i:>2}: {m} | PB {p}")

# 8) (Optional) Save cleaned data and frequency tables to files
df.to_csv("powerball_clean.csv", index=False)
freq_main.to_csv("freq_main_full.csv", header=['count'])
freq_pb.to_csv("freq_powerball_full.csv", header=['count'])
print("\nSaved: powerball_clean.csv, freq_main_full.csv, freq_powerball_full.csv")
