from dropbox import session, client

from DTL import __appdata__
from DTL.api import Path, Utils, Logger

class Dropbox(object):
    __metaclass__ = Logger.getMetaClass()
    
    def __init__(self, appKey, appSecret, appAccessType):
        Utils.synthesize(self, "appKey", appKey)
        Utils.synthesize(self, "appSecret", appSecret)
        Utils.synthesize(self, "appAccessType", appAccessType)
        self._tokenPath = Path(__appdata__).join(self.appKey() + '_token')
        
        self._accessKey = ''
        self._accessSecret = ''
    
    def getSession(self):
        return session.DropboxSession(self.appKey(), self.appSecret(), self.appAccessType())
    
    def _readToken(self):
        with open(self._tokenPath.caseSensative, 'r') as token_file :
            self._accessKey, self._accessSecret = token_file.read().split('|')
        
    def _saveToken(self, key, secret):
        with open(self._tokenPath.caseSensative, 'w') as token_file :
            token_file.write("%s|%s" % (key,secret) )
    
    def _requestToken(self):
        sess = self.getSession()
        request_token = sess.obtain_request_token()
        
        url = sess.build_authorize_url(request_token)

        # Make the user sign in and authorize this token
        print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
        print "url:", url
        raw_input()
        
        access_token = sess.obtain_access_token(request_token)
        self._accessKey = access_token.key
        self._accessSecret = access_token.secret
        
        self._saveToken(self._accessKey, self._accessSecret)
    
    def getAccessToken(self):
        if self._tokenPath.exists() :
            self._readToken()
        else:
            self._requestToken()
    
    def getClient(self):
        sess = self.getSession()
        self.getAccessToken()
        sess.set_token(self._accessKey, self._accessSecret)
        return client.DropboxClient(sess)

    def uploadFile(self, srcPath, destPath):
        db = self.getClient()
        result = db.put_file(destPath, open(srcPath,'rb'))
        return result


if __name__ == '__main__':
    db = Dropbox('c2kqug22n304xh7',
                 'mxhi4vfyyw8dtlh',
                 'dropbox')
    db.uploadFile('C:/Users/krockman/Desktop/stan_body_anim_color.tga',
                  '/Star Citizen Shotgun Sync/stan_body_anim_color.tga')