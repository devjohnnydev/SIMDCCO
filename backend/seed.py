"""Database seeder - Populate with IMCO and FDAC questions"""
from app.database import SessionLocal, init_db
from app.models.question import Question, QuestionType
from app.models.user import User, UserRole
from app.security import hash_password


# IMCO Questions (88 total) - Organizational Climate
IMCO_QUESTIONS = [
    # Vector: Liderança (Leadership) - Dimension: Apoio (Support)
    {"vector": "Liderança", "dimension": "Apoio", "text": "Meu gestor imediato me apoia nas decisões do dia a dia."},
    {"vector": "Liderança", "dimension": "Apoio", "text": "Sinto que posso contar com meu gestor em situações desafiadoras."},
    {"vector": "Liderança", "dimension": "Apoio", "text": "Meu gestor reconhece meus esforços e conquistas."},
    {"vector": "Liderança", "dimension": "Controle", "text": "Meu gestor estabelece metas claras e alcançáveis."},
    {"vector": "Liderança", "dimension": "Controle", "text": "Recebo feedback construtivo sobre meu desempenho."},
    {"vector": "Liderança", "dimension": "Controle", "text": "As expectativas sobre meu trabalho são bem definidas."},
    {"vector": "Liderança", "dimension": "Coesão", "text": "Meu gestor promove a colaboração entre a equipe."},
    {"vector": "Liderança", "dimension": "Coesão", "text": "Sinto que meu gestor valoriza a união do time."},
    
    # Vector: Comunicação (Communication)
    {"vector": "Comunicação", "dimension": "Apoio", "text": "A comunicação na empresa é clara e transparente."},
    {"vector": "Comunicação", "dimension": "Apoio", "text": "Recebo informações necessárias para realizar meu trabalho."},
    {"vector": "Comunicação", "dimension": "Apoio", "text": "Sinto que posso me expressar livremente na organização."},
    {"vector": "Comunicação", "dimension": "Coesão", "text": "A comunicação entre departamentos funciona bem."},
    {"vector": "Comunicação", "dimension": "Coesão", "text": "Informações importantes são compartilhadas de forma eficaz."},
    {"vector": "Comunicação", "dimension": "Coesão", "text": "Existe diálogo aberto entre lideranças e colaboradores."},
    {"vector": "Comunicação", "dimension": "Controle", "text": "As mudanças organizacionais são comunicadas adequadamente."},
    {"vector": "Comunicação", "dimension": "Controle", "text": "Tenho acesso aos canais de comunicação da empresa."},
    
    # Vector: Integração (Integration)
    {"vector": "Integração", "dimension": "Coesão", "text": "Me sinto parte da equipe."},
    {"vector": "Integração", "dimension": "Coesão", "text": "Tenho bom relacionamento com meus colegas."},
    {"vector": "Integração", "dimension": "Coesão", "text": "Sou bem recebido e incluído nas atividades do time."},
    {"vector": "Integração", "dimension": "Apoio", "text": "Posso contar com o apoio dos colegas quando preciso."},
    {"vector": "Integração", "dimension": "Apoio", "text": "Existe espírito de equipe no meu ambiente de trabalho."},
    {"vector": "Integração", "dimension": "Conforto", "text": "Me sinto confortável no ambiente de trabalho."},
    {"vector": "Integração", "dimension": "Conforto", "text": "O clima entre os colegas é agradável."},
    {"vector": "Integração", "dimension": "Conforto", "text": "Sinto que pertenço a esta organização."},
    
    # Vector: Satisfação (Satisfaction)
    {"vector": "Satisfação", "dimension": "Conforto", "text": "Estou satisfeito com meu trabalho atual."},
    {"vector": "Satisfação", "dimension": "Conforto", "text": "Gosto do que faço na organização."},
    {"vector": "Satisfação", "dimension": "Conforto", "text": "Sinto realização profissional nesta empresa."},
    {"vector": "Satisfação", "dimension": "Apoio", "text": "A empresa valoriza meu trabalho."},
    {"vector": "Satisfação", "dimension": "Apoio", "text": "Sinto orgulho de trabalhar nesta organização."},
    {"vector": "Satisfação", "dimension": "Controle", "text": "Minha remuneração é justa considerando minhas responsabilidades."},
    {"vector": "Satisfação", "dimension": "Controle", "text": "Os benefícios oferecidos atendem minhas necessidades."},
    
    # Vector: Motivação (Motivation)
    {"vector": "Motivação", "dimension": "Apoio", "text": "Sinto-me motivado para trabalhar todos os dias."},
    {"vector": "Motivação", "dimension": "Apoio", "text": "A empresa estimula meu desenvolvimento profissional."},
    {"vector": "Motivação", "dimension": "Apoio", "text": "Vejo oportunidades de crescimento na organização."},
    {"vector": "Motivação", "dimension": "Controle", "text": "Meu trabalho é desafiador de forma positiva."},
    {"vector": "Motivação", "dimension": "Controle", "text": "Tenho autonomia para tomar decisões no meu trabalho."},
    {"vector": "Motivação", "dimension": "Coesão", "text": "Sinto que meu trabalho faz diferença para a empresa."},
    {"vector": "Motivação", "dimension": "Coesão", "text": "Vejo propósito no que realizo."},
    
    # Vector: Conflitos (Conflicts)
    {"vector": "Conflitos", "dimension": "Controle", "text": "Conflitos são resolvidos de forma justa."},
    {"vector": "Conflitos", "dimension": "Controle", "text": "Existe mediação adequada quando surgem problemas."},
    {"vector": "Conflitos", "dimension": "Controle", "text": "Problemas interpessoais são tratados rapidamente."},
    {"vector": "Conflitos", "dimension": "Coesão", "text": "O ambiente é livre de hostilidades."},
    {"vector": "Conflitos", "dimension": "Coesão", "text": "Não há favoritismo na minha equipe."},
    {"vector": "Conflitos", "dimension": "Conforto", "text": "Me sinto seguro para expressar divergências."},
    {"vector": "Conflitos", "dimension": "Conforto", "text": "Não sofro assédio ou intimidação no trabalho."},
    
    # Vector: Objetivos (Goals)
    {"vector": "Objetivos", "dimension": "Controle", "text": "Conheço os objetivos estratégicos da empresa."},
    {"vector": "Objetivos", "dimension": "Controle", "text": "Entendo como meu trabalho contribui para os resultados."},
    {"vector": "Objetivos", "dimension": "Controle", "text": "As metas são realistas e bem planejadas."},
    {"vector": "Objetivos", "dimension": "Coesão", "text": "Todos trabalham alinhados aos mesmos objetivos."},
    {"vector": "Objetivos", "dimension": "Coesão", "text": "Existe clareza sobre o que se espera de cada área."},
    {"vector": "Objetivos", "dimension": "Apoio", "text": "Recebo suporte para atingir minhas metas."},
    {"vector": "Objetivos", "dimension": "Apoio", "text": "Tenho os recursos necessários para cumprir objetivos."},
    
    # Vector: Cooperação (Cooperation)
    {"vector": "Cooperação", "dimension": "Coesão", "text": "As equipes colaboram entre si."},
    {"vector": "Cooperação", "dimension": "Coesão", "text": "Existe trabalho em equipe efetivo."},
    {"vector": "Cooperação", "dimension": "Coesão", "text": "Colegas compartilham conhecimento e experiências."},
    {"vector": "Cooperação", "dimension": "Apoio", "text": "Posso contar com outras áreas quando necessário."},
    {"vector": "Cooperação", "dimension": "Apoio", "text": "A empresa promove a cooperação."},
    {"vector": "Cooperação", "dimension": "Conforto", "text": "O ambiente estimula ajuda mútua."},
    {"vector": "Cooperação", "dimension": "Conforto", "text": "Não há competição prejudicial entre colegas."},
    
    # Vector: Reconhecimento (Recognition)
    {"vector": "Reconhecimento", "dimension": "Apoio", "text": "Meu trabalho é reconhecido pela liderança."},
    {"vector": "Reconhecimento", "dimension": "Apoio", "text": "Recebo elogios quando faço um bom trabalho."},
    {"vector": "Reconhecimento", "dimension": "Apoio", "text": "Sinto que minhas contribuições são valorizadas."},
    {"vector": "Reconhecimento", "dimension": "Controle", "text": "Existem critérios claros para reconhecimento."},
    {"vector": "Reconhecimento", "dimension": "Controle", "text": "O sistema de recompensas é justo."},
    {"vector": "Reconhecimento", "dimension": "Coesão", "text": "Colegas reconhecem o trabalho uns dos outros."},
    {"vector": "Reconhecimento", "dimension": "Coesão", "text": "Conquistas da equipe são celebradas."},
    
    # Vector: Desenvolvimento (Development)
    {"vector": "Desenvolvimento", "dimension": "Apoio", "text": "A empresa investe no meu desenvolvimento."},
    {"vector": "Desenvolvimento", "dimension": "Apoio", "text": "Tenho acesso a treinamentos e capacitações."},
    {"vector": "Desenvolvimento", "dimension": "Apoio", "text": "Meu gestor me incentiva a aprender coisas novas."},
    {"vector": "Desenvolvimento", "dimension": "Controle", "text": "Existe plano de carreira claro."},
    {"vector": "Desenvolvimento", "dimension": "Controle", "text": "Oportunidades de crescimento são divulgadas."},
    {"vector": "Desenvolvimento", "dimension": "Coesão", "text": "A empresa valoriza o aprendizado contínuo."},
    {"vector": "Desenvolvimento", "dimension": "Coesão", "text": "Tenho oportunidades para desenvolver novas habilidades."},
    
    # Vector: Ambiente (Environment)
    {"vector": "Ambiente", "dimension": "Conforto", "text": "O ambiente físico é adequado para o trabalho."},
    {"vector": "Ambiente", "dimension": "Conforto", "text": "Tenho condições ergonômicas satisfatórias."},
    {"vector": "Ambiente", "dimension": "Conforto", "text": "O local de trabalho é seguro e saudável."},
    {"vector": "Ambiente", "dimension": "Controle", "text": "Tenho as ferramentas necessárias para trabalhar."},
    {"vector": "Ambiente", "dimension": "Controle", "text": "A infraestrutura tecnológica é adequada."},
    {"vector": "Ambiente", "dimension": "Apoio", "text": "A empresa se preocupa com meu bem-estar."},
    {"vector": "Ambiente", "dimension": "Apoio", "text": "Posso equilibrar vida pessoal e profissional."},
    {"vector": "Ambiente", "dimension": "Apoio", "text": "A carga de trabalho é gerenciável."},
]

