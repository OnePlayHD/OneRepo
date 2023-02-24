import six
if six.PY3:
    import zipfile
else:
    from zp import zipfile
    

def all(_in, _out, dp=None):
    if dp:
        allWithProgress(_in, _out, dp)
    else:
        allNoProgress(_in, _out)

def allNoProgress(_in, _out):
    try:
        zin = zipfile.ZipFile(_in, 'r')
        zin.extractall(_out)
    except Exception as e:
        pass

def allWithProgress(_in, _out, dp):
    zin = zipfile.ZipFile(_in,  'r')
    nFiles = float(len(zin.infolist()))
    count = 0
    try:
        for item in zin.infolist():
            count += 1
            update = count / nFiles * 100
            dp.update(int(update))
            zin.extract(item, _out)
    except Exception as e:
        pass