import requests

r=requests.get("https://raw.githubusercontent.com/bieli/stopwords/master/polish.stopwords.txt")
bieli_sw=set(r.content.decode().split('\n')[:-1])

r=requests.get("https://raw.githubusercontent.com/stopwords-iso/stopwords-pl/master/stopwords-pl.txt")
iso_sw=set(r.content.decode().split('\n')[:-1])

SW_list=iso_sw|bieli_sw

with open("data/stop_words.txt", "w") as f:
    for word in sorted(SW_list):
        f.write("{}\n".format(word))
