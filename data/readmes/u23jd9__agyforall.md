# 🚀 Antigravity for ALL

> **Универсальный шлюз-транслятор моделей Google Antigravity с мульти-аккаунтной каруселью, динамической оптимизацией контекста и защищенной панелью управления.**

**Antigravity for ALL** позволяет использовать мощные модели нового поколения Google Antigravity (**Gemini 3.8 Flash High, Claude Sonnet 4.6, Claude Opus 4.6 Thinking, GPT-OSS 120B**) в любых сторонних клиентах и средах разработки (**OpenCode CLI, Cursor, Cline, Roo Code, Continue, Claude Code, Aider, Harness, Zed / zcode, Open WebUI**) через стандартные API **OpenAI** (`/v1/chat/completions`, `/v1/responses`) и **Anthropic** (`/v1/messages`).

---

## 📑 Содержание

1. [🌟 Ключевые возможности](#-ключевые-возможности)
2. [📋 Таблица поддерживаемых моделей](#-таблица-поддерживаемых-моделей)
3. [⚡ Быстрый старт (Хостинг и запуск)](#-быстрый-старт-хостинг-и-запуск)
   - [Способ 1: В Docker (Рекомендуется для VDS)](#способ-1-в-docker-рекомендуется-для-vds)
   - [Способ 2: Через Docker Compose](#способ-2-через-docker-compose)
   - [Способ 3: Нативный запуск на Node.js](#способ-3-нативный-запуск-на-nodejs)
   - [Настройка HTTPS и домена через Caddy / Nginx](#настройка-https-и-домена-через-caddy--nginx)
4. [🔐 Защита панели управления и хэширование пароля (.env)](#-защита-панели-управления-и-хэширование-пароля-env)
5. [🎠 Как работает карусель мульти-аккаунтов](#-как-работает-карусель-мульти-аккаунтов)
6. [🎛️ Оптимизатор контекста (Antigravity Presets)](#️-оптимизатор-контекста-antigravity-presets)
7. [🔌 Подробнейший гайд: Как и куда подключать модели](#-подробнейший-гайд-как-и-куда-подключать-модели)
   - [1. OpenCode CLI](#1-opencode-cli)
   - [2. Cursor IDE](#2-cursor-ide)
   - [3. Cline & Roo Code (VS Code)](#3-cline--roo-code-vs-code)
   - [4. Zed Editor (zcode)](#4-zed-editor-zcode)
   - [5. Harness (CI/CD Pipelines & AI Code Review)](#5-harness-cicd-pipelines--ai-code-review)
   - [6. Continue.dev](#6-continuedev)
   - [7. Claude Code CLI](#7-claude-code-cli)
   - [8. Aider CLI](#8-aider-cli)
   - [9. Python / LangChain / OpenAI SDK](#9-python--langchain--openai-sdk)
   - [10. cURL (Проверка из терминала)](#10-curl-проверка-из-терминала)
8. [🛠️ Переменные окружения (.env)](#️-переменные-окружения-env)
9. [❓ Решение частых проблем (FAQ & Troubleshooting)](#-решение-частых-проблем-faq--troubleshooting)

---

## 🌟 Ключевые возможности

* 🎭 **100% аутентичная мимикрия под Antigravity**:
  * Прямой защищенный доступ к Google Cloud Code PA endpoint (`daily-cloudcode-pa.googleapis.com`).
  * Полный комплект оригинальных заголовков (`User-Agent: antigravity/2.28.2`, `X-Goog-Api-Client`, `X-Aicode-Request-Id`).
* 🎠 **Автоматическая карусель мульти-аккаунтов**:
  * Подключайте несколько бесплатных аккаунтов Google.
  * Если на активном аккаунте исчерпана квота (HTTP 429), прокси **мгновенно и бесшовно переключается на следующий аккаунт пула**, не прерывая генерацию клиенту.
  * Интеллектуальный Cooldown таймер: отслеживает время остывания и возвращает аккаунты в строй по истечении лимита.
* ⚡ **Экономия до ~93% контекста (Presets & Skills Conductor)**:
  * Встроенная библиотека из 15 пресетов (веб, бэкенд, девопс, аппсек, реверс-инжиниринг, минимальный и т.д.).
  * Отправляет в модель только те системные навыки, которые нужны для текущей задачи, кардинально снижая потребление токенов и ускоряя ответ (Time to First Token).
* 🔒 **Защищенная веб-панель с криптографическим хэшированием пароля**:
  * Пароли администратора хранятся в виде криптографических SHA-256 хэшей в `.env` (без открытого текста).
  * Авторизация по защищенным HttpOnly Cookie-сессиям.
  * Управление аккаунтами, ручное переключение слотов, выбор пресета в 1 клик.
* 🌐 **Двойной протокол API**:
  * OpenAI совместимый: `/v1/chat/completions` и `/v1/responses` со сверхбыстрым стримингом SSE.
  * Anthropic совместимый: `/v1/messages`.
  * Эндпоинт списка моделей `/v1/models`.

---

## 📋 Таблица поддерживаемых моделей

Вы можете обращаться к моделям как по их нативным именам Antigravity, так и по популярным алиасам:

| Модель в Antigravity | Оригинальная нейросеть | Описание и назначение | Поддерживаемые алиасы |
| :--- | :--- | :--- | :--- |
| `gemini-3.8-flash-high` *(По умолчанию)* | Gemini 3.8 Flash (High reasoning) | Молниеносная скорость, глубокое мышление, огромный контекст. Идеальна для написания и ревью кода. | `gpt-4o`, `gpt-4`, `gemini-flash`, `gemini-pro`, `gemini-1.5-pro`, `gemini-2.5-pro` |
| `gemini-3.8-flash-medium` | Gemini 3.8 Flash (Balanced) | Быстрая сбалансированная модель для повседневных задач и коротких скриптов. | `gpt-4o-mini`, `gemini-1.5-flash`, `gemini-2.0-flash` |
| `claude-sonnet-4-6` | Claude 3.5 / 3.7 Sonnet | Топовая модель для архитектуры, сложного рефакторинга и чистого кода. | `claude-3-5-sonnet`, `claude-3-7-sonnet`, `claude-sonnet` |
| `claude-opus-4-6-thinking` | Claude 3 / 4 Opus (Thinking) | Максимальная мощность рассуждений, сложные логические алгоритмы. | `claude-3-opus`, `claude-opus` |
| `gpt-oss-120b-medium` | Open-Source 120B Mixture | Высокопроизводительная открытая модель. | `gpt-oss` |
| `gemini-3.5-flash-lite` | Gemini 3.5 Flash Lite | Ультралегкая модель для простых текстовых задач. | `gemini-lite` |

---

## ⚡ Быстрый старт (Хостинг и запуск)

### Требования к серверу (VDS)
* Любой минимальный сервер (от 1 vCPU, 1 GB RAM).
* ОС: Linux (Ubuntu 22.04 / 24.04, Debian 12, Fedora и др.).
* Установленный Docker (или Node.js 20+).
* **Геолокация**: Сервер должен находиться в регионе, поддерживаемом Google Cloud Code (Европа, США, Азия и др.), либо должен быть настроен outbound proxy (см. раздел [FAQ](#-решение-частых-проблем-faq--troubleshooting)).

---

### Способ 1: В Docker (Рекомендуется для VDS)

#### 1. Клонируйте репозиторий
```bash
git clone https://github.com/u23jd9/agyforall.git
cd agyforall
```

#### 2. Создайте файл `.env` с паролем администратора
Сгенерируйте SHA-256 хэш для своего пароля:
```bash
# Пример создания файла .env из шаблона:
cp .env.example .env

# Сгенерируйте хэш вашего секретного пароля:
npm run hash-password "ваш_секретный_пароль"
```
Скопируйте строку `ADMIN_PASSWORD_HASH=...` в ваш `.env`.

#### 3. Соберите Docker-образ
```bash
docker build -t agyforall:latest .
```

#### 4. Запустите контейнер
```bash
docker run -d \
  --name agyforall \
  --restart unless-stopped \
  -p 8080:8080 \
  --env-file .env \
  -v ~/.gemini:/root/.gemini:z \
  agyforall:latest
```

> 💡 **Что делают флаги:**
> * `-p 8080:8080` — открывает порт прокси на сервере.
> * `--env-file .env` — передает хэшированный пароль и конфигурацию в контейнер.
> * `-v ~/.gemini:/root/.gemini:z` — **критически важный параметр!** Монтирует хранилище токенов с хоста в контейнер. Ваши добавленные Google-аккаунты не пропадут при обновлении или перезапуске контейнера.

Проверьте логи:
```bash
docker logs -f agyforall
```

---

### Способ 2: Через Docker Compose

Создайте файл `.env`, затем запустите:

```bash
docker compose up -d --build
```

---

### Способ 3: Нативный запуск на Node.js

```bash
# 1. Клонируйте и установите зависимости
git clone https://github.com/u23jd9/agyforall.git
cd agyforall
npm install

# 2. Настройте .env файл
cp .env.example .env

# 3. Скомпилируйте TypeScript
npm run build

# 4. Запустите сервер
npm start

# Для постоянной работы в фоне через PM2:
sudo npm install -g pm2
pm2 start dist/index.js --name agyforall
pm2 save
pm2 startup
```

---

### Настройка HTTPS и домена через Caddy / Nginx

#### Вариант с Caddy (Самый простой — 3 строки конфига):
Установите Caddy (`apt install caddy`), добавьте в `/etc/caddy/Caddyfile`:

```caddy
agyforall.yourdomain.com {
    reverse_proxy 127.0.0.1:8080
}
```

Перезапустите Caddy: `sudo systemctl reload caddy`. Бесплатный Let's Encrypt SSL-сертификат будет выпущен автоматически.

#### Вариант с Nginx:
```nginx
server {
    server_name agyforall.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Отключаем буферизацию для мгновенного SSE-стриминга токенов:
        proxy_buffering off;
        proxy_cache off;
        chunked_transfer_encoding on;
    }
}
```

---

## 🔐 Защита панели управления и хэширование пароля (.env)

Пароль администратора **никогда не хранится в открытом виде** в кодовой базе.

### Генерация хэша пароля
Запустите встроенную утилиту:
```bash
npm run hash-password "ваш_пароль_здесь"
```

Команда выведет готовый SHA-256 хэш:
```text
=============================================================
  🔒 Antigravity for ALL - Password Hash Generator
=============================================================
Password:            ваш_пароль_здесь
SHA-256 Hash:        ac6d03de53a7e1e4d581940acc5d2aae0366cde93ab6624ed9cdf1d8f7ceddf2

Add this line to your .env file or Docker environment:
ADMIN_PASSWORD_HASH=ac6d03de53a7e1e4d581940acc5d2aae0366cde93ab6624ed9cdf1d8f7ceddf2
```

Вставьте полученную строку в `.env`. Сервер сравнивает введенный пользователем пароль при помощи `crypto.timingSafeEqual` для защиты от атак по времени (timing attacks).

### Авторизация в веб-панели:
1. Откройте в браузере: `http://<IP-СЕРВЕРА>:8080/admin` (или `https://ваш-домен/admin`).
2. Введите имя пользователя (`admin`) и ваш пароль в открытом виде (прокси сам хэширует ввод и сверяет с `.env`).
3. Нажмите **«+ Add Account (OAuth)»** для привязки Google-аккаунта в 1 клик.

---

## 🎠 Как работает карусель мульти-аккаунтов

Google накладывает лимиты запросов в минуту (RPM) и в сутки (RPD) на один Google-аккаунт.

**Antigravity for ALL решает эту проблему автоматически:**
1. **Sticky Session**: Запросы идут на текущий активный аккаунт (`ACTIVE`), сохраняя максимальную скорость ответа.
2. **Бесшовный 429 Failover**: Как только Google возвращает ошибку `429 Too Many Requests` или `RESOURCE_EXHAUSTED`, прокси моментально:
   * Помечает текущий аккаунт статусом `COOLDOWN` и включает таймер остывания.
   * Переключает активный слот на следующий готовый аккаунт в карусели.
   * **Повторяет текущий запрос клиента уже на новом аккаунте.** Клиент даже не замечает сбоя и не получает ошибку!
3. **Авто-восстановление**: После истечения времени остывания аккаунт снова становится доступным для ротации.

---

## 🎛️ Оптимизатор контекста (Antigravity Presets)

Оригинальный клиент Antigravity отправляет десятки системных инструкций и навыков в каждое сообщение. Это тратит от 15 000 до 35 000 токенов контекста еще до того, как вы напечатали первый символ промпта.

В панели управления доступен блок **Skills & Context Optimizer**:
* **Minimal Context (`minimal`)** — оставляет только критически важные инструкции. **Снижает расход токенов на ~93%!**
* **Frontend Design (`frontend`)** — включает инструменты верстки, Tailwind v4, React/Next.js.
* **Backend Systems (`backend`)** — включает FastAPI, PostgreSQL DBA, Go highload, Redis, архитектурные гайды.
* **Reverse Engineering (`reversing`)** — для анализа кода, распаковки Electron ASAR, чистых реплик.
* **All Skills (`all`)** — все навыки активны одновременно.

Вы можете переключить пресет прямо на дашборде в 1 клик, либо передать заголовок `x-agy-preset: minimal` в запросе.

---

## 🔌 Подробнейший гайд: Как и куда подключать модели

Для всех клиентов базовые параметры подключения одинаковы:
* **Base URL**: `http://<IP-СЕРВЕРА>:8080/v1` (или `https://ваш-домен/v1`)
* **API Key**: `sk-antigravity` *(любая непустая строка)*
* **Основная модель**: `gemini-3.8-flash-high` или `claude-sonnet-4-6`

Ниже приведены пошаговые инструкции для каждого инструмента.

---

### 1. OpenCode CLI

[OpenCode](https://opencode.ai) — мощный терминальный AI-ассистент.

#### Настройка:
Откройте или создайте файл конфигурации `~/.config/opencode/opencode.jsonc` (или локальный `opencode.json` в корне проекта):

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "antigravity": {
      "npm": "@ai-sdk/openai",
      "name": "openai",
      "options": {
        "baseURL": "https://agyforall.delyoself.site/v1",
        "apiKey": "sk-antigravity"
      },
      "models": {
        "gemini-3.8-flash-high": {
          "name": "Gemini 3.8 Flash High"
        },
        "gemini-3.8-flash-medium": {
          "name": "Gemini 3.8 Flash Medium"
        },
        "claude-sonnet-4-6": {
          "name": "Claude Sonnet 4.6"
        },
        "claude-opus-4-6-thinking": {
          "name": "Claude Opus 4.6 Thinking"
        }
      }
    }
  },
  "model": "antigravity/gemini-3.8-flash-high"
}
```

#### Запуск:
```bash
# Выполнить задачу в кодовой базе:
opencode run "Добавь валидацию email в форме регистрации"

# Использовать Claude Sonnet 4.6:
opencode run -m antigravity/claude-sonnet-4-6 "Сделай рефакторинг модуля auth"
```

---

### 2. Cursor IDE

1. Откройте **Cursor Settings** (`Ctrl + ,` или шестеренка в правом верхнем углу).
2. Перейдите во вкладку **Models**.
3. В секции **OpenAI API Key**:
   * Включите переключатель **Override OpenAI Base URL**.
   * В поле **Base URL** введите: `http://<IP-СЕРВЕРА>:8080/v1` (или ваш HTTPS URL).
   * В поле **API Key** введите: `sk-antigravity`.
4. В секции **Model Names**:
   * Нажмите **+ Add model**.
   * Добавьте модели:
     * `gemini-3.8-flash-high`
     * `claude-sonnet-4-6`
     * `claude-opus-4-6-thinking`
5. Сохраните. Теперь в окне чата Cursor (`Ctrl + L` / `Cmd + L`) выберите добавленную модель.

---

### 3. Cline & Roo Code (VS Code)

1. Откройте расширение **Cline** или **Roo Code** в VS Code.
2. Нажмите на иконку шестеренки (Settings).
3. В выпадающем списке **API Provider** выберите: **OpenAI Compatible**.
4. Заполните поля:
   * **Base URL**: `http://<IP-СЕРВЕРА>:8080/v1`
   * **API Key**: `sk-antigravity`
   * **Model ID**: `gemini-3.8-flash-high` (или `claude-sonnet-4-6`)
5. Нажмите **Save**.

---

### 4. Zed Editor (zcode)

Высокопроизводительный редактор [Zed](https://zed.dev) поддерживает подключение любых OpenAI-совместимых моделей для встроенного AI Assistant Panel (`Ctrl + ?` / `Cmd + ?`) и Inline Assistant (`Ctrl + Enter` / `Cmd + Enter`).

#### Настройка в Zed:
Откройте конфигурационный файл настроек Zed (`~/.config/zed/settings.json` в Linux/macOS или через меню `Zed -> Preferences -> Open Settings`):

```jsonc
{
  "language_models": {
    "openai": {
      "version": "1",
      "api_url": "https://agyforall.delyoself.site/v1", // или http://<IP-СЕРВЕРА>:8080/v1
      "available_models": [
        {
          "name": "gemini-3.8-flash-high",
          "display_name": "Antigravity Gemini 3.8 Flash High",
          "max_tokens": 64000
        },
        {
          "name": "claude-sonnet-4-6",
          "display_name": "Antigravity Claude Sonnet 4.6",
          "max_tokens": 64000
        },
        {
          "name": "claude-opus-4-6-thinking",
          "display_name": "Antigravity Claude Opus 4.6 Thinking",
          "max_tokens": 64000
        }
      ]
    }
  },
  "assistant": {
    "version": "2",
    "default_model": {
      "provider": "openai",
      "model": "gemini-3.8-flash-high"
    }
  }
}
```

Установите переменную окружения для API-ключа (в `~/.bashrc` или `~/.zshrc`):
```bash
export OPENAI_API_KEY="sk-antigravity"
```

Перезапустите Zed — теперь встроенный ассистент использует модели Antigravity с ультрабыстрым стримингом!

---

### 5. Harness (CI/CD Pipelines & AI Code Review)

В платформе [Harness.io](https://harness.io) (Harness CI/CD, Harness Code Repository, AIDA Assistant) модели Antigravity можно использовать для автоматизированного ревью пулл-реквестов, генерации тестов, объяснения сбоев пайплайнов и поиска уязвимостей.

#### Вариант A: Шаг автоматического AI Code Review в пайплайне Harness CI
Добавьте шаг типа `ShellScript` в ваш пайплайн Harness (`pipeline.yaml`):

```yaml
- step:
    type: ShellScript
    name: Antigravity AI Code Review
    identifier: antigravity_code_review
    spec:
      shell: Bash
      source:
        type: Inline
        spec:
          script: |
            echo "Fetching git diff for pull request..."
            DIFF_CONTENT=$(git diff origin/main...HEAD | head -n 500)

            echo "Sending code diff to Antigravity Gemini 3.8 Flash High..."
            REVIEW_OUTPUT=$(curl -s -X POST "https://agyforall.delyoself.site/v1/chat/completions" \
              -H "Content-Type: application/json" \
              -H "Authorization: Bearer sk-antigravity" \
              -d '{
                "model": "gemini-3.8-flash-high",
                "messages": [
                  {
                    "role": "system",
                    "content": "You are a senior AppSec and code auditor in a CI pipeline. Review the pull request diff for security vulnerabilities, logic errors, and performance bugs. Provide a concise bulleted markdown summary."
                  },
                  {
                    "role": "user",
                    "content": "Git Diff:\n\n'"$DIFF_CONTENT"'"
                  }
                ]
              }')

            # Извлекаем ответ модели через jq:
            echo "$REVIEW_OUTPUT" | jq -r '.choices[0].message.content'
```

#### Вариант B: Harness Custom LLM Provider / AI Gateway
В настройках Harness Account / Project Settings -> **Connectors**:
* **Connector Type**: `Custom AI / OpenAI Compatible`
* **Base URL**: `https://agyforall.delyoself.site/v1` (или `http://<IP-СЕРВЕРА>:8080/v1`)
* **API Key Secret**: Секрет Harness со значением `sk-antigravity`
* **Model Name**: `gemini-3.8-flash-high` или `claude-sonnet-4-6`

---

### 6. Continue.dev

В файле `~/.continue/config.json`:

```json
{
  "models": [
    {
      "title": "Antigravity Gemini 3.8 Flash",
      "provider": "openai",
      "model": "gemini-3.8-flash-high",
      "apiBase": "http://<IP-СЕРВЕРА>:8080/v1",
      "apiKey": "sk-antigravity"
    },
    {
      "title": "Antigravity Claude Sonnet 4.6",
      "provider": "openai",
      "model": "claude-sonnet-4-6",
      "apiBase": "http://<IP-СЕРВЕРА>:8080/v1",
      "apiKey": "sk-antigravity"
    }
  ]
}
```

---

### 7. Claude Code CLI

Для работы через официальный CLI Anthropic (`claude`):

```bash
export ANTHROPIC_BASE_URL="http://<IP-СЕРВЕРА>:8080"
export ANTHROPIC_API_KEY="sk-antigravity"

# Запуск Claude Code:
claude
```

---

### 8. Aider CLI

[Aider](https://aider.chat) — популярный инструмент парного программирования в терминале:

```bash
aider \
  --openai-api-base http://<IP-СЕРВЕРА>:8080/v1 \
  --openai-api-key sk-antigravity \
  --model openai/gemini-3.8-flash-high
```

---

### 9. Python / LangChain / OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://<IP-СЕРВЕРА>:8080/v1",
    api_key="sk-antigravity"
)

response = client.chat.completions.create(
    model="gemini-3.8-flash-high",
    messages=[
        {"role": "system", "content": "Ты опытный Python разработчик."},
        {"role": "user", "content": "Напиши асинхронный генератор чисел Фибоначчи."}
    ],
    stream=True
)

for chunk in response:
    content = chunk.choices[0].delta.content or ""
    print(content, end="", flush=True)
print()
```

---

### 10. cURL (Проверка из терминала)

```bash
curl -X POST http://<IP-СЕРВЕРА>:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-antigravity" \
  -d '{
    "model": "gemini-3.8-flash-high",
    "messages": [
      {"role": "user", "content": "Привет! Ответь одним словом: РАБОТАЕТ"}
    ]
  }'
```

---

## 🛠️ Переменные окружения (.env)

Вы можете передать эти параметры в Docker через `-e KEY=VALUE` или в `.env` файле:

| Переменная | По умолчанию | Описание |
| :--- | :--- | :--- |
| `PORT` | `8080` | Порт, на котором слушает Fastify сервер. |
| `HOST` | `0.0.0.0` | Сетевой интерфейс привязки. |
| `ADMIN_USER` | `admin` | Логин администратора для доступа к `/admin`. |
| `ADMIN_PASSWORD_HASH` | *(пусто)* | **SHA-256 хэш** пароля администратора (генерируется через `npm run hash-password`). |
| `COOKIE_SECRET` | *(сгенерирован)* | Секретный ключ для подписи Cookie сессий. |
| `HTTPS_PROXY` / `ALL_PROXY` | *(пусто)* | HTTP/SOCKS5 прокси для исходящих запросов к Google (если сервер в РФ). |

---

## ❓ Решение частых проблем (FAQ & Troubleshooting)

### 1. Ошибка `400 Bad Request: User location is not supported for the API use`
* **Причина**: Google Cloud Code блокирует IP-адреса ряда дата-центров (включая РФ и некоторые серверные подсети).
* **Решение**: Направьте исходящие запросы сервера через прокси (например, локальный `sing-box`, `v2ray`, `xray` или любой внешний HTTP/SOCKS5 прокси в Европе/США).
* **Как настроить в Docker**:
  Добавьте параметр `-e HTTPS_PROXY=http://127.0.0.1:1081 --network host` при запуске контейнера.

### 2. При переходе в `/admin` постоянно кидает на `/login`
* **Причина**: Введен неверный пароль, либо браузер блокирует Cookie.
* **Решение**: Проверьте хэш в `.env` файле (`ADMIN_PASSWORD_HASH`). Убедитесь, что запросы идут по протоколу HTTP (для локальной сети) или HTTPS (для внешнего домена).

### 3. Ошибка `429 Too Many Requests`
* **Причина**: Исчерпан минутный или дневной лимит токенов на Google-аккаунте.
* **Решение**: Добавьте еще 1–2 Google-аккаунта в панель управления. Карусель автоматически распределит нагрузку и переключит слот при возникновении лимита.

### 4. Сохраняются ли добавленные аккаунты после перезапуска Docker?
* **Да**, если вы указали том `-v ~/.gemini:/root/.gemini:z` при запуске `docker run` (или в `docker-compose.yml`). Все токены и сессии сохраняются в файле `~/.gemini/antigravity_for_all_vault.json` на хост-машине.

---

## 📄 Лицензия

Проект распространяется под свободной лицензией **MIT License**.
Разработано для сообщества Antigravity. Приятного использования!
