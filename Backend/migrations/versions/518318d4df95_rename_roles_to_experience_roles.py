"""rename roles to experience_roles

Revision ID: 518318d4df95
Revises: 5f17238f061b
Create Date: 2026-05-11 13:19:04.942840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '518318d4df95'
down_revision = '5f17238f061b'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Rename the existing roles table → experience_roles
    op.rename_table('roles', 'experience_roles')

    # 2. Rename columns inside the renamed table
    op.alter_column('experience_roles', 'role_name', new_column_name='ex_role_name')
    op.alter_column('experience_roles', 'role_category', new_column_name='ex_role_category')

    # 3. Create the new identity roles table
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('role_name', sa.String(length=50), nullable=False)
    )

    # 4. Create the user_experience_roles association table
    op.create_table(
        'user_experience_roles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('experience_role_id', sa.Integer(), sa.ForeignKey('experience_roles.id'), nullable=False)
    )

    # 5. Update tour_crew foreign key
    with op.batch_alter_table('tour_crew') as batch_op:
        batch_op.drop_constraint(batch_op.f('tour_crew_role_id_fkey'), type_='foreignkey')
        batch_op.drop_column('role_id')
        batch_op.add_column(sa.Column('experience_role_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'experience_roles', ['experience_role_id'], ['id'])

    # 6. Update show_crew foreign key
    with op.batch_alter_table('show_crew') as batch_op:
        batch_op.drop_constraint(batch_op.f('show_crew_role_id_fkey'), type_='foreignkey')
        batch_op.drop_column('role_id')
        batch_op.add_column(sa.Column('experience_role_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'experience_roles', ['experience_role_id'], ['id'])


def downgrade():
    # 1. Revert show_crew
    with op.batch_alter_table('show_crew') as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('experience_role_id')
        batch_op.add_column(sa.Column('role_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(batch_op.f('show_crew_role_id_fkey'), 'roles', ['role_id'], ['id'])

    # 2. Revert tour_crew
    with op.batch_alter_table('tour_crew') as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('experience_role_id')
        batch_op.add_column(sa.Column('role_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(batch_op.f('tour_crew_role_id_fkey'), 'roles', ['role_id'], ['id'])

    # 3. Drop user_experience_roles
    op.drop_table('user_experience_roles')

    # 4. Drop new identity roles table
    op.drop_table('roles')

    # 5. Rename columns back
    op.alter_column('experience_roles', 'ex_role_name', new_column_name='role_name')
    op.alter_column('experience_roles', 'ex_role_category', new_column_name='role_category')

    # 6. Rename table back
    op.rename_table('experience_roles', 'roles')
