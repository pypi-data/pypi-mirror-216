from docutils import nodes
from docutils.parsers.rst import Directive, directives

from sphinx.util.docutils import SphinxDirective

# required for file system path building
import os
import pathlib

# required to copy stylesheet
from sphinx.util.fileutil import copy_asset_file

# required to generalte HTML from jinja templates
from jinja2 import Template

class AzgaarMap(SphinxDirective):
    """The AzgaarMap class provides an API to add a HOOPS Web Viewer to any Sphinx documentation page."""

    has_content = True

    """The ``option_spec`` variable is used by :class:`sphinx.util.docutils.SphinxDirective` to validate directive parameters. Review the `option_spec documentation <https://www.sphinx-doc.org/en/master/extdev/markupapi.html#docutils.parsers.rst.Directive.option_spec>`_ for more details."""
    option_spec = {
        'burg': directives.unchanged_required,
    }

    def run(self):
        """
        This function is **required** for any class that inherits from:

        - :class:`sphinx.util.docutils.SphinxDirective` or,
        - :class:`docutils.parsers.rst.Directive`

        Find more information in the `official Sphinx Documentation <https://www.sphinx-doc.org/en/master/extdev/markupapi.html#docutils.parsers.rst.Directive.run>`_
        """

        # create docutils node as Sphinx expects
        gen_node = azgaar_map_node()

        # base_url = "https://azgaar.github.io/Fantasy-Map-Generator"
        # maplink_query = "maplink=http://veldus.net/_static/world_map/veldus.map"
        # iframe_src = "{0}?{1}".format(base_url, maplink_query)
        # self.options['iframe_src'] = iframe_src
        # base_url = "http://127.0.0.1:4242/_static/map/"
        # base_url = "http://veldus.net/_static/map/"
        base_url = "http://map.veldus.net/"
        self.options['iframe_src'] = base_url

        try:
            self.options['iframe_src'] = "{0}?burg={1}".format(self.options['iframe_src'], self.options['burg'])
        except:
            self.options['iframe_src'] = self.options['iframe_src']

        # configure node
        gen_node['jinja_config'] = {
            'iframe_src': self.options['iframe_src'],
        }

        # return node as Sphinx expects
        return [gen_node]


class azgaar_map_node(nodes.Body, nodes.Element):
    """
    We need to create our own node class that inherits from both ``nodes.Body`` and ``nodes.Element``, see :class:`~sphinx_ts3d_ext.azgaar_map.AzgaarMap.run()` for usage.

    On build, Sphinx will replaced any ``.. azgaar_map::`` with a doctil node representation. Eventually, this node will be replaced with the HTML we generated from `azgaar_map.html`. See :class:`~sphinx_ts3d_ext.azgaar_map.AzgaarMap.handle_azgaar_map_node()` for more details.
    """
    pass

def handle_azgaar_map_node(self, node):
    """
    This function is responsible for generating the ``azgaar_map.html`` from its Jinja template and replacing the respective :class:`~sphinx_ts3d_ext.azgaar_map.azgaar_map_node` during the build.
    """
    # get azgaar_map template
    template = os.path.join(pathlib.Path(__file__).parent.absolute(), 'azgaar-map.html')

    # build jinja config
    # generate html with template+config
    html = generate_HTML_from_jinja(template, node['jinja_config'])

    # append html where node was found
    self.body.append(html)

    # tell sphinx to skip processing this node, we took care of everything
    raise nodes.SkipNode

def generate_HTML_from_jinja(template, config):
    """
    A helper function responsible for generating HTML from a Jinja template.
    """
    # Open jinja template and get file content as String
    jinja2_template_string = open(template, 'r').read()

    # Create template object
    template = Template(jinja2_template_string)

    # Render HTML template String
    html_template_string = template.render(config = config)

    return html_template_string

def handle_build_finished(app, exc):
    """
    After the build has finished we need to add the AzgaarMap's CSS to the project's asset files, but only if a Web Viewer has been used in the project.
    """
    # We will provide basic styling for the widget
    # Sphinx provides a utility method to copy asset files during build: copy_asset_file()
    #
    # source: https://groups.google.com/g/sphinx-users/c/Z-wcktOhIAc/m/pGDWO0yVBQAJ
    if exc is None: # build succeeded
        azgaar_mapStylesheet = os.path.join(os.path.dirname(__file__), 'css/azgaar-map.css')
        destionation = os.path.join(app.outdir, '_static/css/azgaar-map.css')

        # Ignore if it is a linkcheck build
        if 'linkcheck' in destionation:
            return

        copy_asset_file(azgaar_mapStylesheet, destionation)

def setup(app):
    """
    This is a required function by Sphinx and contains all the logic to initiate the Web Viewer extension. Review the source comments for details.
    """
    # Add our AzgaarMap directive to the Sphinx app
    app.add_directive('azgaar_map', AzgaarMap)

    # Add the azgaar_map_node that replaces the directive during processing
    # Provide custom HTML processor
    app.add_node(azgaar_map_node,
            html=(handle_azgaar_map_node, None))

    # This only adds the appropriate <link> tag to the page
    #
    # We still need to copy the actual asset file into the expected location
    # See the 'build-finished' even handler for details
    # app.add_css_file('css/azgaar_map.css')

    # Set up sphinx core event handler(s)
    app.connect('build-finished', handle_build_finished)

    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
