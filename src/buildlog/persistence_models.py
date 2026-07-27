"""SQLAlchemy table mappings for BuildLog metadata."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Declarative base for BuildLog persistence tables."""


class ProjectTable(Base):
    """Stored project metadata."""

    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    iterations: Mapped[list[IterationTable]] = relationship(back_populates="project")


class IterationTable(Base):
    """Stored iteration metadata and raw validated input."""

    __tablename__ = "iterations"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    title: Mapped[str] = mapped_column(String(500))
    goal: Mapped[str] = mapped_column(Text)
    context: Mapped[str] = mapped_column(Text)
    problem: Mapped[str] = mapped_column(Text)
    audience: Mapped[str] = mapped_column(Text)
    raw_input_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    project: Mapped[ProjectTable] = relationship(back_populates="iterations")
    runs: Mapped[list[RunTable]] = relationship(back_populates="iteration")


class PromptVersionTable(Base):
    """Stored prompt file metadata."""

    __tablename__ = "prompt_versions"
    __table_args__ = (
        UniqueConstraint(
            "prompt_name",
            "version",
            "content_hash",
            name="uq_prompt_name_version_hash",
        ),
    )

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    prompt_name: Mapped[str] = mapped_column(String(100), index=True)
    version: Mapped[str] = mapped_column(String(50))
    file_path: Mapped[str] = mapped_column(Text)
    content_hash: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class RunTable(Base):
    """Stored pipeline run state and prompt lineage."""

    __tablename__ = "runs"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    iteration_id: Mapped[str] = mapped_column(ForeignKey("iterations.id"), index=True)
    model: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(30), index=True)
    revision_performed: Mapped[bool] = mapped_column(Boolean, default=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    planner_prompt_version_id: Mapped[str] = mapped_column(ForeignKey("prompt_versions.id"))
    writer_prompt_version_id: Mapped[str] = mapped_column(ForeignKey("prompt_versions.id"))
    evaluator_prompt_version_id: Mapped[str] = mapped_column(ForeignKey("prompt_versions.id"))
    reviser_prompt_version_id: Mapped[str] = mapped_column(ForeignKey("prompt_versions.id"))

    iteration: Mapped[IterationTable] = relationship(back_populates="runs")
    artifacts: Mapped[list[ArtifactTable]] = relationship(back_populates="run")
    evaluation: Mapped[EvaluationTable | None] = relationship(back_populates="run")


class ArtifactTable(Base):
    """Stored path and hash for one filesystem artifact."""

    __tablename__ = "artifacts"
    __table_args__ = (
        UniqueConstraint("run_id", "artifact_type", name="uq_artifact_run_type"),
    )

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("runs.id"), index=True)
    artifact_type: Mapped[str] = mapped_column(String(100))
    file_path: Mapped[str] = mapped_column(Text)
    content_hash: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    run: Mapped[RunTable] = relationship(back_populates="artifacts")


class EvaluationTable(Base):
    """Stored evaluation scores and feedback."""

    __tablename__ = "evaluations"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    run_id: Mapped[str] = mapped_column(
        ForeignKey("runs.id"),
        unique=True,
        index=True,
    )
    technical_accuracy: Mapped[int]
    specificity: Mapped[int]
    readability: Mapped[int]
    reader_value: Mapped[int]
    evidence_coverage: Mapped[int]
    feedback_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    run: Mapped[RunTable] = relationship(back_populates="evaluation")
