import datetime
from core.db.sqlite import connect_to_ddbb, close_connection_to_ddbb

def create_new_project(new_project):
    connection = None
    try:
        connection = connect_to_ddbb()
        cursor = connection.cursor()
        if check_if_project_exists(new_project['project_name']):
            print(f'... there is an existing project with the name {new_project["project_name"]}. Choose other name!')
        else:
            cursor.execute('INSERT INTO project VALUES (?, ?, ?)', (new_project['project_name'],
                                                                    new_project['start_date'],
                                                                    new_project['plugin_manager']))
            connection.commit()
            print(f'... project created with name {new_project["project_name"]}')
    except Exception as e:
        print(f'... project could not be created because of: {e}')
    finally:
        if connection:
            close_connection_to_ddbb(connection)


def update_project(project_name, attribute_name, value):
    connection = None
    try:
        connection = connect_to_ddbb()
        cursor = connection.cursor()
        if check_if_project_exists(project_name):
            cursor.execute(f'UPDATE project SET {attribute_name} = ? WHERE project_name = ?', (value, project_name))
            connection.commit()
            print(f'... updated project with name {project_name}')
        else:
            print(f'... there is no project with name {project_name}')
    except Exception as e:
        print(f'... project could not be updated because of: {e}')
    finally:
        if connection:
            close_connection_to_ddbb(connection)


def check_if_project_exists(project_name):
    connection = None
    try:
        connection = connect_to_ddbb()
        cursor = connection.cursor()
        cursor.execute('SELECT count(*) FROM project WHERE project_name = ?', (project_name,))
        total = cursor.fetchone()[0]
        if total > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f'... could not check projects with name {project_name} because of: {e}')
    finally:
        if connection:
            close_connection_to_ddbb(connection)


def delete_project(project_name):
    connection = None
    try:
        connection = connect_to_ddbb()
        cursor = connection.cursor()
        if check_if_project_exists(project_name):
            cursor.execute('DELETE FROM project WHERE project_name = ?', (project_name,))
            connection.commit()
            print(f'... deleted project with name {project_name}')
        else:
            print(f'... there is no project with name {project_name}')
    except Exception as e:
        print(f'... project could not be deleted because of: {e}')
    finally:
        if connection:
            close_connection_to_ddbb(connection)


def list_projects():
    connection = None
    try:
        connection = connect_to_ddbb()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM project')
        projects = []
        for project in cursor.fetchall():
            project = list(project)
            project[1] = datetime.datetime.fromtimestamp(project[1]).strftime('%d-%m-%Y')
            projects.append(tuple(project))
        column_names = [columns[0] for columns in cursor.description]
        return column_names, projects
    except Exception as e:
        print(f'... could not check projects because of: {e}')
    finally:
        if connection:
            close_connection_to_ddbb(connection)


def get_plugin_manager(project_name):
    connection = None
    try:
        connection = connect_to_ddbb()
        cursor = connection.cursor()
        cursor.execute('SELECT plugin_manager FROM project WHERE project_name = ?', (project_name,))
        plugin_manager = cursor.fetchone()[0]
        return plugin_manager
    except Exception as e:
        print(f'... could not check plugin manager for project {project_name} because of: {e}')
    finally:
        if connection:
            close_connection_to_ddbb(connection)
