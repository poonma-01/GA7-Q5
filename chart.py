# chart.py
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Styling (professional)
sns.set_style("whitegrid")
sns.set_context("talk", font_scale=1.0)

# Synthetic data generation for support response times (minutes)
rng = np.random.default_rng(seed=2025)

channels = ["Email", "Phone", "Chat", "Social"]
records = []

# Create realistic distributions (in minutes)
# Email: typically slower, longer-tail (lognormal)
# Phone: faster, concentrated low latency
# Chat: very fast but a bit variable
# Social: highly variable & often slower than chat but shorter than email
for ch in channels:
    if ch == "Email":
        # median ~120 min, long tail
        samples = rng.lognormal(mean=4.5, sigma=0.6, size=300)
    elif ch == "Phone":
        # median ~10 min, tight
        samples = rng.normal(loc=12, scale=6, size=300)
        samples = np.clip(samples, 1, None)
    elif ch == "Chat":
        # median ~5 min, low variance
        samples = rng.normal(loc=6, scale=3, size=300)
        samples = np.clip(samples, 0.5, None)
    else:  # Social
        # mixture: many quick responses + some long delays
        quick = rng.normal(loc=20, scale=8, size=220)
        slow = rng.lognormal(mean=4.0, sigma=0.9, size=80)
        samples = np.concatenate([quick, slow])
        samples = np.clip(samples, 1, None)

    for s in samples:
        records.append({"Channel": ch, "ResponseTime": float(s)})

df = pd.DataFrame.from_records(records)

# Create plot (one figure, violin plot)
plt.figure(figsize=(8, 8))  # 8x8 inches * dpi 64 -> 512x512 px
ax = sns.violinplot(x="Channel", y="ResponseTime", data=df,
                    inner="quartile", cut=0, scale="width", palette="Set2")
ax.set_title("Distribution of Customer Support Response Times by Channel", pad=14)
ax.set_ylabel("Response Time (minutes)")
ax.set_xlabel("Support Channel")

# Improve readability: show log scale tick if distribution very skewed (optional)
ax.set_ylim(0, max(300, df["ResponseTime"].quantile(0.99)))  # cap y to avoid extreme outliers visually

# Annotate medians on each violin
medians = df.groupby("Channel")["ResponseTime"].median()
for i, ch in enumerate(channels):
    med = medians.loc[ch]
    ax.text(i, med + med * 0.05, f"median: {med:.0f}m", horizontalalignment="center", fontsize=9)

# Save exactly 512x512 px
plt.tight_layout()
plt.savefig("chart.png", dpi=64, bbox_inches="tight")
plt.close()
