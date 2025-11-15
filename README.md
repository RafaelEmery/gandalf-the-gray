# Gandalf The Gray 🧙‍♂️

The one you can trust! He's always right because he has the best references 📚

## Running the project

### Set the environment

Set the Python `3.12.0` and install the project:

```bash
pyenv install 3.12.0p

pyenv local 3.12.0

poetry env use 3.12.0

poetry install --no-root
```

### Install Ollama (MacOS)

To install and test `llama3.1`:

```bash
brew install ollama

ollama serve

ollama pull llama3.1

ollama run llama3.1 "who is gandalf?"
```


