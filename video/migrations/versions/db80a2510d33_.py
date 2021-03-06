"""empty message

Revision ID: db80a2510d33
Revises: 
Create Date: 2019-05-24 10:18:21.413709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db80a2510d33'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('addr', sa.String(length=250), nullable=True),
    sa.Column('phone', sa.String(length=10), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('passport', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_client_name'), 'client', ['name'], unique=False)
    op.create_table('film',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('studio', sa.String(length=100), nullable=True),
    sa.Column('year', sa.String(length=4), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('genre', sa.String(length=50), nullable=True),
    sa.Column('nom_count', sa.Integer(), nullable=True),
    sa.Column('fact_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_film_name'), 'film', ['name'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('issuance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('film_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('weeks', sa.Integer(), nullable=True),
    sa.Column('sum', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.ForeignKeyConstraint(['film_id'], ['film.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_issuance_client_id'), 'issuance', ['client_id'], unique=False)
    op.create_index(op.f('ix_issuance_film_id'), 'issuance', ['film_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_issuance_film_id'), table_name='issuance')
    op.drop_index(op.f('ix_issuance_client_id'), table_name='issuance')
    op.drop_table('issuance')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_film_name'), table_name='film')
    op.drop_table('film')
    op.drop_index(op.f('ix_client_name'), table_name='client')
    op.drop_table('client')
    # ### end Alembic commands ###