# FDAC Questions (12 total) - Organizational Culture
FDAC_QUESTIONS = [
    {"dimension": "Poder", "text": "Decisões importantes são concentradas na alta liderança."},
    {"dimension": "Poder", "text": "A hierarquia é bem definida e respeitada."},
    {"dimension": "Poder", "text": "Autoridade e poder estão centralizados."},
    
    {"dimension": "Regras", "text": "A empresa possui processos e normas bem estabelecidos."},
    {"dimension": "Regras", "text": "Procedimentos e regras são seguidos rigorosamente."},
    {"dimension": "Regras", "text": "Existe formalização nas atividades diárias."},
    
    {"dimension": "Resultados", "text": "A empresa é orientada para atingir resultados."},
    {"dimension": "Resultados", "text": "Metas e performance são altamente valorizadas."},
    {"dimension": "Resultados", "text": "O foco está em produtividade e eficiência."},
    
    {"dimension": "Pessoas", "text": "A empresa se preocupa com o bem-estar dos colaboradores."},
    {"dimension": "Pessoas", "text": "Relações humanas são priorizadas."},
    {"dimension": "Pessoas", "text": "Existe valorização do desenvolvimento pessoal."},
]


def seed_questions():
    """Seed database with IMCO and FDAC questions"""
    db = SessionLocal()
    
    try:
        # Check if questions already exist
        existing = db.query(Question).count()
        if existing > 0:
            print(f"⚠️  Database already has {existing} questions. Skipping seed.")
            return
        
        print("📝 Seeding IMCO questions (88)...")
        for idx, q in enumerate(IMCO_QUESTIONS, start=1):
            question = Question(
                type=QuestionType.IMCO,
                vector=q["vector"],
                dimension=q["dimension"],
                text=q["text"],
                order=idx
            )
            db.add(question)
        
        print("📝 Seeding FDAC questions (12)...")
        for idx, q in enumerate(FDAC_QUESTIONS, start=89):
            question = Question(
                type=QuestionType.FDAC,
                vector=None,
                dimension=q["dimension"],
                text=q["text"],
                order=idx
            )
            db.add(question)
        
        db.commit()
        total = db.query(Question).count()
        print(f"✅ Successfully seeded {total} questions!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding questions: {e}")
    finally:
        db.close()


def create_admin_user():
    """Create default admin user"""
    db = SessionLocal()
    
    try:
        # Check if admin exists
        existing = db.query(User).filter(User.email == "admin@simdcco.com").first()
        if existing:
            print("⚠️  Admin user already exists.")
            return
        
        print("👤 Creating admin user...")
        admin = User(
            email="admin@simdcco.com",
            password_hash=hash_password("admin123"),  # CHANGE IN PRODUCTION!
            name="Administrador SIMDCCO",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin)
        db.commit()
        print("✅ Admin user created!")
        print("   Email: admin@simdcco.com")
        print("   Password: admin123")
        print("   ⚠️  CHANGE PASSWORD IN PRODUCTION!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating admin: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Starting database seed...")
    init_db()
    seed_questions()
    create_admin_user()
    print("🎉 Database seed completed!")
