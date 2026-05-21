# seed_convenios_teste.py

from datetime import date, timedelta
from backend.database import criar_app_flask, db
from backend.models.convenio import Convenio

app = criar_app_flask()

with app.app_context():
    c1 = Convenio(
        data_inicio=date.today(),
        data_fim=date.today() + timedelta(days=60),
        status="VIGENTE"
    )

    c2 = Convenio(
        data_inicio=date.today(),
        data_fim=date.today() + timedelta(days=10),
        status="VIGENTE"
    )

    c3 = Convenio(
        data_inicio=date.today() - timedelta(days=100),
        data_fim=date.today() - timedelta(days=1),
        status="VIGENTE"
    )

    db.session.add_all([c1, c2, c3])
    db.session.commit()

    print("Convênios de teste criados.")