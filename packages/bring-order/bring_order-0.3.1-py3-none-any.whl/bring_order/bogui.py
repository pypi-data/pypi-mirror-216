"""Methods for creating widgets"""
from ipywidgets import widgets

class BOGui:
    """General methods for creating widgets"""
    def __init__(self):
        """Class constructor"""

    def create_button(self, desc: str, command, style='success', tooltip=''):
        """Creates button"""
        button = widgets.Button(description=desc,
                                button_style=style,
                                tooltip=tooltip)
        button.on_click(command)
        return button

    def init_buttons(self, buttons):
        """Initializes buttons.

        args:
            buttons: list of tuples.

        returns:
            dictionary containing the buttons

        """
        button_list = {}
        for button in buttons:
            new_button = self.create_button(desc=button[0],
                                                  command=button[1],
                                                  style=button[2])
            button_list[button[0]] = new_button
        return button_list

    def create_message(self, value, style={'font_size': '15px'}):
        """Creates HTML"""
        message = widgets.HTML(value=value, style=style)
        return message

    def create_error_message(self, value=''):
        """Creates HTML, color: red"""
        error = self.create_message(value=value,
                                    style={'font_size': '12px',
                                           'text_color': 'red'})
        return error

    def create_input_field(self, default_value=''):
        """Creates input field"""
        input_field = widgets.Text(value=default_value)
        return input_field

    def create_text_area(self, default_value='', place_holder=''):
        """Creates text box"""
        text_area = widgets.Textarea(value=default_value,layout={'width': '70%'}, placeholder=place_holder)
        return text_area
    
    def create_label(self, value):
        """Creates label"""
        label = widgets.Label(value=value,
                              layout=widgets.Layout(justify_content='flex-end'))
        return label

    def create_placeholder(self):
        """Creates empty label"""
        placeholder = self.create_label('')
        return placeholder

    def create_grid(self, rows, cols, items, width='50%'):
        """Creates grid of widgets"""
        grid = widgets.GridspecLayout(rows,
                                      cols,
                                      height='auto',
                                      width=width,
                                      grid_gap="0px")
        item_index = 0
        for i in range(rows):
            for j in range(cols):
                grid[i, j] = items[item_index]
                item_index += 1

        return grid

    def create_int_text(self, default_value=1, desc=''):
        """Creates integer input"""
        int_text = widgets.IntText(value=default_value, description=desc, layout={'width':'80px'})
        return int_text

    def create_radiobuttons(self, options, desc=''):
        """Creates radiobuttons"""
        radiobuttons = widgets.RadioButtons(
            options=options,
            description=desc,
            disabled=False,
            font_size ="15px")

        return radiobuttons
