from metaphor_python import Metaphor
import re
import bardapi
import os
import random
from urllib.parse import urlparse


client = Metaphor(api_key="METAPHOR_API_KEY")

token = "BARD_API_KEY"

TOPIC_MESSAGE = "You are an intelligent assistant. I will provide you a text and you need to find out the content category of that text in no more than 4 words. While generating the response, keep that in mind that you should output only topic and no additional extra words: "



def top10_websites(topic):
    relevant_response = client.search("This is the best website to learn about: " + topic, 
        num_results= 10
    )

    url_array=[]
    for result in relevant_response.results:
        url_array.append(result.url)

    domain_array=[]
    for url in url_array:
        domain_array.append(urlparse(url).netloc)

    return domain_array



def display(result):
    id = result.id
    print("\n\nTitle: ", result.title)
    print("Author: ", result.author, end = '\n\n')

    response = client.get_contents(id)
    blog_content = response.contents[0].extract
    data = re.sub(r'<.*?>', '', blog_content)

    print(data, end="\n\n")
    print("To read further: ", response.contents[0].url)

    return response.contents[0]



def search():   
    user_query = input("What do you want to read about: ")
    topic = bardapi.core.Bard(token).get_answer(TOPIC_MESSAGE + user_query)['content']

    domain_array = top10_websites(topic)

    response = client.search("Here is only one article about: " + user_query,
        num_results=1,
        include_domains=domain_array
    )
    
    result = response.results[0]

    return display(result)



def get_similar_link(previous):
    blog_content = previous.extract
    data = re.sub(r'<.*?>', '', blog_content)

    topic = bardapi.core.Bard(token).get_answer(TOPIC_MESSAGE + data)['content']
    
    domain_array = top10_websites(topic)

    response = client.find_similar(previous.url, 
        num_results=3,
        include_domains=domain_array
    )
    
    result = response.results[1]

    return display(result)



def get_random_result():
    RANDOM_MESSAGE = "You are an intelligent assistant. Suggest me topic in no more than 3 words I could read article about. While generating the response, keep that in mind that you should output only topic and no additional extra words."
    topic = bardapi.core.Bard(token).get_answer(RANDOM_MESSAGE)['content']

    domain_array = top10_websites(topic)

    response = client.search("Here is only one article about: " + topic,
        num_results=10,
        include_domains=domain_array
    )
    
    result = random.choice(response.results)

    return display(result)



user_input = "random"
previous = ""

while user_input != 'quit':
    if(user_input == "similar"):
        previous = get_similar_link(previous)
    elif(user_input == "random"):
        previous = get_random_result()
    else:
        previous = search()

    user_input = input("\n\n search, similar, random or quit: ")
