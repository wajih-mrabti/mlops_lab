# ModelOps Lab Backend Architecture Proposal

## 1. Purpose and scope

This document proposes a backend architecture for ModelOps Lab, a multi-user MLOps platform for managing the machine learning lifecycle. It is intentionally design-only and does not implement backend code or database services.

This proposal reflects the current repository state:

- the frontend is a Next.js App Router application in TypeScript and Tailwind CSS;
- the dashboard routes are placeholder pages, not yet connected to a backend;
- no database, API layer, or artifact-storage system exists yet;
- the product vision is team-oriented and includes model registration, versioning, deployment, monitoring, and collaboration.

This proposal distinguishes:

- initial requirements: the first small, testable registry slice;
- future capabilities: broader platform features that should not be forced into v1;
- design decisions and assumptions: choices that are intentionally proposed for evaluation, not claims of implementation details.

## 2. System context and component responsibilities

### 2.1 System context

ModelOps Lab is designed for teams to manage machine learning assets across the lifecycle. The first usable slice should support a small but meaningful set of workflows:

- create a project;
- register a model;
- register a new model version;
- list models and their versions;
- view model and artifact metadata;
- enforce team-scoped access control.

The frontend remains the Next.js application already in this repository. The backend architecture uses a separate Python service layer implemented with FastAPI. Persistent relational metadata is stored in PostgreSQL. Model binaries and package files are stored using a local filesystem-backed abstraction in the first phase, with a clear boundary for future cloud/object storage providers.

### 2.2 Proposed component responsibilities

#### Frontend (Next.js + TypeScript)

Responsibilities:

- render the existing dashboard shell and feature pages;
- authenticate users or obtain an authenticated session;
- call backend APIs through a small typed client;
- render model and project metadata in the dashboard;
- remain decoupled from persistence architecture.

Current status:

- frontend app structure is present and build-valid;
- pages are mostly static placeholders;
- no backend API contract or data integration is in place.

#### API layer (FastAPI)

Responsibilities:

- expose REST endpoints described in this document;
- validate request payloads and enforce schema constraints;
- perform project/team authorization checks;
- coordinate model registration, version creation, and artifact metadata persistence;
- return structured responses and consistent error codes.

Initial scope:

- project creation and membership;
- model registry and versioning;
- artifact metadata and checksums;
- authorization and audit log records.

Not in the initial slice:

- asynchronous training jobs;
- deployment orchestration;
- drift monitoring and alerting;
- multi-service background workers.

#### Database layer (PostgreSQL)

Responsibilities:

- persist users, teams, projects, models, versions, artifacts, and audit records;
- enforce uniqueness and referential integrity;
- support transactional creation of model versions and artifact metadata;
- support team-scoped queries and authorization checks.

#### Artifact storage abstraction

Responsibilities:

- store uploaded model packages or files behind a storage interface;
- generate storage keys instead of trusting client-provided paths;
- store artifact metadata separately from binary data;
- replace filesystem storage with cloud/object storage later without changing core app logic.

Initial implementation direction:

- local development filesystem storage behind an interface such as `ArtifactStorage`;
- later replace the storage backend behind the same interface.

#### Future async ML execution

Responsibilities:

- run training jobs, evaluation jobs, and deployment workflows asynchronously;
- decouple long-running work from synchronous API calls;
- provide queue tracking and monitoring.

This is future work and should not be required for the initial registry slice.

## 3. Proposed architecture diagram

```mermaid
flowchart LR
    User[User / Team Member] --> FE[Next.js Frontend
App Router + Tailwind]
    FE --> API[FastAPI Backend
REST API for projects, models, versions, artifacts]
    API --> DB[(PostgreSQL
Users / Teams / Projects / Models / Versions / Artifacts / Audit)]
    API --> ART[Artifact Storage
Local filesystem abstraction
Later cloud/object storage]
    API --> FUT[Future Async ML Execution
Training / evaluation / deployment jobs]
    FUT --> DB
    FUT --> ART

    FE -. typed client .-> API
    API -. audit events .-> DB
    API -. artifact metadata .-> DB
```

