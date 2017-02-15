data = """

"""

for minion in data.strip().split('\n'):
    if 'not' not in minion:
        print 'salt-key -d %s -y' % minion.strip(':')
