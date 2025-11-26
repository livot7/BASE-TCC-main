class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://neondb_owner:npg_vqIRaegOyB09@ep-weathered-dew-acld0qqw-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # TODO: Esconder chave secreta
    SECRET_KEY = "dev"
