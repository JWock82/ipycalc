import os
from traitlets.config import Config
from nbconvert.exporters import WebPDFExporter

class ipycalcExporter(WebPDFExporter):
    """
    A custom PDF exporter for ipycalc.
    """

    export_from_notebook = 'ipycalc via webpdf'

    def _template_name_default(self):
        return 'ipycalc'

    @property
    def _template_paths(self):
        return super()._template_paths + [os.path.join(os.path.dirname(__file__), "nbconvert_templates")]
    
    def _default_extra_template_basedirs(self):
        return [os.path.join(os.path.dirname(__file__), 'nbconvert_templates')]

    def _template_file_default(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'nbconvert_templates')
        return os.path.join(template_dir, 'ipycalc.tpl')
    