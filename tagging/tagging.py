
import cgi
import decimal
import pkg_resources
import requests
import string

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment


class TaggingXBlock(XBlock):
    """
    An XBlock providing tagging
    """
    tag = String(
        help="This name appears in the horizontal navigation at the top of the page.",
        scope=Scope.settings,
        default="CS")
    
    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def studio_view(self, context=None):
        """
        Studio view part
        """
        tag = self.tag or ''
        html_str = self.resource_string("/static/html/tagging_edit.html")
        frag = Fragment(html_str.format(tag=tag))

        js_str = self.resource_string("/static/js/tagging_edit.js")
        frag.add_javascript(js_str)
     
        css_str = self.resource_string("/static/css/tagging_edit.css")
        frag.add_css(css_str)

        frag.initialize_js('TaggingEditBlock')

        return frag

    def student_view(self, context=None):
        """
        Create a fragment used to display the XBlock to a student
        `context` is a dictionary used to configure the display (unused).
        Returns a `Fragment` object specifying the HTML, CSS and JavaScript to display
        """
        tag = self.tag or ''
        html_str = self.resource_string("static/html/tagging.html")

        # Construct the HTML
        frag = Fragment(html_str.format(
            self=self,
            tag=cgi.escape(tag)))

        # And construct the CSS
        css_str = self.resource_string("static/css/tagging.css")
        # css_str = string.replace(unicode(css_str), "{aspect_ratio}", cgi.escape(unicode(round(ratio, 2))))
        frag.add_css(css_str)
        
        return frag

    @XBlock.json_handler
    def studio_submit(self, data, suffic=''):
        self.tag = data.get('tag')
        return {'result': 'success'}

    @staticmethod
    def workbench_scenarios():
        return [
            ("Tag",
             """
             <tagging/>
             """),
        ]