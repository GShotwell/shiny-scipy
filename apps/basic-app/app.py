from shiny import ui, render, reactive, App
import pandas as pd
from pathlib import Path
from plots import temp_distirbution, daily_error

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_date_range(
                "dates",
                "Date",
                start="2022-01-01",
                end="2022-01-30",
            )
        ),
        ui.panel_main(
            ui.output_plot("error_distribution"),
            ui.output_plot("error_by_day"),
            ui.input_slider("alpha", "Plot Alpha", value=0.5, min=0, max=1),
        ),
    )
)


def server(input, output, session):
    infile = Path(__file__).parent / "weather.csv"
    weather = pd.read_csv(infile)
    weather["error"] = weather["observed_temp"] - weather["forecast_temp"]

    @reactive.Calc
    def filtered_data():
        df = weather.copy()
        df["date"] = pd.to_datetime(df["date"])
        dates = pd.to_datetime(input.dates())
        df = df[(df["date"] > dates[0]) & (df["date"] <= dates[1])]
        return df

    @output
    @render.plot
    def error_distribution():
        return temp_distirbution(filtered_data())

    @output
    @render.plot
    def error_by_day():
        return daily_error(filtered_data(), input.alpha())


app = App(app_ui, server)
