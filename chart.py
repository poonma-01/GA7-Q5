# chart.py
# Author: 23f2003677@ds.study.iitm.ac.in
# Generates a Seaborn violinplot for customer support response times

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Set Seaborn style for professional appearance
sns.set_style('whitegrid')
sns.set_context('talk', font_scale=1.1)

# Generate synthetic data for support response times
np.random.seed(42)
channels = ['Email', 'Chat', 'Phone', 'Social Media']
response_times = []
for channel in channels:
    if channel == 'Email':
        times = np.random.normal(loc=24, scale=8, size=120)
    elif channel == 'Chat':
        times = np.random.normal(loc=6, scale=2, size=120)
    elif channel == 'Phone':
        times = np.random.normal(loc=12, scale=4, size=120)
    else:
        times = np.random.normal(loc=18, scale=6, size=120)
    response_times.extend(zip([channel]*120, times))

# Create DataFrame
support_df = pd.DataFrame(response_times, columns=['Channel', 'Response_Time'])

# Create violinplot
plt.figure(figsize=(8, 8))  # 512x512 pixels at dpi=64
ax = sns.violinplot(x='Channel', y='Response_Time', data=support_df, palette='Set2', inner='quartile')
ax.set_title('Customer Support Response Time Distribution by Channel', fontsize=16)
ax.set_xlabel('Support Channel', fontsize=14)
ax.set_ylabel('Response Time (hours)', fontsize=14)
plt.tight_layout()
plt.savefig('chart.png', dpi=64, bbox_inches='tight')
plt.close()
