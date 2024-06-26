"""Record and Qestion classes

Revision ID: 691fcff55507
Revises: 
Create Date: 2024-04-25 01:08:34.855974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '691fcff55507'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('answer1', sa.String(), nullable=False),
    sa.Column('answer2', sa.String(), nullable=False),
    sa.Column('answer3', sa.String(), nullable=False),
    sa.Column('answer4', sa.String(), nullable=False),
    sa.Column('right_answer', sa.Integer(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('record', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('record')
    op.drop_table('question')
    # ### end Alembic commands ###
