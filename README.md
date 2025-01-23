# pyharmonics-gpt

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

```OPENAI_API_KEY=YOUR_KEY_GOES_HERE
```

### Use environment variable
On a bash shell do the following.
```
> export OPENAI_API_KEY=YOUR_KEY_GOES_HERE
```

### Edit/use the docker file
Add the following line to the Dockerfile

```
# Set your open API key
ENV OPENAI_API_KEY=YOUR_KEY_GOES_HERE
```

## Run the docker image
```
pyharmonics-gpt > sudo docker compose up --build
```

## Visit the web page and query GPT with pharmonics api integrated.
Then visit http://localhost:5000 to interact with the GPT prompt enabled with pyharmonics.