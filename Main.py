import random
from operator import truediv
import os
import discord

sentenceTemplates = [

    "The {adj1} {noun1} {verb1} the {adj2} {noun2}.",

    "{noun1} {verb1} {adv1}",

    "The {noun1} {verb1} {adv1}",

    "Why does the {noun1} {verb1} {prep1} the {adj1} {noun2}?",

    "If the {noun1} {verb1} {prep1} the {adj1} {noun2}, what happens?",

    "A {adj1} {noun1} {verb1} in the {adj2} {place}.",

    "When {noun1} {verb1}, the {adj1} {noun2} {verb2} {adv1}.",

    "{adv1}, the {adj1} {noun1} {verb1}.",

    "In the {place}, the {noun2} {verb1} {adv1}.",

    "The {noun1} {verb1} because of the {adj1} {noun1}."

]


def conjugate_verb(verb):
    if verb.endswith(('s', 'sh', 'ch', 'x', 'z', 'o')):
        return verb + 'es'
    elif verb.endswith('y') and verb[-2] not in 'aeiou':
        return verb[:-1] + 'ies'
    else:
        return verb + 's'


def generateNoun():
    file = open("Dictionary/nouns.txt")
    nouns = [line.strip() for line in file]
    word = random.choice(nouns)
    file.close()
    return word


def generateVerb():
    file = open("Dictionary/verbs.txt")
    verbs = [line.strip() for line in file]
    word = random.choice(verbs)
    file.close()
    return word


def generateAdj():
    file = open("Dictionary/adjs.txt")
    adj = [line.strip() for line in file]
    word = random.choice(adj)
    file.close()
    return word


def generateAdverb():
    file = open("Dictionary/adverbs.txt")
    adverbs = [line.strip() for line in file]
    word = random.choice(adverbs)
    file.close()
    return word


def generatePlace():
    file = open("Dictionary/places.txt")
    places = [line.strip() for line in file]
    word = random.choice(places)
    file.close()
    return word


def generatePrep():
    file = open("Dictionary/preps.txt")
    preps = [line.strip() for line in file]
    word = random.choice(preps)
    file.close()
    return word


def pickTemplate():
    template = random.choice(sentenceTemplates)
    return template


def generateSentence():
    template = pickTemplate()

    if template.startswith("Why does"):
        verb = generateVerb()
        verb2 = generateVerb()
    else:
        verb = conjugate_verb(generateVerb())
        verb2 = conjugate_verb(generateVerb())

    sentence = template.format(
        noun1=generateNoun(),
        noun2=generateNoun(),
        verb1=verb,
        verb2=verb2,
        adj1=generateAdj(),
        adj2=generateAdj(),
        adv1=generateAdverb(),
        prep1=generatePrep(),
        place=generatePlace()
    )
    return sentence


print(generateSentence())


class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')

    async def on_message(self, message):
        # prevent the bot from responding to itself
        if message.author == self.user:
            return

        if message.content.startswith('!whim'):
            sentence = generateSentence()
            await message.channel.send(sentence)


intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into the environment

# Access your token
discord_token = os.getenv("DISCORD_TOKEN")

client.run(discord_token)