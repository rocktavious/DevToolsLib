# Code snippets taken from Guernsey REST client package, based on the Java Jersey client.

from urlparse import urljoin
import urllib2
import base64

from DTL.api import InternalError, Logger, apiUtils
from DTL.gui.widgets import LoginWidget

#------------------------------------------------------------
#------------------------------------------------------------
class RequestWithMethod(urllib2.Request):
    """ This simple class is used to allow us to use the standard urllib2
        module to make PUT, POST and DELETE methods. This requires a pretty
        simple addition so that we can use this efficiently.
    """
    #------------------------------------------------------------
    def __init__(self, method, *args, **kwargs):
        """ RequestWithMethod(method, args, kwargs) -> object
            Construct a new request for urllib2 but with a specified
            HTTP method.
        """
        self._method = method
        urllib2.Request.__init__(self, *args, **kwargs)
    
    #------------------------------------------------------------
    def get_method(self):
        """ get_method() -> string
            Return the method provided in the initializer.

            :rtype: string
        """
        return self._method

#------------------------------------------------------------
#------------------------------------------------------------
class ExecClient(object):
    """ This class actually implements the HTTP Request and Response packaging"""
    __metaclass__ = Logger.getMetaClass()
    #------------------------------------------------------------
    def __init__(self, auth_handler):
        apiUtils.synthesize(self, 'opener', urllib2.build_opener(auth_handler))
    
    #------------------------------------------------------------
    def _prep_request(self, client_request):
        if client_request.method in ['GET', 'POST']:
            request = urllib2.Request(url=client_request.url, data=client_request.resource.req_entity)
        else:
            request = RequestWithMethod(client_request.method, url=client_request.url, data=client_request.resource.req_entity)
        for k, v in client_request.resource.headers.iteritems():
            request.add_header(k, v)
        
        return request
    
    #------------------------------------------------------------
    def _request(self, request):
        try:
            response = self.opener().open(request)
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                self.logger.error('We failed to reach a server. Reason: {0}'.format(e.reason))
            elif hasattr(e, 'code'):
                self.logger.error('The server could not fulfill the request. Status code: {0}'.format(e.code))
            return ClientResponse(client_request.resource, e, client_request.resource.client)
        else:
            return ClientResponse(client_request.resource, response, client_request.resource.client)
    
    #------------------------------------------------------------
    def handle(self, client_request):
        return self._request(self._prep_request(client_request))

#------------------------------------------------------------
#------------------------------------------------------------
class RestClient(object):
    #------------------------------------------------------------
    def __init__(self, host, requires_auth=True, login_msg='Login', username='', password=''):
        if not host.endswith('/'):
            host += '/'

        auth_handler = urllib2.HTTPBasicAuthHandler()
        apiUtils.synthesize(self, 'host', host)
        apiUtils.synthesize(self, 'username', username)
        apiUtils.synthesize(self, 'password', password)
        apiUtils.synthesize(self, 'client', ExecClient(auth_handler))        
        
        if requires_auth :
            if not self.get_credentials(login_msg=login_msg) :
                raise InternalError('Login failed!')

    #------------------------------------------------------------
    def get_credentials(self, login_msg):
        success, username, password = LoginWidget.getCredentials(loginMsg=login_msg,
                                                                 credentialsFile=apiUtils.getTempFilepath(self.__class__.__name__ + '_login.dat'))
        if not success :
            return False
        self.username = username
        self.password = password

        return self.test_credentials()

    #------------------------------------------------------------
    def get_headers(self):
        return {}

    #------------------------------------------------------------
    def get_auth_header(self):
        return 'Basic %s' % base64.encodestring("%s:%s" % (self.username, self.password))[:-1]