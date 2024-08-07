# dia-backend

## Build the dockerfile

```
docker build -t dia-backend .
```

## Run the docker file

```
docker run -p 5002:5000 -e TRAVILY_SECRET_KEY=secret dia-backend
```
