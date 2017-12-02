import os
import time
from slackclient import SlackClient

from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

# greeting classification training data
train = [
    ('Hi!', 'greeting'),
    ('Hello', 'greeting'),
    ('Hey!', 'greeting'),
    ('Hi everyone', 'greeting'),
    ("Hey bot", 'greeting'),
    ('His car is nice!', 'other'),
    ('Hey, you\'re a bot!', 'other'),
    ("I said hi to him the other day", 'other'),
    ('He is my sworn enemy!', 'other'),
    ('My boss is horrible.', 'other')
]

cl = NaiveBayesClassifier(train)

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "hi"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

if "0".isalpha():
    print("yep")

def handle_command(command, channel, user):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "I just say hello man, don't bother me."
    if cl.classify(command) == "greeting": # replace this with nlp boolean
        response = "Hi <@" + user + ">! I'm John's bot."
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                print("Message received: " + output['text'])
                print("Parsed as: " + output['text'].replace(AT_BOT, "").strip().lower())
                # return text after the @ mention, whitespace removed
                return output['text'].replace(AT_BOT, "").strip().lower(), \
                       output['channel'], \
                       output['user']
    return None, None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
