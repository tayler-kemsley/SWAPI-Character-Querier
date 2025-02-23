import asyncio
import click
import os

from openai import OpenAI
from openai.types.chat import ChatCompletion

from exceptions import NotFound
from api import SWAPI


class Agent:
    """
    This class is for interacting with ChatGPT.
    The main purpose is to extract the answer to the user's question from the
    data available, and to put it in a nicely formatted response.
    """
    openai_api_key = os.getenv('OPENAI_API_KEY')

    def __init__(self, swapi: SWAPI):
        self.swapi = swapi
        self.client = OpenAI(api_key=self.openai_api_key)
        self.gpt_model = 'gpt-4o'

    def ask_question(self, question: str) -> str:
        result: ChatCompletion = self.client.chat.completions.create(
            model=self.gpt_model,
            n=1,
            messages=[
                {'role': 'user', 'content': f'''
                    Given this data: {self.swapi.data}
                    Return this answer: {question}
                    Where possible give the name in the response.
                    Do not return URLs.
                    If unknown, return apologetic response
                '''},
            ],
        )
        return result.choices[0].message.content


@click.command()
def cli_agent():
    sw_api = SWAPI()

    def _ask_question():
        agent = Agent(sw_api)
        question = click.prompt(
            f'Ok, what would you like to know about {sw_api.character_name}?'
        )
        click.echo(agent.ask_question(question))
        if click.confirm(
            f'Would you like to know something '
            f'else about {sw_api.character_name}?'
        ):
            return _ask_question()

    character = click.prompt('Who would you like to know about?')
    try:
        asyncio.run(sw_api.search('people', character))
    except NotFound:
        if click.confirm("Oh, I couldn't find that. Try again?"):
            return cli_agent()
        else:
            return

    _ask_question()

    if click.confirm('Would you like to know about someone else?'):
        cli_agent()

    click.echo('Thanks for stopping by!')


if __name__ == "__main__":
    cli_agent()
