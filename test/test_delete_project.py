from model.project import Project


def test_delete_first_project(app, ensure_login):
    projects = app.soap.get_project_list()
    if len(projects) == 0:
        new_project = Project(name="qwerty")
        app.project.create(new_project)
        projects = app.soap.get_project_list()
    app.project.delete_first_project()
    updated_projects = app.soap.get_project_list()
    assert len(updated_projects) == len(projects) - 1, "Количество проектов не уменьшилось на 1 после удаления."
    assert all(project["name"] != projects[0]["name"] for project in
               updated_projects), "Удаленный проект все еще присутствует в списке."
