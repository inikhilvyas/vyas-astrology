@echo off
cd /d G:\software\simpa\VYAS
echo Starting VYAS Astrology System...
echo URL: http://localhost:8501
python -m streamlit run app.py --server.port 8501
pause
