from shiny import module, ui, render


@module.ui
def city_state_ui():
    return ui.TagList(
        ui.input_selectize("state", "State", choices=["NY", "CO", "OR", "MI"], selected="NY"),
        ui.output_ui("cities_ui")
    )


@module.server
def city_state_server(input, output, session, df):
    @output
    @render.ui
    def cities_ui():
        opts = df[df['state'] == input.state()]['city'].unique().tolist()
        return ui.input_selectize("cities", "Cities", choices=opts, selected=opts[0], multiple=True)
    return input.cities