"""Visualizing Twitter Sentiment Across America"""

from data import word_sentiments, load_tweets
from datetime import datetime
from geo import us_states, geo_distance, make_position, longitude, latitude
from maps import draw_state, draw_name, draw_dot, wait
from string import ascii_letters
from ucb import main, trace, interact, log_current_line
import string
from sys import float_info

###################################
# Phase 1: The Feelings in Tweets #
###################################

# The tweet abstract data type, implemented as a dictionary.

def make_tweet(text, time, lat, lon):
    """Return a tweet, represented as a Python dictionary.

    text  -- A string; the text of the tweet, all in lowercase
    time  -- A datetime object; the time that the tweet was posted
    lat   -- A number; the latitude of the tweet's location
    lon   -- A number; the longitude of the tweet's location

    >>> t = make_tweet("just ate lunch", datetime(2012, 9, 24, 13), 38, 74)
    >>> tweet_text(t)
    'just ate lunch'
    >>> tweet_time(t)
    datetime.datetime(2012, 9, 24, 13, 0)
    >>> p = tweet_location(t)
    >>> latitude(p)
    38
    >>> tweet_string(t)
    '"just ate lunch" @ (38, 74)'
    """
    return {'text': text, 'time': time, 'latitude': lat, 'longitude': lon}


def tweet_text(tweet):
    """Return a string, the words in the text of a tweet."""
    "*** YOUR CODE HERE ***"
    return tweet['text']


def tweet_time(tweet):
    """Return the datetime representing when a tweet was posted."""
    "*** YOUR CODE HERE ***"
    return tweet['time']


def tweet_location(tweet):
    """Return a position representing a tweet's location."""
    "*** YOUR CODE HERE ***"
    return make_position(tweet['latitude'], tweet['longitude'])


# The tweet abstract data type, implemented as a function.

def make_tweet_fn(text, time, lat, lon):
    """An alternate implementation of make_tweet: a tweet is a function.

    >>> t = make_tweet_fn("just ate lunch", datetime(2012, 9, 24, 13), 38, 74)
    >>> tweet_text_fn(t)
    'just ate lunch'
    >>> tweet_time_fn(t)
    datetime.datetime(2012, 9, 24, 13, 0)
    >>> latitude(tweet_location_fn(t))
    38
    """
    "*** YOUR CODE HERE ***"
    # Please don't call make_tweet in your solution
    t = {'text': text, 'time': time, 'lat': lat, 'lon': lon}

    # def tweet(key):
    #     return t[key]
    return lambda key: t[key]


def tweet_text_fn(tweet):
    """Return a string, the words in the text of a functional tweet."""
    return tweet('text')


def tweet_time_fn(tweet):
    """Return the datetime representing when a functional tweet was posted."""
    return tweet('time')


def tweet_location_fn(tweet):
    """Return a position representing a functional tweet's location."""
    return make_position(tweet('lat'), tweet('lon'))

# === +++ ABSTRACTION BARRIER +++ === ###


def tweet_words(tweet):
    """Return the words in a tweet."""
    return extract_words(tweet_text(tweet))


def tweet_string(tweet):
    """Return a string representing a functional tweet."""
    location = tweet_location(tweet)
    point = (latitude(location), longitude(location))
    return '"{0}" @ {1}'.format(tweet_text(tweet), point)


def extract_words(text):
    """Return the words in a tweet, not including punctuation.

    >>> extract_words('anything else.....not my job')
    ['anything', 'else', 'not', 'my', 'job']
    >>> extract_words('i love my job. #winning')
    ['i', 'love', 'my', 'job', 'winning']
    >>> extract_words('make justin # 1 by tweeting #vma #justinbieber :)')
    ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber']
    >>> extract_words("paperclips! they're so awesome, cool, & useful!")
    ['paperclips', 'they', 're', 'so', 'awesome', 'cool', 'useful']
    >>> extract_words('@(cat$.on^#$my&@keyboard***@#*')
    ['cat', 'on', 'my', 'keyboard']
    """
    "*** YOUR CODE HERE ***"
    word, ret = '', []

    for char in text:
        if char in string.ascii_letters:
            word += char
        elif word != '':
            ret.append(word)
            word = ''
    # for final word
    if word != '':
        ret.append(word)

    return ret


