# pyharmonics-gpt

This is a docker project that will integrate pyharmonics with any OpenAI models.  You will need an open ai API key for your model.
This project will work with any model that is implemented with the openai API spec.  That includes deepseek, GPT, daVinci e.t.c
Please see the model pricing structure to determine which model works best for you.


When you are up and running you can ask your model questions like.

```
Are there tradable patterns for BTCUSDT on the 15min time frame?
```

The model will then leverage pyharmonics to respond to your query.

NOTE: You must ask a question that can be converted into arguments for pyharmonics chart analysis.  If you attempt to build this for your own application then you need to consider how you want to limit the range of queries and map those your own API.

### What assets are supported.

Stock symbols in yahoo finance e.g MSFT, AAPL, TSLA etc.
Crypto pairs on binance e.g. BTCUSDT, ETHUSDT, SOLUSDT etc.

Time frames supported are 1m, 15m, 1h, 4h, 1d, 1w.

# Installation

## Clone Repo

Requires docker and python to be installed on your machine.
Requires an OpenAI API key.
```
> git clone git@github.com:niall-oc/pyharmonics-gpt.git
> cd pyharmonics-gpt
```

## OpenAI API key

You can explicitly set the key in code, but the risk of commiting code with keys in it is unacceptable.  Instead use your environment to hold the keys.

### Use env file ( Easiest method on desktop )
Create a file in the pyharmonics-gpt called ```.env```. Add the following line so python-dotenv can load your key.

```
OPENAI_API_KEY=YOUR_KEY_GOES_HERE
OPENAI_API_MODEL=gpt-3.5-turbo
OPENAI_API_BASE_URL=https://api.openai.com/v1
```

### Use environment variable ( Easiest method on server/cloud deployment )
On a bash shell do the following.
```
> export OPENAI_API_KEY=YOUR_KEY_GOES_HERE
> export OPENAI_API_MODEL=gpt-3.5-turbo
> export OPENAI_API_BASE_URL=https://api.openai.com/v1
```

### Edit/use the docker file ( Works but your key would be part of the repo if you accidentally commit! )
Add the following line to the Dockerfile

```
# Set your open API key
ENV OPENAI_API_KEY=YOUR_KEY_GOES_HERE
ENV OPENAI_API_MODEL=gpt-3.5-turbo
ENV OPENAI_API_BASE_URL=https://api.openai.com/v1
```

## Run the docker image
```
pyharmonics-gpt > sudo docker-compose up --build
```

## Visit the web page and query GPT with pharmonics api integrated.
Then visit http://localhost:5000 to interact with the GPT prompt enabled with pyharmonics.