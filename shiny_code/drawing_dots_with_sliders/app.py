import matplotlib.pyplot as plt
import numpy as np
from shiny import App, render, ui, reactive

# Notes: 
# In this silly example we'll draw some dots using two sliders
# my_variable = reactive.Value( starting_value )
#         this creates a variable that is used same as input
#         to get its value use my_variable.get()  
#         to set its value use my_variable.set(new_value)
# @reactive.Effect - below function is neither input or output
#                    - but it will be triggered by some action
# @reactive.event(some_event, event2, event3) 
#            - this specifies which event/events trigger this function
# 
# def _(): - this means we create a function with no name (or rather name _ ), 
#            can be used when a function is never actually called/triggered by you,
#            by name. but eg. is called by event

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider("x_position", "X position", 0, 100, 20),
            ui.input_slider("y_position", "Y position", 0, 100, 20),
            ui.input_action_button("add_dot", "Add a dot!"),
        ),
        ui.panel_fixed(
            ui.output_plot("scatterplot"),
        ),
    ),
)

def server(input, output, session):
    all_dots = reactive.Value([])
    
    @output
    @render.plot()
    def scatterplot():
        # nonlocal all_dots
        plt.xlim(0, 100)
        plt.ylim(0, 100)

        dots_to_show =  all_dots.get().copy()
        dots_to_show.append(current_spot_location(color='black'))

        xs = [dot['x'] for dot in dots_to_show]
        ys = [dot['y'] for dot in dots_to_show]
        colors = [dot['c'] for dot in dots_to_show]

        return plt.scatter(xs, ys, s=[200], c=colors, alpha=0.5)

    def current_spot_location(color = 'red'):
        return {'x':input.x_position(), 'y': input.y_position(), 'c': color}

    @reactive.Effect
    @reactive.event(input.add_dot)
    def _():
        new_dots = all_dots.get().copy()
        new_dots.append(current_spot_location())
        all_dots.set(new_dots)
        print(f"new all_dots {new_dots}") 

    @reactive.Effect
    @reactive.event(input.x_position,input.y_position)
    def _():
        new_dots = all_dots.get().copy()
        new_dots.append(current_spot_location(color='grey'))
        all_dots.set(new_dots)
        print(f"slider moved {all_dots()}") 
        
        

app = App(app_ui, server, debug=True)