## 4. Relational data model

This section describes the proposed first-release schema. It is not a claim that this schema already exists in the repository.

### 4.1 Core principles

- team and project ownership are first-class concepts;
- all project-scoped APIs are authorized against team membership and project access;
- model versions are immutable once created;
- artifact metadata is persisted separately from binary storage;
- the first schema is intentionally narrow and only includes data needed for the registry slice.

### 4.2 Initial entities for the registry slice

#### `users`

Key fields:

- `id` (UUID primary key)
- `email` (unique)
- `display_name`
- `password_hash` or external identity reference
- `is_active`
- `created_at`
- `last_login_at`

Purpose:

- identity and authentication anchor.

#### `teams`

Key fields:

- `id` (UUID primary key)
- `name`
- `slug` (unique)
- `description`
- `created_by_user_id`
- `created_at`

Purpose:

- collaboration boundary for users and projects.

#### `team_memberships`

Key fields:

- `id` (UUID primary key)
- `team_id` (FK)
- `user_id` (FK)
- `role` (`owner`, `admin`, `member`, `viewer`)
- `created_at`

Constraints:

- unique `(team_id, user_id)`

Purpose:

- map users to teams and their permissions.

#### `projects`

Key fields:

- `id` (UUID primary key)
- `team_id` (FK)
- `name`
- `slug`
- `description`
- `created_by_user_id`
- `created_at`

Constraints:

- unique `(team_id, slug)`
- unique `(team_id, name)` or a validated internal slug model depending on UX requirements

Purpose:

- project-level container for one team’s model assets.

#### `models`

Key fields:

- `id` (UUID primary key)
- `project_id` (FK)
- `name`
- `slug`
- `description`
- `model_type`
- `status`
- `created_by_user_id`
- `created_at`
- `updated_at`

Constraints:

- unique `(project_id, slug)`
- index on `(project_id, created_at DESC)`

Purpose:

- top-level model catalog entry within a project.

#### `model_versions`

Key fields:

- `id` (UUID primary key)
- `model_id` (FK)
- `version_number` (integer, starting at 1)
- `status` (`draft`, `registered`, `archived`)
- `created_by_user_id`
- `created_at`
- `updated_at`
- `metadata_json`
- `notes`

Constraints:

- unique `(model_id, version_number)`
- index on `(model_id, version_number DESC)`

Purpose:

- immutable version identity for a model. This is the authoritative version number. Tags such as `candidate` or `production` are metadata labels and must not replace the immutable version identity.

#### `artifacts`

Key fields:

- `id` (UUID primary key)
- `model_version_id` (FK)
- `storage_provider` (`local` for v1)
- `storage_key` (generated, not user supplied)
- `original_filename`
- `content_type`
- `size_bytes`
- `checksum_sha256`
- `created_by_user_id`
- `created_at`

Constraints:

- unique on `(model_version_id, storage_key)` if the same artifact path is not allowed more than once
- index on `(model_version_id, created_at DESC)`
- index on `(checksum_sha256)` for integrity checks and deduplication review

Purpose:

- stores artifact metadata and checksum for a specific model version. Each artifact is always linked to a version, and each version may have many artifacts.

#### `audit_logs`

Key fields:

- `id` (UUID primary key)
- `actor_user_id` (nullable if anonymous/unknown)
- `entity_type`
- `entity_id`
- `action`
- `details_json`
- `created_at`

Purpose:

- audit trail for key changes and authorized actions.

### 4.3 Relationship model

The artifact relationship should be consistent and simple:

- one `team` has many `projects`.
- one `project` has many `models`.
- one `model` has many `model_versions`.
- one `model_version` has many `artifacts`.
- one `user` may belong to many teams via `team_memberships`.
- one `user` may create many projects, models, versions, artifacts, and audit log entries.

