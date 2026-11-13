import base64
import os
from urllib.parse import quote, unquote

try:
    from bs4 import BeautifulSoup
    try:
        # Jinja 3 renamed contextfilter to pass_context. Both decorators pass
        # the current template context to the Markdown filter.
        from jinja2 import pass_context
    except ImportError:
        from jinja2 import contextfilter as pass_context
    from nbconvert.exporters import WebPDFExporter
    from nbconvert.preprocessors import TagRemovePreprocessor
except ImportError:
    WebPDFExporter = object
    TagRemovePreprocessor = None
    # Keep the module importable without the exporter dependencies; attempting
    # to construct an exporter will raise an ImportError in its constructor.
    def pass_context(function):
        return function

def import_vars(notebook_name, *var_names):
    from .calc import import_vars as _import_vars
    return _import_vars(notebook_name, *var_names)


def save_vars(notebook_name):
    from .calc import save_vars as _save_vars
    return _save_vars(notebook_name)


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
        if TagRemovePreprocessor is None:
            raise ImportError("nbconvert is required for ipycalc exporters.")

        # Set template config before parent init so the template environment
        # is built with the correct paths from the start
        kw.setdefault('extra_template_basedirs', [self.pkg_dir])
        kw.setdefault('template_name', self.custom_template_name)

        super().__init__(config=config, **kw)

        # Set up preprocessors
        trp = TagRemovePreprocessor()
        trp.remove_cell_tags = ['hide_cell']
        trp.remove_input_tags = ['hide_input']
        self.register_preprocessor(trp, enabled=True)
        self.embed_images = True
        self.exclude_input_prompt = True
        self.exclude_output_prompt = True

    @pass_context
    def markdown2html(self, context, source):
        """Render Markdown and embed images attached to the current cell."""
        # Attachments belong to individual cells, so names must be resolved
        # against the current cell rather than against the entire notebook.
        cell = context.get('cell', {})
        attachments = cell.get('attachments', {})
        if attachments and 'attachment:' in source:
            # Work with copies so preparing data for export does not modify the
            # notebook or its original attachments.
            aliases = {}
            for name, attachment in attachments.items():
                attachment = dict(attachment)
                svg = attachment.get('image/svg+xml')
                # SVG attachments can be stored as XML text, but a base64 data
                # URL requires the UTF-8 bytes to be encoded first.
                if isinstance(svg, str) and svg.lstrip().startswith('<'):
                    attachment['image/svg+xml'] = base64.b64encode(svg.encode('utf-8')).decode('ascii')
                aliases[name] = attachment
            # Markdown image URLs may percent-encode spaces or other filename
            # characters. Add aliases without replacing any real filenames.
            for name, attachment in list(aliases.items()):
                aliases.setdefault(quote(name, safe=''), attachment)
            attachments = aliases
            # Supply the copied attachment map to nbconvert through a derived
            # Jinja context, leaving the original cell and context untouched.
            cell = dict(cell, attachments=aliases)
            context = context.derived({'cell': cell})

        # Let nbconvert render Markdown and resolve Markdown image attachments.
        html = super().markdown2html(context, source)
        if not attachments or 'attachment:' not in html:
            return html

        # Raw HTML image tags bypass nbconvert's Markdown image renderer. Parse
        # the rendered HTML and replace their attachment URLs with data URLs.
        soup = BeautifulSoup(html, 'html.parser')
        for image in soup.find_all('img', src=True):
            src = image['src']
            if not src.startswith('attachment:'):
                continue
            name = src[len('attachment:'):]
            # Try the literal filename first, then its URL-decoded form.
            attachment = attachments.get(name) or attachments.get(unquote(name))
            if not attachment:
                continue
            # Match nbconvert's preference for SVG, PNG, then JPEG; fall back
            # to the first available MIME type for other attachment formats.
            mime_type = next((mime for mime in ('image/svg+xml', 'image/png', 'image/jpeg')
                              if mime in attachment), next(iter(attachment)))
            image['src'] = f'data:{mime_type};base64,{attachment[mime_type]}'
        return str(soup)


class ipycalcNumberedExporter(ipycalcExporter):
    """
    A custom PDF exporter for ipycalc with section numbering.

    Same as ipycalcExporter but adds automatic section numbers to headings
    (h2 and below). h1 headings are treated as titles and are not numbered.

    This exporter is registered as an entry point so it can be selected in
    JupyterLab via "File -> Save and Export Notebook As... -> Ipycalc (Numbered)"
    """

    custom_template_name = 'nbconvert_template_numbered'
