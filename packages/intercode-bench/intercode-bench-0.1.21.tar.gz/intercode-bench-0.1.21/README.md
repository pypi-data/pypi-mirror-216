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

For an overview of InterCode, building interactive code tasks with InterCode, and evaluating agents on InterCode environments, please check out our [wiki](https://github.com/princeton-nlp/intercode/wiki), [website](https://intercode-benchmark.github.io/) and the original paper:

**[InterCode: Standardizing and Benchmarking Interactive Coding with Execution Feedback](https://arxiv.org/abs/2306.14898)**  

## 🛠️ Installation
> **Note**
> InterCode requires `python` >= 3.8 a local `docker` installation to run. Learn more [here](https://docs.docker.com/get-docker/) to install.

```
pip install intercode-bench
```

## 🚀 Quick Start

### Bash
Create a python file and copy + paste the following code to interact with the InterCode Bash environment.
```python
from intercode.assets import bash_build_docker, bash_image_name, bash_test_data
from intercode.envs import BashEnv

if __name__ == '__main__':
    bash_build_docker()
    env = BashEnv(bash_image_name, data_path=bash_test_data, traj_dir="logs/", verbose=True)

    try:
        for idx in range(3):
            env.reset()
            obs, done = env.observation, False
            while not done:
                action = input('> ')
                obs, reward, done, info = env.step(action)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected")
    finally:
        env.close()
```
If InterCode was installed successfully, the InterCode Bash environment should be started successfully and a CLI interpreter should appear, allowing you to enter `bash` commands to interact with the task setting's file system.

### SQL
Create a python file and copy + paste the following code to interact with the InterCode SQL environment.
```python
from intercode.assets import sql_build_docker, sql_image_name, sql_test_data
from intercode.envs import SqlEnv

from typing import Dict
def preprocess(record: Dict) -> str:
    db = record["extra"]["db"]
    return f"use {db}"

if __name__ == '__main__':
    sql_build_docker()
    env = SqlEnv(sql_image_name, data_path=sql_test_data, preprocess=preprocess, traj_dir="logs/", verbose=True)

    try:
        for idx in range(3):
            env.reset()
            obs, done = env.observation, False
            while not done:
                action = input('> ')
                obs, reward, done, info = env.step(action)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected")
    finally:
        env.close()
```
If InterCode was installed successfully, the InterCode SQL environment should be started successfully and a CLI interpreter should appear, allowing you to enter `SQL` commands to interact with the task setting's MySQL database.

## 🔎 Learn More
To learn more about the InterCode framework, please check out the [website](https://intercode-benchmark.github.io/) and GitHub [repository](https://github.com/princeton-nlp/intercode)

## 🪪 License
Check `LICENSE.md`