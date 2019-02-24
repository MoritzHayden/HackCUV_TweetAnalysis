# from aylienapiclient import textapi

# client = textapi.Client("9285c70a", "b584db7607f9ce7421e9aab4a95f394f")
# sentiment = client.Sentiment({'text': 'John is a very good football player!'})
# print(sentiment)

import requests
import json

test_phrases = ["I am not happy", "I am very happy", "I love chocolate", "I hate chocolate"]
results = []
f = open("result.txt", "w")
concat_line = ""
testsite_array = []
with open('tweets', encoding = "utf8") as my_file:
    testsite_array = my_file.readlines()


for line in testsite_array:
	concat_line = concat_line + line

for phrase in testsite_array:
  response = requests.post("https://text-sentiment.p.rapidapi.com/analyze",
  headers={
   	"X-RapidAPI-Key": "6bde0e5f4dmsh90a1686a25bb696p1f1051jsnb55aa01cecf8",
  	"Content-Type": "application/x-www-form-urlencoded"
  },
  params={
   	"text": phrase
  })
  results.append(json.loads(response.text))
  print(response.text)
  # f.write(response.text)

no_pos = 0
no_neg = 0
no_neutral = 0

for result in results:
	# print(result["pos_percent"])
	if result["pos_percent"]> result["neg_percent"]:
		no_pos+=1
	elif result["pos_percent"]< result["neg_percent"]:
		no_neg+=1
	else:
		no_neutral+=1

r = requests.post(
    "https://api.deepai.org/api/summarization",
    data={
        'text': concat_line,
    },
    headers={'api-key': '66e9a48a-32d6-4863-acdb-037cd1b67efc'}
)
print(r.json())
output_summary = r.json()

total = no_neutral + no_neg + no_pos

print("Percent positive: ", no_pos/total * 100)
print("Percent negative: ", no_neg/total * 100)
print("Percent neutral: ", no_neutral/total * 100)

f.write("Percent positive: "+ str(no_pos/total * 100) + "\n")
f.write("Percent negative: "+ str(no_neg/total * 100)+ "\n")
f.write("Percent neutral: "+ str(no_neutral/total * 100)+ "\n")
f.write("Summary: "+ output_summary["output"])



