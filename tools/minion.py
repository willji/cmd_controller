data = """

"""
from keyadmin import SaltTool
a = SaltTool().get_minions()
c = [str(k) for k in a]
b = data.strip().split('\n')
print c
print b
d = list(set(b).difference(set(c)))
print len(d)
print d
