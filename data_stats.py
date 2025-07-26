"""
Documentation

"""

from scipy import stats
from scipy.stats import pearsonr

def compute_t_p_values(df):
    # Example data (paired measurements)
    x = [20, 22, 19, 25, 28]
    y = [23, 25, 20, 28, 30]

    # Perform paired t-test
    t_stat, p_value = stats.ttest_rel(x, y)
    print(f"Paired t-test: t = {t_stat:.3f}, p = {p_value:.3f}")

    # Calculate Pearson's r and p-value
    r, p = pearsonr(x, y)
    print(f"Pearson's r = {r:.3f}, p = {p:.3f}")