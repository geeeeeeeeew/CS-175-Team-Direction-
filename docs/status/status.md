---
layout: default
title:  Status
---

## Summary of the Project
The main idea of our project is using Python to implement a way for the user to control the AI agent via speech. We used natural language processing to convert audio into commands, and let the agent perform all of them in Minecraft. For example, saying “kill the cow, find a goat and then move backwards for 6 steps” into a microphone would create 3 commands: "kill cow", "find goat", and "move backwards(6)", which automatically call the responding functions and let the agent to execute these commands. To accomplish this, we first converted speech to text using SpeechRecognition, and then converted the text into commands using Spacy, a library for advanced NLP, so that the agent can perform using Malmo. 

## Approach




We plan to use supervised machine learning algorithms for natural language processing and text analysis, such as SVM and Neural Networks, with the support of the SpeechRecognition Library. We will also use the PyAudio library to parse microphone input into audio data that can be sent to a speech recognition API. Specifically, we are planning on using the Google Cloud Speech API to parse the audio data of user-given commands, which would then be further analyzed with the NLTK library. The agent would then execute the required tasks by calling a certain function related to the command using the Malmo platform. 

## Evaluation
We will evaluate the success of our project based on the complexity of the commands we can implement accurately and how well the agent performs tasks. There are different tiers of difficulty for commands: “walk to the right” is much easier to implement than “find and mine a diamond.” We are aiming to implement commands that are pretty complex and interact with the environment (e.g. “place down a dirt block to the left,” “take a gold ingot from the chest”), with a moonshot case being extremely complex commands that need contextual understanding (e.g. “enter the third house on the right”).
  
## Remaining Goals and Challenges

## Resources Used
### SpeechRecognition
library for performing speech recognition\
https://pypi.org/project/SpeechRecognition/
- Pyaudio
record audio input from microphone
- Spacy
information extraction and natural language understanding \
https://spacy.io/usage/spacy-10z
- NeuralCoref
a pipeline extension for spaCy 2.1+ which annotates and resolves coreference clusters using a neural network
https://github.com/huggingface/neuralcoref/pulls



