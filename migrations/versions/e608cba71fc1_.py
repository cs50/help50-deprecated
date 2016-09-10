"""empty message

Revision ID: e608cba71fc1
Revises: 3b25e13c81bf
Create Date: 2016-09-10 13:56:11.228559

"""

# revision identifiers, used by Alembic.
revision = 'e608cba71fc1'
down_revision = '3b25e13c81bf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # http://stackoverflow.com/a/28369544
    conn = op.get_bind()
    conn.execute(sa.sql.text('ALTER TABLE alembic_version CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci'))
    conn.execute(sa.sql.text('ALTER TABLE inputs CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci'))
    conn.execute(sa.sql.text('ALTER TABLE outputs CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci'))
    op.create_index(op.f('ix_inputs_reviewed'), 'inputs', ['reviewed'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_inputs_reviewed'), table_name='inputs')
