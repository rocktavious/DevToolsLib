from __future__ import absolute_import
from urlparse import urljoin
import xml.etree.ElementTree as ElementTree
from xml.sax.saxutils import escape
import urllib2
import base64

from DTL.api import apiUtils
from DTL.gui.widgets import LoginWidget


#------------------------------------------------------------
LOGIN_URL = 'rest-service/auth-v1/login?userName=%s&password=%s'
CREATE_REVIEW_URL = 'rest-service/reviews-v1'
ADD_PATCH_URL = 'rest-service/reviews-v1/%s/patch'
ADD_REVIEWERS_URL = 'rest-service/reviews-v1/%s/reviewers'
APPROVE_URL = 'rest-service/reviews-v1/%s/transition?action=action:approveReview'

#------------------------------------------------------------
CREATE_REVIEW_XML_TEMPLATE = \
"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<createReview>
    <reviewData>
        <allowReviewersToJoin>true</allowReviewersToJoin>
        <author>
            <userName>%s</userName>
        </author>
        <creator>
            <userName>%s</userName>
        </creator>
        <description>%s</description>
        %s
        <moderator>
            <userName>%s</userName>
        </moderator>
        <name>%s</name>
        <projectKey>%s</projectKey>
        <state>Draft</state>
        <type>REVIEW</type>
    </reviewData>
</createReview>
"""

#------------------------------------------------------------
ADD_PATCH_XML_TEMPLATE = \
'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addPatch>
    <patch>%s</patch>
    <anchor>
        <anchorPath></anchorPath>
        <anchorRepository>%s</anchorRepository>
        <stripCount>1</stripCount>
    </anchor>
</addPatch>
'''

#------------------------------------------------------------
#------------------------------------------------------------
class CrucibleClient(object):
    #------------------------------------------------------------
    def __init__(self, host, verbose=False):
        if not host.endswith('/'):
            host += '/'
        self.host = host
        self.verbose = verbose
        if self.get_credentials() :
            raise Exception('Login to crucible failed!')
    
    #------------------------------------------------------------
    def _request(self, url, method, body=None, username=None, password=None):
        headers={'Content-Type': 'application/xml',
                 "Accept": 'application/xml'}
        if username:
            headers["Authorization"] = 'Basic %s' % base64.encodestring("%s:%s" % (username, password))[:-1]
    
        req = urllib2.Request(url=url, data=body, headers=headers)
        return urllib2.urlopen(req)
    
    #------------------------------------------------------------
    def _post(self, url, body, error_message):
        url = urljoin(self.host, url)

        if self.verbose:
            print "URL: %s" % url
            print "Request Body:\n%s" % body

        try:
            resp = self._request(url, method='POST', body=body,
                                 username=self.username,
                                 password=self.password)
        except urllib2.HTTPError, e:
            xml = e.read()
            if self.verbose:
                print xml
            message = ElementTree.fromstring(xml).findtext('.//message')
            if message :
                raise Exception(error_message+": "+message)
            else:
                print error_message
                raise Exception()
        return resp
    
    #------------------------------------------------------------
    def get_credentials(self, msg='Please enter your Crucible password.'):
        success, username, password = LoginWidget.getCredentials(loginMsg=msg,
                                                                 credentialsFile=apiUtils.getTempFilepath('crucible_login.dat'))
        if not success :
            return 1      
        self.username = username
        self.password = password
        
        return self.test_credentials()
    
    #------------------------------------------------------------
    def test_credentials(self):
        url = urljoin(self.host, LOGIN_URL % (self.username, self.password))
        try:
            resp = self._request(url, method='POST')
            return 0
        except urllib2.HTTPError, e:
            if e.code == 403 :
                xml = e.read()
                error = ElementTree.fromstring(xml).find('error')
                if error.text == 'authentication failed':
                    #Retry credentials
                    return self.get_credentials(msg='Invalid Username or Password! Retry...')
                raise Exception(error.text)
            return 1
    
    #------------------------------------------------------------
    def add_patch(self, permaid, patch, repository):
        """Add one changeset to the review as a patch."""
        body = ADD_PATCH_XML_TEMPLATE % (escape(patch), escape(repository))
        self._post(ADD_PATCH_URL % permaid, body, "Unable to add patch")
        
    #------------------------------------------------------------
    def add_reviewers(self, permaid, reviewers):
        """Add reviewers to the review."""
        self._post(ADD_REVIEWERS_URL % permaid, reviewers, 
                "Unable to add reviewers '%s' to review" % reviewers)
    
    #------------------------------------------------------------
    def create_review(self, title, description, project, jira_issue=None, moderator=None):
        """
        Creates a new review
        :return the new review's permaId string.
        """
        moderator = moderator if moderator else self.username
        jira_issue = "" if not jira_issue else "<jiraIssueKey>%s</jiraIssueKey>" % escape(jira_issue),

        body = CREATE_REVIEW_XML_TEMPLATE % \
               (escape(self.username), escape(self.username), escape(description), jira_issue[0],
                escape(moderator), escape(title[:255]), escape(project))
        resp = self._post(CREATE_REVIEW_URL, body, "Unable to create new review")
        xml = resp.read()
        return ElementTree.XML(xml).findtext('.//permaId/id')
    
    #------------------------------------------------------------
    def open_review(self, permaid):
        '''Takes the specified review from Draft to Under Review state.  Not yet 100%.'''
        self._post(APPROVE_URL % permaid, "", "Unable to open review")
        
    #------------------------------------------------------------
    def review_url(self, permaid):
        """Returns the crucible url of the review"""
        return urljoin(self.host, "cru/"+permaid)

