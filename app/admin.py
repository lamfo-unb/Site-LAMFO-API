from sqladmin import Admin, ModelView
from .database import get_engine
from .models import Member, Project


def create_admin(app):
    """Create and configure SQLAdmin for the FastAPI app"""

    admin = Admin(app, get_engine(), title="LAMFO Admin")
    
    # Add model views
    admin.add_view(MemberAdmin)
    admin.add_view(ProjectAdmin)
    
    return admin


class MemberAdmin(ModelView, model=Member):
    """Admin interface for Member model"""
    column_list = [
        Member.id, Member.name, Member.email, Member.role, Member.created_at
    ]
    column_searchable_list = [Member.name, Member.email]
    column_sortable_list = [
        Member.id, Member.name, Member.email, Member.created_at
    ]
    column_filters = [Member.role]
    
    # Form configuration
    form_excluded_columns = [Member.created_at, Member.updated_at]
    
    # Display configuration
    name = "Member"
    name_plural = "Members"
    icon = "fa-solid fa-user"


class ProjectAdmin(ModelView, model=Project):
    """Admin interface for Project model"""
    column_list = [
        Project.id, Project.title, Project.status, Project.created_at
    ]
    column_searchable_list = [Project.title, Project.description]
    column_sortable_list = [Project.id, Project.title, Project.created_at]
    column_filters = [Project.status]
    
    # Form configuration
    form_excluded_columns = [Project.created_at, Project.updated_at]
    
    # Display configuration
    name = "Project"
    name_plural = "Projects"
    icon = "fa-solid fa-project-diagram"
