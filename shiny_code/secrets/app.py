# two silly examples of secrets
from shiny import App, render, ui

app_ui = ui.page_fixed(
    ui.div(
        ui.input_slider("some_number", "Secter formula input", 10, 25, 10),
        ui.output_text_verbatim("formula_output")
    ),
     ui.div(
        ui.input_numeric("letter_which", "Which letter of secret word:", 0, min = 0, max = 7 ),
        ui.output_text_verbatim("letter_output")
     )
)


def server(input, output, session):
    @output
    @render.text
    def formula_output():
        formula_input = input.some_number()
        if formula_input % 7 == 0:
            formula_output = "fizz"
        elif formula_input % 5 == 0:
            formula_output = "buzz"
        elif formula_input % 3 == 0:
            formula_output = "oomph"
        else:
            formula_output = f"{formula_input}"

        return f"Secret formula output for {formula_input:<2} is {formula_output}"

    @output
    @render.text
    def letter_output():
        secret_word = "Bananas!"
        return f"Letter at index {input.letter_which()} is {secret_word[input.letter_which()]}"


app = App(app_ui, server)
