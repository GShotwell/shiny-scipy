from shiny import ui, render, reactive, App, req
import pandas as pd
from pathlib import Path
from plots import temp_distirbution, daily_error
from city_state import city_state_ui, city_state_server


ui.tags.style( """
.card {
  flex: 0 0 30%; /* Adjust the width as needed */
  background-color: #f1f1f1;
  border-radius: 5px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
};

.card-row {
  display: flex;
  justify-content: space-between;
  align-items: stretch;
  flex-wrap: wrap;
}
"""
)

def divided_row(col1, col2):
    out = ui.row(
        ui.column(4, col1, {"class": "card"}),
        ui.column(8, col2, {"class": "card"}),
        {"class": "card-row"}
    )
    return out



top_filters = ui.TagList(
    ui.input_date_range("dates", "Date", start="2022-01-01", end="2022-01-30"),
    city_state_ui("city_state_selector")
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

    cities = city_state_server("city_state_selector", weather)

    @reactive.Calc
    def filtered_data():
        df = weather.copy()
        req(cities())
        df = df[df['city'].isin(cities())]
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
