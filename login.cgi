#!D:\Python\Python34\python.exe

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


def login(username, passHash, cookie, schule, fromDate, toDate):
    postdata = "verbindung=" + schule
    headers = {'Host': 'gymnasium1.de', 'Accept': '*/*',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'X-Requested-With': 'XMLHttpRequest',
               'Referer': 'http://gymnasuim1.de/CJT.php', 'Content-Length': len(postdata),
               'Cookie': cookie, 'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
               'Connection': 'keep-alive'}
    requests.post(url="http://gymnasium1.de/sqlVerbindungFestlegen.php",
                        data=postdata, headers=headers)
    postdata = "todo=Anmelden&name=" + username + "&passHash=" + passHash
    response = requests.post("http://gymnasium1.de/Anmeldung.php", headers=headers, data=postdata).text
    if "NO" in response:
        return "Falsches Passwort oder Benutzername"
    else:
        return krankmelden(cookie=cookie, fromDate=fromDate, toDate=toDate)


def krankmelden(cookie, fromDate, toDate):
    postdata = "tan=&vonDatum=" + fromDate + "&vonStunde=1&bisDatum=" + toDate + "&bisStunde=11&begruendung="
    headers = {'Host': 'gymnasium1.de', 'Accept': '*/*',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest',
               'Referer': 'http://gymnasuim1.de/CJT.php', 'Content-Length': len(postdata),
               'Cookie': cookie, 'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
               'Connection': 'keep-alive'}
    url = "http://gymnasium1.de/sqlSchuelerKrankmeldung.php"
    print("<br><br>Krankmeldung:<br><br>")
    return requests.post(url=url, headers=headers, data=postdata).text


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
    school = formData.getvalue('school')
    htmlTop()
    print(login(username, passhash, cookie, schule=school, fromDate=fromDate, toDate=toDate))
    htmlTail()
except:
    cgi.print_exception()
