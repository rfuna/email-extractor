import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

function_descriptions = [
    {
        "name": "extract_info_from_email",
        "description": "categorise & extract key info from an email, such as the company name, email type etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "companyName": {
                    "type": "string",
                    "description": "The name of the startup that is mentioned in the email"
                },                                        
                "product": {
                    "type": "string",
                    "description": "Try to identify what the startup company does and what their solution is, if any"
                },
                "problem": {
                    "type": "string",
                    "description": "Try to identify the problem the startup is trying to solve, if any"
                },
                "category": {
                    "type": "string",
                    "description": "Try to categorise this email into 1) Deal flow 2) Networking 3) Portfolio Updates 4) Other.  Deal flow emails are from entrepreneurs and companies pitching their business ideas and seeking funding. Networking emails are from other VCs, investors, advisors, etc. looking to connect, share deals, syndicate investments, etc. Portfolio Update emails from portfolio companies providing business updates, milestones, asking for advice, etc. Other emails are those that are not Deal flow, networking, or portfolio updates."
                },
                "nextStep":{
                    "type": "string",
                    "description": "What is the suggested next step to move this forward?"
                },
                "priority": {
                    "type": "string",
                    "description": "Try to give a priority score to this email based on how likely this email will leads to a good investment opportunity, from 0 to 10; 10 most important"
                },
                "urgency": {
                    "type": "string",
                    "description": "Try to give a urgency score to this email based on how urgently and time-sensitive this email should be responded to, from 0 to 10; 10 most important"
                },
            },
            "required": ["companyName", "amount", "product", "priority", "category", "nextStep", "urgency"]
        }
    }
]


email = """
Dear Dr. Ray,

My name is Sarah Howard, and I'm the CEO of RetroTech - a startup that is modernizing vintage tech products.

I wanted to introduce RetroTech because I think we would make an exciting addition to Raven Capital's portfolio.

As you know, vintage products like record players and Polaroids have seen a major resurgence in popularity lately. RetroTech is capitalizing on this growing nostalgia market by re-engineering classic tech into modern versions with contemporary features.

For example, our vinyl record player has built-in Bluetooth capabilities so customers can wirelessly play their digitized collection. We also added USB ports for converting records to digital files. Our reinvented Polaroid camera uploads printed photos to the cloud for easy sharing on social media.

These product upgrades and hybridizations of analog and digital allow RetroTech to deliver the nostalgic appeal people love while providing the connectivity today's consumers expect.

We already have over 5,000 pre-orders for our record player and camera products launching later this year. With your investment support, we can scale up inventory production, expand our product line into more vintage tech, and disrupt a market valued at over $200 million.

I would love to schedule a meeting to show you our prototypes and discuss RetroTech's growth roadmap in more detail. Are you available next Tuesday at 11am? I look forward to your reply.

Best,
Sarah Howard
CEO, RetroTech
sarah@retrotech.com
555-123-4567
"""

prompt = f"Please extract key information from this email: {email} "
message = [{"role": "user", "content": prompt}]

response = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=message,
    functions = function_descriptions,
    function_call="auto"
)

print(response)


class Email(BaseModel):
    from_email: str
    content: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def analyse_email(email: Email):
    content = email.content
    query = f"Please extract key information from this email: {content} "

    messages = [{"role": "user", "content": query}]

    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=messages,
        functions = function_descriptions,
        function_call="auto"
    )

    arguments = response.choices[0]["message"]["function_call"]["arguments"]
    companyName = eval(arguments).get("companyName")
    priority = eval(arguments).get("priority")
    product = eval(arguments).get("product")
    problem = eval(arguments).get("problem")
    category = eval(arguments).get("category")
    nextStep = eval(arguments).get("nextStep")
    urgency = eval(arguments).get("urgency")

    return {
        "companyName": companyName,
        "product": product,
        "problem": problem,
        "priority": priority,
        "category": category,
        "nextStep": nextStep,
        "urgency": urgency
    }
