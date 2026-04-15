# colab_demo.py
# Simple entry script to run in Colab or local Jupyter.
# Usage in Colab:
#   !pip install -r requirements.txt
#   from colab_demo import run
#   run()

from bike_tool.ui import launch_ui

def run():
    """
    Launch the interactive bike comparison UI.
    """
    launch_ui()

if __name__ == "__main__":
    run()
