# required by Sphinx
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective

# required for file system path building
import os

# required to generalte HTML from jinja templates
from jinja2 import Template

################################################################################
#                           Global Functions                                   #
#                                                                              #
#  This section includes global functions used by both directives              #
#                                                                              #
#  1. def generate_HTML_from_jinja()                                           #
#     This function will generate HTML from the provided template and config   #
################################################################################

# abs_template_path: a path to an absolute path to a jinja template file
# config: the jinja config dict expected by the template
def generate_HTML_from_jinja(abs_template_path, config):
  # Open jinja template and get file content as String
  jinja2_template_string = open(abs_template_path, 'r').read()

  # Create template object
  template = Template(jinja2_template_string)

  # Render HTML template String
  html_template_string = template.render(config = config)

  # Return HTML to HTML parser
  return html_template_string

################################################################################
#                           Place StatBlock                                    #
#                                                                              #
#  This section will include all functions and classes required to implement   #
#  the .. place_statblock:: directive. This includes:                          #
#                                                                              #
#  1. def validTableType() and validKingdom                                    #
#     These functions validate the value provided for a particular :option:.   #
#                                                                              #
#  2. class Place_Statblock                                                    #
#     This class requires a run() function that is executed when this          #
#     directive is found in an .rst file. Must return a doctree node.          #
#                                                                              #
#  3. class place_statblock                                                    #
#     This class is used to inherit from existing docutils.nodes and provides  #
#     the directive with a doctree node.                                       #
#                                                                              #
#  4. def html_place_statblock()                                               #
#     This function is invoked once per directive found during the             #
#     Sphinx core event 'html-page-context'. It replaces the doctree node      #
#     with the proper HTML generated from a jinja.                             #
#                                                                              #
################################################################################

# validates values given for option :table_type:
def validTableType(arg):
  validTableTypes = ['place', 'npc']

  return directives.choice(arg, validTableTypes)

# validates values given for option :kingdom:
def validKingdom(arg):
  validKingdomList = ['Belrd', 'Dynnt', 'White Peaks', 'Clan Gildkin', 'Unknown']

  return directives.choice(arg, validKingdomList)

"""
This is Place Statblock
"""
class Place_Statblock(Directive):
  has_content = True

  # TODO: write validators for all required, at least
  # dict required by docutils/Sphinx for Directives
  # name is *not* optional
  # these are only split for readability, can be added to option_spec directly if desired
  option_spec = {}

  # a dict of required args
  required_args = {
    'table_type': validTableType,
    'place': directives.unchanged_required,
    'kingdom': directives.unchanged_required,
    'territory': directives.unchanged_required,
    'type': directives.unchanged_required,
  }

  # can be empty
  optional_args = {
    'population': directives.unchanged,
    'demographics': directives.unchanged,
    'leader': directives.unchanged,
    'region': directives.unchanged,
    'founded': directives.unchanged,
  }

  # add to docutils/Sphinx option dict
  option_spec.update(required_args)
  option_spec.update(optional_args)

  # only validates if the option is present
  # add a function similar to validTableType() to validate the value of the option
  def has_required_options(self, docname):

    # list of :options: that are required
    # a ValueError will be raised at build if a required arg is missing
    required_arguments = ['table_type']

    for arg in required_arguments:
      if not self.options.get(arg):
        error_message = 'Missing option :{0}: for Statblock in {1}.rst on lineno: {2}'.format(arg, docname, self.lineno)
        raise ValueError(error_message)

  # run() is required by Sphinx
  def run(self):
    env = self.state.document.settings.env

    # ensure a required options are present
    # TODO: the validators provided in the option_spec might be able to handle this, not sure
    self.has_required_options(docname=env.docname)

    # create doctree node
    table_node = place_statblock()

    storage = env.veldus.get('all_placeinfos')
    if not storage:
    # if not hasattr(env.veldus, 'all_placeinfos'):
      env.veldus['all_placeinfos'] = []

    env.veldus['all_placeinfos'].append({
      'docname': env.docname,
      'options': self.options
    })

    return [table_node]

# this needs to be all-lower, else place_statblockList throws warning that Sphinx can't find the directive
class place_statblock(nodes.Body, nodes.Element):
  pass

