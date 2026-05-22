class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:@localhost/convenios_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False