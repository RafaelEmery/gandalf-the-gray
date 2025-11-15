# Gandalf The Gray 🧙‍♂️

The one you can trust! He's always right because he has the best references 📚

![gandalf-the-gray](/images/ian-mckellen-lord-of-the-rings-the-fellowship.jpg)

> “I wish it need not have happened in my time,” said Frodo. “So do I,” said Gandalf, “and so do all who live to see such times. But that is not for them to decide. All we have to decide is what to do with the time that is given us.”

## Running the project

### Set the environment

Set the Python `3.12.0` and install the project:

```bash
pyenv install 3.12.0p

pyenv local 3.12.0

poetry env use 3.12.0

poetry install --no-root
```

### Install and run Ollama (MacOS)

To install and test `qwen2.5:3b` (optimized for Mac Air M1 8Gb):

```bash
brew install ollama

ollama serve

ollama pull qwen2.5:3b

ollama run qwen2.5:3b "who is gandalf?"
```


