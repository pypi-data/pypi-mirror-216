import os

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective

from jinja2 import Template

# this shit has to be all-lower, else npc_statblockList throws warning that Sphinx can't find the directive
class npc_statblock(nodes.Body, nodes.Element):
  pass

class NPC_Statblock(Directive):

  has_content = True

  # TODO: can this be improved?
  option_spec = {
    'npc': directives.unchanged_required,
    'race': directives.unchanged_required,
    'height': directives.unchanged_required,
    'weight': directives.unchanged_required,
    'eyes': directives.unchanged_required,
    'skin': directives.unchanged_required,
    'hair': directives.unchanged_required,
    'occupation': directives.unchanged_required,
    'motivations': directives.unchanged_required
  }

  def run(self):
    env = self.state.document.settings.env

    # create doctree node
    table_node = npc_statblock()

    if not hasattr(env, 'veldus_all_npcstats'):
      env.veldus_all_npcstats = []

    # save info to global variable
    env.veldus_all_npcstats.append({
      'docname': env.docname,
      'options': self.options
    })

    return [table_node]

def html_npc_statblock(self, node):
  # find options for current node
  for npc in self.document.settings.env.veldus_all_npcstats:
    if npc['docname'] in node.source:
      options = npc['options']

  # create a statblock_table object
  statblock_table = Statblock_Table(options)

  # build html from provided options and append
  self.body.append(statblock_table.build())

  raise nodes.SkipNode

class npc_summarytable(nodes.Body, nodes.Element):
  pass

class NPC_SummaryTable(Directive):
    def run(self):
        return [npc_summarytable()]

def html_npc_summarytable(self, node):
    # controls the header row of the table
    headers = ['npc', 'race', 'occupation']
    summary_rows = []
    urls = []

    # for each npc with an npc_statblock...
    # print(self.document.settings.env.veldus_all_npcstats)
    for npc in self.document.settings.env.veldus_all_npcstats:
      # build a url for a backlink
      urls.append(npc['docname'] + '.html')

      row = []
      # for each header of table...
      for header in headers:
        # collect stats of current npc_statblock
        row.append(npc['options'].get(header))

      summary_rows.append(row)

    # create a summary_table object
    summary_table = Summary_Table(headers, summary_rows, urls)

    # build html from provided options and append
    self.body.append(summary_table.build())

    raise nodes.SkipNode

# after env is finished updating, put places is desired order for summary table
def handle_env_updated(app, env):
  if hasattr(env, 'veldus_all_npcstats'):
    # sort alpha ascend by kingdom then name of place
    stats_sorted = sorted(env.veldus_all_npcstats, key = lambda i: (i['options']['race'], i['options']['npc']))
    env.veldus_all_npcstats = stats_sorted

def setup(app):

  # Add NPC Statblock directive
  app.add_node(npc_statblock,
               html=(html_npc_statblock, None))
  app.add_directive('npc_statblock', NPC_Statblock)

  # Add NPC Statblock Summary Table directive
  app.add_node(npc_summarytable,
               html=(html_npc_summarytable, None))
  app.add_directive('npc_summarytable', NPC_SummaryTable)

  app.connect('env-updated', handle_env_updated)

  return {
      'version': '0.1',
      'parallel_read_safe': True,
      'parallel_write_safe': True,
  }

class Statblock_Table():
  def __init__(self, stats):
    self.stats = stats
    self.project_root = os.path.dirname(__file__)
    self.template_path = "{0}/{1}".format(self.project_root, 'npc.html')

  def build(self):
    # Get File Content in String
    jinja2_template_string = open(self.template_path, 'r').read()

    # Create Template Object
    template = Template(jinja2_template_string)

    # Render HTML Template String
    config = {
      'stats': self.stats
    }
    html_template_string = template.render(config = config)

    return html_template_string

class Summary_Table():
  def __init__(self, headers, summary_rows, urls):
    self.headers = headers
    self.summary_rows = summary_rows
    self.urls = urls
    self.project_root = os.path.dirname(__file__)
    self.template_path = "{0}/{1}".format(self.project_root, 'summary-table.html')

  def build(self):
    # Get File Content in String
    jinja2_template_string = open(self.template_path, 'r').read()

    # Create Template Object
    template = Template(jinja2_template_string)

    # Render HTML Template String
    config = {
      'headers': self.headers,
      'summary_rows': self.summary_rows,
      'urls': self.urls
    }
    html_template_string = template.render(config = config)

    return html_template_string
