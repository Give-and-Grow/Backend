"""remove day_id from evaluation

Revision ID: 02185d226d29
Revises: 14ebb2e47dd8
Create Date: 2025-05-20 19:00:23.830132

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '02185d226d29'
down_revision = '14ebb2e47dd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('participant_evaluation', schema=None) as batch_op:
        batch_op.drop_constraint('participant_evaluation_ibfk_1', type_='foreignkey')
        batch_op.drop_column('opportunity_day_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('participant_evaluation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('opportunity_day_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('participant_evaluation_ibfk_1', 'opportunity_day', ['opportunity_day_id'], ['id'])

    # ### end Alembic commands ###
