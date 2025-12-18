@echo off
echo ========================================
echo CRIANDO TABELA api_keys NO SUPABASE
echo ========================================
echo.

cd backend

echo Tentando rodar alembic upgrade head...
alembic upgrade head
if errorlevel 1 (
    echo.
    echo ERRO com alembic direto! Tentando com script UTF-8...
    echo.
    python rodar_alembic.py
    if errorlevel 1 (
        echo.
        echo ERRO persistente! Verifique o .env e conexao com Supabase.
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo PRONTO! Tabela criada no banco.
echo ========================================
echo.
echo Proximos passos:
echo   1. Volte para a pasta anterior: cd ..
echo   2. Crie sua primeira API key: python criar_minha_primeira_key.py
echo.
pause
