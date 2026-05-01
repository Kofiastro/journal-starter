from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class AnalysisResponse(BaseModel):
    """Response model for journal entry analysis."""
    entry_id: str = Field(description="ID of the analyzed entry")
    sentiment: str = Field(
        description="Sentiment: positive, negative, or neutral")
    summary: str = Field(description="2 sentence summary of the entry")
    topics: list[str] = Field(
        description="2-4 key topics mentioned in the entry")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when the analysis was created"
    )


class EntryCreate(BaseModel):
    """Model for creating a new journal entry (user input)."""
    work: str = Field(
        min_length=1,
        max_length=256,
        description="What did you work on today?",
        json_schema_extra={
            "example": "Studied FastAPI and built my first API endpoints"}
    )
    struggle: str = Field(
        min_length=1,
        max_length=256,
        description="What's one thing you struggled with today?",
        json_schema_extra={
            "example": "Understanding async/await syntax and when to use it"}
    )
    intention: str = Field(
        min_length=1,
        max_length=256,
        description="What will you study/work on tomorrow?",
        json_schema_extra={
            "example": "Practice PostgreSQL queries and database design"}
    )

    @field_validator("work", "struggle", "intention")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        """Ensure fields are not empty or whitespace-only."""
        if not v or v.isspace():
            raise ValueError("Field cannot be empty or whitespace")
        return v.strip()


class EntryUpdate(BaseModel):
    """Model for updating a journal entry (partial updates supported)."""
    work: str | None = Field(
        None,
        min_length=1,
        max_length=256,
        description="What did you work on today?",
    )
    struggle: str | None = Field(
        None,
        min_length=1,
        max_length=256,
        description="What's one thing you struggled with today?",
    )
    intention: str | None = Field(
        None,
        min_length=1,
        max_length=256,
        description="What will you study/work on tomorrow?",
    )

    @field_validator("work", "struggle", "intention", mode="before")
    @classmethod
    def validate_not_empty_or_none(cls, v: str | None) -> str | None:
        """Ensure fields are not empty/whitespace if provided."""
        if v is None:
            return None
        if not v or v.isspace():
            raise ValueError("Field cannot be empty or whitespace")
        return v.strip()


class Entry(BaseModel):
    # TODO: Add field validation rules
    # TODO: Add custom validators
    # TODO: Add schema versioning
    # TODO: Add data sanitization methods

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for the entry (UUID)."
    )
    work: str = Field(
        ...,
        max_length=256,
        description="What did you work on today?"
    )
    struggle: str = Field(
        ...,
        max_length=256,
        description="What’s one thing you struggled with today?"
    )
    intention: str = Field(
        ...,
        max_length=256,
        description="What will you study/work on tomorrow?"
    )
    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when the entry was created."
    )
    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when the entry was last updated."
    )
