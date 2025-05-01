# various types of output
from shiny import App, render, ui, reactive
import pandas as pd    
import matplotlib

app_ui = ui.page_fluid(
    ui.output_text("show_text"),
    ui.output_text_verbatim("show_text_verbatim"),
    ui.output_data_frame("show_data_frame"),
    ui.output_table("show_table"),
    ui.output_plot("show_plot"),
    ui.output_ui("show_ui_output"),
)
# for all options see https://shiny.posit.co/py/components/#inputs

def server(input, output, session):
    fruits_df = pd.DataFrame({
        'fruit': ["banana", "kiwi", "orange"],
        'amount': [3, 7, 2]
    })
    @render.text
    def show_text():
        return fruits_df
    
    @render.text
    def show_text_verbatim():
        return fruits_df

    @render.data_frame
    def show_data_frame():
        return fruits_df
        
    @render.table
    def show_table():
        return fruits_df
        
    @render.plot
    def show_plot():
        return fruits_df.plot(kind="bar",
                              x="fruit",
                              y="amount",
                              title="fruit amounts")

    @render.ui
    def show_ui_output():
        return ui.input_checkbox_group("order",
                                       "Fruits?", 
                                       list(fruits_df['fruit'].values), 
                                       selected=[]),

app = App(app_ui, server)