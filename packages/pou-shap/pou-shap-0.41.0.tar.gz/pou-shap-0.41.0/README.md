## This is a fork of a newer version of the Shap library originally created by Scott Lundberg. Unfortunately, the PyPi version (as of June 2023) is outdated with the current version of Numpy so I am creating my own private fork to work with numpy 1.24 and 1.25.


<p align="center">
  <img src="https://raw.githubusercontent.com/slundberg/shap/master/docs/artwork/shap_header.svg" width="800" />
</p>

---
![example workflow](https://github.com/slundberg/shap/actions/workflows/run_tests.yml/badge.svg)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/slundberg/shap/master)
[![Documentation Status](https://readthedocs.org/projects/shap/badge/?version=latest)](https://shap.readthedocs.io/en/latest/?badge=latest)

**SHAP (SHapley Additive exPlanations)** is a game theoretic approach to explain the output of any machine learning model. It connects optimal credit allocation with local explanations using the classic Shapley values from game theory and their related extensions (see [papers](#citations) for details and citations).

<!--**SHAP (SHapley Additive exPlanations)** is a unified approach to explain the output of any machine learning model. SHAP connects game theory with local explanations, uniting several previous methods [1-7] and representing the only possible consistent and locally accurate additive feature attribution method based on expectations (see our [papers](#citations) for details and citations).-->



## Install

SHAP can be installed from either [PyPI](https://pypi.org/project/shap) or [conda-forge](https://anaconda.org/conda-forge/shap):
