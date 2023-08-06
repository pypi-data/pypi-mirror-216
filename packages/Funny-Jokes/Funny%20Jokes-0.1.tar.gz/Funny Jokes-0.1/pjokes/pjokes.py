import random
from markdown import markdown
# from jokes import jokelist

jokelist = [
    "Complaining about the lack of smoking shelters, the nicotine addicted Python programmers said there ought to be 'spaces for tabs'.",
    "Ubuntu users are apt to get this joke.",
    "Obfuscated Reality Mappers (ORMs) can be useful database tools.",
    "Asked to explain Unicode during an interview, Geoff went into detail about his final year university project. He was not hired.",
    "Triumphantly, Beth removed Python 2.7 from her server in 2030. 'Finally!' she said with glee, only to see the announcement for Python 4.4.",
    "An SQL query goes into a bar, walks up to two tables and asks, 'Can I join you?'",
    "When your hammer is C++, everything begins to look like a thumb.",
    "If you put a million monkeys at a million keyboards, one of them will eventually write a Java program. The rest of them will write Perl.",
    "To understand recursion you must first understand recursion.",
    "I suggested holding a 'Python Object Oriented Programming Seminar', but the acronym was unpopular.",
    "'Knock, knock.' 'Who's there?' ... very long pause ... 'Java.'",
    "How many programmers does it take to change a lightbulb? None, that's a hardware problem.",
    "What's the object-oriented way to become wealthy? Inheritance.",
    "Why don't jokes work in octal? Because 7 10 11.",
    "How many programmers does it take to change a lightbulb? None, they just make darkness a standard.",
    "Two bytes meet. The first byte asks, 'Are you ill?' The second byte replies, 'No, just feeling a bit off.'",
    "Two threads walk into a bar. The barkeeper looks up and yells, 'Hey, I want don't any conditions race like time last!'",
    "Old C programmers don't die, they're just cast into void.",
    "Eight bytes walk into a bar. The bartender asks, 'Can I get you anything?' 'Yeah,' replies the bytes. 'Make us a double.'",
    "Why did the programmer quit his job? Because he didn't get arrays.",
    "Why do Java programmers have to wear glasses? Because they don't see sharp."
]


def get_joke():
    return markdown(random.choice(jokelist))

