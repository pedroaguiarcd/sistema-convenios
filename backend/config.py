class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://pedro:123456@localhost/convenios_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False