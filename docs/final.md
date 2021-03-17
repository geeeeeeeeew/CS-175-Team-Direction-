---
layout: default
title: Final Report
---
## Video Summary

[![Speech-To-Steve](https://img.youtube.com/vi/zW-2gKv0eEE/0.jpg)](https://www.youtube.com/watch?v=zW-2gKv0eEE)

## Project Summary

The main idea of our project is using Python to implement a way for the user to control the AI agent via speech. We used natural language processing to convert audio into commands, and let the agent perform all of them in Minecraft. For example, saying “kill the cow, find a goat and then move backwards for 6 steps” into a microphone would create 3 commands: "kill cow", "find goat", and "move backwards(6)", which automatically call the responding functions and let the agent to execute these commands. To accomplish this, we first converted speech to text using SpeechRecognition, and then converted the text into commands using spaCy, a library for advanced NLP, so that the agent can perform using Malmo.

- Language: Python
- Library Support: 
      - SpeechRecognition
      - PyAudio
      - NeuralCoref
      - spaCy
- Implemented Commands

| Basic | Advanced| 
| -------------   | ------------- |
|Turn left or right  | Find blocks /entities|
|Walk/run in a direction| Kill entities|
|Crouch| Break blocks |
|Jump| Cook food|
|| Swtich item|
|| Combination of basic and advanced commands|

what we can achieve
why need Spacy?
why need NeuralCoref?
why not hard code?
image
evaluation method 
