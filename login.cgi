#!D:\Python\Python34\python.exe

import urllib, http, cgi, requests, random, string, hashlib

def htmlTop():
    print("""Content-type:text/html\n\n
                <!DOCTYPE html>
                <html lang="en">
                    <head>
                        <meta charset="utf-8"/>
                        <title></title>
                    </head>
                    <body>""")


def htmlTail():
    print("""</body>
    </html>""")

def login(username, passHash, cookie):
    postdata = "todo=Anmelden&name="+username+"&passHash="+passHash


    headers = {'Host':'gymnasium1.de', 'Accept': '*/*',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','X-Requested-With':'XMLHttpRequest',
                   'Referer': 'http://gymnasuim1.de/CJT.php','Content-Length': len(postdata),
                   'Cookie': cookie, 'Pragma':'no-cache', 'Cache-Control':'no-cache',
                    'Connection': 'keep-alive'}
    response = requests.post("http://gymnasium1.de/Anmeldung.php", headers=headers, data=postdata)
    return response




try:
    random = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
    cookie = "PHPSESSID="+random
    formData = cgi.FieldStorage()
    username = formData.getvalue('username')
    password = formData.getvalue('password')
    if username is None and password is None:
        username = "zienjuli"
        password = "09213"
    m=hashlib.md5()
    m.update(password.encode("utf-8"))
    passhash=m.hexdigest()
    fromDate = formData.getvalue('fromdate')
    toDate = formData.getvalue('todate')
    htmlTop()
    print(login(username, passhash, cookie))
    htmlTail()
except:
    cgi.print_exception()