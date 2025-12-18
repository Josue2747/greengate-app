@echo off
echo ================================================================================
echo INSTALANDO PACOTES PYTHON - WINDOWS (SEM COMPILACAO)
echo ================================================================================
echo.
echo Este script tenta instalar versoes pre-compiladas dos pacotes.
echo.
pause

cd backend

echo ================================================================================
echo Atualizando pip, setuptools e wheel...
echo ================================================================================
echo.
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 goto :error

echo.
echo ================================================================================
echo Instalando pacotes essenciais (versoes com wheels pre-compilados)...
echo ================================================================================
echo.

echo [1/8] FastAPI e Uvicorn...
pip install fastapi uvicorn[standard] python-multipart
if errorlevel 1 goto :error

echo [2/8] SQLAlchemy e Alembic...
pip install sqlalchemy alembic
if errorlevel 1 goto :error

echo [3/8] Tentando instalar asyncpg (pode falhar)...
pip install asyncpg --only-binary :all:
if errorlevel 1 (
    echo.
    echo ============================================================
    echo AVISO: asyncpg precisa de compilacao!
    echo ============================================================
    echo.
    echo asyncpg nao tem wheel pre-compilado para sua versao do Python.
    echo.
    echo SOLUCOES:
    echo.
    echo OPCAO 1 - Instalar Build Tools da Microsoft:
    echo   https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo   Depois rode: pip install asyncpg
    echo.
    echo OPCAO 2 - Usar versao mais antiga do asyncpg:
    echo   pip install asyncpg==0.27.0
    echo.
    echo OPCAO 3 - Usar Docker (mais facil):
    echo   docker-compose up
    echo.
    echo ============================================================
    echo.
    echo Tentando versao mais antiga do asyncpg...
    pip install asyncpg==0.27.0
    if errorlevel 1 (
        echo.
        echo FALHOU! Voce precisa instalar o Build Tools.
        echo.
        pause
        exit /b 1
    )
)

echo [4/8] psycopg2-binary...
pip install psycopg2-binary
if errorlevel 1 goto :error

echo [5/8] NumPy e pacotes geoespaciais...
pip install "numpy<2.0" shapely pyproj geoalchemy2
if errorlevel 1 (
    echo AVISO: Alguns pacotes geoespaciais falharam
    pip install "numpy<2.0"
    pip install shapely --only-binary :all:
    pip install geoalchemy2
)

echo [6/8] Pydantic...
pip install pydantic pydantic-settings email-validator
if errorlevel 1 goto :error

echo [7/8] Auth (python-jose pode falhar, tentando alternativa)...
pip install python-jose[cryptography] passlib[bcrypt]
if errorlevel 1 (
    echo Tentando sem extras...
    pip install python-jose passlib
)

echo [8/8] Utilitarios...
pip install httpx aiohttp reportlab python-dotenv orjson tenacity psutil structlog qrcode pillow
if errorlevel 1 (
    echo Alguns utilitarios falharam, mas continuando...
)

echo.
echo ================================================================================
echo SUCESSO! Pacotes principais instalados.
echo ================================================================================
echo.
pause
exit /b 0

:error
echo.
echo ================================================================================
echo ERRO na instalacao!
echo ================================================================================
echo.
pause
exit /b 1
