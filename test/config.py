#-*-coding:utf-8-*-

import os
import sys
import codecs
import ConfigParser

# file = sys.path[0]+r'\url.conf'
# if os.path.exists(file):
#     print 'have'
# else:
#     print 'have not'
# cp = ConfigParser.SafeConfigParser()
# cp.read(file)

# print cp.get('http','url')

file = sys.path[0]+r'\app.conf'
cp = ConfigParser.SafeConfigParser()
with codecs.open(file, 'r', encoding='utf-8') as f:
    cp.readfp(f)

talk_user = cp.get('nika','talk_user').split(',')
print type(talk_user)
print talk_user
for target_list in talk_user:
    print target_list
    pass

# print cp.sections()
# print cp.options('db')
# print cp.items('ssh')

# print cp.get('db','host')
# print cp.getint('db','port')

# print cp.has_section('db')
# print cp.has_section('db2')

# print cp.has_option('db','port')
# print cp.has_option('db','port2')
# print cp.has_option('db2','port')

# cp.add_section('db3')

# cp.write(open(file, 'w'))
# cp.write(sys.stdout)


