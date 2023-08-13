"""
This file contains common functions that are used by the other Python scripts.


"""

def execute_terraform_script(script_content):
    """
    This function executes a Terraform script after user approves it. 
    """
    # Get the current working directory
    import os
    current_directory = os.getcwd()
    print("Current directory:", current_directory)

    # Navigate into a subdirectory
    subdirectory = "terraform"
    os.chdir(subdirectory)

    # Get the updated current working directory
    updated_directory = os.getcwd()
    print("Updated directory:", updated_directory)

    # Save the Terraform script to a temporary file
    tf_script_path = "main.tf"
    with open(tf_script_path, "w") as f:
        f.write(script_content)

    # Run Terraform commands using subprocess
    try:
        subprocess.run(["terraform", "init"], check=True)
        subprocess.run(["terraform", "apply", "-auto-approve"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error executing Terraform:", e)

    # Clean up: Remove the temporary Terraform script file
    import os
    os.remove(tf_script_path)

def ask_yes_no_question(prompt):
    while True:
        response = input(prompt + " (yes/no): ").strip().lower()
        if response == "yes":
            return True
        elif response == "no":
            return False
        else:
            print("Please respond with 'yes' or 'no'.")

def replace_aws_provider(response):
    # Define the code snippet markers (triple backticks)
    start_marker = "provider"
    end_marker = "}"
    code_snippet = ""
    provider_string = """
        provider "aws" {
        shared_config_files      = ["./../.aws/conf"]
        shared_credentials_files = ["./../.aws/creds"] 
        }

        """
    # Find the start and end positions of the code snippet
    start_pos = response.find(start_marker)
    end_pos = response.find(end_marker, start_pos + len(start_marker))
    
    # Extract the code snippet
    if start_pos != -1 and end_pos != -1:
        code_snippet = response[start_pos:end_pos + len(end_marker)]
        print("Original Code Snippet:")
        print(code_snippet)
        
        # Remove the code snippet from the response
        response = provider_string + response[:start_pos] + response[end_pos + len(end_marker):]
        print("Remaining Response:")
        print(response)
    else:
        print("No code snippet found.")
    
    return response

def Extract_code(response):

    # Define the code snippet markers (triple backticks)
    start_marker = "```"
    end_marker = "```"
    code_snippet = ""
    # Find the start and end positions of the code snippet
    start_pos = response.find(start_marker)
    end_pos = response.find(end_marker, start_pos + len(start_marker))

    # Extract the code snippet
    if start_pos != -1 and end_pos != -1:
        code_snippet = response[start_pos + len(start_marker):end_pos]
        print("Code Snippet:")
        print(code_snippet)
    else:
        print("No code snippet found.")

    return code_snippet