def make_sentiment(value):
    """Return a sentiment, which represents a value that may not exist.

    >>> positive = make_sentiment(0.2)
    >>> neutral = make_sentiment(0)
    >>> unknown = make_sentiment(None)
    >>> has_sentiment(positive)
    True
    >>> has_sentiment(neutral)
    True
    >>> has_sentiment(unknown)
    False
    >>> sentiment_value(positive)
    0.2
    >>> sentiment_value(neutral)
    0
    """
    assert value is None or (-1 <= value <= 1), 'Illegal value'
    "*** YOUR CODE HERE ***"
    ret = [True, 0]
    if value is None:
        ret[0] = False
    else:
        ret[1] = value
    return ret


def has_sentiment(s):
    """Return whether sentiment s has a value."""
    "*** YOUR CODE HERE ***"
    return s[0]


def sentiment_value(s):
    """Return the value of a sentiment s."""
    assert has_sentiment(s), 'No sentiment value'
    "*** YOUR CODE HERE ***"
    return s[1]


def get_word_sentiment(word):
    """Return a sentiment representing the degree of positive or negative
    feeling in the given word.

    >>> sentiment_value(get_word_sentiment('good'))
    0.875
    >>> sentiment_value(get_word_sentiment('bad'))
    -0.625
    >>> sentiment_value(get_word_sentiment('winning'))
    0.5
    >>> has_sentiment(get_word_sentiment('Berkeley'))
    False
    """
    # Learn more: http://docs.python.org/3/library/stdtypes.html#dict.get
    return make_sentiment(word_sentiments.get(word))


def analyze_tweet_sentiment(tweet):
    """ Return a sentiment representing the degree of positive or negative
    sentiment in the given tweet, averaging over all the words in the tweet
    that have a sentiment value.

    If no words in the tweet have a sentiment value, return
    make_sentiment(None).

    >>> positive = make_tweet('i love my job. #winning', None, 0, 0)
    >>> round(sentiment_value(analyze_tweet_sentiment(positive)), 5)
    0.29167
    >>> negative = make_tweet("saying, 'i hate my job'", None, 0, 0)
    >>> sentiment_value(analyze_tweet_sentiment(negative))
    -0.25
    >>> no_sentiment = make_tweet("berkeley golden bears!", None, 0, 0)
    >>> has_sentiment(analyze_tweet_sentiment(no_sentiment))
    False
    """
    # You may change any of the lines below.
    "*** YOUR CODE HERE ***"
    sent_value_list = []
    for word in tweet_words(tweet):
        sent = get_word_sentiment(word)
        if has_sentiment(sent):
            sent_value_list.append(sentiment_value(sent))

    if not sent_value_list:
        return make_sentiment(None)
    else:
        total_value = 0
        for value in sent_value_list:
            total_value += value
        return make_sentiment(total_value / len(sent_value_list))


#################################
# Phase 2: The Geometry of Maps #
#################################

