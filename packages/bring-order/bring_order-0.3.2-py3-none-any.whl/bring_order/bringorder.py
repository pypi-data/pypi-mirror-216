"""Main class"""
import os
import sys
from ipywidgets import widgets
from IPython.display import display

wd = os.getcwd()
class_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, class_dir)
from bogui import BOGui
from bodi import Bodi
from boutils import BOUtils
from deductive import Deductive
from inductive import Inductive


class BringOrder:
    """Main class"""
    def __init__(self):
        """Class constructor"""
        self.boutils = BOUtils()
        self.bogui = BOGui()
        self.deductive = None
        self.inductive = None
        self.deductive_button = None
        self.inductive_button = None
        self.bodi = Bodi(
            self.boutils,
            self.bogui,
            self.start_analysis)
        self.bring_order()

    def create_deductive_button(self):
        """Creates deductive button"""
        button = self.bogui.create_button(
            desc='Deductive',
            command=self.start_deductive_analysis)

        return button

    def create_inductive_button(self):
        """Creates inductive button"""
        button = self.bogui.create_button(
            desc='Inductive',
            command=self.start_inductive_analysis)

        return button

    def close_buttons(self):
        """Hides buttons"""
        self.deductive_button.close()
        self.inductive_button.close()

    def start_deductive_analysis(self, _=None):
        """Starts deductive analysis"""

        self.close_buttons()
        if not hasattr(self, 'data_limitations'):
            self.data_limitations = self.bodi.data_limitations
        self.deductive.data_limitations = self.bodi.data_limitations
        self.deductive.start_deductive_analysis()

    def start_inductive_analysis(self, _=None):
        """Starts inductive analysis"""
        self.close_buttons()
        self.inductive.start_inductive_analysis()

    def bring_order(self):
        """Starts data import phase"""
        self.bodi.bodi()

    def start_analysis(self):
        """Starts analysis phase"""
        self.deductive = Deductive(
            self.bogui,
            self.boutils,
            self.start_analysis
        )
        self.inductive = Inductive(
            self.bogui,
            self.boutils,
            self.start_analysis
        )
        self.deductive_button = self.create_deductive_button()
        self.inductive_button = self.create_inductive_button()
        display(widgets.HBox([self.deductive_button, self.inductive_button]))

    def __repr__(self):
        return ''