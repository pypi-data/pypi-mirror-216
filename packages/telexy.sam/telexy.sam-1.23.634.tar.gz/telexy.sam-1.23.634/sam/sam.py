from mars import *
import cherrypy

@cherrypy.tools.allow(methods=['POST'])
@cherrypy.tools.json_out()
class SamPlugin(MarsPluginBase):

    def __init__(self):
        super().__init__()

    @cherrypy.expose
    def uploadImage(self):
        return {"test": "upload"}
    
    def configuration(self):
        return {
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')]
        }