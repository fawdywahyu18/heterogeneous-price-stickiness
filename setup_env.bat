:: Define environment name
set ENV_NAME=venv_fawdy_phd

:: Remove existing environment if it exists
if exist %ENV_NAME% (
    echo Removing existing virtual environment...
    rmdir /s /q %ENV_NAME%
)

:: Create a new virtual environment
echo Creating new virtual environment...
python -m venv %ENV_NAME%

:: Activate the virtual environment
call %ENV_NAME%\Scripts\activate

:: Upgrade pip and install dependencies
echo Upgrading pip and installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Virtual environment setup complete. To activate, run:
echo call %ENV_NAME%\Scripts\activate

