# slim_api_boilerplate
Slim API boilerplate for Node, Go, Python

## Golang Slim Build
```
docker build . -t golang-boilerplate:slim
docker run -d -p 8080:8080 golang-boilerplate:slim
```

### Golang Test
`http://127.0.0.1:8080/myking`

## Node
docker build . -t node-boilerplate:slim
docker run -d -p 3000:3000 node-boilerplate:slim

### Node Test
`http://127.0.0.1:3000`

## Python - Flask
docker build . -t py-boilerplate:slim
docker run -d -p 9000:9000 py-boilerplate:slim

### Python Test
`http://127.0.0.1:9000`
