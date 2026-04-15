# thinkpalm-agentai-Nethaji-GetItOwn_2.0
A Python-based CLI utility to view motorcycle specifications and calculate standard loan EMI breakdowns based on custom down payments.

# Bike Assistant & EMI Calculator 🏍️

A Python tool to compare motorcycle specifications and compute loan EMI breakdowns with custom down payments. Designed to run interactively in Google Colab or as a lightweight local CLI utility.

## 🚀 Features

**Hierarchical Selection**: Choose a Brand then a Model to view detailed specifications.

**Expanded Specifications**: Each model includes Ex-Showroom Price, Engine Displacement cc, Max Power bhp, Max Torque Nm, Fuel Tank Capacity L, and Mileage kmpl.

**Comparison Engine**: Select two or more bikes for a side-by-side comparison presented as a Pandas DataFrame with specs as rows and models as columns.

**EMI Calculator**: Compute EMI breakdowns for tenures 3, 6, 9, 12, 36, 60 months at a configurable annual interest rate (default 10%) with a custom down payment.

**Export**: Export the last comparison or EMI table to CSV for offline review.

## Repository Structure
bike-comparison-tool/
├─ src/
│   ├─ bike_tool/
│       ├─ __init__.py
│       ├─ data.py
│       ├─ utils.py
│       └─ ui.py
├─ Download.ipynb
├─ requirements.txt
└─ README.md


## 🛠️ Prerequisites

* Python 3.x
* Pandas library 1.3
* ipywidgets 7.6

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/Nethaji2606/thinkpalm-agentai-Nethaji-GetItOwn.git](https://github.com/Nethaji2606/thinkpalm-agentai-Nethaji-GetItOwn_2.0.git)
   cd thinkpalm-agentai-Nethaji-GetItOwn_2.0

## ▶️ How to run?
1. Upload this repo to Colab or mount from GitHub.
2. Install dependencies:
       !pip install -r requirements.txt
3. Run the UI:
       ```python
       from colab_demo import run
       run()
