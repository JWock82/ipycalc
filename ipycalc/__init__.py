import os
from nbconvert.exporters import WebPDFExporter
from nbconvert.preprocessors import TagRemovePreprocessor

class ipycalcExporter(WebPDFExporter):
    """
    A custom PDF exporter for ipycalc.
    
    Exporters in nbconvert are used to convert Jupyter notebooks (.ipynb files) 
    into other formats such as HTML, PDF, Markdown, etc. This exporter extends 
    the WebPDFExporter to create PDF files with custom styling specific to ipycalc.
    
    The exporter automatically:
    - Applies the ipycalc custom template with proper print margins
    - Embeds images directly in the output
    - Hides cells tagged with 'hide_cell' 
    - Hides inputs tagged with 'hide_input'
    - Removes cell execution prompts (In[1], Out[1], etc.)
    
    This exporter is registered as an entry point so it can be selected in 
    JupyterLab via "File -> Save and Export Notebook As... -> Ipycalc"
    """

    # This is the name of the folder containing the template in `ipycalc`
    custom_template_name = 'nbconvert_template'

    # This is the directory where ipycalc is installed on the user's machine
    pkg_dir = os.path.dirname(__file__)

    # This is the location where the `ipycalc` template is installed on the user's machine
    template_dir = os.path.join(pkg_dir, custom_template_name)

    def __init__(self, config=None, **kw):

        super().__init__(config=config, **kw)

        # Set up preprocessors
        trp = TagRemovePreprocessor()
        trp.remove_cell_tags=['hide_cell']
        trp.remove_input_tags=['hide_input']
        self.register_preprocessor(trp, enabled=True)
        self.embed_images=True
        self.exclude_input_prompt=True
        self.exclude_output_prompt=True

        # Set the template directory for nbconvert to find custom templates
        self.extra_template_basedirs = [self.template_dir]

        # Set the template name to use
        self.template_name = self.custom_template_name