def find_centroid(polygon):
    """Find the centroid of a polygon.

    http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon

    polygon -- A list of positions, in which the first and last are the same

    Returns: 3 numbers; centroid latitude, centroid longitude, and polygon area

    Hint: If a polygon has 0 area, use the latitude and longitude of its first
    position as its centroid.

    >>> p1, p2, p3 = make_position(1, 2), make_position(3, 4), make_position(5, 0)
    >>> triangle = [p1, p2, p3, p1]  # First vertex is also the last vertex
    >>> round5 = lambda x: round(x, 5) # Rounds floats to 5 digits
    >>> tuple(map(round5, find_centroid(triangle)))
    (3.0, 2.0, 6.0)
    >>> tuple(map(round5, find_centroid([p1, p3, p2, p1])))
    (3.0, 2.0, 6.0)
    >>> tuple(map(float, find_centroid([p1, p2, p1])))  # A zero-area polygon
    (1.0, 2.0, 0.0)
    """
    "*** YOUR CODE HERE ***"
    a, x, y = 0.0, 0.0, 0.0
    for i in range(len(polygon)):
        j = i
        if (j+1) == len(polygon):
            j = -1
        a += (latitude(polygon[i])*longitude(polygon[j+1]) - latitude(polygon[j+1])*longitude(polygon[i]))/2
        x += (latitude(polygon[i])+latitude(polygon[j+1]))*(latitude(polygon[i])*\
                                    longitude(polygon[j+1]) - latitude(polygon[j+1])*longitude(polygon[i]))
        y += (longitude(polygon[i])+longitude(polygon[j+1]))*(latitude(polygon[i])*\
                                    longitude(polygon[j+1]) - latitude(polygon[j+1])*longitude(polygon[i]))
    if a != 0.0:
        x /= (6*a)
        y /= (6*a)
    else:
        x, y = latitude(polygon[0]), longitude(polygon[0])
    return x, y, abs(a)


def find_state_center(polygons):
    """Compute the geographic center of a state, averaged over its polygons.

    The center is the average position of centroids of the polygons in polygons,
    weighted by the area of those polygons.

    Arguments:
    polygons -- a list of polygons

    >>> ca = find_state_center(us_states['CA'])  # California
    >>> round(latitude(ca), 5)
    37.25389
    >>> round(longitude(ca), 5)
    -119.61439

    >>> hi = find_state_center(us_states['HI'])  # Hawaii
    >>> round(latitude(hi), 5)
    20.1489
    >>> round(longitude(hi), 5)
    -156.21763
    """
    "*** YOUR CODE HERE ***"
    denom, nume_x, nume_y = 0.0, 0.0, 0.0
    for polygon in polygons:
        # print(find_centroid(polygon))
        denom += find_centroid(polygon)[2]
        nume_x += find_centroid(polygon)[0]*find_centroid(polygon)[2]
        nume_y += find_centroid(polygon)[1]*find_centroid(polygon)[2]
    return make_position(nume_x/denom, nume_y/denom)


###################################
# Phase 3: The Mood of the Nation #
###################################

def group_tweets_by_state(tweets):
    """Return a dictionary that aggregates tweets by their nearest state center.

    The keys of the returned dictionary are state names, and the values are
    lists of tweets that appear closer to that state center than any other.

    tweets -- a sequence of tweet abstract data types

    >>> sf = make_tweet("welcome to san francisco", None, 38, -122)
    >>> ny = make_tweet("welcome to new york", None, 41, -74)
    >>> two_tweets_by_state = group_tweets_by_state([sf, ny])
    >>> len(two_tweets_by_state)
    2
    >>> california_tweets = two_tweets_by_state['CA']
    >>> len(california_tweets)
    1
    >>> tweet_string(california_tweets[0])
    '"welcome to san francisco" @ (38, -122)'
    """
    tweets_by_state = {}
    "*** YOUR CODE HERE ***"
    def close_to_state(location):
        distance = float_info.max
        closest_state = ''
        for s in us_states:
            # print(geo_distance(find_state_center(us_states[s]), location), '---------------------')
            if geo_distance(find_state_center(us_states[s]), location) < distance:
                distance = geo_distance(find_state_center(us_states[s]), location)
                closest_state = s
        return closest_state   # if closest_state else None

    for tweet in tweets:
        state = close_to_state(tweet_location(tweet))
        # if state:
        if state not in tweets_by_state:
            tweets_by_state[state] = [tweet]   # list(tweet)   do this make error, just list the keys
            # print(tweets_by_state)
        else:
            tweets_by_state[state].append(tweet)

    return tweets_by_state


