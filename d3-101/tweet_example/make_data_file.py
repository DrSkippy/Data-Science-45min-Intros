import json
import fileinput

num_records = 50
users = ['alibabaoglan']
tweets = []

for record in fileinput.input("test_twitter_data.json"):
    try:
        t = json.loads(record)
        if t['actor']['preferredUsername'] not in users:
            users.append(t['actor']['preferredUsername'])
            tweets.append(t)
    except ValueError:
        continue
    except KeyError:
        continue
    if len(tweets) == num_records:
        break

print json.dumps(tweets)
