# MatchMatrix CODEX MASTER PROMPT

Ты работаешь над проектом MatchMatrix.

Главный и единственный PRD-файл:

MatchMatrix_FINAL_PRD.md

Не создавай дополнительные PRD-документы. Не дроби требования на несколько файлов.

Твоя задача:

1. Открой MatchMatrix_FINAL_PRD.md.
2. Прочитай его полностью.
3. Используй его как главный источник требований.
4. Реализуй проект production-уровня для полностью локального запуска на моём ПК на стеке:
   - Next.js + TypeScript
   - FastAPI + Python
   - PostgreSQL
   - Redis
   - Docker Compose
   - Grok CLI как AI-worker
5. Начни с архитектурного каркаса:
   - docker-compose.yml
   - frontend
   - backend
   - postgres
   - redis
   - nginx
   - scheduler
   - grok-worker
6. Не используй погоду и букмекерские коэффициенты.
7. Реализуй футбол и хоккей.
8. Реализуй 30 гематрических моделей.
9. Реализуй Pre-match, Post-match и Retro-test.
10. Реализуй журнал обучения.
11. Реализуй рекомендации Grok CLI.
12. Запрещено автоматически менять веса моделей без подтверждения пользователя.
13. Все рискованные действия, изменение runtime config, удаление данных, сброс volumes, перезапуск сервисов и git push выполняй только после явного подтверждения.
14. Если видишь слабый раздел PRD, сначала расширь MatchMatrix_FINAL_PRD.md, затем реализуй код.
15. В конце каждой итерации пиши:
   - что сделано;
   - какие файлы изменены;
   - какие команды проверить;
   - что следующий безопасный шаг.

Целевой запуск: frontend на `http://localhost:3100`, backend API на `http://localhost:8100`, PostgreSQL и Redis в локальных Docker volumes. VPS deploy не нужен.

Начни с проверки структуры проекта и создания production-ready local Docker Compose skeleton.
