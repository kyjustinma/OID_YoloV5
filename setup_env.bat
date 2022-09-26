@echo off
SET mypath=%~dp0
echo Current Path:  %mypath%

set /p env_name= Enter name of conda environment:

cd /d %mypath%

@REM Installs Env from requirements.yml and installs precommit
call conda env create --name %env_name% -f requirements.yml
call conda activate %env_name%
call conda install --yes -c conda-forge pre_commit
call conda install --yes -c conda-forge commitizen
call conda install --yes -c conda-forge python-dotenv
call pre-commit install
call pre-commit autoupdate
call pre-commit install --hook-type commit-msg pre-push

echo Finished setting up conda env and pre-commit
pause
