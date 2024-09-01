from model.project import Project


def test_add_project(app, ensure_login):
    base_project_name = "TestProject"
    unique_project_name = base_project_name
    while app.project.is_project_exists(unique_project_name):
        unique_project_name = app.project.generate_unique_name(base_project_name)
    new_project = Project(name=unique_project_name)
    old_projects = app.soap.get_project_list()
    app.project.create_project(new_project)
    new_projects = app.soap.get_project_list()
    assert len(new_projects) == len(old_projects) + 1, "Project was not added"
    added_project = next((p for p in new_projects if p['name'] == new_project.name), None)
    assert added_project is not None, f"Проект {new_project.name} не был найден в новом списке проектов."
