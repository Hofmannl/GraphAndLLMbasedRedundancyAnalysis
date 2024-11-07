# Abstract
User stories (USs) are a widely used notation for requirements in agile development. 
However, it can easily happen that two USs are redundant, at least partially. 
While some form of redundancy may be acceptable, the user should keep an eye on redundancy in USs for the sake of conciseness and to reduce the risk of inconsistencies.
We present two different approaches to analysing USs for redundancy and compare their potential and limitations.
The first approach translates annotated USs into graph transformation rules, which are then analysed for conflicts to infer redundancies.
The second approach uses a large language model (LLM), here *GPT*, to analyse annotated USs for redundancy. 
We compare the results of these redundancy analyses and discuss their similarities and differences. 
We found that the graph transformation (GT)-based approach is particularly suitable for syntactic analysis, whereas the LLM-based approach seems to find semantic redundancies.

![Example User Story](ExampleSentence.pdf)
  
## Redundancy Detection with LLMs
Redundant requirements can be paired and between this pairs redundancies can be found. 

We use the User Stories from [nlp-stories](https://github.com/ace-design/nlp-stories/tree/main) and [user story repo](https://zenodo.org/records/8136975) 
We compared our LLM approach against a formal approach from [Alexander Lauer, Amir Rabieyan Nejad, Lukas Hofmann](https://github.com/amirrabieyannejad/USs_Annotation.git) 

## Folder explanation
- Datasets: Contains the annotated [nlp-stories](https://github.com/ace-design/nlp-stories/tree/main)
- ExperimentsWordSimilarity: Contains a future project idea
- results: Important results shown in the paper for [MDE Intelligence - 6th Workshop on Artificial Intelligence and Model-driven Engineering](https://mde-intelligence.github.io/)
- src: containg the source code of our implementation. Please, consider for installation our installation and dependecies description
  - [ ] /controller: Implementation of the Fask API endpoint.
  - [ ] /future_work: Contains future experiments in jupyter notebook form (partly done).
  - [X] /prompt_structure : Containing the prompts used for our experiments.  
  - [X] /results: All results achieved during our developments.
  - [X] /support_functions: As our implementation is based on a functional approach this src folder contains all abstracted functions. 
  - [X] /support_functions_test: Tests for the support functions (pythonic style to organise tests).
  - [X] /utils: Utility functions.
  - [X] /Various Jupyter Notebooks: To connect and execute to our progam logic.
  - [X] /setup.py: -
 
## Architecture
![Component Diagram](ComponentDiagramLLM.pdf)

## Workflow
![Workflow for an LLM-based approach to redundancy detection](WorkflowAgent.pdf)

## IDE + Plugins
- VSCode
- Jupyter
- Jupyter Cell Tags
- Jupyter Keymap
- Pylint
- Pylance
- Python
- Python Debugger
- Python Environment Manager

## Dependencies
- Listed in the requirements.txt

## Installation guide
- Install python >= 3.12
- Create a .venv
- pip pip install -r /<usr_path>/requirements.txt
- pip install . in src
- configure [jupyter notebook env](https://jupyter-notebook.readthedocs.io/en/5.7.1/public_server.html)
- start jupyter notebook in src

## Env.
You have to create an *.env*-file in the *src_gpt_approach* folder. The following entries have to be considered:
- OPENAI_API_KEY (Enter here your API key)
- MODEL_VERSION (GPT 3.5 = gpt-3.5-turbo points to gpt-3.5-turbo-0125, GPT-4o = gpt-4o-2024-05-13)
- TPM (Tokens-Per-Minute)
- RPM (Requests-Per-Minute)
- TOKEN_DELTA (Approximation of the Request Size to avoid GPT "Deadlocks")
- TEMPERATURE (e.g. 0.2)
- OUTPUT_EXCEL_NAME_WITH_JUST_TEXT (Insert here the name of the .xlsx-file which stores the results of results from without annoations)
- OUTPUT_EXCEL_NAME_WITH_ANNOTATIONS (Insert here the name of the .xlsx-file which stores the results of results from with annoations)
- OUTPUT_EXCEL_NAME_WITH_TEXT_AND_ANNOTATIONS (Insert here the name of the .xlsx-file which stores the results of results from with plain annoations)
- THRESHOLD_REPAIR (Any number of repairs, e.g., "3")
- THREADING ("1" = ON, "2" = OFF)
- THREAD_MULTIPLICATOR (Any number for thread multiplication > 0)
- LIMIT  ("-1" =None, "n" = any number)
  

This Repo was created for 'Redundancy Analysis of Annotated User Stories Using Graph Transformation and Large Language Models' for the [MDE Intelligence - 6th Workshop on Artificial Intelligence and Model-driven Engineering](https://mde-intelligence.github.io/)


## Contributors
- [Lukas Sebastian Hofmann](lukas.hofmann@uni-marburg.de)
- [Alexander Lauer](alexander.lauer@uni-marburg.de)
- [Arno Kesper](arno.kesper@uni-marburg.de)
- [Gabriele Taentzer](taentzer@mathematik.uni-marburg.de)
