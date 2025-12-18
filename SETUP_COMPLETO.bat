@echo off
echo ================================================================================
echo SETUP COMPLETO - GREENGATE API KEYS
echo ================================================================================
echo.
echo Este script vai:
echo   1. Instalar pacotes Python necessarios
echo   2. Criar tabela no banco (Supabase)
echo   3. Criar sua primeira API key (1 validacao gratis)
echo.
pause
echo.

echo ================================================================================
echo PASSO 1/3: Instalando pacotes Python...
echo ================================================================================
echo.
echo Usando instalador otimizado para Windows...
echo.
call INSTALAR_WINDOWS.bat
if errorlevel 1 (
    echo.
    echo ERRO ao instalar pacotes!
    pause
    exit /b 1
)
echo.
echo Pacotes instalados com sucesso!
echo.
cd backend

echo ================================================================================
echo PASSO 2/3: Criando tabela api_keys no Supabase...
echo ================================================================================
echo.
alembic upgrade head
if errorlevel 1 (
    echo.
    echo ERRO ao criar tabela! Verifique se o .env esta configurado.
    pause
    exit /b 1
)
echo.
echo Tabela criada com sucesso!
echo.

echo ================================================================================
echo PASSO 3/3: Criar primeira API key
echo ================================================================================
echo.
cd ..
python criar_minha_primeira_key.py

echo.
echo ================================================================================
echo SETUP COMPLETO!
echo ================================================================================
echo.
pause
