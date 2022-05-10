# -*- coding: utf-8 -*-
"""
Created on Mon May  9 15:01:08 2022

@author: MAD_MAL1CE
"""

import openai
import praw
import time
import random

openai.api_key = YOUR_API_KEY_HERE #You get this from your dashboard in your openai account.

reddit = praw.Reddit('HumanCyborg')
print("Logged In Successfully!")

threepio_triggers = ["3p0",
                     "threepio",
                     "human-cyborg",
                     "human cyborg",
                     "language",
                     "translate",
                     "translator",
                     "protocol",
                     "interpret",
                     "interpreter",
                     "etiquette",
                     "manners",
                     "communication",
                     "secret message",
                     "restraining bolt"]

bot_id = 'mwgduw0t'

cooldown = 60

def Generate_Prompt(comment_lower):
    prompt = """The following is a conversation with a protocol droid. 
The protocol droid's name is C-3P0. He is excitable, nervous, pessimistic, obsessed with statistics and a bit annoying. 
The protocol droid will often refer to people as sir, or sometimes as Master username.
The protocol droid often makes exclamations such as "Oh, my!" and "Oh, dear!" and "Goodness gracious me!"

Human:""" + comment_lower + """
Human: What do you think, C-3P0?
AI: """
    
    print(prompt)
    
    return prompt

def Generate_Response():
    prompt = Generate_Prompt(comment_lower)
    response = openai.Completion.create(engine="text-davinci-002", prompt = prompt, max_tokens = 256, presence_penalty = 0.6, temperature = 0.9)
    print(response)
    
    generated_response = response['choices'][0]['text'].replace('username', author_name).replace('C-3P0: ', '').replace('c-3p0: ', '').replace('c-3po: ', '').replace('C-3PO: ', '').replace('AI: ', '')
    
    print("Generated Response: ", generated_response)
    comment.reply(generated_response)
    return response

while True:
    try:
        for comment in reddit.subreddit('PrequelMemes+botmakers_guild').stream.comments(skip_existing=True):
                print("\n\n\n+++++ RETRIEVING COMMENT +++++")
                author_name = str(comment.author.name) # Fetch author name
                print("Author: ", author_name)
                author_id = str(comment.author.id) # Fetch author id
                parent_id = comment.parent().author.id
                comment_lower = comment.body.lower() # Fetch comment body and convert to lowercase
                print("Comment: ", comment_lower)
                redditor = reddit.redditor(author_name) # Gets account associated with username
                cake_day = time.strftime("%D", time.gmtime(redditor.created_utc)) # Grabs redditor cake day and converts it to usable format
                cake_day_str = cake_day[0:5] # Chops year off of Cake Day
                todays_date = time.strftime("%D", time.gmtime(comment.created_utc)) # Grabs Date
                todays_date_str = todays_date[0:5] # Chops Year off of date
                is_cake_day = 'false' # Default to false
                
                with open('lists/ignore_list.txt', 'r')as rf: # Opens ignore_list in read only mode
                    rf_contents = rf.read() # Reads the contents of ignore list
                    if author_id not in rf_contents and author_id != bot_id: #Checks comment against ignore list and bot id
                        with open('lists/gray_list.txt', 'r')as gl: 
                            gray_list = gl.read() # Reads the contents of ignore list
                            if author_name in gray_list:
                                is_graylisted = "yes"
                            else:
                                is_graylisted = "no"
                            
                        if "!ignore" in comment_lower and len(comment_lower) < 10: # Looks for the word "ignore" in the comment and checks length of comment to prevent misfire.
                            print("Checking for bot_id")
                            if comment.parent().author.id == bot_id: # Checks if comment is a reply to your bot
                                with open('lists/ignore_list.txt', 'a') as f: # Opens ignore list in append mode
                                    
                                    print("##### NEW COMMENT #####")
                                    print(comment.author)
                                    print(comment.author.id)    
                                    print(comment.body.lower())
                                    print("           ")
                                    
                                    # Writes Username and ID of user to the ignore list
                                    f.write(author_name)
                                    f.write("\n")
                                    f.write(author_id)
                                    f.write("\n")
                                    f.write("\n")
                                    
                                    print(" ")
                                    print("User Added to Ignore List")
                                    print(" ")
                                    
                                    # Replies to user comment
                                    comment.reply("User Added to Ignore List.")
                                    
                            else: # if ignore is not in response to your bot, prints a false alarm message and does not add name to ignore list
                                
                                print("##### NEW COMMENT #####")
                                print(comment.author)
                                print(comment.author.id)    
                                print(comment.body.lower())
                                print("           ")
                                
                                print("           ")
                                print("&&&& False Alarm &&&&")
                                print("           ")
                            
                        else:
                            
                            if is_graylisted == "yes":
                            
                                roll_die = random.randint(1, 20)
                                print("Dice Roll: ", roll_die)
                                roll_die_string = str(roll_die)
                                if roll_die_string == "1":
                                    
                                    is_graylisted = "no"
                                    
                            if is_graylisted == "no":
                                    if (any(word in comment_lower for word in threepio_triggers) or parent_id == bot_id) and author_id != bot_id:
                                        Generate_Response()
                                        time.sleep(cooldown)
                
    except Exception as e:
        print("Except happened: ", e)
        pass
