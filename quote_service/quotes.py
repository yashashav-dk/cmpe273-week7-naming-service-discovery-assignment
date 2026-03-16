import random

QUOTES = [
    {"text": "You have power over your mind - not outside events. Realize this, and you will find strength.", "book": "Meditations, Book 6"},
    {"text": "The happiness of your life depends upon the quality of your thoughts.", "book": "Meditations, Book 5"},
    {"text": "Waste no more time arguing about what a good man should be. Be one.", "book": "Meditations, Book 10"},
    {"text": "The best revenge is not to be like your enemy.", "book": "Meditations, Book 6"},
    {"text": "Accept the things to which fate binds you, and love the people with whom fate brings you together.", "book": "Meditations, Book 6"},
    {"text": "When you arise in the morning think of what a privilege it is to be alive, to think, to enjoy, to love.", "book": "Meditations, Book 5"},
    {"text": "It is not death that a man should fear, but he should fear never beginning to live.", "book": "Meditations, Book 8"},
    {"text": "Never esteem anything as of advantage to you that will make you break your word or lose your self-respect.", "book": "Meditations, Book 3"},
    {"text": "The soul becomes dyed with the colour of its thoughts.", "book": "Meditations, Book 5"},
    {"text": "Very little is needed to make a happy life; it is all within yourself in your way of thinking.", "book": "Meditations, Book 7"},
    {"text": "Loss is nothing else but change, and change is Nature's delight.", "book": "Meditations, Book 9"},
    {"text": "How much more grievous are the consequences of anger than the causes of it.", "book": "Meditations, Book 11"},
    {"text": "Dwell on the beauty of life. Watch the stars, and see yourself running with them.", "book": "Meditations, Book 7"},
    {"text": "The object of life is not to be on the side of the majority, but to escape finding oneself in the ranks of the insane.", "book": "Meditations, Book 6"},
    {"text": "Everything we hear is an opinion, not a fact. Everything we see is a perspective, not the truth.", "book": "Meditations, Book 4"},
    {"text": "If it is not right do not do it; if it is not true do not say it.", "book": "Meditations, Book 12"},
    {"text": "The impediment to action advances action. What stands in the way becomes the way.", "book": "Meditations, Book 5"},
    {"text": "Do not indulge in dreams of having what you have not, but reckon up the chief of the blessings you do possess.", "book": "Meditations, Book 7"},
    {"text": "Begin each day by telling yourself: Today I shall be meeting with interference, ingratitude, insolence, disloyalty, ill-will, and selfishness.", "book": "Meditations, Book 2"},
    {"text": "Look well into thyself; there is a source of strength which will always spring up if thou wilt always look.", "book": "Meditations, Book 7"},
]


def get_random_quote():
    return random.choice(QUOTES)
