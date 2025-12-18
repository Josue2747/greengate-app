# 🌿 GreenGate - Guia de Integração da API

**Versão:** 2.0
**Última Atualização:** 2025-12-17
**Base URL:** `https://api.greengate.com.br/api/v1`

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Autenticação](#autenticação)
3. [Endpoints](#endpoints)
4. [Exemplos de Integração](#exemplos-de-integração)
5. [Sistema de Score](#sistema-de-score)
6. [Códigos de Erro](#códigos-de-erro)
7. [Rate Limits](#rate-limits)
8. [Webhooks](#webhooks)
9. [Boas Práticas](#boas-práticas)
10. [Suporte](#suporte)

---

## 🎯 Visão Geral

A API do GreenGate permite validar áreas rurais quanto a conformidade ambiental, verificando sobreposições com:

- ✅ Desmatamento (PRODES, MapBiomas)
- ✅ Terras Indígenas (FUNAI)
- ✅ Territórios Quilombolas
- ✅ Embargos IBAMA
- ✅ Unidades de Conservação (ICMBio)
- ✅ APP / Hidrografia (ANA)

**Casos de Uso:**
- ERP Agrícola: Validação automática de propriedades
- Tradings: Due diligence em fornecedores
- Bancos/Investidores: Compliance ESG em financiamentos
- Plataformas de Monitoramento: Alertas de não conformidade

---

## 🔐 Autenticação

### API Key via Header

Todas as requisições requerem uma API Key no header `x-api-key`:

```bash
curl -X POST https://api.greengate.com.br/api/v1/validations/quick \
  -H "Content-Type: application/json" \
  -H "x-api-key: sua-api-key-aqui" \
  -d '{"type": "Polygon", "coordinates": [...]}'
```

### Obter API Key

**Contato:**
- 📞 WhatsApp: +55 19 9 7104-6171
- 🌐 Website: www.greengate.com.br
- 📧 Email: contato@greengate.com.br

**Planos:**
- **Profissional:** 50 validações/mês
- **Empresarial:** Validações ilimitadas + SLA + Suporte prioritário

---

## 📡 Endpoints

### 1. Validação Rápida (Quick Validation)

Valida uma geometria e retorna resultado completo.

**Endpoint:** `POST /validations/quick`

**Request:**
```json
{
  "type": "Polygon",
  "coordinates": [[
    [-56.0958, -15.6014],
    [-56.0958, -15.6114],
    [-56.0858, -15.6114],
    [-56.0858, -15.6014],
    [-56.0958, -15.6014]
  ]]
}
```

**Response (200 OK):**
```json
{
  "plot_id": null,
  "status": "approved",
  "risk_score": 100,
  "checks": [
    {
      "check_type": "prodes",
      "status": "pass",
      "score": 100,
      "message": "Nenhum desmatamento detectado",
      "details": {
        "overlap_area_ha": 0,
        "overlap_percentage": 0
      }
    },
    {
      "check_type": "terra_indigena",
      "status": "pass",
      "score": 100,
      "message": "Sem sobreposição com terras indígenas"
    }
    // ... outros checks
  ],
  "validated_at": "2025-12-17T10:30:00Z",
  "processing_time_ms": 245
}
```

**Status Possíveis:**
- `approved` - Área conforme (score ≥ 75)
- `warning` - Atenção necessária (score 60-74)
- `rejected` - Não conforme (score < 60 ou blocker crítico)

**Check Status:**
- `pass` - Passou na verificação
- `warning` - Alerta (não bloqueia, mas requer atenção)
- `fail` - Falhou (pode bloquear se for blocker crítico)

---

### 2. Geração de Relatório PDF

Gera relatório profissional em PDF com mapa, análises e QR Code de verificação.

**Endpoint:** `POST /reports/due-diligence/quick`

**Request:**
```json
{
  "geometry": {
    "type": "Polygon",
    "coordinates": [[...]]
  },
  "property_info": {
    "farm_name": "Fazenda Santa Maria",
    "plot_name": "Talhão 01 - Soja",
    "municipality": "Sinop",
    "state": "MT",
    "car_code": "MT-5107909-1234567890"
  },
  "lang": "pt"
}
```

**Parâmetros:**
- `lang`: `"pt"` (Português) ou `"en"` (English)
- `property_info.municipality`: Opcional, mas recomendado (permite incluir histórico de uso do solo)
- `property_info.car_code`: Opcional (código CAR da propriedade)

**Response:** Arquivo PDF (binary)

**Headers da Resposta:**
```
Content-Type: application/pdf
Content-Disposition: attachment; filename=GreenGate_Relatorio_20251217.pdf
X-Report-Code: GG-20251217103045-A1B2
X-Content-Hash: 3a5f7c9d...
```

---

### 3. Verificação de Relatório (Público)

Verifica autenticidade de um relatório pelo código QR.

**Endpoint:** `GET /reports/verify/{report_code}`

**Sem autenticação necessária.**

**Response:**
```json
{
  "valid": true,
  "report_code": "GG-20251217103045-A1B2",
  "status": "approved",
  "risk_score": 100,
  "created_at": "2025-12-17T10:30:45Z",
  "plot_name": "Talhão 01",
  "property_name": "Fazenda Santa Maria",
  "state": "MT",
  "geometry_hash": "7f3a9b2c...",
  "pdf_hash": "9d2e5f1a..."
}
```

---

### 4. Health Check

Verifica status da API e dependências.

**Endpoint:** `GET /health/detailed`

**Sem autenticação necessária.**

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-17T10:30:00Z",
  "version": "2.0.0",
  "database": "connected",
  "reference_layers": {
    "prodes": 87867,
    "mapbiomas": 26076,
    "terra_indigena": 645,
    "embargo_ibama": 74203
  }
}
```

---

## 💻 Exemplos de Integração

### JavaScript / Node.js

```javascript
const axios = require('axios');

async function validarArea(geometry) {
  try {
    const response = await axios.post(
      'https://api.greengate.com.br/api/v1/validations/quick',
      geometry,
      {
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': process.env.GREENGATE_API_KEY
        }
      }
    );

    const { status, risk_score, checks } = response.data;

    if (status === 'rejected') {
      console.error('❌ Área NÃO CONFORME');

      // Listar blockers críticos
      const blockers = checks.filter(c =>
        c.status === 'fail' &&
        ['terra_indigena', 'prodes', 'embargo_ibama'].includes(c.check_type)
      );

      blockers.forEach(b => {
        console.error(`  • ${b.check_type}: ${b.message}`);
      });

      return false;
    } else if (status === 'warning') {
      console.warn('⚠️  Área COM RESTRIÇÕES (score: ${risk_score})');
      return 'review_required';
    } else {
      console.log('✅ Área CONFORME (score: ${risk_score})');
      return true;
    }

  } catch (error) {
    if (error.response) {
      console.error(`Erro HTTP ${error.response.status}:`, error.response.data);
    } else {
      console.error('Erro na requisição:', error.message);
    }
    throw error;
  }
}
```

### Python

```python
import requests
import os

def validar_area(geometry: dict) -> dict:
    """
    Valida uma área via API GreenGate.

    Args:
        geometry: GeoJSON Polygon

    Returns:
        dict com resultado da validação

    Raises:
        requests.HTTPError: Se a API retornar erro
    """
    response = requests.post(
        'https://api.greengate.com.br/api/v1/validations/quick',
        json=geometry,
        headers={
            'Content-Type': 'application/json',
            'x-api-key': os.getenv('GREENGATE_API_KEY')
        },
        timeout=30  # 30 segundos timeout
    )

    response.raise_for_status()  # Levanta exceção se erro HTTP

    resultado = response.json()

    # Interpretar resultado
    if resultado['status'] == 'rejected':
        # Área não conforme
        if resultado['risk_score'] == 0:
            print('🔴 BLOCKER CRÍTICO: Terra Indígena, PRODES, ou Embargo')
        else:
            print(f'❌ Área reprovada (score: {resultado["risk_score"]})')

    elif resultado['status'] == 'warning':
        print(f'⚠️  Requer atenção (score: {resultado["risk_score"]})')

    else:
        print(f'✅ Aprovada (score: {resultado["risk_score"]})')

    return resultado


def gerar_pdf(geometry: dict, property_info: dict, lang='pt') -> bytes:
    """Gera relatório PDF."""

    response = requests.post(
        'https://api.greengate.com.br/api/v1/reports/due-diligence/quick',
        json={
            'geometry': geometry,
            'property_info': property_info,
            'lang': lang
        },
        headers={
            'Content-Type': 'application/json',
            'x-api-key': os.getenv('GREENGATE_API_KEY')
        },
        timeout=60  # PDFs podem demorar mais
    )

    response.raise_for_status()

    # Salvar PDF
    report_code = response.headers.get('X-Report-Code')
    filename = f'relatorio_{report_code}.pdf'

    with open(filename, 'wb') as f:
        f.write(response.content)

    print(f'📄 PDF gerado: {filename}')
    print(f'🔍 Código de verificação: {report_code}')

    return response.content
```

### C# / .NET

```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

public class GreenGateClient
{
    private readonly HttpClient _httpClient;
    private readonly string _apiKey;

    public GreenGateClient(string apiKey)
    {
        _apiKey = apiKey;
        _httpClient = new HttpClient
        {
            BaseAddress = new Uri("https://api.greengate.com.br/api/v1/"),
            Timeout = TimeSpan.FromSeconds(30)
        };
        _httpClient.DefaultRequestHeaders.Add("x-api-key", _apiKey);
    }

    public async Task<ValidationResult> ValidateAreaAsync(object geometry)
    {
        var json = JsonSerializer.Serialize(geometry);
        var content = new StringContent(json, Encoding.UTF8, "application/json");

        var response = await _httpClient.PostAsync("validations/quick", content);
        response.EnsureSuccessStatusCode();

        var resultJson = await response.Content.ReadAsStringAsync();
        return JsonSerializer.Deserialize<ValidationResult>(resultJson);
    }
}

// Uso
var client = new GreenGateClient(Environment.GetEnvironmentVariable("GREENGATE_API_KEY"));
var result = await client.ValidateAreaAsync(geometry);

if (result.Status == "rejected")
{
    Console.WriteLine($"❌ Área reprovada (score: {result.RiskScore})");
}
```

---

## 📊 Sistema de Score (ATUALIZADO 2025-12-17)

### Como o Score Funciona

O score de conformidade varia de **0 a 100**, onde:
- **100**: Perfeito, sem restrições
- **75-99**: Aprovado (com ou sem alertas menores)
- **60-74**: Atenção necessária
- **0-59**: Reprovado
- **0**: Blocker crítico identificado

### Blockers Críticos → Score ZERO

Essas 5 restrições **sempre resultam em score = 0** e status `rejected`:

| Blocker | Base Legal | Por quê score zero? |
|---------|------------|---------------------|
| **Terra Indígena** | CF/88 Art. 231 | Proteção constitucional absoluta |
| **Quilombola** | CF/88 Art. 68 | Proteção constitucional absoluta |
| **Embargo IBAMA** | Lei 9.605/98 | Sanção administrativa ativa |
| **PRODES pós-2020** | Reg. UE 2023/1115 | Requisito EUDR |
| **UC Proteção Integral** | Lei 9.985/2000 | Vedação total de uso |

**Exemplo:**
```json
{
  "status": "rejected",
  "risk_score": 0,  // ← ZERO!
  "checks": [
    {
      "check_type": "terra_indigena",
      "status": "fail",
      "message": "Sobreposição com Terra Indígena Xingu (homologada)"
    }
  ]
}
```

### Thresholds de Aprovação

```
Score ≥ 75  →  ✅ APROVADO
Score 60-74 →  ⚠️  ATENÇÃO (requer análise)
Score < 60  →  ❌ REPROVADO
Blocker     →  ❌ REPROVADO (score = 0)
```

### Interpretação para Sistemas

```python
def interpretar_resultado(resultado):
    score = resultado['risk_score']
    status = resultado['status']

    if score == 0:
        return 'BLOCKER_CRÍTICO'  # Terra Indígena, PRODES, etc
    elif status == 'approved':
        return 'APROVADO'  # Score ≥ 75
    elif status == 'warning':
        return 'REVISÃO_NECESSÁRIA'  # Score 60-74
    else:
        return 'REPROVADO'  # Score < 60
```

---

## ⚠️ Códigos de Erro

### HTTP Status Codes

| Código | Significado | Ação Recomendada |
|--------|-------------|------------------|
| 200 | Sucesso | - |
| 400 | Bad Request (geometria inválida) | Verificar formato GeoJSON |
| 401 | Unauthorized (API key inválida) | Verificar API key |
| 403 | Forbidden (API key não fornecida) | Incluir header x-api-key |
| 413 | Payload Too Large (>10.000 ha) | Reduzir área ou dividir |
| 422 | Unprocessable Entity (geometria fora do Brasil) | Verificar coordenadas |
| 429 | Too Many Requests (rate limit) | Aguardar ou aumentar plano |
| 500 | Internal Server Error | Contactar suporte |
| 503 | Service Unavailable | Tentar novamente em alguns minutos |

### Formato de Erro

```json
{
  "detail": "Geometria inválida: coordenadas fora do Brasil",
  "error_code": "INVALID_GEOMETRY",
  "field": "coordinates"
}
```

### Retry Logic Recomendado

```python
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_session_with_retry():
    session = requests.Session()

    retry = Retry(
        total=3,
        backoff_factor=1,  # 1s, 2s, 4s
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)

    return session
```

---

## 🚦 Rate Limits

### Limites por Plano

| Plano | Validações/mês | Requests/minuto | Requests/segundo |
|-------|----------------|-----------------|------------------|
| **Profissional** | 50 | 10 | 2 |
| **Empresarial** | Ilimitadas | 100 | 10 |

### Headers de Rate Limit

```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1702820400
```

### Tratamento de Rate Limit

```javascript
async function validarComRetry(geometry, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await validarArea(geometry);

    } catch (error) {
      if (error.response?.status === 429) {
        const retryAfter = error.response.headers['retry-after'] || 60;
        console.log(`Rate limit atingido. Aguardando ${retryAfter}s...`);
        await sleep(retryAfter * 1000);
        continue;
      }
      throw error;
    }
  }
  throw new Error('Máximo de tentativas excedido');
}
```

---

## 🔔 Webhooks

### Configuração (Plano Empresarial)

Receba notificações em tempo real quando uma validação for concluída.

**Cadastro de Webhook:**
```bash
POST /webhooks
Content-Type: application/json
x-api-key: sua-api-key

{
  "url": "https://seu-sistema.com/api/greengate-webhook",
  "events": ["validation.completed", "validation.failed"],
  "secret": "seu-secret-para-verificacao"
}
```

**Payload do Webhook:**
```json
{
  "event": "validation.completed",
  "timestamp": "2025-12-17T10:30:00Z",
  "data": {
    "validation_id": "uuid-da-validacao",
    "status": "approved",
    "risk_score": 100,
    "property_name": "Fazenda Santa Maria"
  },
  "signature": "sha256=..."
}
```

**Verificação de Assinatura:**
```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    computed = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(f'sha256={computed}', signature)
```

---

## ✅ Boas Práticas

### 1. Armazenar Resultados Localmente

```python
# Armazene o resultado completo para auditoria
resultado = validar_area(geometry)
salvar_no_banco(resultado)  # Seu sistema
```

### 2. Validar Geometrias Antes de Enviar

```python
from shapely.geometry import shape

def validar_geometria_local(geojson):
    try:
        geom = shape(geojson)

        # Verificações básicas
        if not geom.is_valid:
            return False, "Geometria inválida"

        if geom.area == 0:
            return False, "Área zero"

        # Verificar se está no Brasil (bbox aproximado)
        bounds = geom.bounds  # (minx, miny, maxx, maxy)
        if not (-74 <= bounds[0] <= -34 and -34 <= bounds[1] <= 6):
            return False, "Fora do Brasil"

        return True, None

    except Exception as e:
        return False, str(e)
```

### 3. Implementar Cache

```python
import hashlib
import json

def cache_key(geometry):
    """Gera chave de cache baseada na geometria."""
    geom_str = json.dumps(geometry, sort_keys=True)
    return hashlib.sha256(geom_str.encode()).hexdigest()

def validar_com_cache(geometry):
    key = cache_key(geometry)

    # Verificar cache (Redis, Memcached, etc)
    cached = redis.get(f'validation:{key}')
    if cached:
        return json.loads(cached)

    # Validar via API
    resultado = validar_area(geometry)

    # Cachear por 24h
    redis.setex(f'validation:{key}', 86400, json.dumps(resultado))

    return resultado
```

### 4. Monitoramento e Alertas

```python
import logging

def validar_com_monitoramento(geometry):
    try:
        resultado = validar_area(geometry)

        # Log de métricas
        logger.info('validation_completed', extra={
            'status': resultado['status'],
            'score': resultado['risk_score'],
            'processing_time_ms': resultado['processing_time_ms']
        })

        # Alertar se área reprovada
        if resultado['status'] == 'rejected':
            enviar_alerta_slack(f"⚠️ Área reprovada: {resultado}")

        return resultado

    except Exception as e:
        logger.error('validation_failed', exc_info=True)
        enviar_alerta_critico(str(e))
        raise
```

---

## 📞 Suporte

### Contatos
- **WhatsApp:** +55 19 9 7104-6171
- **Email:** suporte@greengate.com.br
- **Website:** www.greengate.com.br

### Documentação Técnica
- **Swagger UI:** https://api.greengate.com.br/docs
- **ReDoc:** https://api.greengate.com.br/redoc
- **OpenAPI Schema:** https://api.greengate.com.br/openapi.json

### SLA (Plano Empresarial)
- **Uptime:** 99.9%
- **Tempo de resposta:** < 2s (p95)
- **Suporte:** 24/7

---

## 📝 Changelog

### v2.0.0 (2025-12-17)
- ✨ **NOVA LÓGICA:** Blockers críticos agora resultam em score = 0
- ✨ Thresholds atualizados: ≥75 aprovado, 60-74 atenção, <60 reprovado
- 🐛 Correção: Score consistente entre API e PDF
- 🐛 Correção: Histórico de uso do solo com busca case-insensitive
- 📝 Mensagens de interpretação melhoradas (PT/EN)

### v1.0.0 (2025-12-02)
- 🎉 Lançamento inicial da API

---

**API GreenGate - Inteligência Ambiental para o Agronegócio** 🌿
