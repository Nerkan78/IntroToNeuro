import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('stroop_data.csv', sep = ';')
congruent = df[df['is congruent'] == 1]['delta T']
not_congruent = df[df['is congruent'] == 0]['delta T']
bins = np.linspace(df['delta T'].min() - 0.1, df['delta T'].max() + 0.1, 20)

plt.hist(congruent, bins, alpha=0.5, label='Congruent')
plt.hist(not_congruent, bins, alpha=0.5, label='Not Congruent')
plt.xlabel('Delta T')
plt.legend(loc='upper right')
plt.savefig('hist.png')