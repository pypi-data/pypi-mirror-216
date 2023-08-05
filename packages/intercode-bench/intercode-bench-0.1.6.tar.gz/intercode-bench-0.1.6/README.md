# 🤖💻 Intercode
Build interactive code environments for training, testing, and augmenting code and decision making agents

<p>
    <a href="https://badge.fury.io/py/intercode-bench">
        <img src="https://badge.fury.io/py/intercode-bench.svg">
    </a>
    <a href="https://www.python.org/">
        <img alt="Build" src="https://img.shields.io/badge/Python-3.8+-1f425f.svg?color=purple">
    </a>
    <a href="https://copyright.princeton.edu/policy">
        <img alt="License" src="https://img.shields.io/badge/License-MIT-blue">
    </a>
</p>

## 👋 Overview
InterCode is a **lightweight, flexible, and easy-to-use framework** for designing interactive code environments. Following the popular [`gym`](https://gymnasium.farama.org/) interface definition, InterCode makes it easy to quickly define a code environment and deploy an agent to operate in code within the context of the environment.

For an overview of InterCode, building interactive code tasks with InterCode, and evaluating agents on InterCode environments, please check out our [wiki](TO DO) and the original paper:

**[InterCode: Standardizing and Benchmarking Interactive Coding with Execution Feedback](https://intercode-benchmark.github.io/)**  

## 🛠️ Installation
> **Note**
> InterCode requires `python` >= 3.8 a local `docker` installation to run. Learn more [here](https://docs.docker.com/get-docker/) to install.

```
pip install intercode-bench
```

## 🚀 Quick Start
* Clone the [InterCode repository](https://github.com/intercode-benchmark/intercode-benchmark)
* Run `./setup.sh`
* Run `python run_sql.py` 

If InterCode was installed successfully, the InterCode SQL environment should be started successfully and a CLI interpreter should appear, allowing you to enter `SQL` commands
to interact with the task setting.

## 🔎 Learn More
To learn more about the InterCode framework, please check out the [website](https://intercode-benchmark.github.io/) and GitHub [repository](https://github.com/intercode-benchmark/intercode-benchmark)

## 🪪 License
Check `LICENSE.md`