class Config:
    SQLALCHEMY_DATABASE_URI = (
      "mysql+pymysql://convenios_user:123456@localhost/convenios_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False