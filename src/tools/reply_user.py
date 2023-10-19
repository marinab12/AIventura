import logging
import os
import sys

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.llms import AzureOpenAI

from prompts.reply_prompt import reply_prompt

logging.basicConfig(level=logging.INFO)

sys.path.append('..')

class ReplyUser:

    def __init__(self, llm=None, verbose=False):
        loaded_dotenv = load_dotenv("/app/.env")
        assert loaded_dotenv, 'Missing .env file with environment variables definition.'
        self.setup_configurations()
        self.verbose = verbose
        self.generated_query = ""

        # Create LLM
        if llm is None:
            self.llm = AzureOpenAI(
                deployment_name=self.deployments["GPT35"],
                temperature=0.7,
                top_p=1,
                max_tokens=1000,
            )

        # Create chains
        self.reply_chain = LLMChain(
            llm=self.llm, prompt=reply_prompt, verbose=self.verbose)

    def setup_configurations(self):
        """Get environment variables and setup OpenAI account settings """
        # Azure OpenAI-related credentials
        AZURE_OPENAI_SERVICE = os.environ.get("AZURE_OPENAI_SERVICE")
        AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
        self.deployments = {
            'CODEX': os.environ.get("AZURE_OPENAI_CODEX"),
            'GPT3': os.environ.get("AZURE_OPENAI_GPT3"),
            'GPT35': os.environ.get("AZURE_OPENAI_GPT35")
        }

        # Setup Azure OpenAI connection
        os.environ["OPENAI_API_TYPE"] = 'azure'
        os.environ["OPENAI_API_VERSION"] = '2022-12-01'
        os.environ["OPENAI_API_BASE"] = f"https://{AZURE_OPENAI_SERVICE}.openai.azure.com/"
        os.environ["OPENAI_API_KEY"] = os.environ.get("AZURE_OPENAI_KEY")
    
    def reply_user(self, nl_query: str) -> str:
        """ Chats with user and tries to help them """
        nl_query += '\n' + self.generated_query + '\nUsuario: ' + nl_query
        logging.info("Ver: ", nl_query)
        self.generated_query = self.reply_chain.run(
        {"nl_query": nl_query, "stop": ['\n\n', '#', '<|im_end|>', '```']})
        self.generated_query = self.generated_query.split('\nUsuario')[0]
    
        return self.generated_query