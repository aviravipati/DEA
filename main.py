import openai, os, boto3 
from api_keys_config import read_api_keys
from COMMON_FUNCTIONS.common_functions import ask_yes_no_question, replace_aws_provider, Extract_code, execute_terraform_script

api_keys = read_api_keys()
openai.api_key   = api_keys['openai_api_key']

chat_response = None
messages = [
 {"role": "system", 
  "content" : "You’re going to help with Data Engineering relevant tasks. Your goal is to direct user to arrive at a solution. You can ask questions to understand the user’s problem. \
  You can also ask for more information if you need it.\
  If user were to ask to execute any script, show them and ask for approval before executing using boto3 library.\
  If user were to ask to execute any terraform script, show them and ask for approval before executing using terraform library.\
  Assume AWS account is setup and configured.\
  Assume terraform is installed and configured.\
  Assume boto3 is installed and configured."},
]

messages_context_bot = [
 {"role": "system", 
  "content" : "Your response will be boolean YES or NO. if you see a terraform code to be executed, then respond with YES otherwise NO. You will not provide any other details.\
    "},
]


while True:
    content = input("User: ")
    messages.append({"role": "user", "content": content})
    # Extract the Terraform script from the response
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    chat_response = completion.choices[0].message.content

    print(f'ChatGPT: {chat_response}')
    ## check if bot response has any code. If yes, then ask for approval before executing
    messages.append({"role": "assistant", "content": chat_response})
    message_context = f"""
    Given the following input, please provide a YES or NO response: 
                                    ---
                                    {chat_response}
                                    ---
    Is there a Terraform script that needs to be executed in this input? (yes/no):
    """
    messages_context_bot.append({"role": "user", "content": message_context })
    completion_context_bot = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages_context_bot
    )

    chat_response_context_bot = completion_context_bot.choices[0].message.content

    print(f'chat response context bot is: {chat_response_context_bot}')
    if chat_response_context_bot == "YES" : 
        script = Extract_code(chat_response)
        cleaned_code = "\n".join(line for line in script.splitlines() if not line.strip().startswith("hcl") and line.strip().startswith("terraform"))
        cleaned_code = replace_aws_provider(cleaned_code)
        print(f'Extracted script is: {cleaned_code}')
        user_response = ask_yes_no_question("Do you want to proceed?")

        if user_response:
            print("Executing terraform script")
            execute_terraform_script(cleaned_code)
        else:
            print("Ok. skipping...")
    