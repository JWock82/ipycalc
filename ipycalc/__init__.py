import os
from nbconvert.exporters import WebPDFExporter
from traitlets.config import Config

class ipycalcExporter(WebPDFExporter):
    """
    A custom PDF exporter for ipycalc.
    """

    custom_template_name = 'nbconvert_template'
    pkg_dir = os.path.dirname(__file__)
    template_dir = os.path.join(pkg_dir, custom_template_name)

    def __init__(self, config=None, **kw):
        if config is None:
            config = Config()
        config.TemplateExporter.template_path.append(self.template_dir)
        config.TemplateExporter.template_file = 'base.html.j2'
        super().__init__(config=config, **kw)
