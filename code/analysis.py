"""
Revisiting the Digital Growth Puzzle

Authors:
Rishabh Jaiswal
Priyanka Saxena

This script reproduces all results from the paper.
"""
# ============================================
# 1. IMPORT LIBRARIES
# ============================================
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

# ============================================
# 2. LOAD + CLEAN DATA
# ============================================
df = pd.read_excel("../data/raw_data.xlsx")

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Keep only required variables
df = df[['country','year','gdp_growth','internet_users','gdp_per_capita']].dropna()

# Rename
df = df.rename(columns={
    'internet_users': 'internet',
    'gdp_per_capita': 'gdp_pc'
})

# ============================================
# 3. DATA PREPARATION
# ============================================
df = df.sort_values(['country','year'])

df = df[df['gdp_pc'] > 0]
df['log_gdp_pc'] = np.log(df['gdp_pc'])

# Center internet (fix multicollinearity)
df['internet_c'] = df['internet'] - df['internet'].mean()
df['internet_sq'] = df['internet_c']**2

# Interaction (convergence test)
df['interaction'] = df['internet'] * df['log_gdp_pc']

# Lag (for IV)
df['internet_lag'] = df.groupby('country')['internet'].shift(1)

# Time trend
df['trend'] = df['year'] - df['year'].min()

df = df.dropna()

# ============================================
# 4. PANEL FIXED EFFECTS (MAIN MODEL)
# ============================================
df_panel = df.set_index(['country','year'])

model_fe = PanelOLS.from_formula(
    'gdp_growth ~ internet + log_gdp_pc + EntityEffects + TimeEffects',
    data=df_panel
).fit(cov_type='clustered', cluster_entity=True)

print("\n===== PANEL FIXED EFFECTS =====")
print(model_fe.summary)

# ============================================
# 5. QUADRATIC MODEL
# ============================================
model_quad = PanelOLS.from_formula(
    'gdp_growth ~ internet_c + internet_sq + log_gdp_pc + EntityEffects + TimeEffects',
    data=df_panel
).fit(cov_type='clustered', cluster_entity=True)

print("\n===== QUADRATIC MODEL =====")
print(model_quad.summary)

# Turning point
b1 = model_quad.params['internet_c']
b2 = model_quad.params['internet_sq']
turning_point = -b1 / (2 * b2)

print("Turning Point:", turning_point)

# ============================================
# 6. INTERACTION (CONVERGENCE TEST)
# ============================================
model_int = PanelOLS.from_formula(
    'gdp_growth ~ internet + interaction + log_gdp_pc + EntityEffects + TimeEffects',
    data=df_panel
).fit(cov_type='clustered', cluster_entity=True)

print("\n===== INTERACTION MODEL =====")
print(model_int.summary)

# ============================================
# 7. MANUAL IV (CLEAN VERSION)
# ============================================
df_reset = df_panel.reset_index()

# First stage
first_stage = smf.ols(
    'internet ~ internet_lag + log_gdp_pc + trend',
    data=df_reset
).fit()

df_reset['internet_hat'] = first_stage.predict(df_reset)

print("\n===== FIRST STAGE =====")
print(first_stage.summary())

# Second stage
second_stage = smf.ols(
    'gdp_growth ~ internet_hat + log_gdp_pc + trend + C(country) + C(year)',
    data=df_reset
).fit(cov_type='cluster', cov_kwds={'groups': df_reset['country']})

print("\n===== SECOND STAGE (IV) =====")
print(second_stage.summary())

# ============================================
# 8. HETEROGENEITY (STRONG SIGNAL)
# ============================================
median = df_reset['gdp_pc'].median()

df_high = df_reset[df_reset['gdp_pc'] > median]
df_low = df_reset[df_reset['gdp_pc'] <= median]

model_high = smf.ols(
    'gdp_growth ~ internet + log_gdp_pc',
    data=df_high
).fit()

model_low = smf.ols(
    'gdp_growth ~ internet + log_gdp_pc',
    data=df_low
).fit()

print("\n===== HIGH INCOME =====")
print(model_high.summary())

print("\n===== LOW INCOME =====")
print(model_low.summary())
