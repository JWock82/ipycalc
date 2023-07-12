import os
from nbconvert.exporters import WebPDFExporter

class ipycalcExporter(WebPDFExporter):
    """
    A custom PDF exporter for ipycalc.
    """

    pkg_dir = os.path.dirname(__file__)
    template_dir = os.path.join(pkg_dir, 'nbconvert_templates')

    @property
    def extra_template_basedirs(self):
        return super()._default_extra_template_basedirs() + [self.template_dir]

    def _template_file_default(self):
        return 'index.pdf.j2'