# this function is invoked once per place_statblock directive found during the
# Sphinx core event 'html-page-context'
# https://www.sphinx-doc.org/en/1.5/extdev/appapi.html#event-html-page-context
def html_place_statblock(self, node):
  # find options for current node
  places = self.document.settings.env.veldus['all_placeinfos']
  for place in places:
    if place['docname'] in node.source:
      options = place['options']

  # build jinja template config dict from Sphinx options
  # remove option :table_type: which is for internal use
  infos = {key:val for key, val in options.items() if key != 'table_type'}
  config = {
    'infos': infos
  }

  # build absolute path to jinja template
  abs_template_path = os.path.join(os.path.dirname(__file__), 'place.html')

  # generate HTML from jinja template
  html = generate_HTML_from_jinja(abs_template_path, config)

  # append HTML
  self.body.append(html)

  raise nodes.SkipNode

################################################################################
#                           Place SummaryTable                                 #
#                                                                              #
#  This section will include all functions and classes required to implement   #
#  the .. place_summarytable:: directive. This includes:                       #
#                                                                              #
#  1. class Place_SummaryTable                                                 #
#     This class requires a run() function that is executed when this          #
#     directive is found in an .rst file. Consumed in Sphinx.setup().          #
#                                                                              #
#  2. class place_summarytable                                                 #
#     This class is used to inherit from existing docutils.nodes and replaces  #
#     the directive with a doctree node. Consumed in Sphinx.setup().           #
#                                                                              #
#  3. def html_place_summarytable()                                            #
#     This function is invoked once per directive found during the             #
#     Sphinx core event 'html-page-context'. It replaces the doctree node      #
#     with the proper HTML generated from a jinja. Consumed in Sphinx.setup(). #
#                                                                              #
#  4. def handle-env-update()                                                  #
#     We sort the rows into the desired order during this phase.               #
#                                                                              #
################################################################################

class Place_SummaryTable(Directive):
    def run(self):
        return [place_summarytable()]

class place_summarytable(nodes.Body, nodes.Element):
  pass

def html_place_summarytable(self, node):
    # controls the header row of the table
    headers = ['place', 'kingdom', 'territory', 'type']
    summary_rows = []
    urls = []

    # for each place with an place_statblock...
    for place in self.document.settings.env.veldus['all_placeinfos']:
      # build a url for a backlink
      urls.append(place['docname'] + '.html')

      row = []
      # for each header of table...
      for header in headers:
        # collect info of current place_statblock
        row.append(place['options'].get(header))

      summary_rows.append(row)

    # build absolute path to jinja template
    abs_template_path = os.path.join(os.path.dirname(__file__), 'summary-table.html')

    # build jinja template config dict from Sphinx options
    config = {
      'headers': headers,
      'summary_rows': summary_rows,
      'urls': urls
    }

    # generate HTML from jinja template
    html = generate_HTML_from_jinja(abs_template_path, config)

    # append HTML
    self.body.append(html)

    raise nodes.SkipNode

# after env is finished updating, put places is desired order for summary table
def handle_env_updated(app, env):
  if env.veldus.get('all_placeinfos'):
    # sort alpha ascend by kingdom then name of place
    kingdom_sorted = sorted(env.veldus['all_placeinfos'], key = lambda i: (i['options']['kingdom'], i['options']['place']))
    env.veldus['all_placeinfos'] = kingdom_sorted

################################################################################
#                               Sphinx API                                     #
################################################################################

# this function is required to setup the directive when it is
# encountered in the project's conf.py
def setup(app):
  # Add Place Statblock directive
  # We provide our function to generate the HTML that will replace the node during build
  app.add_node(place_statblock,
               html=(html_place_statblock, None))
  app.add_directive('place_statblock', Place_Statblock)

  # Add Place Statblock Summary Table directive
  # We provide our function to generate the HTML that will replace the node during build
  app.add_node(place_summarytable,
               html=(html_place_summarytable, None))
  app.add_directive('place_summarytable', Place_SummaryTable)

  # Connect event handlers
  app.connect('env-updated', handle_env_updated)

  app.connect('env-before-read-docs', handle_env_before_read_docs)

  # TODO: figure out exactly what we are, and could be, returing here
  return {
      'version': '0.1',
      'parallel_read_safe': True,
      'parallel_write_safe': True,
  }

def handle_env_before_read_docs(app, env, docnames):
    # make sure global storage has init
    if not hasattr(env, 'veldus'):
      # print('MISSING GLOBAL VAR "veldus" but in HANDLER')
      env.veldus = {}
