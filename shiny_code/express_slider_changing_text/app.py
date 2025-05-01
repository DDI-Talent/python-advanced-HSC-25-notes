# shiny express example
from shiny.express import input, render, ui

with ui.panel_fixed():
    ui.input_slider("investment", "N", 0, 100, 20)
    
    @render.text    
    def earnings():
        new_number = input.investment() *2
        return f"2*n is {new_number}"