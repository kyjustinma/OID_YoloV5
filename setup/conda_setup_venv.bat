@echo off
cd ..
SET mypath=%~dp0
echo Current Path:  %mypath%

set /p env_name= Enter name of conda environment:

cd /d %mypath%
cd ..

@REM Installs Env from requirements.yml and installs precommit
call conda env create --name %env_name% -f  setup\requirements\requirements.yml
call conda activate %env_name%
call conda install --yes -c conda-forge pre_commit
call conda install --yes -c conda-forge commitizen
call conda install --yes -c conda-forge python-dotenv

echo Pre-commit Installing ...
call pre-commit install
call pre-commit autoupdate
call pre-commit install --hook-type commit-msg pre-push

echo Finished setting up conda env "%env_name%" and Pre-Commit
pause
