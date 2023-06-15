from shiny import ui, render, reactive, App
import pandas as pd
from pathlib import Path
from plots import temp_distirbution, daily_error


def divided_row(col1, col2):
    out = ui.row(
        ui.column(4, col1),
        ui.column(8, col2)
    )
    return out


top_filters = ui.TagList(
    ui.input_date_range("dates", "Date", start="2022-01-01", end="2022-01-30"),
    ui.input_selectize("state", "State", choices=["NY", "CO", "OR", "MI"], selected="NY"),
    ui.output_ui("cities_ui")
    )


app_ui = ui.page_fluid(
    divided_row(top_filters, ui.output_plot("error_distribution")),
    divided_row(
        ui.input_slider("alpha", "Plot Alpha", value=0.5, min=0, max=1),
        ui.output_plot("error_by_day")
        )
)


def server(input, output, session):
    infile = Path(__file__).parent / "weather.csv"
    weather = pd.read_csv(infile)
    weather["error"] = weather["observed_temp"] - weather["forecast_temp"]

    @reactive.Calc
    def filtered_data():
        df = weather.copy()
        df = df[df['city'].isin(input.cities())]
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
    
    @output
    @render.ui
    def cities_ui():
        opts = weather[weather['state'] == input.state()]['city'].unique().tolist()
        return ui.input_selectize("cities", "Cities", choices=opts, selected=opts[0], multiple=True)


app = App(app_ui, server)
