#!/usr/bin/env python3

import os
import openai
from dotenv import load_dotenv
import pandas as pd


# First we import the OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Import csv with contact data
contact_data = pd.read_csv("Data so far with email fields.csv")
print(contact_data.columns)

# Initialise a list which will hold all contact prompt lists
contact_prompt_lists = []

# Define a prompt list for each contact
for index, row in contact_data.iterrows():

    prompt_list = [
        {"role": "user", "content":
        """Write a casual follow up email of no more than 100 words to someone you met at the Gamescom conference in Singapore. I will provide context.

        Name: {}
        Surname: {}
        Company: {}
        Info about company: {}
        Position: {}
        Location: {}
        Previous experience with influencer marketing: {}
        Needs: {}
        Pain points: {}
        Fun fact / hook: {}
        Miscellaneous information: {}
        """.format(row["First Name"],
                   row["Surname"],
                   row["Company"],
                   row["if no website, info about the company"],
                   row["Position"],
                   row["Location"],
                   row["Previous experience with IM"],
                   row["Needs"],
                   row["Other pain points"],
                   row["Fun fact / Hook (favorite game)"],
                   row["Notes"],
                   )
        },
        {"role": "user", "content": "It's been four days since you sent your last email. They haven't replied yet. Please send another follow up email of less than 100 words asking if they've had the time to read your previous message. At the end, offer them our intro deck to look over and let them know to get back in contact if they have any questions."
        },
        {"role": "user", "content": "It's been 11 days since you sent your last email. They haven't replied yet. Please send another follow up email of less than 250 words. Mention some of the benefits of influencer marketing in bullet point form, namely: Influencers have a powerful voice that will vouch for your game, creating reputation & trust; Creator codes and other affiliate programs incentivize influencers to help your game acquire users and with IAP; Influencers create video content that is permanently accessible on social media and reach organic growth, while ads are limited directly to the invested budget; Influencers prefer direct cooperation, rather than running ads of which the platform will take their cut; Social Media provides direct audience feedback; About 42.5% of users are using ad-blocks and are therefore missed out on by paid ads targeting, so an additional marketing channel fills this gap"
        },
        {"role": "user", "content": "It's been 24 days since you sent your last email. They haven't replied yet. Please send another follow up email of less than 100 words. Emphasise that influencer marketing can increase their game's user acquisition. ns."},
        {"role": "user", "content": "It's been 1 month since you sent your last email. They haven't replied yet. Please send another follow up email of less than 100 words. Emphasise that CreatorDB is skilled at cross-border campaigns in Japan, South Korea, Taiwan, and SEA."},
    ]
    contact_prompt_lists.append(prompt_list)
    print("Prompt list appended to contact prompt lists")

# System prompt
system_prompt = {"role": "system", "content": "You are a business development manager from CreatorDB. CreatorDB is an influencer marketing agency that helps games companies execute influencer marketing campaigns. You have just come back from a business trip to Singapore for the Gamescom conference where you have spoken to many influential people in the gaming industry who are looking to do influencer marketing."}

output_list_list = []

for prompt_list in contact_prompt_lists:

    # We define a message list which is passed to the ChatCompletion API
    message_list = []

    # Append the system prompt to the message list
    message_list.append(system_prompt)

    output_list = []

    # Append prompts one by one and run the ChatCompletion API, appending the output to the message list so that ChatGPT remembers previous output
    for prompt in prompt_list:

        # Append new prompt to chat history
        message_list.append(prompt)

        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_list
        )

        output = completion.choices[0].message
        print(output)

        # Append the actual content to a list tied to a specific contact
        output_list.append(output.content)
        print("Output content appended to output list")

        # Append output to message list for chat history
        message_list.append(output)

    # Append all content for a specific contact to a master list
    output_list_list.append(output_list)
    print("Output list appended to master output list")

# Append content to appropriate rows
for index, row in contact_data.iterrows():
    row["Email 1"] = output_list_list[index][0]
    print(row["Email 1"])
    row["Email 2"] = output_list_list[index][1]
    print(row["Email 2"])
    row["Email 3"] = output_list_list[index][2]
    print(row["Email 3"])
    row["Email 4"] = output_list_list[index][3]
    print(row["Email 4"])
    row["Email 5"] = output_list_list[index][4]
    print(row["Email 5"])
