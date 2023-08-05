import openai
from tenacity import retry, stop_after_attempt, wait_fixed
import os

from utilspkg import utils_init
utils_init.load_env_variables_from_yaml('/Users/croft/VScode/ptagit/channels_from_slack/env_vars.yaml')

# ****** IMPORTANT OPENAI VARIABLES TO SET *********** #####
GPT_MODEL = os.environ["OPENAI_GPT_MODEL"] #"gpt-4" #3.5-turbo"
MAX_TOKENS = int(os.environ["OPENAI_MAX_TOKENS"]) #1500 - need to convert env strings to int, float
GPT_TEMP = float(os.environ["OPENAI_GPT_TEMP"]) #0.8
GPT_N = 1
GPT_STOP = None
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
# *********************
API_RETRY_COUNT = 4
API_RETRY_DELAY = 30 # seconds


class GPTConnect: 
    """    A class that composes replies using OpenAI's GPT model. 

    Attributes:
    default_parameters: A dictionary to hold the default values for parameters to pass to GPT model.
    api_key: A string for the API key to access OpenAI's GPT model.
    """
    def __init__(self, api_key=OPENAI_API_KEY, gpt_model=GPT_MODEL, max_tokens=MAX_TOKENS, gpt_temp=GPT_TEMP, gpt_n = GPT_N, gpt_stop = GPT_STOP):         
        """     Constructs all the necessary attributes for the ReplyComposer object.

        Parameters:
        api_key: A string for the API key to access OpenAI's GPT model.
        gpt_model: A string for the name of the GPT model to use.
        max_tokens: An integer for the maximum number of tokens to generate.
        gpt_temp: A float for the temperature setting of the GPT model.
        gpt_n: An integer for the number of best candidates to consider.
        gpt_stop: A list of strings for the stop sequence(s) for the GPT model.
        """
        self.default_parameters = {
            'gpt_model': gpt_model,
            'max_tokens': max_tokens,
            'gpt_temp': gpt_temp,
            'gpt_stop': gpt_stop,
            'gpt_n': gpt_n,
        }
        self.api_key = api_key
        openai.api_key = self.api_key


    def change_gpt_model (self, gpt_model):
        """Takes a string ('gpt-4') and updates the chatgpt default model parameter"""
        self.default_parameters['gpt_model'] = gpt_model


    @retry(stop=stop_after_attempt(API_RETRY_COUNT), wait=wait_fixed(API_RETRY_DELAY))
    def get_gpt_reply(self, system_init_message, user_message, **kwargs): 
        """  Compose a chat reply using GPT model.

        Parameters:
        system_init_message: A string for the initial system message to feed to the GPT model.
        user_message: A string for the user message to feed to the GPT model.
        **kwargs: Optional parameters for GPT model (gpt_model, max_tokens, gpt_temp, gpt_n, gpt_stop).

        Returns:
        A string for the generated chat reply from GPT model.
        """
        # Use passed parameters or instance variables if no parameters were passed
        parameters = {**self.default_parameters, **kwargs}
    
        response = openai.ChatCompletion.create(
            model=parameters['gpt_model'],
            messages=[
                {"role": "system", "content": system_init_message},
                {"role": "user", "content": user_message}
            ],
            max_tokens=parameters['max_tokens'],
            n=parameters['gpt_n'],
            stop=parameters['gpt_stop'],
            temperature=parameters['gpt_temp'],
        )
        
        return response.choices[0].message['content']  