This removes the design ambiguity of a reverse foreign key on `model_versions` and keeps artifact ownership clear: artifacts belong to a version, and a version is the natural root for artifact lineage.

### 4.4 Recommended initial database constraints and indexes

Required for the v1 registry slice:

- `UNIQUE (team_id, slug)` on `projects`
- `UNIQUE (project_id, slug)` on `models`
- `UNIQUE (model_id, version_number)` on `model_versions`
- `UNIQUE (team_id, user_id)` on `team_memberships`
- index on `projects(team_id, created_at DESC)`
- index on `models(project_id, created_at DESC)`
- index on `model_versions(model_id, version_number DESC)`
- index on `artifacts(model_version_id, created_at DESC)`
- index on `artifacts(checksum_sha256)`
- foreign keys on all project-scoped tables to enforce valid ownership chains

Future entities such as `deployments`, `experiments`, `monitoring_events`, and related jobs should be added only after the registry is stable and tested.

### 4.5 Tenant and team isolation

Initial design should enforce these principles:

- a project belongs to exactly one team;
- a model belongs to exactly one project;
- a model version belongs to exactly one model;
- an artifact belongs to exactly one model version;
- all project-scoped reads and writes must resolve the user’s team membership before accessing the project.

The system should never allow a user to fetch or mutate a resource outside their team unless they are explicitly invited and the project membership is validated.

## 5. Proposed REST API endpoints

The endpoint naming below is intentionally consistent and versioned.

### 5.1 Projects

- `POST /api/v1/projects`
  - create a project in a team; returns project metadata
- `GET /api/v1/projects`
  - list projects visible to the current user
- `GET /api/v1/projects/{project_id}`
  - fetch one project
- `PATCH /api/v1/projects/{project_id}`
  - update project metadata

### 5.2 Models

- `POST /api/v1/projects/{project_id}/models`
  - create a model within a project
- `GET /api/v1/projects/{project_id}/models`
  - list models within a project, with pagination
- `GET /api/v1/projects/{project_id}/models/{model_id}`
  - fetch one model and latest metadata
- `PATCH /api/v1/projects/{project_id}/models/{model_id}`
  - update model metadata or state

### 5.3 Model versions

- `POST /api/v1/projects/{project_id}/models/{model_id}/versions`
  - create a new version for a model
- `GET /api/v1/projects/{project_id}/models/{model_id}/versions`
  - list versions for a model
- `GET /api/v1/projects/{project_id}/models/{model_id}/versions/{version_id}`
  - fetch one version

### 5.4 Artifacts

- `POST /api/v1/projects/{project_id}/models/{model_id}/versions/{version_id}/artifacts`
  - register artifact metadata after upload completes
- `GET /api/v1/projects/{project_id}/models/{model_id}/versions/{version_id}/artifacts`
  - list artifacts for a version
- `GET /api/v1/projects/{project_id}/models/{model_id}/versions/{version_id}/artifacts/{artifact_id}`
  - fetch a single artifact record

### 5.5 Users, teams, and memberships

- `GET /api/v1/users/me`
  - current user profile
- `GET /api/v1/teams`
  - list teams visible to the user
- `POST /api/v1/teams`
  - create a team
- `GET /api/v1/teams/{team_id}/members`
  - list team members

### 5.6 Pagination conventions

List endpoints should support:

- `page` integer, default `1`
- `page_size` integer, default `20`, max `100`
- response envelope:

```json
{
  "items": [],
  "page": 1,
  "page_size": 20,
  "total": 0,
  "has_more": false
}
```

This keeps the API consistent and scalable before larger dataset queries are required.

## 6. Model registration and versioning workflow

The initial vertical slice should be built around a real, testable model registry flow.

### 6.1 Initial workflow

1. a user creates a project in a team;
2. the user registers a model in that project;
3. the system validates project membership and uniqueness of the model slug;
4. the user registers a new model version;
5. the system assigns the next integer `version_number` for that model;
6. the system creates artifact metadata after validation and upload completion;
7. the model version becomes queryable and listable through the API.

