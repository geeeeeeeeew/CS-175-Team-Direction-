---
layout: default
title: Final Report
---
## Video Summary

[![Speech-To-Steve](https://img.youtube.com/vi/zW-2gKv0eEE/0.jpg)](https://www.youtube.com/watch?v=zW-2gKv0eEE)

## Project Summary

The main idea of our project is using Python to implement a way for the user to control the AI agent via speech. At a high level, this is implemented by taking speech from the user and coverting it into text using Google SpeechRecognition, and using NLP libraries spaCy to parse and process the text to parameters, which will be fed to the commands in malmo. In addition, we implemented similarity check to the objects and multistep commands. This allows our agent, for example, understanding that stallions and horses are the same, or jumping exactly 10 times if such commands are given. 


#### Language: Python
#### Library Support: 
- SpeechRecognition
- PyAudio
- NeuralCoref
- spaCy

#### Implemented Commands

| Basic | Advanced| 
| -------------   | ------------- |
|Turn left or right  | Find blocks /entities|
|Walk/run in a direction| Kill entities|
|Crouch| Break blocks |
|Jump| Cook food|
|| Swtich item|
|| Combination of basic and advanced commands|

## Evaluation
We will evaluate the success of our project based on the complexity of the commands we can implement accurately and how well the agent performs tasks. There are different tiers of difficulty for commands: “Find a sheep” is much easier to implement than “Find a sheep and kill it with diamond sword, then cook it”. We are aiming to implement commands that are pretty complex and interact with the environment (e.g. “break a coal block”), with a moonshot case being extremely complex commands that need contextual understanding (e.g. “enter the third house on the right”).

### Qualitative:
We intend to evaluate our success qualitatively by visually checking if the agent can actually perform commands. For example, we will check if the the agent actually moves 5 blocks to the left if it is given the command “walk 5 blocks left". 

### Quantitative:
We intend to evaluate our success quantitatively by measuring the accuracy of our voice commands and command completion rate. In other words, we will calculate the proportion of successfully recognized voice commands to the total number of voice commands given, and proportion of correctly executed commands to the total successfully recognized voice commands. (e.g. the agent actually moves north when given the command to go north, the agent can recognize objects in Minecraft successfully). 

###  Basic Commands
We tested 50 basic commands in total, and the details can be checked in "docs/basic_commands_evaluation.md". Below shows some examples and our evaluation criterion for basic commands. 

| walk to the left for 10 steps|run 10 steps to the right, and then jump 5 times|hurdle 5 times go forward for 10 blocks| 
| -------------   | ------------- | ------------- |
|Speech Recognized | Speech Recognized|Speech Recognized|
|Parse Correctly| Parse Correctly|Parse Correctly|
|Execute Successfully| Execute Successfully|Execute Successfully|

According to the evaluation table in 'basic_commands_evaluation.md', we derived that speech recognition rate is, command parsing rate is, and successfully executed commands rate is. 

###  Advanced Commands
We tested 50 advanced commands in total, and the details can be checked in "docs/advanced_commands_evaluation.md". Below shows some examples and our evaluation criterion for advanced commands. 

| Find Iron| Find a pig and a sheep, and kill them |Find a pig and cook porkchop| Murder the farthest stallion with a blade | 
| -------------   | ------------- | ------------- | ------------- |
|Speech Recognized | Speech Recognized|Speech Recognized| Speech Recognized|
|Parse Correctly| Parse Correctly|Parse Correctly|Parse Correctly|
|Execute 1/1 action Successfully| Execute 4/4 actions Successfully|Execute 2/2 Successfully|Execute 1/1 Successfully|

According to the evaluation table in 'basic_commands_evaluation.md', we derived that speech recognition rate is, command parsing rate is, and successfully executed commands rate is. 

## Resources Used
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)\
library for performing speech recognition
- [PyAudio](https://pypi.org/project/PyAudio/)\
record audio input from microphone
- [spaCy](https://spacy.io/usage/spacy-10z)\
information extraction and natural language understanding
- [NeuralCoref](https://github.com/huggingface/neuralcoref/pulls)\
a pipeline extension for spaCy 2.1+ which annotates and resolves coreference clusters using a neural network

## References
- David M. Bignell. craft_work.py https://github.com/microsoft/malmo/blob/master/Malmo/samples/Python_examples/craft_work.py (2018)
- Food -Official Minecraft Wiki https://minecraft.gamepedia.com/Food




