from core.db.sqlite import connect_to_ddbb, close_connection_to_ddbb


def create_new_project(new_project):
    connection = None
    try:
        connection = connect_to_ddbb()
        cursor = connection.cursor()
        if check_if_project_exists(new_project['project_name']):
            print(f'... there is an existing project with the name {new_project["project_name"]}. Choose other name!')
        else:
            cursor.execute('INSERT INTO project VALUES (?, ?, ?, ?, ?)', (new_project['project_name'],
                                                                          new_project['start_date'],
                                                                          new_project['proposal_manager'],
                                                                          new_project['data_management_system'],
                                                                          new_project['metadata_path']))
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
        cursor.execute(f'UPDATE project SET {attribute_name} = ? WHERE project_name = ?', (value, project_name))
        connection.commit()
        print(f'... updated project with name {project_name}')
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


def get_metadata_path(project_name):
    connection = None
    try:
        connection = connect_to_ddbb()
        cursor = connection.cursor()
        cursor.execute('SELECT metadata_path FROM project WHERE project_name = ?', (project_name,))
        metadata_path = cursor.fetchone()[0]
        return metadata_path
    except Exception as e:
        print(f'... could not check projects with name {project_name} because of: {e}')
    finally:
        if connection:
            close_connection_to_ddbb(connection)
