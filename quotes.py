import random 

popularQuotes = [
    ("It's how you deal with failure that determines how you achieve success.", "David Feherty"), 
    ("An investment in knowledge pays the best interest.","Benjamin Franklin"),
    ("Formal education will make you a living; self-education will make you a fortune.","Jim Rohn"), 
    ("The real measure of your wealth is how much you'd be worth if you lost all your money.","Anonymous"), 
    ("You must gain control over your money or the lack of it will forever control you.","Dave Ramsey"), 
    ("Courage is being scared to death, but saddling up anyway.","John Wayne"), 
    ("The successful warrior is the average man, with laser-like focus. ","Bruce Lee"), 
    ("The question isn’t who is going to let me; it’s who is going to stop me.","Ayn Rand"), 
    ("Screw it, Let’s do it!","Richard Branson"), 
    ("As long as you’re going to be thinking anyway, think big.","Donald Trump")
]

def generateQuote() : 
    return popularQuotes[random.randint(0, len(popularQuotes)-1)]

if __name__ == "__main__" :
    generateQuote()