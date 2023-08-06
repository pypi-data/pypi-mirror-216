# multi-start

This tool aims to help running multiple services inside a single docker container.

Sometimes you might want to have backend, frontend and nginx (or a combination of those)
inside a single container. This tool may help with:

- Prepare final Nginx configs using
  [parse-template](https://github.com/cocreators-ee/parse-template)
- Wait until backend and frontend start responding before running Nginx
- Stop every process if one of them is shut down so a container stops gracefully

## Installation

```shell
pip install multi-start
```

## Usage

```shell
multi-start --help
```
