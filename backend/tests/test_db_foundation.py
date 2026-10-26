from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base
from app.db.models import Artifact, AuditLog, Model, ModelVersion, Project, Team, TeamMembership, User

EXPECTED_TABLES = {
    "users",
    "teams",
    "team_memberships",
    "projects",
    "models",
    "model_versions",
    "artifacts",
    "audit_logs",
}


def _unique_constraint_names(table_name: str) -> set[str]:
    table = Base.metadata.tables[table_name]
    return {
        str(constraint.name)
        for constraint in table.constraints
        if isinstance(constraint, UniqueConstraint)
    }


def _index_names(table_name: str) -> set[str]:
    table = Base.metadata.tables[table_name]
    return {index.name for index in table.indexes if index.name is not None}


def test_database_foundation_registers_all_required_tables() -> None:
    table_names = set(Base.metadata.tables)

    assert EXPECTED_TABLES.issubset(table_names)

    users_table = Base.metadata.tables["users"]
    teams_table = Base.metadata.tables["teams"]
    memberships_table = Base.metadata.tables["team_memberships"]
    projects_table = Base.metadata.tables["projects"]
    models_table = Base.metadata.tables["models"]
    model_versions_table = Base.metadata.tables["model_versions"]
    artifacts_table = Base.metadata.tables["artifacts"]
    audit_logs_table = Base.metadata.tables["audit_logs"]

    for table in [users_table, teams_table, memberships_table, projects_table, models_table, model_versions_table, artifacts_table, audit_logs_table]:
        assert "id" in table.columns
        assert table.primary_key.columns.keys() == ["id"]
        assert isinstance(table.columns["id"].type, UUID)
        assert table.columns["id"].nullable is False

    assert users_table.columns["email"].nullable is False
    assert users_table.columns["display_name"].nullable is False
    assert users_table.columns["is_active"].nullable is False
    assert users_table.columns["created_at"].nullable is False
    assert users_table.columns["password_hash"].nullable is True
    assert users_table.columns["email"].unique is True

    assert teams_table.columns["name"].nullable is False
    assert teams_table.columns["slug"].nullable is False
    assert teams_table.columns["created_at"].nullable is False
    assert teams_table.columns["slug"].unique is True

    assert memberships_table.columns["team_id"].nullable is False
    assert memberships_table.columns["user_id"].nullable is False
    assert memberships_table.columns["role"].nullable is False
    assert memberships_table.columns["created_at"].nullable is False
    assert any(
        {column.name for column in constraint.columns} == {"team_id", "user_id"}
        for constraint in memberships_table.constraints
        if hasattr(constraint, "columns")
    )

    assert projects_table.columns["team_id"].nullable is False
    assert projects_table.columns["name"].nullable is False
    assert projects_table.columns["slug"].nullable is False
    assert projects_table.columns["created_at"].nullable is False
    assert any(
        {column.name for column in constraint.columns} == {"team_id", "slug"}
        for constraint in projects_table.constraints
        if hasattr(constraint, "columns")
    )
    assert any(
        {column.name for column in constraint.columns} == {"team_id", "name"}
        for constraint in projects_table.constraints
        if hasattr(constraint, "columns")
    )

    assert models_table.columns["project_id"].nullable is False
    assert models_table.columns["name"].nullable is False
    assert models_table.columns["slug"].nullable is False
    assert models_table.columns["model_type"].nullable is False
    assert models_table.columns["status"].nullable is False
    assert models_table.columns["created_at"].nullable is False
    assert models_table.columns["updated_at"].nullable is False
    assert any(
        {column.name for column in constraint.columns} == {"project_id", "slug"}
        for constraint in models_table.constraints
        if hasattr(constraint, "columns")
    )

    assert model_versions_table.columns["model_id"].nullable is False
    assert model_versions_table.columns["version_number"].nullable is False
    assert model_versions_table.columns["status"].nullable is False
    assert model_versions_table.columns["created_at"].nullable is False
    assert model_versions_table.columns["updated_at"].nullable is False
    assert any(
        {column.name for column in constraint.columns} == {"model_id", "version_number"}
        for constraint in model_versions_table.constraints
        if hasattr(constraint, "columns")
    )

    assert artifacts_table.columns["model_version_id"].nullable is False
    assert artifacts_table.columns["storage_provider"].nullable is False
    assert artifacts_table.columns["storage_key"].nullable is False
    assert artifacts_table.columns["original_filename"].nullable is False
    assert artifacts_table.columns["created_at"].nullable is False
    assert any(
        {column.name for column in constraint.columns} == {"model_version_id", "storage_key"}
        for constraint in artifacts_table.constraints
        if hasattr(constraint, "columns")
    )

    assert audit_logs_table.columns["entity_type"].nullable is False
    assert audit_logs_table.columns["entity_id"].nullable is False
    assert audit_logs_table.columns["action"].nullable is False
    assert audit_logs_table.columns["created_at"].nullable is False
    assert audit_logs_table.columns["actor_user_id"].nullable is True

    assert "uq_team_memberships_team_user" in _unique_constraint_names("team_memberships")
    assert "uq_model_versions_model_version_number" in _unique_constraint_names("model_versions")
    assert "uq_projects_team_slug" in _unique_constraint_names("projects")
    assert "uq_projects_team_name" in _unique_constraint_names("projects")
    assert "uq_models_project_slug" in _unique_constraint_names("models")
    assert "uq_artifacts_model_version_storage_key" in _unique_constraint_names("artifacts")

    assert {"ix_team_memberships_team_user", "ix_projects_team_created_at", "ix_models_project_created_at", "ix_model_versions_model_version_number", "ix_artifacts_model_version_created_at", "ix_artifacts_checksum_sha256"}.issubset(_index_names("team_memberships") | _index_names("projects") | _index_names("models") | _index_names("model_versions") | _index_names("artifacts"))

    assert User.__tablename__ == "users"
    assert Team.__tablename__ == "teams"
    assert TeamMembership.__tablename__ == "team_memberships"
    assert Project.__tablename__ == "projects"
    assert Model.__tablename__ == "models"
    assert ModelVersion.__tablename__ == "model_versions"
    assert Artifact.__tablename__ == "artifacts"
    assert AuditLog.__tablename__ == "audit_logs"


def test_alembic_metadata_includes_all_orm_tables() -> None:
    assert EXPECTED_TABLES.issubset(set(Base.metadata.tables))
    assert len(Base.metadata.tables) >= len(EXPECTED_TABLES)
