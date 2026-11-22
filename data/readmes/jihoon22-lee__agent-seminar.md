# agent-seminar

**AI 에이전트 확장하기: 스킬, MCP, 플러그인 (opencode 편)**

코딩 에이전트 opencode에 팀의 지식과 시스템, 규칙을 붙이는 세 가지 방법을 다룬 60분 세미나 자료입니다.
발표 슬라이드와 글로 읽는 가이드, 그리고 직접 실행해 볼 수 있는 예제 52개가 들어 있습니다.

- **발표 자료**: https://jihoon22-lee.github.io/agent-seminar/ (브라우저에서 바로 열립니다. `?` 키로 단축키를 볼 수 있습니다)
- **가이드**: [docs/guide](docs/guide/)
- **예제 목록**: [examples/README.md](examples/README.md)

모든 내용은 **opencode 1.19.5**에서 직접 실행해 확인했습니다. 모든 예제의 `check.py`를 Windows(PowerShell 5.1)와 Linux 양쪽에서 실행해 통과시켰습니다. 도구가 없어 건너뛴 부분과 확인하지 못한 부분은 각 README에 "미검증"으로 적었습니다.

## 한 줄 요약

| 확장 | 한 줄 설명 | 이럴 때 |
|---|---|---|
| **스킬** | 모델이 필요할 때 꺼내 읽는 업무 매뉴얼 (`SKILL.md`) | 모델이 알아야 할 절차나 지식: 커밋 규칙, 리뷰 기준, 분석 순서 |
| **MCP** | 에이전트 바깥의 프로그램이 도구를 제공하는 표준 방식 | 에이전트 밖의 시스템에 닿아야 할 때: 티켓 DB, 위키, 모니터링 |
| **플러그인** | 도구 실행 앞뒤에 끼어드는 코드 | 모델 판단과 상관없이 항상 일어나야 할 때: 차단, 감사 로그, 알림 |

셋을 켜고 끄는 곳은 `opencode.json`입니다. 개념 설명은 [가이드 0. 개념](docs/guide/00-concepts.md)에서 시작하세요.

## 준비물

- **opencode 1.19.5** (`opencode --version`으로 확인)
- **Python 3.10 이상**: 예제 스크립트와 Python MCP 서버는 표준 라이브러리만 씁니다. M2 예제만 `mcp` 패키지를 설치합니다.
- **git 2.28 이상**: 예제 준비 스크립트(`prepare.py`)가 `git init -b`를 씁니다.
- **Node/npm** (선택): 플러그인 예제의 단위 테스트와 패키지 미러 지정(`npm config`)에 씁니다. npm이 없으면 `%USERPROFILE%\.npmrc`(Linux `~/.npmrc`) 파일에 `registry=<미러 주소>` 한 줄을 직접 써도 됩니다. M10(Node 서버)과 M11(`npx`로 파일 서버)은 Node 18 이상이 필요합니다. 없으면 두 예제의 해당 부분은 건너뜁니다(`check.py`가 경고만 냅니다).
- **uv** (선택): M11(`uvx`로 시간 서버)과 M12(`uvx` 배포 경로)에 씁니다. 없으면 `uvx`를 쓰는 부분만 건너뜁니다. M12의 `python -m` 기본 경로는 uv가 필요 없습니다.
- **Rust(cargo)** (선택): M14(실행 파일 하나로 된 서버)를 직접 빌드할 때만 씁니다. 없으면 M14의 빌드와 검사를 건너뜁니다.
- **모델**: 평소 쓰는 모델을 그대로 쓰면 됩니다. 설정된 모델이 없다면 무료 모델 `opencode/big-pickle`을 `-m`으로 지정할 수 있습니다.

