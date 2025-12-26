# Exercise 1 - FastAPI and PydanticAI

In this exercise, you get to work with fastapi to create APIs of different kinds. You'll get to know the simple patterns of CRUD in fastapi. Also you'll learn how to serve csv data, and serve machine learning models. You will also use pydanticai together with fastapi.

## 0. FastAPI glossary API

Read the data from this repository called `fastapi_glossary.json`. Create Pydantic model(s) of the data in a separate script called `data_processing.py`.

a) Now create an endpoint `/glossary` which will return all words and their meaning.

b) Create a query parameter to filter out a specific word

c) Turn your API into a CRUD API, so that you can add glossary, update and delete glossary.

d) Test out your API in Swagger UI.

e) Test out your API using requests inside of a Jupyter notebook or a separate Python script. Try the different request types.

## 1. PydanticAI fundamentals

Make a PydanticAI model that can take an input of a location and then it should suggest 5 restaurants nearby that place. The restaurant model should have

- name
- type of food (cuisine)
- price level
- rating
- short description
- opening hours
- location

It's okay if your model is making up a restaurant that doesn't exist

## 2. FastAPI to serve PydanticAI

Now make a fastapi with a post endpoint in natural language to prompt for a location and what type of food. Based on these it should generate a restaurant and store it in a duckdb database.

Also implement a get endpoint for showing all restaurants in the database.

## 3. Extend Books API 

Add a post endpoint to 06_fast_api_crud that can take a natural language prompt, which will create a new book. 

## 4. Theory questions

a) What is FastAPI and why is it popular for building APIs?

b) What is the role of a Pydantic model in a FastAPI application?

c) How does FastAPI automatically generate documentation?

d) What is an endpoint, and what are GET and POST methods?

e) What problem does PydanticAI solve when using LLMs?

f) How can FastAPI be used to serve PydanticAI? Give an example

g) Why is PydanticAI’s validated output better than plain-text LLM responses?

## Glossary

Fill in this table either by copying this into your own markdown file or copy it into a spreadsheet if you feel that is easier to work with.

| terminology          | explanation |
| -------------------- | ----------- |
| fastapi              |             |
| endpoint             |             |
| route                |             |
| query                |             |
| field                |             |
| dependency injection |             |
| request body         |             |
| response model       |             |
| pydantic model       |             |
| swagger ui           |             |
| agent                |             |
| output_type          |             |
|                      |             |
|                      |             |
|                      |             |
|                      |             |
