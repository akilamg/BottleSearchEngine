from bottle import route, run, request, template, static_file, get, redirect, app, Bottle, error
from beaker.middleware import SessionMiddleware

from oauth2client.client import OAuth2WebServerFlow, flow_from_clientsecrets
from googleapiclient.discovery import build

from youtubeAPI import youtube_search
from pymongo import MongoClient
import sys
import json
import httplib2
from spellcheck import correct

#Define history data as a global dictionary to store previously queried words and their word count in total
USER_HISTORY = {}
code = ""
use_google_login = True
HOST = 'localhost'
DB_HOST = 'localhost'
DB_PORT = 27017
urls_rank = []

baseURL = "http://" + HOST + ":8080"
SCOPE = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'
REDIRECT_URI = 'http://'+ HOST + ':8080/redirect'
#Configure middleware
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True,
}

#initialize bottle app
b_app = app()
session_app = SessionMiddleware(b_app, session_opts)

# Initialize mongodb connection
client = MongoClient(DB_HOST, DB_PORT)
db = client.randomSearch

@route('/')
def frontEnd():
    """Returns the homepage at frontEnd.html"""
    user = None
    signin_state = "Sign in with Google+"
    link = "sign-in"
    input = request.query.get("keywords")
    page = request.query.get("page")
    math = request.query.get("math")
    image_input = request.query.get("image_keywords")
    video_input = request.query.get("video_keywords")

    # if the query parameters contain an invalid path, return the error page instead
    if not queryCheck(request.query):
        return error_page()

    # if it's a get request, treat it as a query or page update, otherwise proceed as usual
    if not input is None:
        if not page is None:
            return updatePage(input, int(page), math)
        else:
            return querySubmit(input, math)
    # image search
    elif not image_input is None:
        if not page is None:
            return updateImgPage(image_input, int(page))
        else:
            return queryImgSubmit(image_input)
    # video search
    elif not video_input is None:
        if not page is None:
            return updateVidPage(video_input, int(page))
        else:
            return queryVidSubmit(video_input)

    # if none of the above, it's a login request, set login parameters to be signed in
    else:
        if use_google_login:
            session = request.environ.get('beaker.session')
            user = session.get('user', None)
            if not user is None:
                signin_state = "Sign Out"
                link = "sign-out"

        return template('templates/homePage.tpl', link=link, signin_state=signin_state, user=user)

@error(404)
@error(405)
@error(500)
def error_page(error=404):
    """Redirect to error page incase of incorrect pathing or unauthorized access"""
    return template('templates/errorPage.tpl')

@route('/redirect')
def session_google():
    """When redirected to the query page use google login or browse anonymously"""
    if use_google_login:
        CLIENT_ID = ''
        CLIENT_SECRET = ''

        with open('client_secrets.json') as data_file:
            data = json.load(data_file)
            CLIENT_ID = data['web']['client_id']
            CLIENT_SECRET = data['web']['client_secret']

        code = request.query.get('code', '')

        flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                                   client_secret=CLIENT_SECRET,
                                   scope=['profile', 'email'],
                                   redirect_uri=REDIRECT_URI)

        # get access token
        credentials = flow.step2_exchange(code)
        token = credentials.id_token['sub']

        http = httplib2.Http()
        http = credentials.authorize(http)

        # get email
        users_service = build('oauth2', 'v2', http=http)
        user_document = users_service.userinfo().get().execute()
        user_email = user_document['email']

        # get other user information
        users_service = build('plus', 'v1', http=http)

        session= request.environ.get('beaker.session')
        session['user'] = user_email
        session.save()

        redirect(Bottle.get_url(b_app, '/'))

def queryCheck(request):
    """Checks requests made to the server, and only accept the ones that a recognized"""

    recognized_req = ['keywords', 'image_keywords', 'video_keywords', 'page', 'math']
    for key, value in request.items():
        if not key in recognized_req:
            return False

    return True

# Default search features