### 6.2 Versioning rules

This proposal intentionally chooses integer version numbers for the initial implementation.

- each model has a monotonic integer sequence starting at `1`;
- the database enforces uniqueness on `(model_id, version_number)`;
- tags such as `candidate`, `staging`, and `production` are labels or deployment states, not the source of identity;
- immutable version identity stays in the integer value, not in the tag.

Example:

- `model_id = 42`
- `version_number = 1` is the first immutable version
- `version_number = 2` is the next immutable version
- `candidate` and `production` may be applied as a tag or status field, but they are not substitutes for the integer version number

### 6.3 Concurrency-safe version creation

To avoid duplicate version numbers during concurrent writes:

- the API should create a model version inside a transaction;
- the service should lock the corresponding `models` row or use a dedicated version-sequence strategy within the same transaction;
- PostgreSQL should enforce the unique constraint on `(model_id, version_number)` as the final integrity check.

The recommended flow is:

1. begin transaction;
2. `SELECT ... FOR UPDATE` on the target `models` row;
3. compute the next available integer from the model’s current version state;
4. insert the new `model_versions` row with the unique `(model_id, version_number)` key;
5. if the insert conflicts, retry or return a conflict error;
6. commit the transaction.

This prevents two simultaneous requests from assigning the same number to the same model.

### 6.4 Artifact upload and metadata creation

Artifact handling should be consistent and explicit:

- the client uploads the file to a temporary staging area or directly to the storage layer via an upload API;
- the backend generates a storage key based on a deterministic path pattern rather than trusting the user-supplied filename or path;
- the backend computes checksum metadata (for example SHA-256);
- the backend stores artifact metadata in the `artifacts` table linked to the specific `model_version_id`;
- the backend records a successful registration only after both storage and metadata persistence succeed.

Example artifact key generation pattern:

```text
projects/{project_id}/models/{model_id}/versions/{version_number}/{uuid}-{sanitized_original_filename}
```

This makes the storage layout predictable and prevents path traversal or malicious path injection.

### 6.5 Model metadata examples

Example project creation:

```json
{
  "team_id": "11111111-1111-1111-1111-111111111111",
  "name": "Demand Forecasting",
  "description": "Customer load forecasting for the operations team"
}
```

Example model registration:

```json
{
  "name": "electricity-forecast-model",
  "description": "Forecasting model for electricity demand.",
  "model_type": "forecasting",
  "status": "draft"
}
```

Example model version creation:

```json
{
  "version_number": 1,
  "status": "registered",
  "metadata_json": {
    "framework": "scikit-learn",
    "training_dataset": "electricity_2024_q1"
  },
  "notes": "Initial registry entry for the model."
}
```

Example artifact registration:

```json
{
  "storage_provider": "local",
  "original_filename": "electricity_model_v1.joblib",
  "content_type": "application/octet-stream",
  "size_bytes": 412500,
  "checksum_sha256": "abc123...",
  "storage_key": "projects/111/.../electricity_model_v1.joblib"
}
```

## 7. Authentication and authorization design

### 7.1 Identity and local development model

The initial system should support two modes clearly separated in policy:

- local development: a minimal shortcut for bootstrapping the application in developer environments; this may include auto-provisioning a default user and a default team for local testing;
- production: secure identity provider or password-based auth with hashed credentials, short-lived tokens, and stronger session controls.

Important distinction:

- local-development shortcuts are convenience tools for developer setup only;
- they must never be mistaken for production-grade authentication and must be disabled or heavily restricted in non-local environments.

### 7.2 Initial access-check flow for every project-scoped endpoint

Every project-scoped endpoint should follow the same sequence:

1. authenticate the request and resolve the current user;
2. resolve the target project by ID;
3. resolve the project’s team by `project.team_id`;
4. verify the current user has a valid record in `team_memberships` for that team;
5. verify the membership role is sufficient for the requested action;
6. reject access if the project is not in the user’s team or if the membership is absent.

