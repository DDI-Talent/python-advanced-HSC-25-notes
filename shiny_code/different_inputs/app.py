# types of inputs
from shiny import App, render, ui, reactive
import asyncio
from datetime import datetime
import pyodide.http    

app_ui = ui.page_fluid(
    ui.input_text("text", label="Enter some text"),
    ui.input_action_button("pay_it", "do something"),
    ui.input_action_link("do_it_again", "or something else!"),
    ui.input_slider("total_bill", "Bill amount", min=0, max=10000, value=5, sep="", pre="$"),
    ui.input_checkbox_group("times", "Food service", ["Snack", "Lunch", "Dinner"], selected=["Lunch", "Dinner"], inline=True),
    ui.input_checkbox("business", "Was this business related?" ),
    ui.input_select(  
        "select",  
        "Select an option below:",  
        {"1A": "Choice 1A", "1B": "Choice 1B", "1C": "Choice 1C"},  
    ),
    ui.output_text_verbatim("text_output"),
)
# for all options see https://shiny.posit.co/py/components/#inputs

def server(input, output, session):
    @render.text
    def text_output():
        final_text = f"Results of all inputs:\n"
        final_text += f"text:\t\t {input.text()}\n"
        final_text += f"button:\t\t {input.pay_it()}\n"
        final_text += f"link:\t\t {input.do_it_again()}\n"
        final_text += f"slider:\t\t {input.total_bill()}\n"
        final_text += f"checkboxes:\t {input.times()}\n"
        final_text += f"checkbox:\t {input.business()}\n"
        final_text += f"dropdown:\t {input.select()}\n"
        return final_text

app = App(app_ui, server)