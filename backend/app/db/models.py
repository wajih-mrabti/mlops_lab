from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    team_memberships: Mapped[list["TeamMembership"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    created_teams: Mapped[list["Team"]] = relationship(back_populates="creator", foreign_keys="[Team.created_by_user_id]")
    created_projects: Mapped[list["Project"]] = relationship(back_populates="creator", foreign_keys="[Project.created_by_user_id]")
    created_models: Mapped[list["Model"]] = relationship(back_populates="creator", foreign_keys="[Model.created_by_user_id]")
    created_model_versions: Mapped[list["ModelVersion"]] = relationship(
        back_populates="creator",
        foreign_keys="[ModelVersion.created_by_user_id]",
    )
    created_artifacts: Mapped[list["Artifact"]] = relationship(
        back_populates="creator",
        foreign_keys="[Artifact.created_by_user_id]",
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="actor", foreign_keys="[AuditLog.actor_user_id]")


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_user_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", name="fk_teams_created_by_user_id"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    creator: Mapped[User | None] = relationship(back_populates="created_teams")
    team_memberships: Mapped[list["TeamMembership"]] = relationship(back_populates="team", cascade="all, delete-orphan")
    projects: Mapped[list["Project"]] = relationship(back_populates="team", cascade="all, delete-orphan")


class TeamMembership(Base):
    __tablename__ = "team_memberships"
    __table_args__ = (
        UniqueConstraint("team_id", "user_id", name="uq_team_memberships_team_user"),
        Index("ix_team_memberships_team_user", "team_id", "user_id"),
    )

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )
    team_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("teams.id", name="fk_team_memberships_team_id"), nullable=False)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", name="fk_team_memberships_user_id"), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="member")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    team: Mapped[Team] = relationship(back_populates="team_memberships")
    user: Mapped[User] = relationship(back_populates="team_memberships")


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = (
        UniqueConstraint("team_id", "slug", name="uq_projects_team_slug"),
        UniqueConstraint("team_id", "name", name="uq_projects_team_name"),
        Index("ix_projects_team_created_at", "team_id", "created_at"),
    )

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )
    team_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("teams.id", name="fk_projects_team_id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_user_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", name="fk_projects_created_by_user_id"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    team: Mapped[Team] = relationship(back_populates="projects")
    creator: Mapped[User | None] = relationship(back_populates="created_projects")
    models: Mapped[list["Model"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class Model(Base):
    __tablename__ = "models"
    __table_args__ = (
        UniqueConstraint("project_id", "slug", name="uq_models_project_slug"),
        Index("ix_models_project_created_at", "project_id", "created_at"),
    )

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )
    project_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("projects.id", name="fk_models_project_id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    model_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft")
    created_by_user_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", name="fk_models_created_by_user_id"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    project: Mapped[Project] = relationship(back_populates="models")
    creator: Mapped[User | None] = relationship(back_populates="created_models")
    versions: Mapped[list["ModelVersion"]] = relationship(back_populates="model", cascade="all, delete-orphan")


class ModelVersion(Base):
    __tablename__ = "model_versions"
    __table_args__ = (
        UniqueConstraint("model_id", "version_number", name="uq_model_versions_model_version_number"),
        Index("ix_model_versions_model_version_number", "model_id", "version_number"),
    )

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )
    model_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("models.id", name="fk_model_versions_model_id"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft")
    created_by_user_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", name="fk_model_versions_created_by_user_id"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    model: Mapped[Model] = relationship(back_populates="versions")
    creator: Mapped[User | None] = relationship(back_populates="created_model_versions")
    artifacts: Mapped[list["Artifact"]] = relationship(back_populates="model_version", cascade="all, delete-orphan")


class Artifact(Base):
    __tablename__ = "artifacts"
    __table_args__ = (
        UniqueConstraint("model_version_id", "storage_key", name="uq_artifacts_model_version_storage_key"),
        Index("ix_artifacts_model_version_created_at", "model_version_id", "created_at"),
        Index("ix_artifacts_checksum_sha256", "checksum_sha256"),
    )

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )
    model_version_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("model_versions.id", name="fk_artifacts_model_version_id"), nullable=False)
    storage_provider: Mapped[str] = mapped_column(String(50), nullable=False, default="local")
    storage_key: Mapped[str] = mapped_column(String(1024), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    size_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    checksum_sha256: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_by_user_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", name="fk_artifacts_created_by_user_id"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    model_version: Mapped[ModelVersion] = relationship(back_populates="artifacts")
    creator: Mapped[User | None] = relationship(back_populates="created_artifacts")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )
    actor_user_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", name="fk_audit_logs_actor_user_id"),
        nullable=True,
    )
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(255), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    details_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    actor: Mapped[User | None] = relationship(back_populates="audit_logs")


__all__ = [
    "Artifact",
    "AuditLog",
    "Model",
    "ModelVersion",
    "Project",
    "Team",
    "TeamMembership",
    "User",
]
