# bike_tool/ui.py
# Colab-friendly interactive UI using ipywidgets and IPython.display
import io
import pandas as pd
from IPython.display import display, HTML, FileLink
import ipywidgets as widgets

from .data import BIKES
from .utils import (
    format_currency,
    build_comparison_df,
    emi_breakdown_for_model
)

def launch_ui():
    """
    Launch the interactive UI. Call this function in a Colab cell:
    from bike_tool.ui import launch_ui
    launch_ui()
    """
    # Widgets with placeholders
    brand_options = [("Select Brand", None)] + [(b, b) for b in sorted(BIKES.keys())]
    brand_dropdown = widgets.Dropdown(options=brand_options, value=None, description="Brand")

    model_dropdown = widgets.Dropdown(options=[("Select Model", None)], value=None, description="Model")

    # Multi-select compare list (brand + model pairs)
    compare_selector = widgets.SelectMultiple(options=[], description="Compare", rows=8)

    down_payment_input = widgets.BoundedFloatText(value=0.0, min=0.0, max=1e12, description="Down Payment ₹")
    interest_input = widgets.BoundedFloatText(value=10.0, min=0.0, max=100.0, step=0.1, description="Annual %")

    compare_button = widgets.Button(description="Show Comparison", button_style="primary")
    emi_button = widgets.Button(description="Show EMI", button_style="info")
    export_compare_btn = widgets.Button(description="Export Comparison CSV", button_style="success")
    export_emi_btn = widgets.Button(description="Export EMI CSV", button_style="success")

    # Output areas
    spec_out = widgets.Output()
    main_output = widgets.Output()
    summary_out = widgets.Output()

    # Globals for export
    _state = {"last_comparison_df": None, "last_emi_df": None}

    # Populate compare selector
    def populate_compare_selector():
        all_pairs = []
        for b in sorted(BIKES.keys()):
            for m in sorted(BIKES[b].keys()):
                all_pairs.append((f"{b} {m}", (b, m)))
        compare_selector.options = all_pairs

    populate_compare_selector()

    # Show specs immediately when both brand and model are selected
    def show_selected_specs(brand, model):
        with spec_out:
            spec_out.clear_output()
            if not brand or not model:
                print("Select a brand and model to view specifications.")
                return
            specs_dict = BIKES[brand][model].copy()
            display_dict = specs_dict.copy()
            if "Ex-Showroom Price" in display_dict:
                display_dict["Ex-Showroom Price"] = format_currency(display_dict["Ex-Showroom Price"])
            df = pd.DataFrame.from_dict(display_dict, orient="index", columns=[f"{brand} {model}"])
            df.index.name = "Specification"
            display(HTML(f"<h4>Specifications: {brand} {model}</h4>"))
            display(df.astype(object))

    # Brand change handler
    def on_brand_change(change):
        brand = change["new"]
        if not brand:
            model_dropdown.options = [("Select Model", None)]
            model_dropdown.value = None
            down_payment_input.max = 1e12
            with spec_out:
                spec_out.clear_output()
                print("Select a brand and model to view specifications.")
            return
        models = sorted(BIKES[brand].keys())
        model_dropdown.options = [("Select Model", None)] + [(m, m) for m in models]
        model_dropdown.value = None
        down_payment_input.max = 1e12
        with spec_out:
            spec_out.clear_output()
            print("Select a model to view specifications.")

    brand_dropdown.observe(on_brand_change, names="value")

    # Model change handler
    def on_model_change(change):
        brand = brand_dropdown.value
        model = change["new"]
        if not brand or not model:
            with spec_out:
                spec_out.clear_output()
                print("Select a brand and model to view specifications.")
            down_payment_input.max = 1e12
            return
        price = float(BIKES[brand][model]["Ex-Showroom Price"])
        down_payment_input.max = price
        show_selected_specs(brand, model)

    model_dropdown.observe(on_model_change, names="value")

    # Compare handler
    def on_compare_clicked(b):
        with main_output:
            main_output.clear_output()
            selected = list(compare_selector.value)
            if len(selected) < 2:
                print("Select at least two bikes to compare.")
                return
            df = build_comparison_df(selected)
            df_display = df.copy().astype(object)
            if "Ex-Showroom Price" in df_display.index:
                df_display.loc["Ex-Showroom Price"] = df.loc["Ex-Showroom Price"].apply(format_currency)
            _state["last_comparison_df"] = df_display
            display(HTML("<h3>Bike Comparison</h3>"))
            display(df_display)

            # Quick summary
            try:
                prices = df.loc["Ex-Showroom Price"].astype(float)
                cheapest = prices.idxmin()
                power = df.loc["Max Power bhp"].astype(float)
                most_powerful = power.idxmax()
                mileage = df.loc["Mileage kmpl"].astype(float)
                best_mileage = mileage.idxmax()
                with summary_out:
                    summary_out.clear_output()
                    display(HTML("<h4>Quick Summary</h4>"))
                    print(f"Cheapest: {cheapest}")
                    print(f"Most Powerful: {most_powerful}")
                    print(f"Best Mileage: {best_mileage}")
            except Exception:
                pass

    compare_button.on_click(on_compare_clicked)

    # EMI handler
    def on_emi_clicked(b):
        with main_output:
            main_output.clear_output()
            brand = brand_dropdown.value
            model = model_dropdown.value
            if not brand or not model:
                print("Select a brand and model first.")
                return
            dp = float(down_payment_input.value)
            rate = float(interest_input.value)
            emi_df = emi_breakdown_for_model(brand, model, down_payment=dp, annual_rate=rate)
            _state["last_emi_df"] = emi_df
            display(HTML(f"<h3>EMI Breakdown for {brand} {model}</h3>"))
            display(emi_df)

    emi_button.on_click(on_emi_clicked)

    # Export helpers
    def export_df_to_csv(df, filename):
        buffer = io.StringIO()
        df.to_csv(buffer)
        buffer.seek(0)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(buffer.getvalue())
        return filename

    def on_export_compare(b):
        with main_output:
            if _state["last_comparison_df"] is None:
                print("No comparison to export.")
                return
            fname = export_df_to_csv(_state["last_comparison_df"], "bike_comparison.csv")
            display(FileLink(fname))

    def on_export_emi(b):
        with main_output:
            if _state["last_emi_df"] is None:
                print("No EMI table to export.")
                return
            fname = export_df_to_csv(_state["last_emi_df"], "emi_breakdown.csv")
            display(FileLink(fname))

    export_compare_btn.on_click(on_export_compare)
    export_emi_btn.on_click(on_export_emi)

    # Layout
    controls = widgets.VBox([
        widgets.HBox([brand_dropdown, model_dropdown]),
        widgets.HBox([down_payment_input, interest_input, emi_button]),
        widgets.HBox([compare_selector, compare_button]),
        widgets.HBox([export_compare_btn, export_emi_btn])
    ])

    display(controls, spec_out, main_output, summary_out)
