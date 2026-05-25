@echo off
title Dashboard de Vendas
 
echo ============================================
echo   Dashboard de Vendas - Iniciando...
echo ============================================
echo.
 
echo Verificando dependencias...
python -m pip install pandas streamlit matplotlib openpyxl --quiet
 
echo.
echo Iniciando o dashboard...
echo Acesse: http://localhost:8501
echo Pressione Ctrl+C nesta janela para encerrar.
echo.
 
python -m streamlit run dashboard_vendas.py
 
pause