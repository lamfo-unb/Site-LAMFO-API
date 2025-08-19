from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Member, Project
import json

def create_mock_data():
    """Create mock data for testing"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create mock members
        members_data = [
            {
                "name": "João Silva",
                "email": "joao.silva@example.com",
                "role": "Data Scientist",
                "bio": "Especialista em Machine Learning e análise de dados",
                "github_username": "joaosilva",
                "linkedin_url": "https://linkedin.com/in/joaosilva"
            },
            {
                "name": "Maria Santos",
                "email": "maria.santos@example.com",
                "role": "AI Engineer",
                "bio": "Desenvolvedora focada em IA e Deep Learning",
                "github_username": "mariasantos",
                "linkedin_url": "https://linkedin.com/in/mariasantos"
            },
            {
                "name": "Pedro Oliveira",
                "email": "pedro.oliveira@example.com",
                "role": "Research Assistant",
                "bio": "Estudante de mestrado em Ciência da Computação",
                "github_username": "pedrooliveira"
            }
        ]
        
        # Create members
        created_members = []
        for member_data in members_data:
            member = Member(**member_data)
            db.add(member)
            created_members.append(member)
        
        db.commit()
        
        # Create mock projects
        projects_data = [
            {
                "title": "Sistema de Recomendação",
                "description": "Sistema de recomendação usando algoritmos de machine learning",
                "status": "active",
                "github_url": "https://github.com/lamfo/recommendation-system",
                "demo_url": "https://demo.lamfo.ai/recommendations"
            },
            {
                "title": "Análise de Sentimentos",
                "description": "Ferramenta para análise de sentimentos em redes sociais",
                "status": "completed",
                "github_url": "https://github.com/lamfo/sentiment-analysis"
            },
            {
                "title": "Chatbot Inteligente",
                "description": "Chatbot usando processamento de linguagem natural",
                "status": "active",
                "github_url": "https://github.com/lamfo/intelligent-chatbot"
            }
        ]
        
        # Create projects and assign members
        for i, project_data in enumerate(projects_data):
            project = Project(**project_data)
            
            # Assign members to projects (rotating assignment for demo)
            if i == 0:  # First project gets first two members
                project.members = created_members[:2]
            elif i == 1:  # Second project gets last two members
                project.members = created_members[1:]
            else:  # Third project gets all members
                project.members = created_members
            
            db.add(project)
        
        db.commit()
        
        print("✅ Mock data created successfully!")
        print(f"Created {len(members_data)} members and {len(projects_data)} projects")
        
    except Exception as e:
        print(f"❌ Error creating mock data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_mock_data()