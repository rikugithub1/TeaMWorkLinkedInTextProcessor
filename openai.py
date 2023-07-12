import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]

def ai_theme_determinator(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user", 
                "content": "I have the following themes: Educational, Employee highlight, Work culture, Job Opportunity, Diversity/Equal opportunity, Branding/Product promo, News, Educational, Casual Communication, and Informational. I have this prompt: {}. Please identify the correct theme to this prompt.".format(prompt)
            },
        ],
    )
    print(response.choices[0]["message"]["content"].strip())



prompt = "Super excited to share that today we took a first step toward a new era of online shopping. At #GoogleIO, we announced how we are supercharging shopping on Search by combining the power of generative AI with Google’s Shopping Graph to make even the most complex purchase decisions faster & easier. This new experience takes the heavy lifting out of online shopping, summarizing insights from 35 billion listings to give you the most accurate and up-to-date snapshot on products and brands to consider. It’s like having an objective and knowledgeable personal shopper at your fingertips. Congratulations to the team for building this delightful experience with the commerce ecosystem at the center!!"
ai_theme_determinator(prompt)