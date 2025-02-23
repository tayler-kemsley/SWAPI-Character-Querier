# SWAPI Character Querier

## Introduction

This is a simple tool for querying the [Star Wars API](https://swapi.dev/) (SWAPI) for character information.

A character can be searched for by name, then a question about that character can be asked. 
ChatGPT is used to extract the answer to the question from the SWAPI data, and return a nicely formatted response.

## Requirements

As this tool uses ChatGPT, an OpenAI API key will need to be provided when running/building.

## Running

The tool can be run as a CLI using `pipenv` like so:

```bash
$ OPENAI_API_KEY=<your-openai-key> pipenv run python src/app.py
```

Alternatively for convenience a Dockerfile has been provided, so the CLI can be run like so:

```bash
$ docker build . -t swapi --build-arg OPENAI_API_KEY=<your-openai-key>
$ docker run -it swapi 
```

## Usage

The SWAPI has data from Star Wars Episodes 1-7, and the character data includes things like movie appearances, height, birth year and star ships flown.

A typical interaction may look like this:

```
Who would you like to know about?: Han Solo
Ok, what would you like to know about Han Solo?: What starship does he fly?
Han Solo flies the Millennium Falcon and the Imperial shuttle.
Would you like to know something else about Han Solo? [y/N]: y
Ok, what would you like to know about Han Solo?: When was he born?
Han Solo was born in the year 29BBY.
Would you like to know something else about Han Solo? [y/N]: n
Would you like to know about someone else? [y/N]: y
Who would you like to know about?: Darth Vader
Ok, what would you like to know about Darth Vader?: How tall is he?
Darth Vader is 202 centimeters tall.
Would you like to know something else about Darth Vader? [y/N]: y     
Ok, what would you like to know about Darth Vader?: What is his shoe size?
I'm sorry, but the data provided does not include information about Darth Vader's shoe size.
Would you like to know something else about Darth Vader? [y/N]: n
Would you like to know about someone else? [y/N]: n
Thanks for stopping by!

```