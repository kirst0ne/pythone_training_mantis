from model.project import Project


def test_delete_project(app):
    app.project.open_manage_projects_page()
    old_projects_list = app.project.get_project_list()
    if len(app.project.get_project_list()) == 0:
        app.project.create_project(Project(name="test"))
        old_projects_list = app.project.get_project_list()
    app.project.delete_first_project()
    updated_projects = app.project.get_project_list()
    assert len(updated_projects) < len(old_projects_list), "Проект не был удалён"
    assert all(project["name"] != old_projects_list[0]["name"] for project in updated_projects), \
        f"Проект {old_projects_list[0]['name']} не был удален"
