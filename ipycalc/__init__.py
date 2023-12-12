import os
from nbconvert.exporters import WebPDFExporter
from nbconvert.preprocessors import TagRemovePreprocessor

class ipycalcExporter(WebPDFExporter):
    """
    A custom PDF exporter for ipycalc.
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

    @property
    def _extra_template_basedirs(self):
        return super()._default_extra_template_basedirs() + [self.template_dir]
    
    def _template_name_default(self):
        return os.path.join(self.pkg_dir, self.custom_template_name)
    