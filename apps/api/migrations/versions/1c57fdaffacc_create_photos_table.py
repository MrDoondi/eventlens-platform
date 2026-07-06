"""create photos table

Revision ID: 1c57fdaffacc
Revises: cbc2760b8366
Create Date: 2026-07-06 15:31:04.634317

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1c57fdaffacc"
down_revision: Union[str, Sequence[str], None] = "cbc2760b8366"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "photos",
        sa.Column("gallery_id", sa.UUID(), nullable=False),
        sa.Column("uploaded_by", sa.UUID(), nullable=True),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("storage_key", sa.String(length=500), nullable=False),
        sa.Column("thumbnail_key", sa.String(length=500), nullable=True),
        sa.Column("mime_type", sa.String(length=100), nullable=False),
        sa.Column("file_size", sa.Integer(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "uploaded",
                "processing",
                "ready",
                "failed",
                name="photo_status",
            ),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["gallery_id"],
            ["galleries.id"],
            name=op.f("fk_photos_gallery_id_galleries"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["uploaded_by"],
            ["accounts.id"],
            name=op.f("fk_photos_uploaded_by_accounts"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_photos"),
        ),
    )

    op.create_index(
        op.f("ix_photos_gallery_id"),
        "photos",
        ["gallery_id"],
    )

    op.create_index(
        op.f("ix_photos_uploaded_by"),
        "photos",
        ["uploaded_by"],
    )

    op.create_index(
        op.f("ix_photos_status"),
        "photos",
        ["status"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_photos_status"),
        table_name="photos",
    )

    op.drop_index(
        op.f("ix_photos_uploaded_by"),
        table_name="photos",
    )

    op.drop_index(
        op.f("ix_photos_gallery_id"),
        table_name="photos",
    )

    op.drop_table("photos")