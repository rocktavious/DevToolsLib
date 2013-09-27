from DTL.api import apiUtils, Path

LOCAL_PATH = Path(__file__).parent
DJANGO_MANAGE_PATH = LOCAL_PATH.join('manage.py')

def runserver():
    cmd = 'python {0} runserver'.format(DJANGO_MANAGE_PATH)
    apiUtils.execute(cmd, verbose=True, catchError=True)