# Deploy RAG FastAPI to Azure Function (serverless)

<a href="" target="_blank">
  <img src="https://github.com/kokchun/assets/blob/main/python_videos/pydantic_ai_practical.png?raw=true" alt="pydantic for data validation" width="600">
</a>

## Setup

In order to deploy a FastAPI app on Azure Functions, you need to start with setting up [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-csharp). Follow the instructions inside that link and set it up on your computer.

Next you need to install the extension for Visual Studio Code called "Azure Functions". You can find it in the Extensions Marketplace.

<img src = "https://github.com/kokchun/assets/blob/main/azure/azure_functions_extension.png?raw=true" alt="Azure Functions Extension" width="200">

You'll need to connect your Azure account to the extension so click on "ACCOUNTS & TENANTS" and follow the steps to sign in to your Azure account and choose your subscription.

<img src = "https://github.com/kokchun/assets/blob/main/azure/azure_function_extension_headlines.png?raw=true" alt="Azure Functions Extension" width="200">

## Create a new Azure Function in Azure through VSCode

We'll now create an Azure Function in Azure, but using this extension

<img src = "https://github.com/kokchun/assets/blob/main/azure/create_function_app.png?raw=true" alt="Create Azure Function" width="200">

Click on "Create Function App in Azure" and you will go through the following steps:

**step 1 - name**

<img src = "https://github.com/kokchun/assets/blob/main/azure/create_new_function_app.png?raw=true" alt="Create Azure Function" width="300">

<br/>

**step 2 - location**

<img src = "https://github.com/kokchun/assets/blob/main/azure/create_function_app_location.png?raw=true" alt="Create Azure Function" width="300">

<br/>

**step 3 - runtime stack**

<img src = "https://github.com/kokchun/assets/blob/main/azure/create_function_app_runtime_stack.png?raw=true" alt="Create Azure Function" width="300">

<br/>

**step 4 - identity**

<img src = "https://github.com/kokchun/assets/blob/main/azure/create_function_app_identity.png?raw=true" alt="Create Azure Function" width="300">

You can go into Azure portal to check out your function app. This is what is deployed in your resource group when creating Azure function app.

<img src = "https://github.com/kokchun/assets/blob/main/azure/function_app_resource_group.png?raw=true" alt="Create Azure Function" width="300">

## Create Function App locally

Now you have created a function app in Azure, but you also need to create a local one and deploy it to Azure. You need to do this to deploy the actual FastAPI api to Azure. So go to workspace and click on the lightning symbol and create function

<img src = "https://github.com/kokchun/assets/blob/main/azure/local_function_0.png?raw=true" alt="Create Azure Function" width="300">

<br/>

Choose your current folder

<img src = "https://github.com/kokchun/assets/blob/main/azure/local_function_1.png?raw=true" alt="Create Azure Function" width="300">

<br/>

Choose your your language

<img src = "https://github.com/kokchun/assets/blob/main/azure/local_function_2.png?raw=true" alt="Create Azure Function" width="300">

<br/>

Choose your HTTP trigger

<img src = "https://github.com/kokchun/assets/blob/main/azure/local_function_3.png?raw=true" alt="Create Azure Function" width="300">

<br/>

Name your function to something descriptive

<img src = "https://github.com/kokchun/assets/blob/main/azure/local_function_4.png?raw=true" alt="Create Azure Function" width="300">

Use FUNCTION as authorization level as we don't want the API to be available without API key

<img src = "https://github.com/kokchun/assets/blob/main/azure/local_function_5.png?raw=true" alt="Create Azure Function" width="300">


## Continuation

These won't be covered by the lectures, but you should be able to continue on the demos with

- deploy frontend to azure web app
- dockerization
- CI/CD
- agentic behaviors to RAG
- add memory to the RAG if justified

## Read more

## Other videos

<a href="https://youtu.be/gwDt5IxPfZg" target="_blank">
  <img src="https://github.com/kokchun/assets/blob/main/azure/azure_functions_fastapi.png?raw=true" alt="deploy fastapi app into azure functions" width="600">
</a>
