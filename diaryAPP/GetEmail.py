# coding=utf-8
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

email_date = ""
email_content = ""

#########下载邮件附件
def Getmail(DAY=10,emailhost="pop.163.com", emailuser="boziaaaaa@163.com", emailpass="jianchi408"):
    global email_date
    global email_content
    result_output = []
    host = emailhost
    username = emailuser
    password = emailpass
    # 需要验证的邮件服务
    pop_conn = poplib.POP3_SSL(host)
    pop_conn.user(username)
    pop_conn.pass_(password)
    num = pop_conn.stat()[0] # 邮件总数
    if num < DAY:  # 当总邮件数目小于50的时候读取所有邮件
        num2 = 0
    else:
        num2 = num - DAY
    for i in range(num, num2, -1):#最新50个邮件
        resp, lines, octets = pop_conn.retr(i)
        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        # 稍后解析出邮件:
        msg = Parser().parsestr(msg_content)
        result = print_info(msg)
        if result!=-1:
            result_output.append(result)
            email_date = ""
            email_content = ""
        else:
            pass

    pop_conn.quit()
    return result_output

def print_info(msg, indent=0):
    global email_date
    global email_content
    if indent == 0:
        for header in ['Subject',"DATE"]:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                    if value!="test":
                        return -1
                elif header=='DATE':
                    email_date = month_EnglishName2number(value)
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            if n==0:
                print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                print(charset)
                content = content.decode(charset)
            email_content = content
    if email_date and email_date:
        print(email_content)
        email_content = (email_content.encode('utf-8')).decode('utf-8')
        print(email_content)
        return (email_date,email_content)

def month_EnglishName2number(inputStr):
    monthes = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    inputStr = inputStr.split()
    month_int = monthes.index(inputStr[2]) + 1
    inputDate = inputStr[3]+str(month_int).zfill(2)+inputStr[1].zfill(2)
    return(inputDate)
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value
def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

Getmail(10,"pop.163.com","boziaaaaa@163.com","jianchi408")