Pseudo-flow:

```text
user -> authenticated?
  -> yes
  -> project exists?
  -> project.team_id -> user has team_membership for that team?
  -> role includes action permission?
  -> permit
  -> else 403
```

This prevents unauthorized cross-team access even if the user guesses a valid project ID.

### 7.3 Minimal role policy

Initial role policy should be intentionally small:

- `owner`: full access to team/project administration and model registry management
- `admin`: can manage project metadata and model resources
- `member`: can create and update models and versions within the project
- `viewer`: read-only access to project contents

Recommended initial rule:

- read operations require membership and project visibility;
- write operations require a role of at least `member`;
- admin-only operations may include membership approvals, project rename, or archival policies.

This is enough for v1 without overengineering role semantics.

### 7.4 Local development provisioning

For local development, a minimal bootstrap flow is acceptable:

- create a default team, for example `local-dev-team`;
- create a default user, for example `dev@example.local`;
- create a default project, for example `demo-project`;
- add the default user to the team with `owner` role;
- allow environment-controlled developer bypass only when `APP_ENV=development`.

This is a local convenience and should never be allowed in production or shared environments.

### 7.5 Production auth design

Production authentication should use a secure and explicit mechanism such as:

- password-hash based auth with secure sessions or tokens;
- external identity provider integration if later required;
- short-lived tokens and refresh flows when appropriate;
- role checks enforced server-side, not in the frontend.

## 8. Error handling, validation, logging, auditability, and basic security

### 8.1 Error response contract

All API endpoints should return a consistent error envelope:

```json
{
  "error": {
    "code": "MODEL_VERSION_EXISTS",
    "message": "A model version with this identifier already exists.",
    "details": {
      "model_id": "uuid",
      "version_number": 2
    }
  }
}
```

Recommended status codes:

- `400` invalid request
- `401` unauthenticated
- `403` forbidden
- `404` not found
- `409` conflict
- `422` validation error
- `500` unexpected server error

### 8.2 Input validation

Validation should happen at the API boundary using explicit schemas. The first registry slice should validate:

- required project, model, and version fields;
- allowed status values;
- duplicate slug or duplicate version numbers;
- upload size and MIME constraints;
- checksum format and content-length consistency.

### 8.3 Logging and auditability

The API should log:

- request path and method;
- status code and error code;
- correlation ID;
- acting user ID when present;
- object-level actions such as project created, model registered, version created, artifact uploaded.

Audit logs should persist key actions in the database so they can be reviewed later.

### 8.4 Security requirements

- all secrets must come from environment variables and never be committed;
- uploaded files must not be executed automatically during registration;
- file upload paths must be generated by the server, not accepted from the client;
- storage paths must be normalized and checked to prevent path traversal;
- content type and file extension should be validated as part of the artifact contract;
- upload limits must be enforced in both API and storage layers;
- artifact registration should fail safely if the database transaction fails after storage success, leaving an explicit cleanup or retry strategy.

### 8.5 Failure and cleanup behavior

If file storage succeeds but the database transaction fails:

- the service should clean up the uploaded file if the artifact record was not committed;
- an audit log should be written or a retry idempotency marker should be considered;
- the API should return a failure response rather than leaving an orphaned artifact record;
- this should be treated as a transactional-outbox or cleanup problem, not as an excuse to accept partial success.

This is especially important for version registration and artifact metadata creation, which must stay consistent.

### 8.6 Uploaded model code is never executed automatically

This is a critical design requirement:

- uploaded model files are treated as artifacts for storage and metadata tracking;
- they are not automatically imported or executed during registration;
- execution must happen only in a controlled future workflow behind explicit job orchestration.

This reduces security risk and keeps the initial registry implementation focused on safe metadata and artifact management.

## 9. Frontend-to-backend integration through a typed API client

The frontend should not scatter raw fetch logic across pages. The recommended pattern is a small typed client centered on a few domain operations.

### 9.1 Representative client shape

