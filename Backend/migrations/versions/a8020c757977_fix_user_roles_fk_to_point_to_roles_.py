"""Fix user_roles FK to point to roles table

Revision ID: a8020c757977
Revises: 518318d4df95
Create Date: 2026-05-11 14:05:29.890733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8020c757977'
down_revision = '518318d4df95'
branch_labels = None
depends_on = None


def upgrade():
    # Drop the old FK that incorrectly pointed to experience_roles
    with op.batch_alter_table('user_roles') as batch_op:
        batch_op.drop_constraint('user_roles_role_id_fkey', type_='foreignkey')

        # Create the correct FK pointing to roles.id
        batch_op.create_foreign_key(
            'user_roles_role_id_fkey',
            'roles',
            ['role_id'],
            ['id'],
            ondelete='CASCADE'
        )


def downgrade():
    # Restore the old FK if needed
    with op.batch_alter_table('user_roles') as batch_op:
        batch_op.drop_constraint('user_roles_role_id_fkey', type_='foreignkey')

        batch_op.create_foreign_key(
            'user_roles_role_id_fkey',
            'experience_roles',
            ['role_id'],
            ['id'],
            ondelete='CASCADE'
        )
