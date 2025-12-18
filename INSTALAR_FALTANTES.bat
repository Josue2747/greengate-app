@echo off
echo ================================================================================
echo INSTALANDO PACOTES QUE FALTARAM
echo ================================================================================
echo.

cd backend

echo Instalando pydantic-settings...
pip install pydantic-settings

echo.
echo Instalando structlog (logging estruturado)...
pip install structlog

echo.
echo Instalando outros pacotes que podem ter faltado...
pip install email-validator
pip install python-jose
pip install passlib
pip install pytest pytest-asyncio pytest-cov
pip install orjson tenacity

echo.
echo ================================================================================
echo PRONTO! Pacotes instalados.
echo ================================================================================
echo.
pause
