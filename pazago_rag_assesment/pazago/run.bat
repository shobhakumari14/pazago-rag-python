@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Creating pdfs directory...
if not exist "pdfs" mkdir pdfs

echo.
echo Starting Berkshire Hathaway Intelligence...
streamlit run app.py