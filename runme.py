#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
from __future__ import print_function
import sys
import io
import os

from converters.template import *
from converters.template import ConverterTemplate
from converters.html import ConverterHTML
# From IPython

# All the stuff needed for the configurable things
from IPython.config.application import Application
from IPython.config.loader import ConfigFileNotFound
from IPython.utils.traitlets import List, Unicode, Type, Bool, Dict, CaselessStrEnum


class NbconvertApp(Application):


    def __init__(self, **kwargs):
        super(NbconvertApp, self).__init__(**kwargs)
        self.classes.insert(0,ConverterTemplate)
        # ensure those are registerd

    def load_config_file(self, profile_name):
        try:
            Application.load_config_file(
                self,
                profile_name+'.nbcv',
                path=[os.path.join(os.getcwdu(),'profile')]
            )
        except ConfigFileNotFound:
            self.log.warn("Config file for profile '%s' not found, giving up ",profile_name)
            exit(1)


    def initialize(self, argv=None):
        self.parse_command_line(argv)
        cl_config = self.config
        profile_file = sys.argv[1]
        self.load_config_file(profile_file)
        self.update_config(cl_config)



    def run(self):
        """Convert a notebook to html in one step"""
        template_file = (self.extra_args or [None])[0]
        ipynb_file = (self.extra_args or [None])[1]

        template_file = sys.argv[1]

        if template_file.startswith('latex'):
            tex_environement=True
        else:
            tex_environement=False

        C = ConverterTemplate(tplfile=sys.argv[1],
                config=self.config)
        C.read(ipynb_file)

        output,resources = C.convert()

        print(output.encode('utf-8'))

        keys = resources.keys()
        if keys :
            print('''
====================== Keys in Resources ==================================
''')
            print(resources.keys())
            print("""
===========================================================================
you are responsible from writing those data do a file in the right place if
they need to be.
===========================================================================
                  """)

def main():
    """Convert a notebook to html in one step"""
    app = NbconvertApp.instance()
    app.initialize()
    app.start()
    app.run()
#-----------------------------------------------------------------------------
# Script main
#-----------------------------------------------------------------------------

if __name__ == '__main__':
    main()
