@echo off
echo ================================================================================
echo INSTALANDO PACOTES PYTHON - WINDOWS
echo ================================================================================
echo.
echo Este script instala os pacotes de forma otimizada para Windows.
echo.
pause

cd backend

echo ================================================================================
echo PASSO 1: Atualizando pip, setuptools e wheel...
echo ================================================================================
echo.
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo ERRO ao atualizar pip!
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo PASSO 2: Instalando pacotes essenciais (pode demorar 2-3 minutos)...
echo ================================================================================
echo.

REM Instalar pacotes um por um para melhor diagnóstico
echo [1/10] Instalando FastAPI e Uvicorn...
pip install fastapi==0.109.0 uvicorn[standard]==0.27.0 python-multipart==0.0.6
if errorlevel 1 goto :error

echo [2/10] Instalando SQLAlchemy e database drivers...
pip install sqlalchemy==2.0.25 asyncpg==0.29.0 alembic==1.13.1
if errorlevel 1 goto :error

echo [3/10] Instalando psycopg2-binary (pode demorar)...
pip install psycopg2-binary==2.9.9
if errorlevel 1 (
    echo AVISO: psycopg2-binary falhou, tentando versao alternativa...
    pip install psycopg2-binary
)

echo [4/10] Instalando NumPy...
pip install "numpy<2.0"
if errorlevel 1 goto :error

echo [5/10] Instalando Shapely (geospatial - pode demorar)...
pip install shapely==2.0.2
if errorlevel 1 (
    echo AVISO: Shapely 2.0.2 falhou, tentando versao mais recente...
    pip install shapely
)

echo [6/10] Instalando PyProj...
pip install pyproj==3.6.1
if errorlevel 1 (
    echo AVISO: PyProj 3.6.1 falhou, tentando versao mais recente...
    pip install pyproj
)

echo [7/10] Instalando GeoAlchemy2...
pip install geoalchemy2==0.14.3
if errorlevel 1 goto :error

echo [8/10] Instalando Pydantic...
pip install pydantic==2.5.3 pydantic-settings==2.1.0 email-validator==2.1.0
if errorlevel 1 goto :error

echo [9/10] Instalando auth e crypto...
pip install "python-jose[cryptography]==3.3.0" "passlib[bcrypt]==1.7.4"
if errorlevel 1 (
    echo AVISO: Crypto com bcrypt falhou, tentando sem bcrypt...
    pip install python-jose passlib
)

echo [10/10] Instalando utilitarios...
pip install httpx==0.26.0 aiohttp==3.9.1 reportlab==4.0.8 python-dotenv==1.0.0
pip install orjson==3.9.10 tenacity==8.2.3 psutil==5.9.8 structlog==24.1.0
pip install "qrcode[pil]==7.4.2"
if errorlevel 1 (
    echo AVISO: Alguns utilitarios falharam, continuando...
)

echo.
echo ================================================================================
echo SUCESSO! Pacotes instalados.
echo ================================================================================
echo.
echo Proximo passo: rodar SETUP_COMPLETO.bat
echo.
pause
exit /b 0

:error
echo.
echo ================================================================================
echo ERRO na instalacao!
echo ================================================================================
echo.
echo Tente instalar Microsoft C++ Build Tools:
echo https://visualstudio.microsoft.com/visual-cpp-build-tools/
echo.
echo Ou me avise qual pacote falhou para eu ajustar.
echo.
pause
exit /b 1
