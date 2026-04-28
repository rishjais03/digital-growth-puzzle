# Digital Growth Puzzle

This repository contains code and data for the paper:

**"Revisiting the Digital Growth Puzzle: Internet Usage and Economic Growth in Cross-Country Panel Data"**

## Overview

This project analyzes the relationship between internet usage and economic growth using panel data.

## Reproducibility

All results in this paper can be fully reproduced using the provided code and dataset.

* Data: `/data/raw_data.xlsx`
* Code: `/code/analysis.py`
* Outputs: `/results/output.txt`

The repository is structured to ensure transparency and replicability of all findings.


## Key Result

The main finding of the analysis is a statistically significant negative relationship between internet usage and GDP growth.

* Internet coefficient ≈ **-0.078**
* Robust to instrumental variable estimation (≈ -0.084)

This suggests that macro-level regressions capture structural effects such as convergence and cross-country heterogeneity rather than direct causal impacts of digitalization.

## Limitations

This study relies on cross-country panel data, which may capture structural relationships rather than causal effects. While instrumental variable techniques are employed, full causal identification remains limited. Results should therefore be interpreted with caution.


## Paper

The full paper is available here:

[Download Paper](paper/paper.pdf)

## SSRN Version

A working paper version is available on SSRN:

https://doi.org/10.2139/ssrn.6657019




## Methods

* Panel Fixed Effects
* Instrumental Variables
* Quadratic model

## Data

World Bank + ITU


## Author

Rishabh Jaiswal

Priyanka Saxena 
