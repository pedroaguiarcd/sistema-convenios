import os
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)


def gerar_termo_convenio(convenio):

    pasta_saida = "uploads/termos_gerados"

    os.makedirs(
        pasta_saida,
        exist_ok=True
    )

    caminho_saida = f"{pasta_saida}/termo_{convenio.id}.pdf"

    nome_empresa = convenio.empresa.nome if convenio.empresa else ""
    endereco = convenio.endereco or ""
    cnpj = convenio.cnpj or ""
    responsavel = convenio.responsavel_legal or ""
    telefone = convenio.telefone or ""
    hoje = date.today()

    doc = SimpleDocTemplate(
        caminho_saida,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=45,
        bottomMargin=45
    )

    estilos = getSampleStyleSheet()

    titulo = ParagraphStyle(
        "Titulo",
        parent=estilos["Title"],
        alignment=TA_CENTER,
        fontSize=13,
        spaceAfter=14
    )

    subtitulo = ParagraphStyle(
        "Subtitulo",
        parent=estilos["Heading2"],
        alignment=TA_CENTER,
        fontSize=11,
        spaceAfter=12
    )

    texto = ParagraphStyle(
        "Texto",
        parent=estilos["BodyText"],
        alignment=TA_JUSTIFY,
        fontSize=10,
        leading=14,
        spaceAfter=8
    )

    elementos = []

    elementos.append(
        Paragraph(
            "GOVERNO DO ESTADO DO PIAUÍ<br/>"
            "UNIVERSIDADE ESTADUAL DO PIAUÍ – UESPI<br/>"
            "PRÓ-REITORIA DE EXTENSÃO, ASSUNTOS ESTUDANTIS E COMUNITÁRIOS – PREX",
            titulo
        )
    )

    elementos.append(
        Paragraph(
            "CONVÊNIO DE CONCESSÃO DE ESTÁGIO",
            subtitulo
        )
    )

    elementos.append(Spacer(1, 12))

    elementos.append(
        Paragraph(
            f"Pelo presente instrumento, de um lado o(a) <b>{nome_empresa}</b>, "
            f"situado(a) à <b>{endereco}</b>, inscrito(a) no CNPJ sob o nº "
            f"<b>{cnpj}</b>, neste ato representado(a) por seu Titular "
            f"<b>{responsavel}</b>, telefone <b>{telefone}</b>, doravante denominado "
            "Unidade Concedente do Estágio e, do outro lado a UESPI, aqui representada "
            "pela Pró-reitora de Extensão, Assuntos Estudantis e Comunitários, resolvem "
            "celebrar este Convênio, de conformidade com as cláusulas e condições a seguir estabelecidas:",
            texto
        )
    )

    clausulas = [
        (
            "CLÁUSULA PRIMEIRA – DO OBJETIVO",
            "O presente convênio tem como objetivo estabelecer condições para viabilizar a concessão "
            "de estágio aos discentes da UESPI, visando à complementação do ensino e da aprendizagem, "
            "através de treinamento prático."
        ),
        (
            "CLÁUSULA SEGUNDA – DA FORMALIZAÇÃO DO ESTÁGIO",
            "A formalização do estágio será realizada mediante assinatura do Termo de Compromisso "
            "de Estágio – TCE, pelo estagiário e pela Unidade Concedente, com interveniência obrigatória da UESPI."
        ),
        (
            "CLÁUSULA TERCEIRA – DO VÍNCULO EMPREGATÍCIO",
            "Os estagiários não terão vínculo empregatício com a Unidade Concedente do Estágio, "
            "nos termos da Lei nº 11.788, de 25 de setembro de 2008."
        ),
        (
            "CLÁUSULA QUARTA – DAS OBRIGAÇÕES DA UESPI",
            "Compete à UESPI acompanhar, avaliar e assinar os termos de compromisso de estágio "
            "como parte interveniente, observando os currículos, programas e calendários escolares."
        ),
        (
            "CLÁUSULA QUINTA – DAS OBRIGAÇÕES DA UNIDADE CONCEDENTE DO ESTÁGIO",
            "Compete à Unidade Concedente informar a disponibilidade de vagas, celebrar termo de "
            "compromisso, oferecer condições adequadas ao estágio, efetuar seguro contra acidentes pessoais "
            "e indicar supervisor responsável."
        ),
        (
            "CLÁUSULA SEXTA – DA EXTINÇÃO DO ESTÁGIO",
            "O estágio poderá ser extinto ao término da vigência, a pedido do estagiário, por descumprimento "
            "das condições pactuadas ou por interesse das partes."
        ),
        (
            "CLÁUSULA SÉTIMA – DA VIGÊNCIA DO CONVÊNIO",
            "O prazo de duração deste Convênio será de 05 (cinco) anos, a contar da data de sua assinatura, "
            "podendo ser alterado mediante termo aditivo ou rescindido de comum acordo."
        ),
        (
            "CLÁUSULA OITAVA – DA DURAÇÃO DO ESTÁGIO",
            "Os Termos de Compromisso de Estágio serão firmados com prazo mínimo de 06 (seis) meses "
            "e prazo máximo de 02 (dois) anos."
        ),
        (
            "CLÁUSULA NONA – DAS DISPOSIÇÕES FINAIS",
            "Fica eleito o Foro de Teresina, Capital do Estado do Piauí, para dirimir quaisquer dúvidas "
            "oriundas da interpretação deste Convênio."
        ),
    ]

    for titulo_clausula, corpo in clausulas:

        elementos.append(
            Paragraph(
                f"<b>{titulo_clausula}</b>",
                texto
            )
        )

        elementos.append(
            Paragraph(
                corpo,
                texto
            )
        )

    elementos.append(Spacer(1, 24))

    elementos.append(
        Paragraph(
            f"Teresina – PI, {hoje.day} de {hoje.month} de {hoje.year}.",
            texto
        )
    )

    elementos.append(Spacer(1, 40))

    elementos.append(
        Paragraph(
            "_________________________________________<br/>"
            "Unidade Concedente do Estágio",
            subtitulo
        )
    )

    elementos.append(Spacer(1, 25))

    elementos.append(
        Paragraph(
            "_________________________________________<br/>"
            "Pró-Reitoria de Extensão, Assuntos Estudantis e Comunitários – PREX/UESPI",
            subtitulo
        )
    )

    doc.build(elementos)

    return caminho_saida