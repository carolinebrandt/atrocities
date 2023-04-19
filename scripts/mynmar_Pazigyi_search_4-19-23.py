from twarc import Twarc2, expansions
import datetime
import json
import pandas as pd
import boto3

aws_access_key_id = "AKIAVJ3SQGJ4NVNEMLGP"
aws_secret_access_key = "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"

s3 = boto3.client('s3',
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  region_name='eu-north-1'
                  )

# Replace your bearer token below
client = Twarc2(
    bearer_token="AAAAAAAAAAAAAAAAAAAAAK97MgEAAAAA14ENaO5sd4600Q%2BWiMB7mehBHmM%3DWMpwqpHI9OnSqTY2DNDWmJuxD2C1vdvrMKMaQzLMUADCeIhQMS")

# with open('/Users/carolinebrandt/Dropbox/AAA_Projects/Atrocities/INGOs/Writing/intextstatistics/no_of_accounts.txt', 'w') as f:
#     f.write(str(len(handles)))

data = []


def main():
    # Specify the start time in UTC for the time period you want Tweets from
    start_time = datetime.datetime(2023, 4, 9, 0, 0, 0, 0, datetime.timezone.utc)

    # Specify the end time in UTC for the time period you want Tweets from
    end_time = datetime.datetime(2023, 4, 18, 0, 0, 0, 0, datetime.timezone.utc)

    # This is where we specify our query as discussed in module 5
    query = "Pazigyi"

    # The search_all method call the full-archive search endpoint to get Tweets based on the query, start and end times
    search_results = client.search_all(query="query", start_time=start_time, end_time=end_time, max_results=100,
                                       media_fields="url", expansions="attachments.media_keys")

    # Twarc returns all Tweets for the criteria set above, so we page through the results
    for page in search_results:
        # The Twitter API v2 returns the Tweet information and the user, media etc.  separately
        # so we use expansions.flatten to get all the information in a single JSON
        result = expansions.flatten(page)
        for tweet in result:
            data.append(tweet)

        with open('myan_april_2023.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        json_data = json.dumps(data)
        s3.put_object(Body=json_data, Bucket='myan2023', Key='myan_april_2023.json')


if __name__ == "__main__":
    main()