def average_sentiments(tweets_by_state):
    """Calculate the average sentiment of the states by averaging over all
    the tweets from each state. Return the result as a dictionary from state
    names to average sentiment values (numbers).

    If a state has no tweets with sentiment values, leave it out of the
    dictionary entirely.  Do NOT include states with no tweets, or with tweets
    that have no sentiment, as 0.  0 represents neutral sentiment, not unknown
    sentiment.

    tweets_by_state -- A dictionary from state names to lists of tweets
    """
    averaged_state_sentiments = {}
    "*** YOUR CODE HERE ***"
    value, i = 0.0, 0
    for state in tweets_by_state:
        for t in tweets_by_state[state]:
            sent = analyze_tweet_sentiment(t)
            if has_sentiment(sent):
                value, i = value + sentiment_value(sent), i + 1
        if value != 0.0:
            averaged_state_sentiments[state] = (value / i)
            value, i = 0.0, 0

    return averaged_state_sentiments


##########################
# Command Line Interface #
##########################

def print_sentiment(text='Are you virtuous or verminous?'):
    """Print the words in text, annotated by their sentiment scores."""
    words = extract_words(text.lower())
    layout = '{0:>' + str(len(max(words, key=len))) + '}: {1:+}'
    for word in words:
        s = get_word_sentiment(word)
        if has_sentiment(s):
            print(layout.format(word, sentiment_value(s)))

def draw_centered_map(center_state='TX', n=10):
    """Draw the n states closest to center_state."""
    us_centers = {n: find_state_center(s) for n, s in us_states.items()}
    center = us_centers[center_state.upper()]
    dist_from_center = lambda name: geo_distance(center, us_centers[name])
    for name in sorted(us_states.keys(), key=dist_from_center)[:int(n)]:
        draw_state(us_states[name])
        draw_name(name, us_centers[name])
    draw_dot(center, 1, 10)  # Mark the center state with a red dot
    wait()

def draw_state_sentiments(state_sentiments):
    """Draw all U.S. states in colors corresponding to their sentiment value.

    Unknown state names are ignored; states without values are colored grey.

    state_sentiments -- A dictionary from state strings to sentiment values
    """
    for name, shapes in us_states.items():
        sentiment = state_sentiments.get(name, None)
        draw_state(shapes, sentiment)
    for name, shapes in us_states.items():
        center = find_state_center(shapes)
        if center is not None:
            draw_name(name, center)

def draw_map_for_query(term='my job'):
    """Draw the sentiment map corresponding to the tweets that contain term.

    Some term suggestions:
    New York, Texas, sandwich, my life, justinbieber
    """
    tweets = load_tweets(make_tweet, term)
    tweets_by_state = group_tweets_by_state(tweets)
    state_sentiments = average_sentiments(tweets_by_state)
    draw_state_sentiments(state_sentiments)
    for tweet in tweets:
        s = analyze_tweet_sentiment(tweet)
        if has_sentiment(s):
            draw_dot(tweet_location(tweet), sentiment_value(s))
    wait()

def swap_tweet_representation(other=[make_tweet_fn, tweet_text_fn,
                                     tweet_time_fn, tweet_location_fn]):
    """Swap to another representation of tweets. Call again to swap back."""
    global make_tweet, tweet_text, tweet_time, tweet_location
    swap_to = tuple(other)
    other[:] = [make_tweet, tweet_text, tweet_time, tweet_location]
    make_tweet, tweet_text, tweet_time, tweet_location = swap_to


@main
def run(*args):
    """Read command-line arguments and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Run Trends")
    parser.add_argument('--print_sentiment', '-p', action='store_true')
    parser.add_argument('--draw_centered_map', '-d', action='store_true')
    parser.add_argument('--draw_map_for_query', '-m', action='store_true')
    parser.add_argument('--use_functional_tweets', '-f', action='store_true')
    parser.add_argument('text', metavar='T', type=str, nargs='*',
                        help='Text to process')
    args = parser.parse_args()
    if args.use_functional_tweets:
        swap_tweet_representation()
        print("Now using a functional representation of tweets!")
        args.use_functional_tweets = False
    for name, execute in args.__dict__.items():
        if name != 'text' and execute:
            globals()[name](' '.join(args.text))
