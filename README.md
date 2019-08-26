![amplrestapi logo](docs/img/logo.png)

<br />
<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000" />
  <a href="https://github.com/jkomyno/ampl-rest-api#readme">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" target="_blank" />
  </a>
  <a href="https://github.com/jkomyno/ampl-rest-api/graphs/commit-activity">
    <img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" target="_blank" />
  </a>
  <a href="https://github.com/jkomyno/ampl-rest-api/blob/master/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" target="_blank" />
  </a>
</p>

> AMPLRESTAPI is a custom asynchronous REST API layer written in modern Python to solve optimization problems in AMPL.

## How to run

A docker-compose.yml file is included in the repository for simplicity.
To run an AMPL REST server on port [localhost:9001](http://localhost:9001), clone the project,
open a terminal window in it and type:

```sh
docker-compose up --build
```

## 🔑 Key features

* ✨ only needs Docker to run
* 💪 written in idiomatic asynchronous Python 3.6 with typings support
* ✔ easy code structure composed of multiple submodules
* ⚠ based on the free demo version of AMPL and the CPLEX engine

## ❔ How to use

This project has been originally created as a University Project.
A complete project report is available in [docs/report.pdf](docs/report.pdf).
The API documentation is also available in [OpenAPI 3 format](https://swagger.io/docs/specification/about/)
in [docs/api/openapi.yml](docs/api/openapi.yml).
An HTML version of the API documentation is available [here](https://jkomyno.github.io/amplrestapi/index.html).

## 👤 Author

**Alberto Schiabel**

* Github: [@jkomyno](https://github.com/jkomyno)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/jkomyno/ampl-rest-api/issues).
The code is short, throughly commented and well tested, so you should feel quite comfortable working on it.
If you have any doubt or suggestion, please open an issue.

## 🦄 Show your support

Give a ⭐ if this project helped or inspired you!

## 📝 License

Built with ❤  by [Alberto Schiabel](https://github.com/jkomyno).<br />
This project is [MIT](https://github.com/jkomyno/ampl-rest-api/blob/master/LICENSE) licensed.

## Related repositories

* [`docker-ampl-python`](https://github.com/jkomyno/docker-ampl-python): Repository containing the Docker image upon
which the current project is built on
