import configparser

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

def read_api_keys(filename='env.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    #print(config.sections())
    # Check if the file has the 'API_KEYS' section
    if 'API_KEYS' not in config:
        raise ValueError(f"{filename} does not have the 'API_KEYS' section.")

    # Read the API keys
    api_keys = dict(config['API_KEYS'])
    aws_keys = dict(config['AWS_KEYS'])
    api_keys = Merge(api_keys, aws_keys)

    return api_keys

# Usage example
if __name__ == '__main__':
    try:
        api_keys = read_api_keys()
        OPENAI_API_KEY = api_keys['openai_api_key']

        # Use the API keys in your code
        print("OPENAI_API_KEY:", OPENAI_API_KEY)

        # Now you can use the keys to make API calls, etc.
        # Your API-related code goes here.

    except Exception as e:
        print("Error reading API keys:", e)
