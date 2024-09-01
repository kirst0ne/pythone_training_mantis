from selenium.webdriver.common.by import By
import random


class ProjectHelper:

    def __init__(self, app):
        self.app = app
        self._manage_projects_page_open = False

    def open_manage_page(self):
        wd = self.app.wd
        self.app.open_home_page()
        wd.find_element_by_link_text("Manage").click()

    def open_manage_projects_page(self):
        wd = self.app.wd
        if not self._manage_projects_page_open:
            self.open_manage_page()
            wd.find_element_by_link_text("Manage Projects").click()
            self._manage_projects_page_open = True

    def close_manage_projects_page(self):
        self._manage_projects_page_open = False

    def is_project_exists(self, project_name):
        wd = self.app.wd
        self.open_manage_projects_page()
        projects = self.get_project_list()
        return any(project["name"] == project_name for project in projects)

    def generate_unique_name(self, base_name):
        return f"{base_name}_{random.randint(1, 9999)}"

    def create_project(self, project):
        wd = self.app.wd
        self.open_manage_projects_page()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        wd.find_element_by_name("name").click()
        wd.find_element_by_name("name").clear()
        wd.find_element_by_name("name").send_keys(project.name)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.close_manage_projects_page()

    def get_project_list(self):
        wd = self.app.wd
        self.open_manage_projects_page()
        project_list = []
        rows = wd.find_elements_by_css_selector("tr.row-1, tr.row-2")
        for row in rows:
            cells = row.find_elements_by_tag_name("td")
            if len(cells) >= 5:
                name = cells[0].text.strip()
                status = cells[1].text.strip()
                view_status = cells[3].text.strip()
                description = cells[4].text.strip()
                project_list.append({
                    "name": name,
                    "status": status,
                    "view_status": view_status,
                    "description": description
                })
        return project_list

    def delete_first_project(self):
        self.open_manage_projects_page()
        projects = self.get_project_list()
        if not projects:
            raise Exception("Для удаления нет доступных проектов")
        first_project = projects[0]
        project_name = first_project["name"]
        project_elements = self.app.wd.find_elements(By.XPATH, f"//a[text()='{project_name}']")
        if not project_elements:
            raise Exception(f"Проект {project_name} не найден")
        project_elements[0].click()
        self.app.wd.find_element(By.XPATH, "//input[@value='Delete Project']").click()
        self.app.wd.find_element(By.XPATH, "//input[@value='Delete Project']").click()
