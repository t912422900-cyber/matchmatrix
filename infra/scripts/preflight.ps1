Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "== MatchMatrix local/VPS preflight =="
Write-Host ""

Write-Host "== Docker containers =="
docker ps
Write-Host ""

Write-Host "== Compose config =="
docker compose -f .\infra\docker-compose.yml config
Write-Host ""

Write-Host "== TCP listeners =="
netstat -ano -p tcp
Write-Host ""

Write-Host "Preflight is read-only. Review output before any VPS deploy or Nginx change."
