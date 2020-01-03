# from GetEmail import Getmail
#
# result = Getmail("pop.163.com","boziaaaaa@163.com","jianchi408")
# for line in result:
#     date = line[0]
#     content = line[1]
#     print(date)
#     print(content,'\n')
# print(email_date,email_content)
import struct
outputFile = "diary/test.bin"
outputStr = bytes("12345我爱北京天安门",encoding='utf-8')
print(outputStr)
outputStr = struct.pack('12s', outputStr)
with open(outputFile,"wb") as f:
    f.write(outputStr)