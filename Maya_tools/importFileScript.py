import sys
filename = 'replaceInstance'
if filename in sys.modules:
    reload(sys.modules[filename])
else:
    import filename
