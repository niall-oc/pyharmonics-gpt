# pyharmonics-gpt

This is a docker project that will integrate pyharmonics with OpenAI chatGPT.  You will need an API key and a GPT model.  
Please see the GPT pricing structure to determine which model works best for you.

When you are up and running you can ask GPT questions like.

```
Are there tradable patterns for BTCUSDT on the 15min time frame?
```

GPT will then leverage pyharmonics to respond to your query.

### What assets are supported.

Stock symbols in yahoo finance e.g MSFT, AAPL, TSLA etc.
Crypto pairs on binance eg. BTCUSDT, ETHUSDT, SOLUSDT etc.

Time frames supported are 1m, 15m, 1h, 4h, 1d, 1w.

# Installation

## Clone repo

Requires docker and python to be installed on your machine.
Requires an OpenAI API key
```
> git clone git@github.com:niall-oc/pyharmonics-gpt.git
> cd pyharmonics-gpt
```

## OpenAI API key 

### Use env file
Create a file in the pyharmonics-gpt called ```.env```. Add the following line so pydotenv can load your key.

```
OPENAI_API_KEY=YOUR_KEY_GOES_HERE
OPENAI_API_MODEL=gpt-3.5-turbo
```

### Use environment variable
On a bash shell do the following.
```
> export OPENAI_API_KEY=YOUR_KEY_GOES_HERE
> export OPENAI_API_MODEL=gpt-3.5-turbo
```

### Edit/use the docker file
Add the following line to the Dockerfile

```
# Set your open API key
ENV OPENAI_API_KEY=YOUR_KEY_GOES_HERE
ENV OPENAI_API_MODEL=gpt-3.5-turbo
```

## Run the docker image
```
pyharmonics-gpt > sudo docker compose up --build
```

## Visit the web page and query GPT with pharmonics api integrated.
Then visit http://localhost:5000 to interact with the GPT prompt enabled with pyharmonics.