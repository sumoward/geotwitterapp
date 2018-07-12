#!/usr/bin/env python
import gmplot
import tweepy
from bottle import route, run, template, request


from src.coords_form import CoordsForm



@route('/', method=['GET'])
def index():
    return template('index_template', error='')


@route('/map', method=['POST'])
def map():
    form = CoordsForm(request.forms)
    if request.method == 'POST' and form.validate():
        coords_available, tweet_details = prepare_response(request.forms)
        if coords_available:
            return template('my_map')
        else:
            return template('tweet_template', tweet_details=tweet_details)
    return template('index_template', error='Please submit accurate coordinates')


def prepare_response(coords):
    lat = float(coords.get('latitude'))
    long = float(coords.get('longitude'))
    coords_available, tweets_details = tweet_per_coords(lat, long)

    if coords_available:
        build_map(lat, long, tweets_details)
    return coords_available, tweets_details


def build_map(lat, long, tweet_details):
    # I had intended to use the map as the default but twitter is no longer returning plentiful coordinates
    # Place map
    gmap = gmplot.GoogleMapPlotter(lat, long, 8)

    for detail in tweet_details:
        # if we have been given coordinates lets render them on a map
        if detail['lat']:
            #gmplot gets flaky with unicode, so we decode the text
            gmap.marker(float(detail['lat']), float(detail['long']), 'cornflowerblue', title=detail['tweet'].encode())

    # Draw te map that we will use if cordinates are actually present
    gmap.draw("views/my_map.html")


def get_tweet_details(tweets):
    tweet_details = []
    for tweet in tweets:
        detail = {}
        detail['lat'] = tweet.coordinates['coordinates'][0] if tweet.coordinates else tweet.coordinates
        detail['long'] = tweet.coordinates['coordinates'][1] if tweet.coordinates else tweet.coordinates
        detail['tweeter'] = tweet.user.screen_name
        detail['tweet'] = tweet.text
        tweet_details.append(detail)
    return tweet_details


def connector():
    # you will need to add your own keys for twitter api
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    print(api.me().name)
    return api


def tweet_per_coords(latitude=53.349137, longitude=-6.247750999999994, max_range=100, num_results=10000):
    api = connector()
    tweets = api.search(q="", geocode="%f,%f,%dkm" % (latitude, longitude, max_range), count=num_results)
    print('We have collected the following number of tweets: ' + str(len(tweets)))
    # this is a sense check as i discovered very few coords being returned
    coords_available = False
    for tweet in tweets:
        if not tweet.coordinates:
            print('no coords in this tweet')
            continue
        print('A sense check that lets us see how many tweets have coordinates. This one has lat: ' + str(
            tweet.coordinates['coordinates'][0]) + 'long: ' + str(tweet.coordinates['coordinates'][1]))
        coords_available = True
    tweet_details = get_tweet_details(tweets)
    return coords_available, tweet_details


if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)