def querySubmit(input, math=None):
    """"Retrieves the links to pages that contain the input string.
    This function will only display the first 5 entries based on page rank
    and relevance (higher the number words that match to the given link,
    the higher the relevance), the rest will be paginated."""
    isSpelledCorrect = True
    search_words = input.split(" ")
    spelled_words = []
    sites_matched = []
    url_to_word = {}
    check_None = lambda a, b: b in a and a[b] or ""

    for word in search_words:
        if word!="":
            spelled_words.append(correct(word))
        else:
            spelled_words.append("")
        sites_info = get_site_info(word)
        sites_matched += sites_info
        for site in sites_info:
            if not site['Url'] in url_to_word:
                url_to_word[site['Url']] = [word]
            elif not word in url_to_word[site['Url']]:
                url_to_word[site['Url']].append(word)

    # Rank the sites
    site_rank = [(check_None(s_info, 'Url'), check_None(s_info,'PageRank') or '', \
                  check_None(s_info, 'Title') or '', check_None(s_info, 'Description'))\
                 for s_info in sites_matched]
    if spelled_words != list(search_words):
        isSpelledCorrect = False

    # Sort urls based on rank
    site_rank.sort(key=lambda tup: tup[1], reverse=True)

    # Calculate the relevance of sites based on searched words
    site_relevance = []
    for site in site_rank:
        site_relevance.append((site[0], len(url_to_word[site[0]]), site[2], site[3]))

        site_relevance.sort(key=lambda tup: tup[1], reverse=True)

    pg_tot = len(site_relevance)
    if 5 > pg_tot:
        u_ = pg_tot
    else:
        u_ = 5

    #place urls-rank in a session variable for quick access
    session = request.environ.get('beaker.session')
    session['site_relevance'] = site_relevance
    session.save()

    user = None
    signin_state = "Sign in with Google+"
    link = "sign-in"
    if use_google_login:
        session = request.environ.get('beaker.session')
        user = session.get('user', None)
        if not user is None:
            signin_state = "Sign Out"
            link = "sign-out"

        return template('templates/results.tpl', spellcheck=isSpelledCorrect,corrected_search=" ".join(spelled_words),
                        correct_link="?keywords="+"+".join(spelled_words), queryInput=input, user=user, link=link,
                        signin_state=signin_state, siteList=site_relevance[0:u_], page=1, pg_tot=pg_tot, math=math)

def updatePage(input, page=1, math=None):
    """Update page numbering and shows the offset of 5 entries that correspond to
     the given page number"""

    session = request.environ.get('beaker.session')
    site_relevance = session.get('site_relevance', None)

    if site_relevance is None:
        search_words = input.split(" ")
        sites_matched = []
        url_to_word = {}
        check_None = lambda a, b: b in a and a[b] or ""

        for word in search_words:
            sites_info = get_site_info(word)
            sites_matched += sites_info
            for site in sites_info:
                if not site['Url'] in url_to_word:
                    url_to_word[site['Url']] = [word]
                elif not word in url_to_word[site['Url']]:
                    url_to_word[site['Url']].append(word)

        # Rank the sites
        site_rank = [(check_None(s_info, 'Url'), check_None(s_info, 'PageRank') or '', \
                    check_None(s_info, 'Title') or '', check_None(s_info, 'Description')) \
                    for s_info in sites_matched]

        # Calculate the relevance of sites based on searched words
        site_relevance = []
        for site in site_rank:
            site_relevance.append((site[0], len(url_to_word[site[0]]), site[2], site[3]))

            site_relevance.sort(key=lambda tup: tup[1], reverse=True)

    pg_tot = len(site_relevance)
    if 5 * page > pg_tot:
        u_ = pg_tot
    else:
        u_ = 5 * page
    l_ = 5 * (page - 1)

    return template('templates/results_view.tpl', siteList=site_relevance[l_:u_], page=page, pg_tot=pg_tot)

# Image search features

def queryImgSubmit(input):
    """Query the images stored in the database that match to the given input string.
    This function will only display the first 5 images based on relevance."""
    isSpelledCorrect = True
    search_words = input.split(" ")
    img_to_word = {}
    spelled_words = []
    for word in search_words:
        if word!="":
            spelled_words.append(correct(word))
        else:
            spelled_words.append("")
        imgs = get_images(word.lower())
        for img in imgs:
            if not img in img_to_word:
                img_to_word[img] = [word]
            elif not word in img_to_word[img]:
                img_to_word[img].append(word)

    img_relevance = []
    if spelled_words != list(search_words):
        isSpelledCorrect = False
    for img, words in img_to_word.items():
        img_relevance.append((img, len(words)))

    img_relevance.sort(key=lambda tup: tup[1], reverse=True)

    pg_tot = len(img_relevance)
    if 5 > pg_tot:
        u_ = pg_tot
    else:
        u_ = 5

    # place image-rank in a session variable for quick access
    session = request.environ.get('beaker.session')
    session['img_relevance'] = img_relevance
    session.save()

    user = None
    signin_state = "Sign in with Google+"
    link = "sign-in"
    if use_google_login:
        session = request.environ.get('beaker.session')
        user = session.get('user', None)
        if not user is None:
            signin_state = "Sign Out"
            link = "sign-out"

    return template('templates/img_results.tpl',spellcheck=isSpelledCorrect,corrected_search=" ".join(spelled_words),
                    correct_link="?image_keywords="+"+".join(spelled_words), queryInput=input, user=user, link=link,
                    signin_state=signin_state, imgList=img_relevance[0:u_], page=1, pg_tot=pg_tot)

