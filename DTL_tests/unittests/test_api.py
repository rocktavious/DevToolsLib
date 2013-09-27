import time
import unittest

from DTL.api import *
from DTL.settings import Settings

class TestCaseApiUtils(unittest.TestCase):
    
    def setUp(self):
        apiUtils.synthesize(self, 'mySynthesizeVar', None)
        self.bit = apiUtils.BitTracker.getBit(self)
    
    def test_wildcardToRe(self):
        self.assertEquals(apiUtils.wildcardToRe('c:\CIG\main\*.*'),
                          '(?i)c\\:\\\\CIG\\\\main\\\\[^\\\\]*\\.[^\\\\]*$')
        self.assertEquals(apiUtils.wildcardToRe('c:\CIG\main\*.*'),
                          apiUtils.wildcardToRe('c:/CIG/main/*.*'))        
    
    def test_synthesize(self):
        self.assertIn('_mySynthesizeVar', self.__dict__)
        self.assertTrue(hasattr(self, 'mySynthesizeVar'))        
        self.assertTrue(hasattr(self, 'getMySynthesizeVar'))
        self.assertTrue(hasattr(self, 'setMySynthesizeVar'))
        
        self.assertEqual(self.getMySynthesizeVar(), self.mySynthesizeVar)
        
    def test_getClassName(self):
        self.assertEqual(apiUtils.getClassName(self), 'TestCaseApiUtils')
        
    def test_bittracker(self):
        self.assertEqual(apiUtils.BitTracker.getBit(self), self.bit)
        
        
        
class TestCaseDotifyDict(unittest.TestCase):
    
    def setUp(self):
        self.dotifydict = DotifyDict({'one':{'two':{'three':'value'}}})
        
    def test_dotifydict(self):
        self.assertEquals(self.dotifydict.one.two, {'three':'value'})
        self.dotifydict.one.two.update({'three':3,'four':4})
        self.assertEquals(self.dotifydict.one.two.four, 4)
        self.assertEquals(self.dotifydict.one, self.dotifydict.one)
        self.assertIn('two.three', (self.dotifydict.one))
        self.assertEquals(str(self.dotifydict), "DotifyDict(datadict={'one': DotifyDict(datadict={'two': DotifyDict(datadict={'four': 4, 'three': 3})})})")
        self.assertEquals(self.dotifydict.one.two, eval(str(self.dotifydict.one.two)))


class TestCasePath(unittest.TestCase):
    
    def setUp(self):
        self.filepath = Settings.getTempPath()
        
    def test_path(self):
        temp_path = Settings.getTempPath()
        self.assertEquals(self.filepath, temp_path)
        self.assertEquals(self.filepath.name, temp_path.name)
        self.assertEquals(self.filepath.parent, temp_path.parent)
        self.assertIn(self.filepath.parent.parent.name, self.filepath)
        
        myPathSepTest = Path('c:\\Users/krockman/documents').join('mytest')
        self.assertEquals(myPathSepTest, 'c:\Users\krockman\documents\mytest')
        self.assertEquals({'TestKey', myPathSepTest},{'TestKey',u'c:\\Users\\krockman\\documents\\mytest'})
        
            
class TestCaseDocument(unittest.TestCase):
    
    def setUp(self):
        self.doc = Document({'Testing':'min'})
        self.doc.filepath = Settings.getTempPath().join('document.dat')
    
    def test_document(self):
        self.assertEquals(self.doc.filepath, Settings.getTempPath().join('document.dat'))
        self.assertEquals(self.doc, eval(str(self.doc)))
        self.doc.save()
        self.assertTrue(self.doc.filepath.exists())
        
    def tearDown(self):
        self.doc.filepath.remove()
        
class TestCaseVersion(unittest.TestCase):
    
    def setUp(self):
        self.version = Version('2.0.5.Beta')
        
    def test_version(self):
        self.assertEquals(self.version,(2,0,5,'Beta'))
        self.assertEquals(self.version,'2.0.5.Beta')
        self.assertEquals(self.version,eval(str(self.version)))
        self.version.update({'status':VersionStatus.Gold})
        self.assertNotEquals(self.version,(2,0,5,'Beta'))        
        
class TestCaseDecorators(unittest.TestCase):
    
    @Safe
    def test_safe(self):
        1/0
    
    @Timer
    def test_timer(self, timer):
        for i in range(5):
            time.sleep(2)
            timer.newLap(i)
            
    @Profile
    def test_profile(self):
        for i in range(5):
            (1 / 20 * 5 - 10 + 15) == 1


def main():
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()