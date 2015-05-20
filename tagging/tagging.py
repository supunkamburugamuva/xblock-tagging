
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

    # Stored values for the XBlock
    href = String(
        help="URL of the Office Mix you want to embed",
        scope=Scope.content,
        default='https://mix.office.com/watch/10g8h9tvipyg8')
        
    tag = String(
        help="This name appears in the horizontal navigation at the top of the page.",
        scope=Scope.settings,
        default="CS")
    
    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def studio_view(self, context):
        """
        Studio view part
        """
        
        href = self.href or ''
        tag = self.tag or ''

        html_str = self.resource_string("/static/html/tagging_edit.html")
        frag = Fragment(html_str.format(tag=cgi.escape(tag)))

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
        href = self.href or ''
        tag = self.tag or ''
        
        # Make the oEmbed call to get the embed code 
        # try:
            # embed_code, width, height = self.get_embed_code(href)
        html_str = self.resource_string("static/html/tagging.html")
        # except Exception as ex:
        #     html_str = self.resource_string("static/html/embed_error.html")
        #     frag = Fragment(html_str.format(self=self, exception=cgi.escape(str(ex))))
        #     return frag

        # Grab and round the aspect ratio
        # ratio = decimal.Decimal(float(height) / width * 100.0)

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
        self.href = data.get('href')
        self.tag = data.get('tag')
        
        return {'result': 'success'}

    def get_embed_code(self, url):
        """
        Makes an oEmbed call out to Office Mix to retrieve the embed code and width and height of the mix
        for the given url.
        """

        parameters = { 'url': url }
 
        oEmbedRequest = requests.get("https://mix.office.com/oembed/", params = parameters)
        oEmbedRequest.raise_for_status()
        responseJson = oEmbedRequest.json()

        return responseJson['html'], responseJson['width'], responseJson['height']

    @staticmethod
    def workbench_scenarios():
        """ Returns a single element which is the Office Mix xblock """
        return [
            ("Tag",
             """
             <tagging href="https://mix.office.com/watch/1otxpj7hz6kbx" />
             """),
        ]