def updateImgPage(input, page=1):
    """Update page numbering and shows the offset of 5 entries that correspond to
     the given page number"""

    session = request.environ.get('beaker.session')
    img_relevance = session.get('img_relevance', None)

    if img_relevance is None:
        search_words = input.split(" ")
        img_to_word = {}
        for word in search_words:
            imgs = get_images(word.lower())
            for img in imgs:
                if not img in img_to_word:
                    img_to_word[img] = [word]
                elif not word in img_to_word[img]:
                    img_to_word[img].append(word)

        img_relevance = []
        for img, words in img_to_word.items():
            img_relevance.append((img, len(words)))

        img_relevance.sort(key=lambda tup: tup[1], reverse=True)

    pg_tot = len(img_relevance)
    if 5 * page > pg_tot:
        u_ = pg_tot
    else:
        u_ = 5 * page
    l_ = 5 * (page - 1)

    return template('templates/img_results_view.tpl', imgList=img_relevance[l_:u_], page=page, pg_tot=pg_tot)

# Video search features

def queryVidSubmit(input):
    """Query the videos on youtube that match to the given input string.
    This function will only display the first 5 images based on relevance."""

    isSpelledCorrect = True
    spelled_words = []
    if input == '':
        vidList = []
    else:
        for word in input.split(" "):
            if word!="":
                spelled_words.append(correct(word))
            else:
                spelled_words.append("")
        vidList = youtube_search({'q': input, 'max_results': 40})

    # place videos in a session variable for quick access
    session = request.environ.get('beaker.session')
    session['vidList'] = vidList
    session.save()
    if spelled_words != list(input.split(" ")):
        isSpelledCorrect = False
    pg_tot = len(vidList)
    if 5 > pg_tot:
        u_ = pg_tot
    else:
        u_ = 5

    user = None
    signin_state = "Sign in with Google+"
    link = "sign-in"
    if use_google_login:
        session = request.environ.get('beaker.session')
        user = session.get('user', None)
        if not user is None:
            signin_state = "Sign Out"
            link = "sign-out"

    return template('templates/video_results.tpl', spellcheck=isSpelledCorrect,corrected_search=" ".join(spelled_words),
                    correct_link="?video_keywords="+"+".join(spelled_words), queryInput=input, user=user, link=link,
                    signin_state=signin_state, vidList=vidList[0:u_], page=1, pg_tot=pg_tot)

def updateVidPage(input, page=1):
    """Update page numbering and shows the offset of 5 entries that correspond to
    the given page number"""

    session = request.environ.get('beaker.session')
    vidList = session.get('vidList', None)

    if vidList is None:
        vidList = youtube_search({'q': input, 'max_results': 40})

    pg_tot = len(vidList)
    if 5 * page > pg_tot:
        u_ = pg_tot
    else:
        u_ = 5 * page
    l_ = 5 * (page - 1)

    return template('templates/video_results_view.tpl', vidList=vidList[l_:u_], page=page, pg_tot=pg_tot)

# Login features

@get('/sign-in')
def signIn():
    """Sign in request using a get method"""
    session = request.environ.get('beaker.session')
    if session.get('user', None) is None:
        googleAPI()
    else:
        redirect(Bottle.get_url(b_app, '/'))

@get('/sign-out')
def signOut():
    """Sign out request using a get method"""
    session = request.environ.get('beaker.session')
    session['user'] = None
    session.save()
    redirect(Bottle.get_url(b_app, '/'))


def googleAPI():
    """Connect to google API"""

    #google api set up
    flow = flow_from_clientsecrets('client_secrets.json',
                                   scope=SCOPE,
                                   redirect_uri=REDIRECT_URI)
    uri = flow.step1_get_authorize_url()
    redirect(str(uri))

# File Referencing
@route('/static/<path:path>')
def server_static(path):
    "Routes static files (HTML, CSS, JS or images) references to their correct file path"
    return static_file(path, root='')

@route('/fonts/<filename>')
def server_fonts(filename):
    "Routes static files in the fonts directory (HTML, CSS, JS or images) references to their correct file path"
    return static_file("fonts/"+ filename, root='')

# Database Access
def get_site_info(word):
    result = db.docs.find_one({'Word': word})
    if result != None:
        return result['Docs']
    else:
        return []

def get_images(word):
    """Retrieve matching image source for a given word by querying the database"""
    result = db.img_docs.find_one({'Word': word})
    if result != None:
        return result['Sources']
    else:
        return []


# Run the server on provided host at port 8080 and app session described
run(host=HOST, port=8080, app=session_app)