```ts
// conceptual only; not implemented
export interface ProjectSummary {
  id: string;
  name: string;
  team_id: string;
  slug: string;
}

export interface ModelSummary {
  id: string;
  project_id: string;
  name: string;
  slug: string;
  status: string;
}

export const api = {
  projects: {
    list: (params?: { page?: number; page_size?: number }) => Promise<{ items: ProjectSummary[]; page: number; page_size: number; total: number; has_more: boolean }>;
    create: (input: { team_id: string; name: string; description?: string }) => Promise<ProjectSummary>;
  },
  models: {
    list: (projectId: string, params?: { page?: number; page_size?: number }) => Promise<{ items: ModelSummary[]; page: number; page_size: number; total: number; has_more: boolean }>;
    get: (projectId: string, modelId: string) => Promise<ModelSummary & { versions: unknown[] }>;
    create: (projectId: string, input: { name: string; description?: string; model_type: string; status?: string }) => Promise<ModelSummary>;
  },
  versions: {
    create: (projectId: string, modelId: string, input: { version_number?: number; status?: string; metadata_json?: Record<string, unknown>; notes?: string }) => Promise<{ id: string; model_id: string; version_number: number; status: string }>;
  },
  artifacts: {
    create: (projectId: string, modelId: string, versionId: string, input: { original_filename: string; content_type: string; size_bytes: number; checksum_sha256: string; storage_key: string }) => Promise<{ id: string; model_version_id: string }>;
  }
};
```

### 9.2 Client design goals

- strict request/response typing;
- centralized API URL and auth configuration;
- consistent parsing of API error payloads;
- support for pagination and future auth/session tokens;
- minimal duplication across pages.

## 10. Phased implementation plan

### Phase 0: project scaffolding and schema foundation

- define FastAPI app structure and modules;
- define PostgreSQL schema for the initial registry domain;
- configure environment variables and local dev settings;
- add Alembic migration setup and a first migration for registry tables;
- implement the storage abstraction interface and local filesystem backend.

### Phase 1: model registry vertical slice (priority)

This is the first functional slice and should be treated as a meaningful product increment.

Requirements:

- create a project;
- register a model with metadata;
- list models for a project;
- view a model’s details;
- create a new version for the model;
- store artifact metadata and checksum;
- ensure the user can only access the project’s own data.

This phase should stay narrow and production-sensible before broader MLOps features are introduced.

### Phase 2: team membership and governance

- refine membership invitations and permission policies;
- add project ownership and admin flows;
- add stronger project-level access enforcement and audit review.

### Phase 3: deployment and release workflow

- add deployment records and environment targeting;
- add release history and rollback capabilities;
- keep this separate from model registration until the registry is stable.

### Phase 4: experiments and observability

- introduce experiments and evaluation jobs;
- add metrics tracking and monitoring endpoints;
- add async execution and job status tracking.

### Phase 5: cloud readiness

- swap local filesystem storage for cloud object storage behind the same abstraction;
- plan managed PostgreSQL, queueing, and infrastructure automation.

## 11. Database migration workflow and schema governance

The initial registry should be implemented with a simple but disciplined migration workflow using Alembic.

Suggested process:

- create a migration for each logical schema change;
- keep migrations small and reviewable;
- version the schema in the backend project, not the frontend;
- require database constraints and indexes to be part of the migration, not only application code;
- maintain migration-based schema history for local development and QA environments.

Recommended ID choice:

- use `UUID` for public API identifiers across the initial registry slice;
- this keeps identifiers portable across services and avoids database-sequence assumptions in clients;
- it is also easier to reason about for cross-service references and future API integrations.

This is a design decision and may be revisited if product requirements strongly favor integer IDs for easier user-facing display.

## 12. Testing strategy

### 12.1 Unit tests

- validation of project request payloads;
- validation of model and version payloads;
- checksum generation and integrity checks;
- authorization policy checks;
- artifact key generation and sanitization tests.

### 12.2 Integration tests

