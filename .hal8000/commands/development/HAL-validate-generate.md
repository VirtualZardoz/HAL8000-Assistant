---
name: HAL-validate-generate
description: Generate project-specific comprehensive validation command
parameters:
  - name: target_directory
    description: Path to project directory to analyze (defaults to current working directory)
    type: string
    required: false
  - name: output_location
    description: Where to create validate.md (project/.claude/commands/ or custom path)
    type: string
    required: false
---

# HAL-validate-generate

**Command Type:** Development
**Category:** development/
**Level:** 6 - Workflow Composition Prompt
**Created:** 2025-11-22
**Version:** 1.0

---

## Purpose

Generate a comprehensive, project-specific `/validate` command that ensures complete codebase confidence through multi-phase validation.

This command analyzes a target project directory (external to HAL8000) to:
- Detect existing development tools (linters, type checkers, formatters, test frameworks)
- Identify project architecture and technology stack
- Understand real user workflows from documentation
- Generate a custom `.claude/commands/validate.md` file with 5-phase validation

**Philosophy:** "If `/validate` passes, your app works" - comprehensive automated testing that mirrors production usage.

**Scope:** This command is designed for **external projects only** (not HAL8000 self-validation). Use `/HAL-system-check` for HAL8000 validation.

---

## Usage

```bash
# Analyze current working directory
/HAL-validate-generate

# Analyze specific project directory
/HAL-validate-generate "/mnt/d/my-web-app"

# Specify custom output location
/HAL-validate-generate "/mnt/d/my-web-app" "/mnt/d/my-web-app/.claude/commands/validate.md"
```

**Parameters:**
- `target_directory` - Path to project to analyze (optional, defaults to current working directory)
- `output_location` - Where to create validate.md (optional, defaults to `{project}/.claude/commands/validate.md`)

---

## Variables/Parameters

**Input Variables:**
- `target_directory` - string - Project root directory to analyze
- `output_location` - string - Output file path for generated command

**Analysis Variables (discovered during execution):**
- `project_type` - string - Frontend, Backend, Full-Stack, Mobile, CLI, Library, Microservices
- `languages` - array - Programming languages detected (JavaScript, TypeScript, Python, Go, Rust, etc.)
- `frameworks` - array - Frameworks in use (React, Vue, FastAPI, Django, Express, etc.)
- `linters` - array - Linting tools configured (eslint, pylint, ruff, golangci-lint, clippy)
- `type_checkers` - array - Type checking tools (TypeScript, mypy, Flow)
- `formatters` - array - Code formatters (prettier, black, gofmt, rustfmt)
- `test_frameworks` - array - Testing tools (jest, pytest, go test, cargo test, Playwright, Cypress)
- `build_tools` - array - Build systems (webpack, vite, cargo, go build, npm scripts)
- `containerization` - boolean - Docker/docker-compose present
- `ci_cd` - array - CI/CD configs (.github/workflows, .gitlab-ci.yml, etc.)
- `external_integrations` - array - External services (APIs, databases, message queues)
- `user_workflows` - array - Documented user journeys from README/docs

**Output Variables:**
- `validation_command_path` - string - Path to generated validate.md file
- `coverage_summary` - object - Summary of validation phases and coverage

---

## Instructions

**End-to-End Workflow Orchestration:**

### Phase 0: Preparation and Validation

**Step 0.1: Validate Target Directory**
- If `target_directory` not provided, use current working directory
- Verify target directory exists and is accessible
- Check that target is NOT HAL8000 itself (`/mnt/d/~HAL8000`)
  - If HAL8000: **ABORT** with message: "This command is for external projects. Use /HAL-system-check for HAL8000 validation."
- Set `project_root` variable to absolute path

**Step 0.2: Determine Output Location**
- If `output_location` not provided:
  - Default: `{project_root}/.claude/commands/validate.md`
  - Create `.claude/commands/` directory if it doesn't exist
- Verify output directory is writable
- Warn if overwriting existing validate.md (ask for confirmation)

