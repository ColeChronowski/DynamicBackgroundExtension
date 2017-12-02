from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

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
test = [
    ('Hey everybody!', 'greeting'),
    ('He said hello to me', 'other')
]

cl = NaiveBayesClassifier(train)

# Classify some text
print(cl.classify("hi"))  # "greeting"
print(cl.classify("This is a nice pizza"))   # "other"

# Compute accuracy
print("Accuracy: {0}".format(cl.accuracy(test)))

# Show 5 most informative features
cl.show_informative_features(5)
