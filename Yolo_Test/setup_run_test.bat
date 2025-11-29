@echo off
title YOLO Model Test Setup and Run
color 0A

echo ======================================================
echo          YOLO MODEL TEST SETUP and RUN
echo ======================================================

:: list options
:menu

    echo.
    echo Select an option:
    echo 1. Setup Environment
    echo 2. Run Test_Model.py
    echo 3. Exit

    set /p choice="Enter your choice (1-3): "

    if "%choice%"=="1" goto setup
    if "%choice%"=="2" goto run
    if "%choice%"=="3" goto close

    echo Invalid choice. Please try again.
    goto menu


:setup
    :: 1. Check if 'yolo_test_env' folder exists
    echo [*] checking environment.
     
    if exist yolo_test_env (
        echo [+] Virtual environment found.
    ) else (
        echo [!] Virtual environment not found. Creating...
        python -m venv yolo_test_env
        if errorlevel 1 (
            echo [X] Failed to create yolo_test_env. Make sure Python is installed.
            pause
            exit
        )
        echo [+] Virtual environment created successfully.
    )

    :: 2. Activate Environment
    echo [*] Activating environment...
    call yolo_test_env\Scripts\activate

    :: 3. Check and Install Libraries
    echo [*] Checking and updating libraries...
    python -m pip install --upgrade pip

    echo [*] Installing dependencies from requirements.txt...
    if exist requirements.txt (
        echo [+] requirements.txt found.
        pip install -r requirements.txt
    ) else (
        echo [X] requirements.txt not found! Make sure the file is in the same directory.
        pause
        exit
    )

    :: 4. Cleanup
    timeout /t 3 /nobreak
    cls
    echo [*] Finalizing setup...

    if exist yolo_test_env (
        echo [+] Setup complete. You can now run the YOLO model test.
        echo.
        
    )

    :: Ask to run Test_Model.py
    set /p choice_run="Do you want to run the Test_Model.py? (y/n): "

    if /i "%choice_run%"=="y" goto run
    if /i "%choice_run%"=="n" goto close


:run

    :: Activate Environment
    echo [*] Activating environment...
    call yolo_test_env\Scripts\activate

    :: Run Test_Model.py
    echo [*] Running Test_Model.py...
    python Test_Model.py

    goto close

:close
    echo Exiting...
    pause
