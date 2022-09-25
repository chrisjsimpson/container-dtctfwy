# AI Audio to Text Transcription 🦾🤖


[app url](https://container-dtctfwy.containers.anotherwebservice.com/)

This app uses the [OpenAI Whisper research](https://openai.com/blog/whisper/) to demonstrate
an automatic audo -> text transcription service.


# Run the code locally


```
git clone git@github.com:chrisjsimpson/container-dtctfwy.git
```

1. [Install docker](https://docs.docker.com/get-docker/)

2. Start your container locally: `docker-compose up`
3. Visit your app locally: http://127.0.0.1:5000/

## View your app locally

Visit: http://127.0.0.1:5000/

### Rebuild container (locally)
If you make changes to `Dockerfile`, then you need to rebuild your container image. To rebuild the container image:
```
docker-compose build
# or 
docker-compose up --build
```