- register a project and a model;
- create and list versions;
- create artifact metadata and verify checksum values;
- reject duplicate model versions for the same model;
- verify permissions across team boundaries.

### 12.3 Security-focused tests

- cross-team isolation: a user cannot read or mutate another team’s project;
- invalid upload tests: too large, invalid MIME, path traversal attempts, malformed metadata;
- checksum mismatch tests: report a failure if the stored checksum does not match content;
- cleanup-after-failure tests: file upload succeeds but DB save fails; ensure cleanup behavior is defined and enforced.

### 12.4 API contract tests

- verify request and response shapes for creation and listing endpoints;
- assert consistent error structure across failures;
- verify pagination metadata on list endpoints.

### 12.5 Testing focus for the first slice

The most important regression tests for v1 are:

- cross-team isolation;
- duplicate version numbers;
- path traversal or malicious artifact key input;
- checksum verification for uploaded artifacts;
- cleanup after failed registration.

## 13. Configuration and environment variables

Recommended development configuration:

```env
APP_ENV=development
API_HOST=0.0.0.0
API_PORT=8000
DATABASE_URL=postgresql://user:password@localhost:5432/modelops_lab
ARTIFACT_STORAGE_PATH=./storage/artifacts
SECRET_KEY=change-me-in-production
ALGORITHM=HS256
ACCESS_TOKEN_TTL_MINUTES=60
LOG_LEVEL=INFO
MAX_UPLOAD_SIZE_BYTES=52428800
```

Design notes:

- keep secrets and environment-specific values outside source control;
- use a local `.env` file for developer setup and exclude it from version control;
- provide a `.env.example` file for documented defaults without committing secrets.

## 14. Windows-friendly local development approach

A Linux-first backend is possible, but the initial environment should be practical for Windows developers.

Recommended local development approach:

- use Docker Desktop or a local PostgreSQL instance with port mapping;
- keep artifact files in a repo-local or user-local directory during development;
- run FastAPI in a Python virtual environment;
- use environment variables from a local `.env` file excluded from source control;
- keep startup scripts small and explicit for API service startup and database health checks.

This keeps the stack accessible and easier to adopt while preserving a clean path to cloud deployment later.

## 15. Initial requirements vs future capabilities

### Initial requirements

- team-aware project organization;
- model registry with metadata and immutable version numbers;
- artifact metadata and checksum tracking;
- basic project-scoped authorization;
- audit logging for key actions;
- local artifact storage behind an abstraction;
- backend contract that can be consumed by the Next.js frontend;
- a migration-based database workflow.

### Future capabilities

- async training and evaluation jobs;
- deployment orchestration and rollback workflows;
- monitoring, drift detection, and alerting;
- broader role policies and fine-grained authorization;
- cloud object storage and managed infrastructure;
- advanced collaboration and external identity provider integration;
- queue-based ML execution pipelines.

## 16. Key design decisions and assumptions

This proposal intentionally makes the following choices explicit:

- FastAPI and PostgreSQL are proposed technologies, not current implementation details.
- Local filesystem storage is the first supported artifact backend behind an abstraction.
- UUIDs are recommended for primary keys in the initial version for portability and safety across app boundaries.
- The initial registry slice is intentionally limited to project, model, version, artifact, team, and audit data.
- Integer version numbers are the initial version identity; tags are metadata labels, not authoritative identity.
- Local-development auth shortcuts are allowed for bootstrap convenience only and must not be treated as production security.

## 17. Summary

The current frontend is structurally ready for backend integration, but it is still a placeholder shell. The next value-adding step is not a broad platform redesign; it is a disciplined backend architecture for a small, testable model-registry slice.

This design keeps the product aligned with the existing Next.js frontend while staying deliberately narrow: project creation, model registration, versioning, artifact metadata, checksum validation, and team-scoped authorization. It leaves future ML execution, deployment, monitoring, and cloud readiness for later phases without prematurely building a large system that the current product does not yet require.