기본 경로의 예제는 인터넷 없이 돕니다. 다만 M10, M11, M12, M14의 설치 단계(`npm install`, `npx`, `uvx`, `cargo build`)는 패키지 레지스트리나 미러가 필요하고, 닿지 않으면 `check.py`는 그 검사를 경고와 함께 건너뜁니다.
또한 `.opencode/` 폴더가 있는 예제는 시작할 때 opencode가 npm 패키지 `@opencode-ai/plugin`을 설치하려고 합니다.
**인터넷이 막힌 환경이라면 먼저 npm 패키지 미러를 지정하세요.** 레지스트리에 닿지 않으면 플러그인이 있는 예제(`.opencode/plugins/`)는 시작할 때마다 약 70초(새 환경의 첫 시작은 약 130초) 멈추고, 이 패키지를 쓰는 플러그인 도구(P6, X1-c)는 조용히 사라집니다. 스킬만 있는 예제는 설치를 시도하지만 눈에 띄게 멈추지는 않았습니다.

```powershell
npm config set registry https://<패키지 미러 주소>/     # %USERPROFILE%\.npmrc 에 저장됩니다
```

미러에 닿으면 첫 시작이 10초 안팎, 그다음부터는 1초 안팎입니다. 자세한 내용은 [P6 README](examples/03-plugins/p6-custom-tool/README.md#npm-자동-설치와-레지스트리패키지-미러)에 있습니다.

## 시작하기

PowerShell:

```powershell
git clone https://github.com/jihoon22-lee/agent-seminar
cd agent-seminar\examples\01-skills\s1a-commit-message
python prepare.py      # 실습용 git 저장소 sandbox\ 를 만듭니다
cd sandbox
opencode
```

Linux bash:

```bash
git clone https://github.com/jihoon22-lee/agent-seminar
cd agent-seminar/examples/01-skills/s1a-commit-message
python3 prepare.py     # 실습용 git 저장소 sandbox/ 를 만듭니다
cd sandbox
opencode
```

예제 폴더 하나하나가 독립된 opencode 프로젝트입니다. 폴더에 들어가서 opencode를 실행하면 그 예제의 설정, 스킬, 플러그인만 적용됩니다.
`prepare.py`가 있는 예제는 먼저 실행하세요. git 저장소가 필요한 예제는 `sandbox/`에 실습용 저장소를 만들고, 그 안에서 opencode를 실행합니다.
각 README는 같은 순서로 되어 있습니다: 무엇을 보여 주나, 실무에서는, 파일 구성, 따라 하기, 기대 결과, 동작 원리, 직접 바꿔 보기, 주의할 점.

Linux에서 `python` 명령이 없으면 예제 설정과 명령의 `python`을 `python3`로 바꾸세요.

## 예제

| 폴더 | 내용 | 예제 |
|---|---|---|
| [examples/00-config](examples/00-config/) | opencode.json의 위치와 병합, 환경 변수, 설정 덧씌우기, 격리, 권한, 커스텀 명령, 모델 제공자 연결, 에이전트 정의 | C1–C8 |
| [examples/01-skills](examples/01-skills/) | `SKILL.md` 하나짜리(스크립트 없이 CLI만 쓰는 S1d 포함)부터 참고 문서, 스크립트, 결과물 생성까지. description 작성법과 공유 방법 | S1a–S5c |
| [examples/02-mcp](examples/02-mcp/) | 표준 라이브러리 서버, 공식 SDK, 환경 변수, 원격 HTTP, SQLite, 리소스와 프롬프트, 도구 관리, 함정, Node SDK와 `npx`, 남의 서버 쓰기, `uvx` 패키지, CLI 감싸기, 실행 파일 하나, 클라이언트 지원 범위 | M1–M15 |
| [examples/03-plugins](examples/03-plugins/) | .env 차단, 위험 명령 차단, 감사 로그, 알림, 셸 환경, 커스텀 도구, 압축 훅, 불러오는 방법, 포맷과 검사 결과 전달, 상태를 보는 가드, 출력 가리기, 요청에 맥락 넣기 | P1–P12 |
| [examples/04-combined](examples/04-combined/) | 같은 일을 셋으로 해 보기, 셋을 엮은 장애 분석 | X1, X2 |

전체 목록과 난이도는 [examples/README.md](examples/README.md)에 있습니다.

## 가이드

| 문서 | 내용 |
|---|---|
| [0. 개념](docs/guide/00-concepts.md) | 스킬, MCP, 플러그인은 무엇이고 무엇이 다른가 |
| [1. opencode.json](docs/guide/01-config.md) | 설정 위치와 범위, 병합, 변수 치환, 권한, 커스텀 명령, 모델 제공자, 에이전트 |
| [2. 스킬](docs/guide/02-skills.md) | 스킬 만들기와 공유하기 |
| [3. MCP](docs/guide/03-mcp.md) | MCP 서버 만들기와 실행하는 방법, 로컬과 원격, 클라이언트 지원 범위 |
| [4. 플러그인](docs/guide/04-plugins.md) | 훅, 이벤트, 플러그인 만들기 |
| [5. 문제 해결](docs/guide/05-troubleshooting.md) | 증상별 원인과 해결, Windows 주의점 |

## 예제가 내 PC에서 도는지 확인하기

모든 예제에는 `check.py`가 있습니다. 실제 opencode 설정과 세션 기록은 건드리지 않습니다. 임시 폴더로 격리해서 실행하고, 끝나면 지웁니다.

```powershell
python tools\run_checks.py examples\01-skills        # 모델 없이 (몇 분)
python tools\run_checks.py examples --model          # 실제 모델 호출까지
```

```bash
python3 tools/run_checks.py examples/01-skills
python3 tools/run_checks.py examples --model
```

모델 없이 하는 검사는 opencode를 실제로 실행합니다. 모델 응답이 필요한 부분은 정해진 도구 호출을 하는 가짜 모델 서버로 확인합니다.
`--model`을 붙이면 실제 모델로도 확인합니다. 모델 응답은 실행마다 달라서 이 검사는 경고(WARN)로만 표시합니다.

## 발표 자료 조작법

| 키 | 동작 |
|---|---|
| `→` `Space` / `←` | 다음 / 이전 |
| 숫자 + `Enter` | 해당 슬라이드로 이동 |
| `O` | 전체 보기 |
| `N` | 발표자 메모 |
| `P` | 발표자 창 (메모, 다음 슬라이드, 타이머) |
| `F` | 전체 화면 |
| `S` | 짧은 버전: 오른쪽 위에 "심화"라고 표시된 슬라이드를 건너뛰며 넘김 (60분 발표용) |

브라우저의 인쇄(PDF로 저장)를 쓰면 한 장에 슬라이드 하나씩 출력됩니다.
슬라이드 원본은 `slides/src/`에 있고, `python tools/build_slides.py`가 `slides/index.html`을 만듭니다.

## 알려 둘 것

- 실제 모델 응답 예시는 무료 모델로 얻은 것입니다. 무료 모델 한도 때문에 확인하지 못한 부분은 각 README에 "미검증"으로 표시했습니다.
- opencode는 빠르게 바뀝니다. 공식 문서 사이트에는 다음 버전의 설정 형식이 먼저 올라와 있습니다. 1.19.5에서 `plugins`(새 형식)는 오류 없이 무시되어 플러그인이 하나도 불리지 않습니다. `mcp.servers`와 `"disabled": true`는 1.19.5도 받아들입니다. 이 세 형태만 확인했으니, 문서를 볼 때는 버전부터 확인하세요.
- [S2a 작업 기록 스킬](examples/01-skills/s2a-workthrough/)은 MIT 라이선스 스킬을 옮겨 온 것입니다. 출처와 라이선스는 `examples/01-skills/s2a-workthrough/.opencode/skills/workthrough/NOTICE.md`에 있습니다.
- 글꼴: 발표 자료는 IBM Plex Sans KR / IBM Plex Mono(SIL Open Font License 1.1)를 발표에 쓰는 글자만 남겨 줄인 것입니다. 라이선스 조건에 따라 이름을 바꿨습니다. 자세한 내용은 [slides/assets/fonts](slides/assets/fonts/)를 보세요.

## 라이선스

[MIT](LICENSE)