**Step 0.3: Initialize Context Tracking**
- Set RAM_ZONE awareness (this is a heavy analysis task)
- Track loaded files in temporary manifest (prevent duplicate loading)
- Prepare for selective file reading (only load what's necessary)

---

### Phase 1: Documentation Analysis (User Workflows First)

**Critical Principle:** Understand how users ACTUALLY use the application before analyzing tools.

**Step 1.1: Discover Documentation Files**

Search for documentation in priority order:
1. `README.md` (root)
2. `CLAUDE.md` (if present - project instructions for Claude)
3. `docs/` directory (any .md files)
4. `USAGE.md`, `GETTING_STARTED.md`, `QUICKSTART.md`
5. API documentation (OpenAPI/Swagger specs, API.md)

Use Glob tool to find files efficiently:
```
Pattern: README.md, CLAUDE.md, docs/**/*.md, USAGE.md, GETTING_STARTED.md
```

**Step 1.2: Extract User Workflows**

Read each documentation file and identify:

**A. Usage Patterns:**
- Installation/setup steps
- Configuration requirements
- Startup procedures
- Common commands/operations

**B. User Journeys (Critical for E2E tests):**
- Multi-step workflows described in documentation
- Example: "Register → Verify Email → Login → Create Item → Edit Item"
- Example: "Clone repo → Install deps → Run dev server → Make changes → Run tests → Commit"
- Example: "API: Authenticate → Get token → Create resource → Query resource → Update → Delete"

**C. External Dependencies:**
- Third-party APIs mentioned (Stripe, Twilio, GitHub API, etc.)
- External services (databases, message queues, storage)
- CLI tools required (git, docker, kubectl)
- Platform integrations (Slack, Discord, Telegram bots)

**D. Feature List:**
- Core features described
- Optional features or plugins
- Admin vs user functionality
- API endpoints documented

**Storage:**
Store extracted workflows in `user_workflows` array:
```javascript
user_workflows = [
  {
    name: "User Registration Flow",
    steps: ["Visit /register", "Fill form", "Submit", "Verify email", "Login"],
    integrations: ["email service"],
    test_priority: "high"
  },
  {
    name: "API CRUD Operations",
    steps: ["POST /auth", "GET /items", "POST /items", "PUT /items/:id", "DELETE /items/:id"],
    integrations: ["database"],
    test_priority: "critical"
  }
]
```

**Step 1.3: Identify Critical Paths**

Determine which workflows are:
- **Critical** - Core functionality, must work (authentication, data creation)
- **High** - Important features, should work (search, filters, reporting)
- **Medium** - Nice-to-have features (optional integrations)
- **Low** - Edge cases, admin tools

This prioritization guides E2E test generation.

---

### Phase 2: Technology Stack Discovery

**Step 2.1: Identify Project Type and Languages**

**A. Detect Programming Languages:**

Look for language-specific files in project root and immediate subdirectories:

**JavaScript/TypeScript:**
- Files: `package.json`, `tsconfig.json`, `*.js`, `*.ts`, `*.jsx`, `*.tsx`
- Package manager: `package-lock.json` (npm), `yarn.lock` (yarn), `pnpm-lock.yaml` (pnpm)

**Python:**
- Files: `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile`, `*.py`
- Virtual env: `venv/`, `.venv/`, `poetry.lock`

**Go:**
- Files: `go.mod`, `go.sum`, `*.go`

**Rust:**
- Files: `Cargo.toml`, `Cargo.lock`, `*.rs`

**Java/Kotlin:**
- Files: `pom.xml`, `build.gradle`, `*.java`, `*.kt`

**Ruby:**
- Files: `Gemfile`, `Gemfile.lock`, `*.rb`

**PHP:**
- Files: `composer.json`, `composer.lock`, `*.php`

**C#/.NET:**
- Files: `*.csproj`, `*.sln`, `*.cs`

**Other:**
- Check for: Swift (`.swift`, `Package.swift`), Dart (`.dart`, `pubspec.yaml`), Elixir (`.ex`, `mix.exs`)

**B. Determine Project Type:**

**Frontend Indicators:**
- Directories: `src/components/`, `src/pages/`, `public/`, `static/`
- Files: `index.html`, `vite.config.*`, `webpack.config.*`, `.babelrc`
- Frameworks: React (`react` in package.json), Vue (`vue`), Svelte (`svelte`), Angular (`@angular`)

**Backend Indicators:**
- Directories: `api/`, `routes/`, `controllers/`, `models/`, `migrations/`
- Frameworks: Express (`express`), FastAPI (`fastapi`), Django (`django`), Flask (`flask`), Rails, Laravel
- Databases: `database/`, `db/`, `prisma/`, `migrations/`

**Full-Stack Indicators:**
- Both frontend and backend directories present
- Monorepo structure (`apps/`, `packages/`)
- Integrated frameworks (Next.js, Nuxt, SvelteKit, Remix)

**Mobile Indicators:**
- React Native: `react-native` in package.json, `android/`, `ios/`
- Flutter: `pubspec.yaml`, `lib/`, `android/`, `ios/`
- Native: Xcode project, Android Studio project

**CLI/Library Indicators:**
- No web server or UI files
- Binary output (Go, Rust `[[bin]]` in Cargo.toml)
- Library markers (Python `setup.py` with lib structure)

**Microservices Indicators:**
- Multiple service directories (`services/`, `apps/`)
- Docker Compose with multiple services
- Kubernetes configs (`k8s/`, `*.yaml` with kind: Deployment)

**Storage:**
```javascript
project_type = "Full-Stack" // or Frontend, Backend, Mobile, CLI, Library, Microservices
languages = ["TypeScript", "Python"]
frameworks = ["React", "FastAPI"]
```

**Step 2.2: Discover Development Tools**

**A. Linters:**

Search for configuration files:
- **JavaScript/TypeScript:** `.eslintrc*` (json, js, yaml), `eslint.config.js`, `package.json` (eslintConfig)
- **Python:** `.pylintrc`, `pylint.cfg`, `.ruff.toml`, `ruff.toml`, `pyproject.toml` ([tool.ruff])
- **Go:** `.golangci.yml`, `.golangci.yaml`
- **Rust:** `rustfmt.toml`, `.rustfmt.toml` (and Clippy via cargo)
- **Other:** `.rubocop.yml` (Ruby), `phpcs.xml` (PHP)

Also check `package.json` scripts or `Makefile` for lint commands.

**B. Type Checkers:**

- **TypeScript:** `tsconfig.json` (always check with `tsc --noEmit`)
- **Python:** `mypy.ini`, `.mypy.ini`, `pyproject.toml` ([tool.mypy])
- **Flow:** `.flowconfig`
- **Other:** Native type checking in Go, Rust (via cargo check)

**C. Formatters:**

- **JavaScript/TypeScript:** `.prettierrc*`, `prettier.config.js`, `package.json` (prettier)
- **Python:** `pyproject.toml` ([tool.black]), `.black.toml`
- **Go:** Uses `gofmt` by default (no config needed)
- **Rust:** Uses `rustfmt` with `rustfmt.toml`
- **Other:** `.editorconfig` (multi-language)

**D. Test Frameworks:**

**Unit Test Frameworks:**
- **JavaScript/TypeScript:**
  - Jest: `jest.config.*`, `"jest"` in package.json
  - Vitest: `vitest.config.*`, `"vitest"` in package.json
  - Mocha: `mocha.opts`, `"mocha"` in package.json
- **Python:**
  - pytest: `pytest.ini`, `pyproject.toml` ([tool.pytest])
  - unittest: `tests/` with `test_*.py` files
- **Go:** Native `*_test.go` files, `go.mod`
- **Rust:** Native tests in `src/`, `tests/` directory, Cargo.toml
- **Other:** RSpec (Ruby), PHPUnit (PHP)

**E2E Test Frameworks:**
- **Playwright:** `playwright.config.*`, `@playwright/test` in package.json
- **Cypress:** `cypress.json`, `cypress/` directory
- **Selenium:** Look for Selenium dependencies
- **Puppeteer:** `puppeteer` in dependencies

**E. Build Tools:**

- **JavaScript/TypeScript:**
  - Webpack: `webpack.config.js`
  - Vite: `vite.config.*`
  - Rollup: `rollup.config.js`
  - Parcel: `package.json` with parcel
  - npm scripts: `"build"` in package.json scripts
- **Python:** Build in `pyproject.toml`, `setup.py`
- **Go:** `go build` (native)
- **Rust:** `cargo build` (native)

**Step 2.3: Analyze Infrastructure**

**A. Containerization:**

Check for:
- `Dockerfile` - Single service containerization
- `docker-compose.yml`, `docker-compose.yaml` - Multi-service orchestration
- `.dockerignore` - Docker build optimization
- `docker/` directory - Multiple Dockerfiles for different services

Parse docker-compose.yml to identify:
- Services defined
- Databases (postgres, mysql, mongodb, redis)
- Exposed ports
- Health check endpoints
- Volume mounts
- Environment dependencies

**B. CI/CD:**

Check for:
- GitHub Actions: `.github/workflows/*.yml`
- GitLab CI: `.gitlab-ci.yml`
- CircleCI: `.circleci/config.yml`
- Travis: `.travis.yml`
- Jenkins: `Jenkinsfile`

Analyze CI configs to discover:
- Test commands actually run in CI
- Build commands
- Deployment steps
- Environment variables needed

**C. Infrastructure as Code:**

- Kubernetes: `k8s/`, `*.yaml` with `kind: Deployment`
- Terraform: `*.tf` files, `terraform/`
- Ansible: `playbooks/`, `*.yml` with tasks
- Helm: `Chart.yaml`, `values.yaml`

**Storage:**
```javascript
containerization = true
ci_cd = ["GitHub Actions", "Docker Compose"]
infrastructure = ["Kubernetes"]
```

**Step 2.4: Database and External Service Detection**

**A. Database Detection:**

From docker-compose.yml services or environment files:
- PostgreSQL: Service `postgres`, connection strings, `psycopg2`, `pg` package
- MySQL: Service `mysql`, `mariadb`, `mysql2` package
- MongoDB: Service `mongodb`, `mongoose`, `pymongo`
- Redis: Service `redis`, `redis` package
- SQLite: `*.db`, `*.sqlite` files, `sqlite3`

**B. External APIs and Integrations:**

Search documentation and code for mentions of:
- **Payment:** Stripe, PayPal, Square
- **Communication:** Twilio, SendGrid, Slack API, Discord API, Telegram Bot API
- **Cloud:** AWS S3, Azure, Google Cloud
- **Auth:** Auth0, Firebase Auth, OAuth providers
- **Analytics:** Google Analytics, Mixpanel, Segment
- **Version Control:** GitHub API, GitLab API
- **Other:** Any `https://api.*` domains in configs

Check environment variable files (`.env.example`, `.env.template`) for:
- API keys (patterns: `*_API_KEY`, `*_SECRET`, `*_TOKEN`)
- Service URLs (`*_URL`, `*_ENDPOINT`)

**Storage:**
```javascript
external_integrations = [
  { name: "PostgreSQL", type: "database", test_required: true },
  { name: "Redis", type: "cache", test_required: true },
  { name: "Stripe API", type: "payment", test_required: false, mock_available: true },
  { name: "GitHub API", type: "vcs", test_required: true }
]
```

---

### Phase 3: Validation Command Structure Design

**Step 3.1: Determine Validation Phases to Include**

Based on discoveries from Phase 2, determine which of the 5 phases are applicable:

**Phase 1: Linting**
- Include if: ANY linters discovered (`linters` array not empty)
- Skip if: No linter configs found (but include a comment in generated file)

**Phase 2: Type Checking**
- Include if: TypeScript (`tsconfig.json`) OR Python with mypy OR Flow
- Skip if: No static type checking

**Phase 3: Style/Format Checking**
- Include if: Prettier, Black, gofmt, rustfmt discovered
- Skip if: No formatters configured

**Phase 4: Unit Testing**
- Include if: Test framework discovered AND tests exist (`tests/`, `__tests__/`, `*_test.go`, etc.)
- Skip if: No tests found (but warn in output and add TODO comment)

**Phase 5: End-to-End Testing**
- **ALWAYS INCLUDE** - This is the critical phase
- Generate E2E tests based on user workflows from Phase 1
- Even if no existing E2E framework, provide manual test instructions

**Step 3.2: Map Tools to Commands**

For each discovered tool, determine the exact command to run:

**Linters:**
- eslint: `npx eslint .` or `npm run lint` (check scripts)
- pylint: `pylint src/` (check for src directory)
- ruff: `ruff check .` or `ruff check src/`
- golangci-lint: `golangci-lint run`
- cargo clippy: `cargo clippy -- -D warnings`

**Type Checkers:**
- TypeScript: `npx tsc --noEmit`
- mypy: `mypy src/` or `mypy .`
- Flow: `flow check`

**Formatters (check mode, no modifications):**
- Prettier: `npx prettier --check .` or `npm run format:check`
- Black: `black --check src/` or `black --check .`
- gofmt: `gofmt -l .` (lists unformatted files)
- rustfmt: `cargo fmt -- --check`

**Unit Tests (with coverage):**
- Jest: `npm test -- --coverage` or `npm run test:coverage`
- Vitest: `npx vitest run --coverage`
- pytest: `pytest tests/ -v --cov=src` or `pytest -v --cov`
- Go: `go test ./... -v -cover`
- Rust: `cargo test`

**Build (if applicable):**
- npm: `npm run build`
- Go: `go build ./...`
- Rust: `cargo build --release`

**Step 3.3: Design E2E Test Strategy**

This is the MOST IMPORTANT phase. Design based on project type:

**For Frontend Applications (React, Vue, Svelte, Angular):**

**IF Playwright/Cypress detected:**
- Use existing E2E test suite: `npx playwright test` or `npm run test:e2e`
- Generate ADDITIONAL tests for workflows from docs if not covered

**IF no E2E framework:**
- Recommend Playwright installation
- Generate complete Playwright test suite based on user workflows from Phase 1

**E2E Test Structure (Playwright example):**
```javascript
// tests/e2e/user-workflows.spec.ts
// Generated based on workflows from README.md

test('User Registration → Email Verification → Login', async ({ page }) => {
  // Step 1: Registration (from workflow)
  await page.goto('/register');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'SecurePass123!');
  await page.click('button[type="submit"]');

  // Step 2: Verify email sent (check for confirmation message)
  await expect(page.locator('.success-message')).toContainText('Check your email');

  // Step 3: Login (from workflow)
  await page.goto('/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'SecurePass123!');
  await page.click('button[type="submit"]');

  // Step 4: Verify logged in
  await expect(page).toHaveURL(/\/dashboard/);
});

test('CRUD Operations - Create → Edit → Delete Item', async ({ page }) => {
  // From workflow: "Create item → Edit item → Delete item"
  // [Generate full test based on documented workflow]
});
```

**For Backend Applications (API servers, microservices):**

**Setup:**
- Use Docker Compose to start services: `docker-compose up -d`
- Wait for health checks: `timeout 60 bash -c 'until curl -f http://localhost:8000/health; do sleep 2; done'`

**API Endpoint Testing:**

For each API endpoint from documentation:

**Authentication workflow:**
```bash
# Test registration
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!"}'

# Test login and capture token
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!"}' \
  | jq -r '.token')
```

**CRUD operations:**
```bash
# GET all items
curl http://localhost:8000/api/items -H "Authorization: Bearer $TOKEN"

# POST new item
ITEM_ID=$(curl -X POST http://localhost:8000/api/items \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Item","description":"Test"}' \
  | jq -r '.id')

# PUT update item
curl -X PUT http://localhost:8000/api/items/$ITEM_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Item"}'

# DELETE item
curl -X DELETE http://localhost:8000/api/items/$ITEM_ID \
  -H "Authorization: Bearer $TOKEN"
```

**Database Verification:**

For each critical operation, verify database state:
```bash
# Verify user was created
docker exec {db_container} psql -U {user} -d {db} -c "SELECT COUNT(*) FROM users WHERE email='test@test.com';"

# Verify item was created
docker exec {db_container} psql -U {user} -d {db} -c "SELECT * FROM items WHERE id='$ITEM_ID';"

# Verify item was deleted
docker exec {db_container} psql -U {user} -d {db} -c "SELECT COUNT(*) FROM items WHERE id='$ITEM_ID';" # Should be 0
```

**Error Scenarios (Critical for comprehensive testing):**
```bash
# Test 404 - Invalid resource
HTTP_CODE=$(curl -w "%{http_code}" -o /dev/null http://localhost:8000/api/items/invalid-uuid)
[ "$HTTP_CODE" = "404" ] && echo "✓ 404 test passed" || echo "✗ 404 test failed"

# Test 401 - No authentication
HTTP_CODE=$(curl -w "%{http_code}" -o /dev/null http://localhost:8000/api/items)
[ "$HTTP_CODE" = "401" ] && echo "✓ 401 test passed" || echo "✗ 401 test failed"

# Test 403 - Forbidden access
HTTP_CODE=$(curl -w "%{http_code}" -o /dev/null \
  http://localhost:8000/api/admin \
  -H "Authorization: Bearer $TOKEN")
[ "$HTTP_CODE" = "403" ] && echo "✓ 403 test passed" || echo "✗ 403 test failed"

# Test 400 - Invalid input
HTTP_CODE=$(curl -w "%{http_code}" -o /dev/null \
  -X POST http://localhost:8000/api/items \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"invalid":"data"}')
[ "$HTTP_CODE" = "400" ] && echo "✓ 400 test passed" || echo "✗ 400 test failed"
```

**External Integration Testing (if applicable):**

For each external integration from Phase 2:

**Mock-able services (Stripe, Twilio, etc.):**
- Include tests with mocked responses OR
- Provide test API keys in comments with instructions

**Required services (GitHub API, etc.):**
- Include actual API calls with test data
- Document required environment variables
- Provide cleanup scripts

Example:
```bash
# Test GitHub API integration (requires GITHUB_TOKEN env var)
if [ -n "$GITHUB_TOKEN" ]; then
  # Test creating a test repository
  REPO_NAME="test-repo-$(date +%s)"
  curl -X POST https://api.github.com/user/repos \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"$REPO_NAME\",\"private\":true}"

  # Verify via app API that repo was created
  curl http://localhost:8000/api/repos \
    -H "Authorization: Bearer $TOKEN" \
    | jq -r '.[] | select(.name=="'$REPO_NAME'")'

  # Cleanup: Delete test repo
  curl -X DELETE https://api.github.com/repos/$(whoami)/$REPO_NAME \
    -H "Authorization: token $GITHUB_TOKEN"
else
  echo "⚠️  Skipping GitHub integration tests (GITHUB_TOKEN not set)"
fi
```

**Cleanup:**
```bash
# Always cleanup Docker resources
docker-compose down -v  # -v removes volumes (clean database)
```

**For Full-Stack Applications:**

Combine frontend + backend approaches:
1. Start backend with Docker Compose
2. Run Playwright tests that exercise full workflows (UI → API → Database)
3. Verify database state after UI operations
4. Test error handling in UI (network errors, API errors)

**For Mobile Applications:**

**React Native:**
- Unit tests: `npm test`
- E2E tests: Detox (`detox test`) or Maestro
- Platform-specific: iOS simulator, Android emulator tests

**Flutter:**
- Unit tests: `flutter test`
- Widget tests: `flutter test`
- Integration tests: `flutter drive`

**For CLI Applications:**

Test command-line workflows:
```bash
# Test installation
./install.sh

# Test basic commands
./my-cli --version
./my-cli init test-project
[ -d "test-project" ] && echo "✓ Init created directory" || echo "✗ Init failed"

# Test command workflows
cd test-project
../my-cli add feature
../my-cli build
[ -f "dist/output" ] && echo "✓ Build successful" || echo "✗ Build failed"

# Test error handling
../my-cli invalid-command 2>&1 | grep -q "Unknown command" && echo "✓ Error handling works"

# Cleanup
cd ..
rm -rf test-project
```

**For Microservices:**

Test service-to-service communication:
```bash
# Start all services
docker-compose up -d

# Test each service independently
curl http://localhost:3001/health  # Service A
curl http://localhost:3002/health  # Service B

# Test cross-service workflows
# Example: Order service → Payment service → Inventory service
ORDER_ID=$(curl -X POST http://localhost:3001/orders \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"items":[{"id":1,"qty":2}]}' \
  | jq -r '.id')

# Verify payment was processed (Service B)
curl http://localhost:3002/payments?order_id=$ORDER_ID | jq -r '.status'

# Verify inventory was updated (Service C)
curl http://localhost:3003/inventory/1 | jq -r '.quantity'  # Should be reduced

# Cleanup
docker-compose down -v
```

**Step 3.4: Determine Test Data Strategy**

For E2E tests, determine how to handle test data:

**Database:**
- Seed script: `docker exec {db} psql -U {user} -d {db} -f /seed.sql`
- Migrations: `npm run migrate` or `alembic upgrade head`
- Test fixtures: Load from `tests/fixtures/` directory

**File uploads:**
- Test files in `tests/fixtures/images/`, `tests/fixtures/documents/`

**External services:**
- Mock data responses or sandbox API keys

---

### Phase 4: Command Generation

**Step 4.1: Generate YAML Frontmatter**

Create frontmatter for the validate command:
```yaml
---
name: validate
description: Comprehensive {project_type} validation - linting, tests, E2E
---
```

**Step 4.2: Generate Command Header**

```markdown
# Validate Codebase

> **Auto-generated validation command** for {project_name}
>
> Generated by HAL8000 on {date}
> Project Type: {project_type}
> Languages: {languages}
> Frameworks: {frameworks}

## Overview

This command performs comprehensive validation across 5 phases:
1. **Linting** - Code quality and style rules
2. **Type Checking** - Static type validation
3. **Format Checking** - Code formatting consistency
4. **Unit Testing** - Component-level tests with coverage
5. **End-to-End Testing** - Complete user workflow validation

**Philosophy:** If this command passes, your application works correctly.
```

**Step 4.3: Generate Phase 1 - Linting**

For each linter discovered:

```markdown
## Phase 1: Linting

### {Language} Linting ({Linter})

**Purpose:** Validate code quality rules for {language} code

**Command:**
!`{linter_command}`

**What this checks:**
- {List specific rules from config if parseable}
- Code style consistency
- Common errors and anti-patterns
- Best practice violations

**Configuration:** `{config_file_path}`

**Expected output:** No linting errors
```

Example (multi-language project):
```markdown
## Phase 1: Linting

### Frontend Linting (ESLint)
!`cd frontend && npm run lint`

**Configuration:** `frontend/.eslintrc.json`
**Checks:** React hooks rules, TypeScript rules, import order, unused variables

### Backend Linting (Ruff)
!`cd backend && ruff check src/`

**Configuration:** `backend/pyproject.toml` ([tool.ruff])
**Checks:** Python style (PEP 8), import sorting, unused code, security issues
```

**If no linters found:**
```markdown
## Phase 1: Linting

⚠️ **No linters detected**

**Recommendation:** Consider adding a linter for code quality:
- JavaScript/TypeScript: `npm install --save-dev eslint`
- Python: `pip install ruff`
- Go: `golangci-lint`

**TODO:** Configure linting and update this validation command
```

**Step 4.4: Generate Phase 2 - Type Checking**

```markdown
## Phase 2: Type Checking

### {Language} Type Validation

**Purpose:** Ensure type safety across codebase

**Command:**
!`{type_check_command}`

**What this checks:**
- Type mismatches
- Null/undefined errors
- Function signature compliance
- Generic type constraints

**Configuration:** `{config_file}`

**Expected output:** No type errors
```

Example:
```markdown
## Phase 2: Type Checking

### TypeScript Type Validation
!`cd frontend && npx tsc --noEmit`

**Configuration:** `frontend/tsconfig.json`
**Strictness:** strict mode enabled

### Python Type Validation (mypy)
!`cd backend && mypy src/`

**Configuration:** `backend/mypy.ini`
**Strictness:** strict optional, disallow untyped defs
```

**Step 4.5: Generate Phase 3 - Format Checking**

```markdown
## Phase 3: Style Checking

### {Language} Code Formatting

**Purpose:** Ensure consistent code formatting

**Command:**
!`{format_check_command}`

**What this checks:**
- Indentation consistency
- Line length limits
- Quote style (single vs double)
- Trailing whitespace
- Import formatting

**Configuration:** `{config_file}`

**Expected output:** All files properly formatted
```

**Step 4.6: Generate Phase 4 - Unit Testing**

```markdown
## Phase 4: Unit Testing

### {Language} Unit Test Suite

**Purpose:** Validate individual component behavior

**Command:**
!`{test_command}`

**Test Framework:** {framework}
**Coverage Threshold:** {threshold}% (if configured)

**What this tests:**
- Individual function behavior
- Component rendering (frontend)
- API endpoint logic (backend)
- Edge cases and error handling
- Mock external dependencies

**Configuration:** `{config_file}`
**Test Files:** `{test_directory_pattern}`

**Expected output:** All tests pass, coverage threshold met
```

Example:
```markdown
## Phase 4: Unit Testing

### Frontend Unit Tests (Jest + React Testing Library)
!`cd frontend && npm test -- --coverage --watchAll=false`

**Test Files:** `src/**/*.test.tsx`, `src/**/*.test.ts`
**Coverage Threshold:** 80% (configured in jest.config.js)
**Tests:**
- Component rendering and props
- User interactions (clicks, form inputs)
- State management
- API mocking

### Backend Unit Tests (pytest)
!`cd backend && pytest tests/unit -v --cov=src --cov-report=term-missing --cov-fail-under=85`

**Test Files:** `tests/unit/test_*.py`
**Coverage Threshold:** 85%
**Tests:**
- API endpoint logic
- Database models
- Business logic functions
- Authentication/authorization
```

**Step 4.7: Generate Phase 5 - End-to-End Testing (MOST CRITICAL)**

This is the most complex and important phase. Generate based on project type:

**For Frontend with Playwright:**
```markdown
## Phase 5: End-to-End Testing

### Frontend User Workflow Testing (Playwright)

**Purpose:** Test complete user journeys as documented in README.md

**Setup:**
!`cd frontend && npm run build`
!`cd frontend && npm run preview &`  # Start preview server
!`timeout 30 bash -c 'until curl -f http://localhost:4173; do sleep 2; done'`

**E2E Test Execution:**
!`cd frontend && npx playwright test`

**User Workflows Tested:**

#### 1. User Registration → Email Verification → Login
**From:** README.md "Getting Started" section
**Steps:**
1. Navigate to registration page
2. Fill registration form (email, password, confirm password)
3. Submit form
4. Verify success message and email sent notification
5. Navigate to login page
6. Login with new credentials
7. Verify dashboard loads and user is authenticated

**Test File:** `tests/e2e/auth-flow.spec.ts`

#### 2. Create Item → Edit Item → Delete Item (CRUD)
**From:** README.md "Core Features" section
**Steps:**
1. Authenticate as test user
2. Navigate to items page
3. Click "Create New Item"
4. Fill item form (name, description, category)
5. Submit and verify item appears in list
6. Click edit on new item
7. Modify item details
8. Save and verify changes reflected
9. Delete item and verify removal from list

**Test File:** `tests/e2e/items-crud.spec.ts`

#### 3. Search and Filter Functionality
**From:** README.md "Features" section
**Steps:**
1. Navigate to items page with test data
2. Enter search query
3. Verify filtered results
4. Apply category filter
5. Verify results match filter
6. Clear filters and verify all items shown

**Test File:** `tests/e2e/search-filter.spec.ts`

#### 4. Error Handling and Validation
**Steps:**
1. Test form validation (empty fields, invalid email, weak password)
2. Test 404 page for invalid routes
3. Test network error handling (offline mode)
4. Test session expiration redirect

**Test File:** `tests/e2e/error-handling.spec.ts`

**Cleanup:**
!`pkill -f "npm run preview"`  # Stop preview server
```

**For Backend with curl:**
```markdown
## Phase 5: End-to-End Testing

### Backend API and Database Integration Testing

**Purpose:** Test complete API workflows from authentication through data persistence

**Setup:**
!`docker-compose up -d`
!`timeout 60 bash -c 'until curl -f http://localhost:8000/health; do sleep 2; done'`

**Database Initialization:**
!`docker exec backend-container python manage.py migrate`
!`docker exec backend-container python manage.py seed_test_data`

---

### Test Suite: Authentication Flow

**From:** API documentation - "Authentication" section

#### Test 1: User Registration
!`curl -X POST http://localhost:8000/api/auth/register -H "Content-Type: application/json" -d '{"email":"test@example.com","password":"SecurePass123!","name":"Test User"}' | jq`

**Expected:** HTTP 201, returns user object with id

#### Test 2: Registration Validation
!`curl -w "%{http_code}" -X POST http://localhost:8000/api/auth/register -H "Content-Type: application/json" -d '{"email":"invalid","password":"weak"}'`

**Expected:** HTTP 400, validation errors

#### Test 3: Login and Token Retrieval
!`TOKEN=$(curl -X POST http://localhost:8000/api/auth/login -H "Content-Type: application/json" -d '{"email":"test@example.com","password":"SecurePass123!"}' | jq -r '.access_token')`
!`echo "Token: $TOKEN"`

**Expected:** HTTP 200, JWT token returned

#### Test 4: Verify Token Works
!`curl http://localhost:8000/api/auth/me -H "Authorization: Bearer $TOKEN" | jq`

**Expected:** HTTP 200, returns authenticated user details

---

### Test Suite: CRUD Operations

**From:** API documentation - "Items API" section

#### Test 5: Create Item
!`ITEM_ID=$(curl -X POST http://localhost:8000/api/items -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"name":"Test Item","description":"E2E test item","category":"test","price":29.99}' | jq -r '.id')`
!`echo "Created Item ID: $ITEM_ID"`

**Expected:** HTTP 201, returns item with generated ID

#### Test 6: Verify Database Persistence
!`docker exec postgres-container psql -U appuser -d appdb -c "SELECT id, name, category, price FROM items WHERE id='$ITEM_ID';"`

**Expected:** Item exists in database with correct values

#### Test 7: List All Items
!`curl http://localhost:8000/api/items -H "Authorization: Bearer $TOKEN" | jq '.items | length'`

**Expected:** HTTP 200, array includes our test item

#### Test 8: Get Single Item
!`curl http://localhost:8000/api/items/$ITEM_ID -H "Authorization: Bearer $TOKEN" | jq`

**Expected:** HTTP 200, returns full item details

#### Test 9: Update Item
!`curl -X PUT http://localhost:8000/api/items/$ITEM_ID -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"name":"Updated Test Item","price":39.99}' | jq`

**Expected:** HTTP 200, returns updated item

#### Test 10: Verify Update in Database
!`docker exec postgres-container psql -U appuser -d appdb -c "SELECT name, price FROM items WHERE id='$ITEM_ID';"`

**Expected:** Database shows updated values (name="Updated Test Item", price=39.99)

#### Test 11: Delete Item
!`curl -X DELETE http://localhost:8000/api/items/$ITEM_ID -H "Authorization: Bearer $TOKEN"`

**Expected:** HTTP 204, no content

#### Test 12: Verify Deletion
!`docker exec postgres-container psql -U appuser -d appdb -c "SELECT COUNT(*) FROM items WHERE id='$ITEM_ID';"`

**Expected:** Count = 0 (item deleted)

---

### Test Suite: Error Handling

**From:** API documentation - "Error Codes" section

#### Test 13: 404 - Resource Not Found
!`HTTP_CODE=$(curl -w "%{http_code}" -o /dev/null -s http://localhost:8000/api/items/non-existent-uuid -H "Authorization: Bearer $TOKEN")`
!`[ "$HTTP_CODE" = "404" ] && echo "✓ 404 test passed" || echo "✗ 404 test failed (got $HTTP_CODE)"`

#### Test 14: 401 - Unauthorized (No Token)
!`HTTP_CODE=$(curl -w "%{http_code}" -o /dev/null -s http://localhost:8000/api/items)`
!`[ "$HTTP_CODE" = "401" ] && echo "✓ 401 test passed" || echo "✗ 401 test failed (got $HTTP_CODE)"`

#### Test 15: 401 - Invalid Token
!`HTTP_CODE=$(curl -w "%{http_code}" -o /dev/null -s http://localhost:8000/api/items -H "Authorization: Bearer invalid.token.here")`
!`[ "$HTTP_CODE" = "401" ] && echo "✓ Invalid token test passed" || echo "✗ Invalid token test failed (got $HTTP_CODE)"`

#### Test 16: 403 - Forbidden (Access Denied)
!`HTTP_CODE=$(curl -w "%{http_code}" -o /dev/null -s http://localhost:8000/api/admin/users -H "Authorization: Bearer $TOKEN")`
!`[ "$HTTP_CODE" = "403" ] && echo "✓ 403 test passed" || echo "✗ 403 test failed (got $HTTP_CODE)"`

**Note:** Assumes $TOKEN is for non-admin user

#### Test 17: 400 - Validation Error
!`HTTP_CODE=$(curl -w "%{http_code}" -o /dev/null -s -X POST http://localhost:8000/api/items -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"invalid_field":"value"}')`
!`[ "$HTTP_CODE" = "400" ] && echo "✓ 400 test passed" || echo "✗ 400 test failed (got $HTTP_CODE)"`

---

### Test Suite: External Integrations

**From:** README.md - "Integrations" section

{IF GitHub API integration detected:}

#### Test 18: GitHub API Integration
!`if [ -n "$GITHUB_TOKEN" ]; then
  # Create test repository via app
  REPO_NAME="e2e-test-$(date +%s)"
  curl -X POST http://localhost:8000/api/github/repos \\
    -H "Authorization: Bearer $TOKEN" \\
    -H "Content-Type: application/json" \\
    -d "{\"name\":\"$REPO_NAME\",\"description\":\"E2E test repo\",\"private\":true}" | jq

  # Verify repo exists on GitHub
  sleep 2  # Allow time for GitHub API propagation
  curl https://api.github.com/repos/$(whoami)/$REPO_NAME \\
    -H "Authorization: token $GITHUB_TOKEN" | jq -r '.name'

  # Cleanup: Delete test repo via app
  curl -X DELETE http://localhost:8000/api/github/repos/$REPO_NAME \\
    -H "Authorization: Bearer $TOKEN"

  echo "✓ GitHub integration test passed"
else
  echo "⚠️  Skipping GitHub integration test (GITHUB_TOKEN not set)"
  echo "   Set GITHUB_TOKEN environment variable to test GitHub integration"
fi`

{IF Stripe API integration detected:}

#### Test 19: Payment Processing (Stripe - Test Mode)
!`# Using Stripe test card
curl -X POST http://localhost:8000/api/payments/charge \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "amount": 1000,
    "currency": "usd",
    "source": "tok_visa",
    "description": "E2E test charge"
  }' | jq

# Verify charge in database
docker exec postgres-container psql -U appuser -d appdb -c "SELECT amount, status FROM payments ORDER BY created_at DESC LIMIT 1;"`

**Expected:** Charge succeeds with test token, recorded in database

---

### Cleanup

**Stop and remove all containers:**
!`docker-compose down -v`

**Remove test artifacts:**
!`rm -rf test-data/`

---

### Summary

**E2E Tests Executed:** {count} tests across {suites} test suites
**Coverage:**
- ✓ Authentication flow (registration, login, token validation)
- ✓ CRUD operations (create, read, update, delete)
- ✓ Database persistence verification
- ✓ Error handling (400, 401, 403, 404)
- ✓ External integrations ({list integrations})

**Philosophy:** These tests mirror real user/client workflows from documentation. If all tests pass, the application functions correctly in production.
```

**For Full-Stack Applications:**
```markdown
## Phase 5: End-to-End Testing

### Full-Stack User Journey Testing

**Purpose:** Test complete workflows from UI through API to database

**Setup:**
!`docker-compose up -d`  # Start backend + database
!`timeout 60 bash -c 'until curl -f http://localhost:8000/health; do sleep 2; done'`
!`cd frontend && npm run build && npm run preview &`  # Start frontend
!`timeout 30 bash -c 'until curl -f http://localhost:4173; do sleep 2; done'`

**Playwright Configuration:**
Update `playwright.config.ts` to use preview server (http://localhost:4173)

**E2E Test Execution:**
!`cd frontend && npx playwright test`

**Workflows Tested:**

#### 1. Complete User Registration and Authentication Flow
**From:** README.md - "Getting Started" section
**Frontend → Backend → Database:**
1. User fills registration form in UI
2. Frontend sends POST to /api/auth/register
3. Backend creates user in PostgreSQL
4. Backend sends verification email (mocked in tests)
5. User logs in via UI
6. Backend returns JWT token
7. Frontend stores token and redirects to dashboard

**Verification:**
- UI shows dashboard
- Database contains user record
- Session token is valid

**Test File:** `tests/e2e/full-stack-auth.spec.ts`

#### 2. Item Management: Create via UI → Persist → Display
**From:** README.md - "Features" section
**Steps:**
1. Authenticated user navigates to "Create Item" page
2. Fills form (name, description, price, category)
3. Submits form (POST /api/items)
4. Backend validates and saves to database
5. Frontend redirects to items list
6. New item appears in list (fetched from GET /api/items)

**Verification:**
- Item visible in UI
- Database query confirms item exists
- Item has correct attributes

**Test File:** `tests/e2e/full-stack-items.spec.ts`

**Playwright Test Includes Database Verification:**
```typescript
test('Create item via UI and verify in database', async ({ page }) => {
  await page.goto('/items/new');
  await page.fill('[name="name"]', 'E2E Test Item');
  await page.fill('[name="price"]', '29.99');
  await page.click('button[type="submit"]');

  // Wait for item to appear in list
  await expect(page.locator('text=E2E Test Item')).toBeVisible();

  // Verify in database
  const result = await exec('docker exec postgres-container psql -U appuser -d appdb -t -c "SELECT name, price FROM items WHERE name=\'E2E Test Item\';"');
  expect(result.stdout).toContain('E2E Test Item');
  expect(result.stdout).toContain('29.99');
});
```

**Cleanup:**
!`pkill -f "npm run preview"`
!`docker-compose down -v`
```

**Step 4.8: Generate Summary Section**

```markdown
---

## Summary

**Validation Complete!**

If you see this message, all validation phases have passed:

✅ **Phase 1: Linting** - Code quality standards met
✅ **Phase 2: Type Checking** - No type errors
✅ **Phase 3: Format Checking** - Code formatting consistent
✅ **Phase 4: Unit Testing** - All tests pass, coverage thresholds met
✅ **Phase 5: End-to-End Testing** - User workflows validated

**Your application is ready for deployment.**

---

## Validation Coverage

**Linting:** {linter_list}
**Type Checking:** {type_checker_list}
**Formatting:** {formatter_list}
**Unit Tests:** {test_framework_list}
**E2E Tests:** {e2e_framework_or_manual}

**User Workflows Tested:** {workflow_count}
**API Endpoints Tested:** {endpoint_count}
**Database Verified:** {yes/no}
**External Integrations:** {integration_list}

---

## Maintenance

This validation command was auto-generated by HAL8000 on {date}.

**To update:**
1. If you add new tools (linters, formatters): Re-run `/HAL-validate-generate`
2. If you add new features: Update E2E tests to cover new workflows
3. If you change infrastructure: Update Docker Compose or setup commands

**Manual E2E test updates:** Add tests to cover new features in {e2e_test_directory}

---

## Troubleshooting

**If Phase 1 fails (Linting):**
- Run linter individually to see errors: `{linter_command}`
- Fix errors and re-run validation
- Consider auto-fixing: `{linter_fix_command}` (if supported)

**If Phase 2 fails (Type Checking):**
- Run type checker individually: `{type_check_command}`
- Review type errors in output
- Add type annotations or fix type mismatches

**If Phase 3 fails (Format Checking):**
- Auto-fix formatting: `{formatter_fix_command}`
- Re-run validation

**If Phase 4 fails (Unit Tests):**
- Run tests with verbose output: `{test_command_verbose}`
- Review failing tests
- Fix implementation or update tests as needed
- Check coverage reports for gaps

**If Phase 5 fails (E2E Tests):**
- Check that all services started correctly (docker-compose ps)
- Verify database is accessible
- Review E2E test output for specific failures
- Check logs: `docker-compose logs {service}`
- Ensure environment variables are set (if needed)
- Verify external services are accessible (if testing integrations)

**Docker issues:**
- Restart services: `docker-compose restart`
- Check logs: `docker-compose logs`
- Clean restart: `docker-compose down -v && docker-compose up -d`

---

## Notes

**Generated by:** HAL8000 validation generator
**Project analyzed:** {project_root}
**Analysis date:** {date}
**Project type:** {project_type}
**Languages detected:** {languages}
**Frameworks detected:** {frameworks}

**Customization:** This command can be manually edited to add project-specific validations.
```

**Step 4.9: Write Generated Command to File**

Write the complete validation command to the output location determined in Phase 0.

Use the Write tool to create `{output_location}` with all generated content.

---

### Phase 5: Verification and Output

**Step 5.1: Verify Generated Command**

After writing the file:
1. Read the generated file to verify it was written correctly
2. Check file size (should be substantial - at least 5KB for a real project)
3. Verify all phases are present
4. Confirm E2E tests are comprehensive

**Step 5.2: Generate Execution Summary**

Create a summary to display to the user:

```
✅ Validation Command Generated

Location: {output_location}
Size: {file_size}

Project Analysis:
  Type: {project_type}
  Languages: {languages}
  Frameworks: {frameworks}

Validation Phases Included:
  ✓ Phase 1: Linting ({linter_count} linters)
  ✓ Phase 2: Type Checking ({type_checker_count} checkers)
  ✓ Phase 3: Format Checking ({formatter_count} formatters)
  ✓ Phase 4: Unit Testing ({test_framework_count} frameworks)
  ✓ Phase 5: E2E Testing ({workflow_count} workflows, {endpoint_count} endpoints)

Coverage Summary:
  User Workflows: {workflow_count} workflows from documentation
  API Endpoints: {endpoint_count} endpoints tested
  Database Verification: {yes/no}
  External Integrations: {integration_count} services
  Error Scenarios: {error_test_count} tests

Next Steps:
  1. Review generated command: Read {output_location}
  2. Customize if needed (add project-specific tests)
  3. Run validation: /validate
  4. Fix any issues and re-run until all phases pass

Ready to validate? Run: /validate
```

**Step 5.3: Offer Next Actions**

Ask user:
```
Would you like me to:
1. Run the generated /validate command now?
2. Review the generated command first?
3. Make customizations to the validation?
```

---

## Delegation Patterns

**No sub-agents used in this command.**

This command performs all analysis and generation directly. The complexity is in the comprehensive analysis logic, not in delegation.

**Rationale:**
- Analysis requires reading many files across the project (would exceed sub-agent RAM with context loading)
- Generation logic is sequential and builds on previous discoveries
- Keeping in main session allows user to see progress and intermediate findings

**RAM Management:**
- Use selective file reading (read only necessary config files)
- Parse configs without loading entire codebase into context
- Generate output incrementally (build string in memory, write once)

---

## Workflow Integration

**This command integrates with:**

**Pre-requisites:**
- Target project must exist and be accessible
- Project should have a `.claude/commands/` directory (created if missing)

**Generates:**
- `/validate` command file in project directory

**Composes with:**
- `/validate` - Run the generated validation (after this command completes)

**Typical workflow:**
```
cd /mnt/d/my-web-app/
/HAL-validate-generate          # Analyze and generate
/validate                        # Run comprehensive validation
[fix any issues]
/validate                        # Re-run until passes
```

**Update workflow:**
```
[Add new linter or test framework to project]
/HAL-validate-generate          # Regenerate with new tools
/validate                        # Validation now includes new tool
```

---

## Output Format

**Console Output During Execution:**

```
🔍 Analyzing project: /mnt/d/my-web-app

Phase 0: Preparation
  ✓ Target directory validated
  ✓ Output location determined: /mnt/d/my-web-app/.claude/commands/validate.md

Phase 1: Documentation Analysis
  ✓ Found README.md
  ✓ Extracted 4 user workflows
  ✓ Identified 2 external integrations (Stripe, GitHub API)

Phase 2: Technology Stack Discovery
  ✓ Project Type: Full-Stack
  ✓ Languages: TypeScript, Python
  ✓ Frontend: React with Vite
  ✓ Backend: FastAPI with PostgreSQL
  ✓ Linters: ESLint, Ruff
  ✓ Type Checkers: TypeScript, mypy
  ✓ Formatters: Prettier, Black
  ✓ Test Frameworks: Jest, pytest, Playwright
  ✓ Containerization: Docker Compose detected

Phase 3: Validation Strategy Design
  ✓ 5 validation phases designed
  ✓ 12 E2E tests planned (4 workflows × 3 test types)
  ✓ Database verification included
  ✓ External integration tests designed

Phase 4: Command Generation
  ✓ Generated 347 lines of validation logic
  ✓ Included comprehensive E2E tests
  ✓ Added error handling tests
  ✓ Included database verification

Phase 5: Verification
  ✓ File written successfully
  ✓ Size: 24.5 KB
  ✓ All phases present

✅ Validation Command Generated

[Summary displayed as in Step 5.2]
```

**Generated File:**
- Path: `{project}/.claude/commands/validate.md`
- Format: HAL-Script command (markdown)
- Size: Typically 10-50 KB depending on project complexity
- Sections: Frontmatter, Overview, 5 Phases, Summary, Troubleshooting, Notes

---

## Error Handling

**Error: Target directory does not exist**
- Detection: Path validation in Phase 0 fails
- Action: ABORT with message: "Directory not found: {path}. Please provide a valid project directory."
- Recovery: User provides correct path

**Error: Target is HAL8000 itself**
- Detection: `project_root` matches `/mnt/d/~HAL8000`
- Action: ABORT with message: "This command is for external projects only. Use /HAL-system-check for HAL8000 validation."
- Recovery: User navigates to different project

**Error: Output location not writable**
- Detection: Directory creation or file write fails
- Action: Try alternative location (`{project_root}/validate.md` in project root)
- If still fails: ABORT with message and suggest user checks permissions

**Error: No documentation found**
- Detection: No README.md or other docs found
- Action: WARN user, continue with limited E2E tests
- Message: "⚠️ No documentation found. E2E tests will be basic. Consider adding README.md with usage examples."

**Error: No development tools detected**
- Detection: No linters, type checkers, formatters, or test frameworks found
- Action: WARN user, generate validation command with TODO placeholders
- Message: "⚠️ No development tools detected. Generated command includes setup recommendations."

**Error: Cannot parse config files**
- Detection: Config file exists but parsing fails (invalid JSON, YAML, TOML)
- Action: WARN user, use default commands for that tool
- Message: "⚠️ Could not parse {config_file}. Using default command for {tool}."

**Error: RAM approaching limits during analysis**
- Detection: RAM_ZONE enters CAUTION during Phase 1 or 2
- Action: Reduce file loading (read only essential files, skip large docs)
- Message: "⚠️ RAM usage high. Limiting file analysis. May need to manually enhance generated validation."

**Validation During Generation:**

After each phase, verify:
- Phase 0: Target exists, output writable
- Phase 1: At least some documentation found (even if minimal)
- Phase 2: At least one language detected
- Phase 3: At least 1 validation phase applicable
- Phase 4: Generated content is not empty
- Phase 5: File was written successfully

If any validation fails, provide clear error message and recovery steps.

---

## Examples

### Example 1: Generate Validation for React + FastAPI Project

**Scenario:** Full-stack web application in `/mnt/d/my-saas-app`

**Execution:**
```bash
cd /mnt/d/my-saas-app
/HAL-validate-generate
```

**What happens:**
1. Analyzes project at `/mnt/d/my-saas-app`
2. Discovers:
   - Frontend: React + TypeScript + Vite + Playwright
   - Backend: Python + FastAPI + PostgreSQL
   - Tools: ESLint, Prettier, mypy, Black, pytest, Jest
   - Docs: README.md with 5 user workflows
3. Generates comprehensive validation with:
   - Frontend linting (ESLint) + Backend linting (Ruff)
   - TypeScript + mypy type checking
   - Prettier + Black formatting
   - Jest + pytest unit tests
   - Playwright E2E tests + API curl tests
   - Database verification
4. Creates `/mnt/d/my-saas-app/.claude/commands/validate.md`
5. File is ~30 KB with 15+ E2E test scenarios

**Output shows:**
```
✅ Validation Command Generated
Location: /mnt/d/my-saas-app/.claude/commands/validate.md
Workflows: 5 (Registration, Login, CRUD, Search, Admin)
Endpoints: 12 API endpoints tested
Database: Yes (PostgreSQL verification included)
```

---

### Example 2: Generate Validation for Go CLI Tool

**Scenario:** Command-line application in `/mnt/d/my-cli-tool`

**Execution:**
```bash
/HAL-validate-generate "/mnt/d/my-cli-tool"
```

**What happens:**
1. Analyzes Go CLI project
2. Discovers:
   - Language: Go
   - Tools: golangci-lint, go test
   - Type: CLI application
   - Docs: README.md with usage examples
3. Generates validation with:
   - Go linting (golangci-lint)
   - Go formatting check (gofmt)
   - Go unit tests (go test -v -cover)
   - CLI workflow tests (bash scripts testing commands)
4. Creates `/mnt/d/my-cli-tool/.claude/commands/validate.md`
5. File includes CLI-specific E2E tests:
   - Installation test
   - Command execution tests
   - Output verification
   - Error handling tests

---

### Example 3: Microservices Project

**Scenario:** Microservices in `/mnt/d/microservices-app` with 4 services

**Execution:**
```bash
cd /mnt/d/microservices-app
/HAL-validate-generate
```

**What happens:**
1. Analyzes microservices project
2. Discovers:
   - Services: API Gateway (Node.js), User Service (Python), Order Service (Go), Payment Service (Python)
   - Docker Compose with 4 services + databases
   - Multiple test frameworks
3. Generates validation with:
   - Per-service linting, type checking, unit tests
   - Service-to-service E2E tests
   - Cross-service workflow validation
   - Database verification for each service
4. File is ~50 KB with complex orchestration tests

---

### Example 4: Mobile App (React Native)

**Scenario:** React Native app in `/mnt/d/mobile-app`

**Execution:**
```bash
/HAL-validate-generate "/mnt/d/mobile-app" "/mnt/d/mobile-app/.claude/commands/validate.md"
```

**What happens:**
1. Analyzes React Native project
2. Discovers:
   - Platform: React Native
   - Languages: TypeScript
   - Tools: ESLint, Jest, Detox
3. Generates validation with:
   - Linting and type checking
   - Unit tests (Jest)
   - Component tests (React Native Testing Library)
   - E2E tests (Detox for iOS/Android simulators)
4. Mobile-specific validations included

---

## Dependencies

**Required Files in HAL8000:**
- This command file (self-contained logic)

**Required Tools/Capabilities:**
- Read tool (file reading)
- Glob tool (file pattern matching)
- Grep tool (content searching, optional)
- Write tool (generating output file)

**External Dependencies (in target project):**
- None for generation (analyzes what's present)
- Generated validation requires project's dev tools to be installed

**Optional Dependencies:**
- Bash tool (for checking directory existence, though can use Read tool for verification)

---

## Performance Considerations

**RAM Usage:**

This command performs extensive file reading and analysis:

**Phase-by-Phase Estimates:**
- Phase 0: ~1K tokens (minimal)
- Phase 1: ~10-30K tokens (reading README, docs)
- Phase 2: ~5-15K tokens (reading config files)
- Phase 3: ~5K tokens (strategy design)
- Phase 4: ~10-20K tokens (generating command content)
- Phase 5: ~2K tokens (verification)

**Total estimated RAM:** 33-73K tokens (16-36% of 200K capacity)

**Peak RAM:** During Phase 1 if documentation is extensive

**RAM Optimization Strategies:**
- Read only first 100 lines of README (use limit parameter)
- Skip reading full docs if >50K total
- Parse config files selectively (only relevant sections)
- Generate output incrementally (build string, don't store in RAM)

**RAM Zone:**
- Expected to stay in SAFE zone (< 80%)
- If approaching CAUTION: Reduce doc analysis depth

**Execution Time:**
- Simple project: ~10-15 seconds (minimal files)
- Medium project: ~20-40 seconds (typical web app)
- Complex project: ~60-120 seconds (microservices, extensive docs)

**Bottlenecks:**
- Reading many documentation files
- Parsing multiple config files
- Generating extensive E2E tests

**Optimization:**
- Use Glob efficiently (single pattern match when possible)
- Read files selectively (check existence first)
- Generate content incrementally

---

## Testing & Validation

**How to test this command:**

**Test 1: Simple React App**
- Create minimal React app with create-react-app
- Run `/HAL-validate-generate`
- Verify validation includes: ESLint, TypeScript, Jest
- Run generated `/validate` and confirm it works

**Test 2: Full-Stack App**
- Use example full-stack repo (React + FastAPI)
- Run `/HAL-validate-generate`
- Verify all 5 phases present
- Verify E2E tests include frontend + backend + database
- Run generated `/validate` and confirm comprehensive coverage

**Test 3: No Tools Detected**
- Create empty project with just source files
- Run `/HAL-validate-generate`
- Verify command generates with warnings and TODOs
- Verify recommendations for adding tools

**Test 4: CLI Application**
- Use Go or Rust CLI project
- Run `/HAL-validate-generate`
- Verify CLI-specific E2E tests generated
- Run generated `/validate` and confirm CLI workflows tested

**Test 5: Microservices**
- Use multi-service Docker Compose project
- Run `/HAL-validate-generate`
- Verify cross-service tests generated
- Verify each service has independent validation

**Validation Checklist:**
- [ ] Generated file exists and is not empty
- [ ] All applicable phases included
- [ ] E2E tests reflect documented workflows
- [ ] Database verification included (if database detected)
- [ ] Error handling tests present
- [ ] Cleanup procedures included
- [ ] Troubleshooting section helpful
- [ ] Generated `/validate` command is runnable

---

## Notes

**Design Rationale:**

This command follows the philosophy from the validation framework at https://github.com/coleam00/context-engineering-intro/tree/main/validation:

1. **Documentation-first E2E testing** - Understand user workflows from docs before analyzing tools
2. **Comprehensive coverage** - "If /validate passes, your app works"
3. **Project-specific generation** - Adapt to whatever tech stack is present
4. **5-phase structure** - Linting → Type Checking → Formatting → Unit Tests → E2E Tests
5. **Database verification** - Not just API tests, verify data persistence
6. **External integration testing** - Test actual external service interactions
7. **Error scenario testing** - Validate proper error handling (400, 401, 403, 404)

**Enhancements over GitHub version:**

1. **HAL-Script format** - Proper command structure for HAL8000
2. **Broader framework support** - More languages, frameworks, tools
3. **Mobile app support** - React Native, Flutter
4. **Microservices support** - Cross-service validation
5. **Explicit RAM management** - Awareness of context limits
6. **Progressive enhancement** - Works even with minimal tool detection
7. **Comprehensive comments** - Every generated test is documented

**Limitations:**

- Cannot test features not documented in README
- Generated E2E tests are based on documentation inference (may need manual refinement)
- External integration tests require API keys/tokens (provided as optional)
- Mobile testing requires simulators/emulators (noted in generated command)

**Future Enhancements:**

- Support for additional frameworks (Laravel, Rails, ASP.NET)
- Integration with CI/CD generation (auto-generate GitHub Actions workflow)
- Performance testing integration (load tests, stress tests)
- Security scanning integration (OWASP ZAP, Snyk)
- Visual regression testing (Percy, Chromatic)

**Maintenance:**

- Update tool detection as new frameworks emerge
- Enhance E2E test generation patterns
- Add more project type templates (mobile, desktop, embedded)

---

## Metadata

**Version History:**
- v1.0 (2025-11-22) - Initial implementation
  - Comprehensive project analysis
  - 5-phase validation generation
  - Support for Frontend, Backend, Full-Stack, Mobile, CLI, Microservices
  - Documentation-driven E2E test generation
  - Database verification
  - External integration testing
  - Error scenario coverage

**Status:** Production
**Template Level:** 6 - Workflow Composition (command generator)
**Inspired by:** https://github.com/coleam00/context-engineering-intro/tree/main/validation
**Author:** HAL8000 System
**Command Category:** Development
**RAM Impact:** Medium (33-73K tokens, ~16-36%)
**Execution Time:** 10-120 seconds depending on project complexity
