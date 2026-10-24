# Estoque Service

Microsserviço de **estoque** (FastAPI + PostgreSQL) do e-commerce em microsserviços.
Cadastra produtos, reserva e estorna estoque (ação compensatória da Saga).

## URLs

| Ambiente | Branch | URL | Swagger |
|---|---|---|---|
| DEV | `develop` | https://SEU-ESTOQUE-DEV.onrender.com | habilitado (`/docs`) |
| HOMOL | `main` | https://SEU-ESTOQUE-HOMOL.onrender.com | desabilitado |

Métricas Prometheus: `/metrics`

## Endpoints

- `GET /health`
- `POST /produtos` · `GET /produtos/{codigo}`
- `POST /estoque/reservar` · `POST /estoque/estornar`

## Rodar localmente

```bash
cp .env.example .env
docker compose up --build
```

- API + Swagger: http://localhost:8002/docs
- Métricas: http://localhost:8002/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (usuário/senha: `admin`/`admin`)

Testes: `pip install -r requirements.txt && pytest --cov=app`

## Fluxo de desenvolvimento (Git Flow)

- `feature/*`: trabalho do dia a dia, sai da `develop` e volta por Pull Request
- `develop`: ambiente **DEV**
- `main`: ambiente **HOMOL**

## Pipeline (GitHub Actions)

`.github/workflows/ci-cd.yml`:

1. **build-test:** instala dependências, roda `pytest` com cobertura e envia para o SonarCloud
2. **docker-build:** valida o build do Dockerfile
3. **deploy-dev / deploy-homol:** em push na `develop` / `main`, chama o *deploy hook* do Render

`.github/workflows/release.yml`: ao criar uma tag `vX.Y.Z`, publica a imagem no GHCR
(`ghcr.io/<usuario>/<repositorio>:X.Y.Z`).

## Versionamento (Semantic Versioning)

`MAJOR.MINOR.PATCH`: correção = PATCH, funcionalidade nova = MINOR, mudança incompatível = MAJOR.

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Segurança

- Dependabot ativo (`pip`, `docker`, `github-actions`)
- Segredos no GitHub Secrets: `SONAR_TOKEN`, `RENDER_DEPLOY_HOOK_DEV`, `RENDER_DEPLOY_HOOK_HOMOL`
- Senhas de banco nunca ficam no código (variáveis de ambiente)
- Observação: `/metrics` é público neste trabalho acadêmico; em produção seria protegido.

## Observabilidade

Prometheus coleta `/metrics` e o Grafana exibe o dashboard (requisições/s, latência p95 e erros 5xx).

![Dashboard](docs/dashboard.png)
