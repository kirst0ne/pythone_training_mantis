from model.project import Project


def test_add_project(app):
    base_project_name = "TestProject"
    unique_project_name = base_project_name
    while app.project.is_project_exists(unique_project_name):
        unique_project_name = app.project.generate_unique_name(base_project_name)
    new_project = Project(name=unique_project_name)
    old_projects = app.project.get_project_list()
    app.project.create_project(new_project)
    new_projects = app.project.get_project_list()
    assert len(new_projects) == len(old_projects) + 1, "Project was not added"
    added_project = next((project for project in new_projects if project["name"] == new_project.name), None)
    assert added_project is not None, f"New project '{new_project.name}' not found in the project list"
