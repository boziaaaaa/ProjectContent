import re
a = "1234567m_1234567m_"
i = re.search("(\d+)m_",a)
print i.start()
print i.end()
print i.endpos