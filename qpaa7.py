from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup
import re

static_head = '''
<html>
<head>
<title>QPFC AA7</title>
<meta content="yes" name="apple-mobile-web-app-capable" />
<meta content="text/html; charset=iso-8859-1" http-equiv="Content-Type" />
<meta content="minimum-scale=1.0, width=device-width, maximum-scale=0.6667, user-scalable=no" name="viewport" />
<link href="css/style.css" type="text/css" rel="stylesheet" />
<script src="javascript/functions.js" type="text/javascript"></script>
<link rel="apple-touch-icon" href="images/icon.png"/>
<link href="images/loading.png" rel="apple-touch-startup-image"/>
</head>
<body>
<div id="topbar">
  <div id="title">QPFC AA7 Team</div>
</div>
<div id="content">
'''

static_foot = '''
</div><!-- close content div -->
<div id="footer">
  Team Site by Oz, iPhone interface by Else.
</div>
</body>
</html>
'''


def runapp():
    url = 'http://www.blasldkjasds.com/qpfc/'

    try:
        fetch_ob = urlopen(url)
        html = ''.join(fetch_ob.readlines())
    except:
        pass

    code = fetch_ob.code
    if code != 200:
        html = 'Failed to fetch url: %d' % code
        return html

    print get_html(html)

def get_html(html):
    soup = BeautifulSoup(html)

    playerinfo = get_playerinfo(soup)
    gameinfo = get_gameinfo(soup)

    html = ''

    # game info
    html += '<span class="graytitle">Next Game Information</span>'
    html += '<ul class="pageitem"><li class="textbox">'
    #html += '<span class="header">Something</span><p>'
    html += '<a class="noeffect" href="%s"><img alt="Google Maps" src="images/maps.png"></a> %s at %s<br>' % (gameinfo['maploc'], gameinfo['gameloc'], gameinfo['time'])
    html += 'Shirts: %s<br>Beers: %s<br>' % (gameinfo['shirts'], gameinfo['beers'])
    html += '</p></li></ul>'

    # player info
    html += '<span class="graytitle">Player Register</span>'
    html += '<ul class="pageitem">'
#<li class="textbox"><span class="header">'

    keys = playerinfo.keys()
    keys.sort(cmp=surname_sort)
    for k in keys:
        v = playerinfo[k]
        html += '''
        <li class="menu">
        <a class="noeffect" href="#" onclick="document.getElementById('player%s').style.display='';return false;">
        <span class="name">%s</span>
        <span class="comment">%s</span>
        <span class="arrow"></span>
        </a>
        </li>
        <li class="textbox" id="player%s" style="display: none">
        <span class="graytitle">Stats</span>
        <p>Goals: %s</p>
        <p>Games: %s</p>
        <p>Available: %s</p>
        <span class="graytitle">Contact</span>
        <p>Phone: <a class="noeffect" href="tel:%s">Call</a> <a class="noeffect" href="sms:%s">SMS</a></p>
        <p>Email: <a class="noeffect" href="mailto:%s">%s</a></p>
        </li>
        ''' % (v['id'], v['name'], v['position'], v['id'], v['goals'], v['games'], "Yes" if v['available'] == '1' else "No", v['contact'], v['contact'], v['email'], v['email'])
    html += '</ul>'

    return static_head + html + static_foot

def surname_sort(x, y):
    m = re.compile('(.*) (\S*)$')
    x1 = m.sub(r'\2 \1', x)
    y1 = m.sub(r'\2 \1', y)

    return cmp(x1, y1)
    

def get_playerinfo(soup):
    playerinfo = {}
    players = soup.findAll('a', {'class': 'player'})
    m = re.compile("'([^']*)':'?([^']*)'?[,}]")
    for player in players:
        pinfo = {}
        info = m.findall(player['name'])
        for item in info:
            pinfo[item[0]] = item[1]
        playerinfo[pinfo['name']] = pinfo

    return playerinfo


def get_gameinfo(soup):
    # time, game and map locations
    time = soup.find('span').text
    gameloc = re.sub(time, '', soup.find('h2').text)
    maploc = soup.find('a', {'target': '_blank'})['href']

    # who's doing what
    task_table = soup.find('table', {'class': 'tasks'})
    task_tbody = task_table.find('tbody')
    tasks = task_tbody.findAll('td')
    beers = tasks[0].string
    shirts = tasks[1].string

    return {'gameloc': gameloc, 'time': time, 'maploc': maploc, 'tasks': tasks, 'beers': beers, 'shirts': shirts}

if __name__ == '__main__':
    runapp()
