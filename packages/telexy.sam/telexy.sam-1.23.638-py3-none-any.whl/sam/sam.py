from mars import *
import cherrypy
import os
import cv2

@cherrypy.tools.allow(methods=['POST'])
@cherrypy.tools.json_out()
class SamPlugin(MarsFileManagementPlugin):

    def __init__(self):
        super().__init__("images")
   
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def predict(self):
        key = cherrypy.request.json
        filePath = self.getCurrentDirectory() + key
        if(os.path.exists(filePath) == False):
            raise cherrypy.HTTPError(404, "File with key: " + key + " does not exist")
        
        image = cv2.imread(filePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        return key

    def configuration(self):
        return {
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')]
        }