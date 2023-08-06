# -*- coding: utf-8 -*-
__author__ = 'S.H. Hawley'

"""
On-the-Fly (User) Control (& Calibration)

This allows for changes to 
"""

from prefigure import get_all_args, arg_eval
import configparser
import gradio as gr
import gradio.blocks as gb
import itertools
from copy import deepcopy
import os
import warnings 
import wandb
from datetime import datetime, timedelta
from collections import OrderedDict

class OFC(object):
    "On-the-Fly Control: Saves args to a new file, updates 'args' when changes occur to file"
    def __init__(self, 
                 args,               # namespace object is *mutable*
                 ofc_file='ofc.ini', # file to which updated args are saved
                 use_gui=True,       # make da gui?
                 sliders=False,     # if True, use sliders instead of text boxes for float/int values, with min/max guessed at from args
                 steerables=None,   # list of names of args allowed to steer. None or [] means Nothing is steerable
                 use_wandb=True,    # make use of wandb for logging changes etc
                 debug=False,
                 ):
        "NOTE: ofc_file should be given a unique name if multiple similar runs are occuring"
        self.ofc_file = args.name+'-'+ofc_file
        self.args = args   
        self.use_gui = use_gui or (hasattr(args,"use_gui") and args.use_gui)
        self.sliders = sliders
        self.steerables = steerables if steerables else [] # Not all args need be steerable
        self.use_wandb, self.debug = use_wandb, debug

        self.section_name = 'OFC'
        self.gradio_url, self.demo, self.demo_datetime = '', None, None
        self.columns = None
        self.args_gui_dict = OrderedDict()     # where we will keep the gui values

        self.save(args)
        if self.use_gui: self.create_gradio_interface(sliders=sliders)


    def save(self, args):
        "saves all steerable params (args) as new INI file"
        config = configparser.ConfigParser()
        config.add_section(self.section_name)
        for key, val in vars(args).items():
            if self.debug: print("OFC.save: Saving ",key," = ",val," to ",self.ofc_file)
            config[self.section_name][key] = str(val)
        if self.debug: print("OFC.save: Saving to ",self.ofc_file)
        with open(self.ofc_file, 'w') as f:
            config.write(f)


    def update(self):
        "generic update loop; find out which variables have changed; see if gui needs relaunching"
        save_args_dict = vars(self.args)
        config = configparser.ConfigParser()
        config.read(self.ofc_file)
        new_args_dict = dict(config.items(self.section_name))

        changed = {}
        for key, val in new_args_dict.items():
            if not (',' in val):  # changes to list variables are not supported yet
                val = arg_eval(val)
                if (val != save_args_dict[key]) and (key != 'wandb_config'):
                    print(f"\n  OFC: {key} has been changed to {val}")
                    changed[key] = val
                    vars(self.args)[key] = val    # NOTE: THIS will overwrite values in args.

        # relaunch gui before temp url expires
        if self.use_gui and self.demo and (not '127.0.0.1' in self.gradio_url) and (self.demo_datetime is not None)  and (self.demo_datetime - datetime.now() >= timedelta(hours=71)): 
            print("OFC: Not long now til Gradio public temp URL would expire. Relaunching GUI.")
            self.create_gradio_interface(columns=self.columns, sliders=self.sliders)
            
        return changed   # changed dict can be used for wandb logging of changes


    def create_gui_element(self,key,value, sliders=False):
        "creates a single gui element based on variable type, by defalt no sliders, just text fields and buttons"
        if isinstance(value, bool):
            input_element = gr.components.Radio([True, False], value=value, label=key)
        elif isinstance(value, int) and sliders:
            maximum = value * 2 if value > 0 else 1
            input_element = gr.components.Slider(minimum=0, maximum=maximum, value=value, label=key, step=1)
        elif isinstance(value, float) and sliders:
            maximum = value * 2 if value > 0.0 else 1.0
            input_element = gr.components.Slider(minimum=0.0, maximum=maximum, value=value, label=key)
        elif isinstance(value, str):
            input_element = gr.components.Textbox(value=value, label=key)
        else:
            input_element = gr.components.Textbox(value=str(value), label=key) # for lists, etc.
        return input_element


    def create_gradio_interface(self, 
                                sliders=False,  # turns on sliders for floats & ints; default is all text fields
                                columns=3, ):
        "for all variables in args, create gui elements"
        self.columns, self.sliders = columns, sliders     # update storage viewed elsewhere

        inputs = []
        args_dict =  vars(self.args)
        column_length = len(args_dict)//columns
        with gr.Blocks(title="OFC", theme=gr.themes.Base()) as demo:
            gr.Markdown(f'<center><h1>prefigure: On-the-Fly Control (OFC)</h1></center>')        
            with gr.Row():
                for c in range(columns):
                    with gr.Column():
                        for key, value in itertools.islice(args_dict.items(), c*column_length, (c+1)*column_length):
                            if key=='gui': continue  # don't add 'gui' var to gui
                            if key not in self.steerables: continue
                            if self.debug: print("key = ",key," value = ",value,", type = ",type(value))
                            self.args_gui_dict[key] = value
                            input_element = self.create_gui_element(key,value, sliders=sliders)
                            inputs.append(input_element)
            submit_button = gr.Button(value="Submit", variant='primary',)
            submit_button.click(fn=self.on_gui_submit, inputs=inputs)
        print()

        auth = ( os.getenv('OFC_USERNAME', ''), os.getenv('OFC_PASSWORD', '') )
        share = True
        if auth[0] == '' or auth[1] == '':
            warnings.warn("OFC: No username/password provided. Authentication & Public GUI URL disabled.")
            auth, share = None, False

        _, local_url, public_url = demo.launch(prevent_thread_lock=True, auth=auth, share=share)  # LAUNCH DA GUI
        gradio_url = public_url if public_url else local_url

        print(f"Demo launched. Gradio URL is {gradio_url} Moving on.")
        if self.use_wandb and wandb.run is not None:
            wandb.log({"gradio_url": wandb.Html(f'OFC Gradio URL = <a href="{gradio_url}" target="_blank">{gradio_url}</a>')})
            demo.integrate(wandb=wandb)
        self.gradio_url = gradio_url   # can access via ofc.gradio_url hook 
        self.demo_datetime = datetime.now()  # save time of deployment


    def on_gui_submit(self, 
                      *gui_values, # tuple of gui values but no keys :-/ 
                      ):
        "writes to the ofc file, then updates the args. detection of param type (float, int, etc.) performed by file reader"
        if self.debug: print(f"gui_values = {gui_values}, type = {type(gui_values)}")

        # update args_gui_dict with new values from gui submit
        for key, new_val in zip(self.args_gui_dict.keys(), gui_values):
            self.args_gui_dict[key] = new_val
       
        # update a copy of args with args_gui_dict values
        args_copy = deepcopy(self.args)
        for key in vars(args_copy).keys():
            for key2 in self.args_gui_dict.keys():
                if key == key2:
                    vars(args_copy)[key] = self.args_gui_dict[key2]
                
        # save args_copy to file and update to fill args
        self.save(args_copy) 
        self.update() 


if __name__ == '__main__':
    # testing
    import time
    args = get_all_args(defaults_file='../examples/defaults.ini')
    args.name = 'test'
    print("args = \n",args)
    ofc = OFC(args, use_gui=True)
    while True:
        changed = ofc.update()
        time.sleep(2)
