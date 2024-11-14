# One Bite: We All Know The Rules (WIP) 

    *Coding without coding*

 - Long Files Only
 - Long Functions Only
 - Python Only
 - One Branch Only
 - Comments Everywhere
 - Install instuctions in the header 
 - LLM Does the coding
 - LLM does the fixes
    - *"In Opus we trust"* 🙏


## Setup
 - [ ] Get an anthropic claude key
 - [ ] Get an OpenI key
 - [ ] Paste them into the code

The reason for two models is incase one model gets stuck. 

(optional) use a virtual env for python
```
python3 -m venv venv && source venv/bin/activate
```

Mac: install `bat`, this is for syntax highlighting. 
```
brew install bat
```

python packages
```
pip install anthropic openai
```

Mac: add the utility to zsh path
```
pwd
echo "'aliass onebite=_GLOBAL_PATH_TO_PROGRAM_FILE'" >> ~/.zshrc
source ~/.zshrc
```

## Usuage
```
(ensure __your_file__ is in a unique git directory) 
onebite __file_name__.py
```

## ToDo

 - [ ] Add in wait bar for responses
 - [ ] Buttons 
    - `I` Implement (Writes to file)
    - `R` Run (Removes debugging) 
    - `S` Git commit `git add __file_name__.py && git commit -m "user message".` 
    - `M` Manual Edit `vim __file_name__.py`
    - `D` debug at line
    - `O` Toggle Open AI or Opus (Claude Opus / OpenAI GPT4 / Oblvious Opus / Obvious Open AI)
        - Oblvious means not aware of code or terminal output. 
    - `C` Clear Chat Memory.
    - `U` Discards the file changes `git restore __file_name__.py`
    - `E` Export export file contents via `cat` and copy (`cmd+c`)
 - [ ] strip the newlines from the input (because of pasting)
 - [ ] fix open ai model
 - [ ] Import readme extension
## Notes


