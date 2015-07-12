#!/usr/bin/env python

import cgi, requests, random, string, hashlib


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
    postdata = "todo=Anmelden&name=" + username + "&passHash=" + passHash

    headers = {'Host': 'gymnasium1.de', 'Accept': '*/*',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'X-Requested-With': 'XMLHttpRequest',
               'Referer': 'http://gymnasuim1.de/CJT.php', 'Content-Length': len(postdata),
               'Cookie': cookie, 'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
               'Connection': 'keep-alive'}
    response = requests.post("http://gymnasium1.de/Anmeldung.php", headers=headers, data=postdata)
    return response


def krankmelden(cookie, fromDate, toDate):
    postdata = "tan=&vonDatum=" + fromDate + "&vonStunde=1&bisDatum=" + toDate + "&bisStunde=11&begruendung="
    headers = {'Host': 'gymnasium1.de', 'Accept': '*/*',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest',
               'Referer': 'http://gymnasuim1.de/CJT.php', 'Content-Length': len(postdata),
               'Cookie': cookie, 'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
               'Connection': 'keep-alive'}
    url = "http://gymnasium1.de/sqlSchuelerKrankmeldung.php"
    return requests.post(url=url, headers=headers, data=postdata)
    #if requests.post(url=url, headers=headers, data=postdata).status_code is 200:
    #    return "Krankmeldung von " + fromDate + " bis " + toDate + " erfolgreich"
    #else:
    #    return "Ungueltiges Datum"


try:
    randomStr = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
    cookie = "PHPSESSID=" + randomStr
    formData = cgi.FieldStorage()
    username = formData.getvalue('username')
    password = formData.getvalue('password')
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    passhash = m.hexdigest()
    fromDate = formData.getvalue('fromdate')
    toDate = formData.getvalue('todate')
    htmlTop()
    if login(username, passhash, cookie).status_code is 200:
        print(krankmelden(cookie=cookie, fromDate=fromDate, toDate=toDate))
    else:
        print("Ungueltiges Passwort oder Username")

    htmlTail()
except:
    cgi.print_exception()
