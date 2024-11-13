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
    Mac: install `bat`
    ```
    brew install bat
    ```

    Mac: add the utility to zsh path
    ```
    pwd
    echo "'aliass onebite=_GLOBAL_PATH_TO_PROGRAM_FILE'" >> ~/.zshrc
    source ~/.zshrc
    ```

## Usuage
    ```
    (ensure __your_file__ is in a unieque git directory) 
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
    - `C` Change Model (Claude Opus / OpenAI GPT4)

## Notes


