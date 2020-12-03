import sqlite3
import hashlib
import datetime
from app.utilities.app_utilities import convert_background_text


app_db_web_location_default = "sqlite:///../app.sqlite"
app_db_local_location_default = "C:\\pycharm\\projects\\my_app\\app.sqlite"


def get_school_list(app_db_web_location=app_db_web_location_default):
    school_rows = search_school_list(app_db_web_location)
    school_list = [(0, 'Please Select')]
    for row in school_rows:
        tmp_tuple = (row[0], row[1]+' - '+row[2]+' - '+row[3])
        school_list.append(tmp_tuple)
    return school_list


def search_school_list(app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = 'select SCHOOL_ID, SCHOOL_NAME, PROVINCE, CITY, SCHOOL_ADDRESS, ZIP_CODE from SCHOOL_DIRECTORY order by school_name, province, city;'
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


def search_schools_by_id(school_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "select SCHOOL_ID, SCHOOL_NAME, PROVINCE, CITY, SCHOOL_ADDRESS, ZIP_CODE, COUNTRY, SCHOOL_STATUS " \
              "from SCHOOL_DIRECTORY WHERE SCHOOL_ID = " + str(school_id) + ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


def search_schools_has_event_team(event_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "select DISTINCT SCHOOL_ID, SCHOOL_NAME, SCHOOL_PROVINCE, SCHOOL_CITY, SCHOOL_ADDRESS, SCHOOL_COUNTRY, SCHOOL_ZIP_CODE " \
              "from v_team WHERE EVENT_ID = " + str(event_id) + " order by SCHOOL_NAME COLLATE NOCASE, SCHOOL_PROVINCE, SCHOOL_CITY;"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


def get_schools_has_event_team(event_id, app_db_web_location=app_db_web_location_default):
    school_rows = search_schools_has_event_team(event_id, app_db_web_location)
    school_list = [(0, 'Please Select')]
    for row in school_rows:
        tmp_tuple = (row[0], row[1]+' - '+row[2]+' - '+row[3])
        school_list.append(tmp_tuple)
    return school_list


def get_schools_for_juror(event_id, app_db_web_location=app_db_web_location_default):
    school_rows = search_schools_has_event_team(event_id, app_db_web_location)
    school_list = []
    for row in school_rows:
        tmp_tuple = (row[0], row[1]+' - '+row[2]+' - '+row[3])
        school_list.append(tmp_tuple)
    return school_list


def get_schools_for_ppant(event_id, app_db_web_location=app_db_web_location_default):
    school_rows = search_schools_has_event_team(event_id, app_db_web_location)
    school_list = []
    for row in school_rows:
        tmp_tuple = (row[0], row[1]+' - '+row[2]+' - '+row[3])
        school_list.append(tmp_tuple)
    return school_list


# search current event: event is not closed
def search_current_event(app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT EVENT_ID, EVENT_NAME, EVENT_STATUS, EVENT_DESCRIPTION, EVENT_YEAR from EVENT WHERE EVENT_STATUS != 'Closed' order by EVENT_YEAR DESC';"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


def get_current_event(app_db_web_location=app_db_web_location_default):
    event_rows = search_current_event(app_db_web_location)
    current_event = tuple()
    for row in event_rows:
        current_event = (row[0], row[1], row[2], row[3], row[4])
        break
    return current_event


# Search event by status, such as Open for Registration, Closed for Registration, Closed
def search_event_by_status(event_status, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT EVENT_ID, EVENT_NAME, EVENT_STATUS, EVENT_DESCRIPTION, EVENT_YEAR from EVENT WHERE EVENT_STATUS = '" + event_status + "';"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


def get_teams_ledbyme(event_id, team_lead_id, app_db_web_location=app_db_web_location_default):
    team_rows = search_teams_ledbyme(event_id, team_lead_id, app_db_web_location)
    teams_ledbyme = [(None, 'Please Select')]
    for row in team_rows:
        tmp_tuple = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])
        teams_ledbyme.append(tmp_tuple)
    return teams_ledbyme


def get_teams_ledbyme_full(event_id, team_lead_id, app_db_web_location=app_db_web_location_default):
    team_rows = search_teams_ledbyme(event_id, team_lead_id, app_db_web_location)
    teams_ledbyme = [(None, 'Please Select')]
    for row in team_rows:
        tmp_tuple = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])
        teams_ledbyme.append(tmp_tuple)
    return teams_ledbyme


# Search teams that are under specific team lead Id
def search_teams_ledbyme(event_id, team_lead_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "EVENT_ID, EVENT_NAME, " \
              "TEAM_ID, TEAM_NAME, TEAM_STATUS, " \
              "SCHOOL_ID, SCHOOL_NAME, SCHOOL_ADDRESS, SCHOOL_CITY, SCHOOL_PROVINCE, SCHOOL_COUNTRY, " \
              "TEAM_LEAD_ID, TEAM_LEAD_FIRST_NAME, TEAM_LEAD_LAST_NAME, TEAM_LEAD_EMAIL " \
              "FROM V_TEAM " \
              "WHERE EVENT_ID=" + str(event_id) + " " \
              "AND TEAM_LEAD_ID=" + str(team_lead_id) + " " \
              "ORDER by SCHOOL_NAME, TEAM_NAME " \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# Search teams that are under specific event Id
def search_event_teams(event_id, app_db_web_location=app_db_web_location_default, team_status=None):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    if team_status is None:
        command = "SELECT " \
                  "EVENT_ID, EVENT_NAME, " \
                  "TEAM_ID, TEAM_NAME, TEAM_STATUS, " \
                  "SCHOOL_ID, SCHOOL_NAME, SCHOOL_ADDRESS, SCHOOL_CITY, SCHOOL_PROVINCE, SCHOOL_COUNTRY, " \
                  "TEAM_LEAD_ID, TEAM_LEAD_FIRST_NAME, TEAM_LEAD_LAST_NAME, TEAM_LEAD_EMAIL " \
                  "FROM V_TEAM " \
                  "WHERE EVENT_ID=" + str(event_id) + " " \
                  "ORDER by SCHOOL_NAME, TEAM_NAME " \
                  ";"
    else:
        command = "SELECT " \
                  "EVENT_ID, EVENT_NAME, " \
                  "TEAM_ID, TEAM_NAME, TEAM_STATUS, " \
                  "SCHOOL_ID, SCHOOL_NAME, SCHOOL_ADDRESS, SCHOOL_CITY, SCHOOL_PROVINCE, SCHOOL_COUNTRY, " \
                  "TEAM_LEAD_ID, TEAM_LEAD_FIRST_NAME, TEAM_LEAD_LAST_NAME, TEAM_LEAD_EMAIL " \
                  "FROM V_TEAM " \
                  "WHERE EVENT_ID=" + str(event_id) + " " \
                  "AND TEAM_STATUS='" + team_status + "' " \
                  "ORDER by SCHOOL_NAME, TEAM_NAME " \
                  ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# Search teams that are under specific event Id
def search_event_teams_inorder(event_id, app_db_web_location=app_db_web_location_default, team_status=None):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    if team_status is None:
        command = "SELECT " \
                  "EVENT_ID, EVENT_NAME, " \
                  "TEAM_ID, TEAM_NAME, TEAM_STATUS, " \
                  "SCHOOL_ID, SCHOOL_NAME, SCHOOL_ADDRESS, SCHOOL_CITY, SCHOOL_PROVINCE, SCHOOL_COUNTRY, " \
                  "TEAM_LEAD_ID, TEAM_LEAD_FIRST_NAME, TEAM_LEAD_LAST_NAME, TEAM_LEAD_EMAIL " \
                  "FROM V_TEAM " \
                  "WHERE EVENT_ID=" + str(event_id) + " " \
                  "ORDER by TEAM_ID " \
                  ";"
    else:
        command = "SELECT " \
                  "EVENT_ID, EVENT_NAME, " \
                  "TEAM_ID, TEAM_NAME, TEAM_STATUS, " \
                  "SCHOOL_ID, SCHOOL_NAME, SCHOOL_ADDRESS, SCHOOL_CITY, SCHOOL_PROVINCE, SCHOOL_COUNTRY, " \
                  "TEAM_LEAD_ID, TEAM_LEAD_FIRST_NAME, TEAM_LEAD_LAST_NAME, TEAM_LEAD_EMAIL " \
                  "FROM V_TEAM " \
                  "WHERE EVENT_ID=" + str(event_id) + " " \
                  "AND TEAM_STATUS='" + team_status + "' " \
                  "ORDER by TEAM_ID " \
                  ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


def get_current_teams_options(event_id, app_db_web_location=app_db_web_location_default):
    team_rows = search_event_teams(event_id, app_db_web_location)
    tmp_school_id = 0
    current_teams_options = list()
    tmp_school_teams = list()
    tmp_school_name = None
    for row in team_rows:
        if row[5] != tmp_school_id:
            if tmp_school_id > 0:
                tmp_tuple2 = (tmp_school_id, tmp_school_name, tmp_school_teams)
                current_teams_options.append(tmp_tuple2)
            tmp_school_id = row[5]
            tmp_school_teams = list()
            tmp_school_name = row[6] + " - " + row[9] + " - " + row[8]

        tmp_tuple1 = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])
        tmp_school_teams.append(tmp_tuple1)

    if tmp_school_id > 0:
        tmp_tuple2 = (tmp_school_id, tmp_school_name, tmp_school_teams)
        current_teams_options.append(tmp_tuple2)

    return current_teams_options


# Search teams and associated members for specific event Id order by name
def search_event_teams_n_members(event_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "EVENT_ID, EVENT_NAME, " \
              "TEAM_ID, TEAM_NAME, TEAM_STATUS, " \
              "SCHOOL_ID, SCHOOL_NAME, SCHOOL_ADDRESS, SCHOOL_CITY, SCHOOL_PROVINCE, SCHOOL_COUNTRY, " \
              "TEAM_LEAD_ID, TEAM_LEAD_FIRST_NAME, TEAM_LEAD_LAST_NAME, TEAM_LEAD_EMAIL, " \
              "TEAM_MEMBER_ID, TEAM_MEMBER_USER_ID, IS_CAPTAIN, MEMBER_STATUS" \
              "TEAM_MEMBER_FIRST_NAME, TEAM_MEMBER_LAST_NAME, TEAM_MEMBER_EMAIL, TEAM_MEMBER_DOB " \
              "FROM V_TEAMS_N_MEMBERS " \
              "WHERE EVENT_ID=" + str(event_id) + " " \
              "ORDER by SCHOOL_NAME, TEAM_NAME, TEAM_MEMBER_LAST_NAME " \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# Search teams and associated members for specific event Id order by name
def search_event_juror(event_id, is_chair, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "EVENT_ID, EVENT_NAME, " \
              "PARTICIPANT_ID, HAS_COI, COI_ID, COI_COMMENTS, COI_SCHOOL_ID, COI_SCHOOL_NAME, " \
              "COI_SCHOOL_STATUS, COI_SCHOOL_ADDRESS, PPANT_TELEC, IS_CHAIR " \
              "FROM v_event_participant_cois_schools " \
              "WHERE EVENT_ID=" + str(event_id) + " "\
              "AND IS_CHAIR = '" + is_chair + "' " \
              "ORDER by PARTICIPANT_ID " \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# Search teams and associated members for specific event Id order by ID
def search_event_teams_n_members_by_id(event_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "EVENT_ID, EVENT_NAME, " \
              "TEAM_ID, TEAM_NAME, TEAM_STATUS, " \
              "SCHOOL_ID, SCHOOL_NAME, SCHOOL_ADDRESS, SCHOOL_CITY, SCHOOL_PROVINCE, SCHOOL_COUNTRY, " \
              "TEAM_LEAD_ID, TEAM_LEAD_FIRST_NAME, TEAM_LEAD_LAST_NAME, TEAM_LEAD_EMAIL, " \
              "TEAM_MEMBER_ID, TEAM_MEMBER_USER_ID, IS_CAPTAIN, MEMBER_STATUS, " \
              "TEAM_MEMBER_FIRST_NAME, TEAM_MEMBER_LAST_NAME, TEAM_MEMBER_EMAIL, TEAM_MEMBER_DOB " \
              "FROM V_TEAMS_N_MEMBERS " \
              "WHERE EVENT_ID=" + str(event_id) + " " \
              "ORDER by SCHOOL_ID, TEAM_ID, TEAM_MEMBER_ID " \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# Search all the team members detail for all the teams of a specific event id
def search_event_teams_n_members_all(event_id, team_status, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    if team_status is None or len(team_status) <1:
        command = "SELECT " \
                  "EVENT_ID, EVENT_NAME, " \
                  "TEAM_ID, TEAM_NAME, TEAM_STATUS, " \
                  "SCHOOL_ID, SCHOOL_NAME, SCHOOL_ADDRESS, SCHOOL_CITY, SCHOOL_PROVINCE, SCHOOL_COUNTRY, " \
                  "TEAM_LEAD_ID, TEAM_LEAD_FIRST_NAME, TEAM_LEAD_LAST_NAME, TEAM_LEAD_EMAIL, " \
                  "TEAM_MEMBER_ID, TEAM_MEMBER_USER_ID, IS_CAPTAIN, MEMBER_STATUS, " \
                  "TEAM_MEMBER_FIRST_NAME, TEAM_MEMBER_LAST_NAME, TEAM_MEMBER_EMAIL, strftime('%Y-%m-%d',TEAM_MEMBER_DOB), " \
                  "strftime('%Y-%m-%d', TEAM_REGISTER_DATE), strftime('%Y-%m-%d',TEAM_MEMBER_APPLY_DATE), SCHOOL_STATUS, " \
                  "TEAM_LEAD_TELEC " \
                  "FROM V_TEAMS_N_MEMBERS " \
                  "WHERE EVENT_ID=" + str(event_id) + " " \
                  "ORDER by TEAM_REGISTER_DATE, TEAM_ID, IS_CAPTAIN DESC, TEAM_MEMBER_FIRST_NAME, TEAM_MEMBER_LAST_NAME " \
                  ";"
    else:
        command = "SELECT " \
                  "EVENT_ID, EVENT_NAME, " \
                  "TEAM_ID, TEAM_NAME, TEAM_STATUS, " \
                  "SCHOOL_ID, SCHOOL_NAME, SCHOOL_ADDRESS, SCHOOL_CITY, SCHOOL_PROVINCE, SCHOOL_COUNTRY, " \
                  "TEAM_LEAD_ID, TEAM_LEAD_FIRST_NAME, TEAM_LEAD_LAST_NAME, TEAM_LEAD_EMAIL, " \
                  "TEAM_MEMBER_ID, TEAM_MEMBER_USER_ID, IS_CAPTAIN, MEMBER_STATUS, " \
                  "TEAM_MEMBER_FIRST_NAME, TEAM_MEMBER_LAST_NAME, TEAM_MEMBER_EMAIL, strftime('%Y-%m-%d',TEAM_MEMBER_DOB), " \
                  "strftime('%Y-%m-%d', TEAM_REGISTER_DATE), strftime('%Y-%m-%d',TEAM_MEMBER_APPLY_DATE), SCHOOL_STATUS, " \
                  "TEAM_LEAD_TELEC " \
                  "FROM V_TEAMS_N_MEMBERS " \
                  "WHERE EVENT_ID=" + str(event_id) + " " \
                  "AND TEAM_STATUS='" + team_status + "' " \
                  "ORDER by TEAM_REGISTER_DATE, TEAM_ID, IS_CAPTAIN DESC, TEAM_MEMBER_FIRST_NAME, TEAM_MEMBER_LAST_NAME " \
                  ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# Search all the team members detail for all the teams led by a specific team lead id of a specific event id
def search_event_teams_n_members_ledbyme(event_id, team_lead_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "EVENT_ID, EVENT_NAME, " \
              "TEAM_ID, TEAM_NAME, TEAM_STATUS, " \
              "SCHOOL_ID, SCHOOL_NAME, SCHOOL_ADDRESS, SCHOOL_CITY, SCHOOL_PROVINCE, SCHOOL_COUNTRY, " \
              "TEAM_LEAD_ID, TEAM_LEAD_FIRST_NAME, TEAM_LEAD_LAST_NAME, TEAM_LEAD_EMAIL, " \
              "TEAM_MEMBER_ID, TEAM_MEMBER_USER_ID, IS_CAPTAIN, MEMBER_STATUS, " \
              "TEAM_MEMBER_FIRST_NAME, TEAM_MEMBER_LAST_NAME, TEAM_MEMBER_EMAIL, strftime('%Y-%m-%d',TEAM_MEMBER_DOB), " \
              "strftime('%Y-%m-%d', TEAM_REGISTER_DATE), strftime('%Y-%m-%d',TEAM_MEMBER_APPLY_DATE), TEAM_LEAD_TELEC  " \
              "FROM V_TEAMS_N_MEMBERS " \
              "WHERE EVENT_ID=" + str(event_id) + " " \
              "AND TEAM_LEAD_ID=" + str(team_lead_id) + " " \
              "ORDER by TEAM_ID, TEAM_MEMBER_FIRST_NAME, TEAM_MEMBER_LAST_NAME " \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the team members detail for all the teams of a specific event id
def get_event_teams_n_members_all(event_id, team_status, app_db_web_location=app_db_web_location_default):
    team_rows = search_event_teams_n_members_all(event_id, team_status, app_db_web_location)
    teams_n_members_all = list()
    tmp_team_id = 0
    tmp_team_members = list()
    tmp_team_name = None
    tmp_status = None
    tmp_team_lead = None
    tmp_school_name = None
    tmp_school_id = 0
    tmp_team_register_date = None
    tmp_school_status = None
    team_approved_members_count = 0
    tmp_team_telec = None

    for row in team_rows:
        # add new team to tmp_school_teams
        if row[2] != tmp_team_id:
            if tmp_team_id > 0:
                # add last team to the return result
                tmp_tuple_team = (tmp_team_id, tmp_team_name, tmp_status, tmp_school_name, tmp_team_lead, len(tmp_team_members), tmp_team_members, tmp_school_id, tmp_team_register_date, tmp_school_status, team_approved_members_count, tmp_team_telec)
                teams_n_members_all.append(tmp_tuple_team)

            # reset team and team member record
            tmp_team_id = row[2]
            tmp_team_members = list()
            team_approved_members_count = 0
            tmp_team_telec = row[26]
            tmp_team_name = row[3]
            tmp_status = row[4]
            tmp_school_name = row[6] + " - " + row[9] + " - " + row[8]
            tmp_team_lead = row[12] + " " + row[13] + " - " + row[14]
            tmp_school_id = row[5]
            tmp_team_register_date = row[23]
            tmp_school_status = row[25]

        # add team members to current team
        if row[15] != None:
            tmp_tuple_member = (row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[24])
            tmp_team_members.append(tmp_tuple_member)
            if row[18] == "Approved":
                team_approved_members_count += 1

    # add last team
    if tmp_team_id > 0:
        tmp_tuple_team = (tmp_team_id, tmp_team_name, tmp_status, tmp_school_name, tmp_team_lead, len(tmp_team_members),
                          tmp_team_members, tmp_school_id, tmp_team_register_date, tmp_school_status,
                          team_approved_members_count, tmp_team_telec)
        teams_n_members_all.append(tmp_tuple_team)

    return teams_n_members_all


# get all the team members detail for all the teams led by a specific team lead id of a specific event id
def get_event_teams_n_members_ledbyme(event_id, team_lead_id, app_db_web_location=app_db_web_location_default):
    team_rows = search_event_teams_n_members_ledbyme(event_id, team_lead_id, app_db_web_location)
    teams_n_members_ledbyme = list()
    tmp_team_id = 0
    tmp_team_members = list()
    tmp_team_name = None
    tmp_status = None
    tmp_team_lead = None
    tmp_school_name = None
    tmp_school_id = 0
    tmp_team_register_date = None
    tmp_captain = 0
    tmp_approved_members_count = 0
    tmp_team_lead_id = 0
    team_members_count = 0
    tmp_teleconference = None

    for row in team_rows:
        # add new team to tmp_school_teams
        if row[2] != tmp_team_id:
            if tmp_team_id > 0:
                # add last team to the return result
                tmp_tuple_team = (tmp_team_id, tmp_team_name, tmp_status, tmp_school_name, tmp_team_lead, len(tmp_team_members), tmp_team_members, tmp_school_id, tmp_team_register_date, tmp_captain, tmp_team_lead_id, tmp_teleconference, tmp_approved_members_count)
                teams_n_members_ledbyme.append(tmp_tuple_team)

            # reset team and team member record
            tmp_team_id = row[2]
            tmp_team_members = list()
            tmp_captain = 0
            tmp_approved_members_count = 0
            tmp_team_name = row[3]
            tmp_status = row[4]
            tmp_school_name = row[6] + " - " + row[8] + " - " + row[9]
            tmp_team_lead = row[12] + " " + row[13] + " - " + row[14]
            tmp_team_lead_id = row[11]
            tmp_school_id = row[5]
            tmp_team_register_date = row[23]
            tmp_teleconference = row[25]

        # add team members to current team
        if row[15] != None:
            tmp_tuple_member = (row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[24])
            if row[17] == 1:
                tmp_captain = tmp_captain + 1
            if row[18] == "Approved":
                tmp_approved_members_count += 1
            tmp_team_members.append(tmp_tuple_member)

    # add last team
    if tmp_team_id > 0:
        tmp_tuple_team = (tmp_team_id, tmp_team_name, tmp_status, tmp_school_name, tmp_team_lead, len(tmp_team_members), tmp_team_members, tmp_school_id, tmp_team_register_date, tmp_captain, tmp_team_lead_id, tmp_teleconference, tmp_approved_members_count)
        teams_n_members_ledbyme.append(tmp_tuple_team)

    return teams_n_members_ledbyme


# get all school teams and associated members for specific event
def get_school_teams_n_members(event_id, app_db_web_location=app_db_web_location_default):
    team_rows = search_event_teams_n_members_by_id(event_id, app_db_web_location)
    tmp_school_id = 0
    tmp_team_id = 0
    current_teams_n_members = list()
    tmp_school_teams = list()
    tmp_school_name = None
    tmp_team_members = list()
    tmp_team_name = None
    tmp_team_lead = None
    tmp_team_lead_id = 0

    for row in team_rows:
        # add new team to tmp_school_teams
        if row[2] != tmp_team_id:
            if tmp_team_id > 0:
                tmp_tuple_team = (tmp_team_id, tmp_team_name, tmp_team_lead, tmp_team_members)
                tmp_school_teams.append(tmp_tuple_team)

        # add new school to current_teams_n_members
        if row[5] != tmp_school_id:
            if tmp_school_id > 0:
                tmp_tuple_school = (tmp_school_id, tmp_school_name, tmp_school_teams)
                current_teams_n_members.append(tmp_tuple_school)

        if row[5] != tmp_school_id:
            # reset school record
            tmp_school_id = row[5]
            tmp_school_teams = list()
            tmp_school_name = row[6] + " - " + row[9] + " - " + row[8]

        if row[2] != tmp_team_id:
            # reset team member record
            tmp_team_id = row[2]
            tmp_team_members = list()
            tmp_team_name = row[3]
            tmp_team_lead = row[12] + " " + row[13] + " - " + row[14]
            tmp_team_lead_id = row[11]

        tmp_tuple_member = (row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22])
        tmp_team_members.append(tmp_tuple_member)

    if tmp_school_id > 0:
        tmp_tuple_team = (tmp_team_id, tmp_team_name, tmp_team_lead, tmp_team_members)
        tmp_school_teams.append(tmp_tuple_team)
        tmp_tuple_school = (tmp_school_id, tmp_school_name, tmp_school_teams)
        current_teams_n_members.append(tmp_tuple_school)

    return current_teams_n_members


def count_team_group_by_status(event_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    # command = "SELECT COUNT(*), TEAM_STATUS from EVENT_TEAM where EVENT_ID=2 group by TEAM_STATUS;"
    command = "SELECT COUNT(*), TEAM_STATUS from EVENT_TEAM where EVENT_ID = " + str(event_id) + " group by TEAM_STATUS;"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    team_counts = list()
    total_count = 0
    for row in result:
        tmp_tuple = (row[0], row[1])
        team_counts.append(tmp_tuple)
        total_count = total_count + row[0]

    count_result = (total_count, team_counts)

    return count_result


def count_team_member_group_by_status(event_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT COUNT(*), MEMBER_STATUS from V_TEAM_MEMBER where EVENT_ID = " + str(event_id) + " group by MEMBER_STATUS;"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    tmp_counts = list()
    total_count = 0
    for row in result:
        tmp_tuple = (row[0], row[1])
        tmp_counts.append(tmp_tuple)
        total_count = total_count + row[0]

    count_result = (total_count, tmp_counts)

    return count_result


def count_juror_group_by_status(event_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT COUNT(*), PPANT_STATUS from EVENT_PARTICIPANT where EVENT_ID= " + str(event_id) + " and PARTICIPANT_ROLE_TYPE = 'Juror' group by PPANT_STATUS;"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    tmp_counts = list()
    total_count = 0
    for row in result:
        tmp_tuple = (row[0], row[1])
        tmp_counts.append(tmp_tuple)
        total_count = total_count + row[0]

    count_result = (total_count, tmp_counts)

    return count_result

def count_volunteer_group_by_status(event_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT COUNT(*), PPANT_STATUS from EVENT_PARTICIPANT where EVENT_ID= " + str(event_id) + " and PARTICIPANT_ROLE_TYPE = 'Volunteer' group by PPANT_STATUS;"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    tmp_counts = list()
    total_count = 0
    for row in result:
        tmp_tuple = (row[0], row[1])
        tmp_counts.append(tmp_tuple)
        total_count = total_count + row[0]

    count_result = (total_count, tmp_counts)

    return count_result


def add_team(event_id, team_lead_id, school_id, team_name, teleconferencing, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())
    _c.execute(
        "insert into EVENT_TEAM (event_id, team_lead_id, school_id, team_name, CREATED_BY, TEAM_STATUS, teleconference, created_date) values(?, ?, ?, ?, ?, 'Approved', ?, ?)",
        (event_id, team_lead_id, school_id, team_name, team_lead_id, teleconferencing, current_timestamp))

    _conn.commit()
    _conn.close()


def update_a_team_status(event_id, team_id, team_status, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())
    _c.execute("UPDATE EVENT_TEAM SET team_status = ?, last_updated_by = ?, last_updated_date = ? WHERE event_id = ? and team_id = ?", (team_status, current_user_id, current_timestamp, event_id, team_id))

    _conn.commit()
    _conn.close()


def update_a_ppant_status(event_id, ppant_id, ppant_status, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())
    _c.execute("UPDATE EVENT_PARTICIPANT SET ppant_status = ?, last_updated_by = ?, last_updated_date = ? WHERE event_id = ? and participant_id = ?", (ppant_status, current_user_id, current_timestamp, event_id, ppant_id))

    _conn.commit()
    _conn.close()


def set_juror_chair(event_id, ppant_id, is_chair, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())
    _c.execute("UPDATE EVENT_PARTICIPANT SET is_chair = ?, last_updated_by = ?, last_updated_date = ? WHERE event_id = ? and participant_id = ?", (is_chair, current_user_id, current_timestamp, event_id, ppant_id))

    _conn.commit()
    _conn.close()


def update_a_team_member_status(team_member_id, member_status, is_captain, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())
    if member_status.lower() == "approved":
        _c.execute("UPDATE TEAM_MEMBER SET member_status = ?, is_captain = ?, approved_date = ?, "
                   "last_updated_by = ?, last_updated_date = ? WHERE team_member_id = ? ",
                   ("Approved", is_captain, current_timestamp, current_user_id, current_timestamp, team_member_id))
    elif member_status.lower() == "rejected":
        _c.execute("UPDATE TEAM_MEMBER SET member_status = ?, is_captain = ?, rejected_date = ?, "
                   "last_updated_by = ?, last_updated_date = ? WHERE team_member_id = ? ",
                   ("Rejected", is_captain, current_timestamp, current_user_id, current_timestamp, team_member_id))
    else:
        pass

    _conn.commit()
    _conn.close()


def update_a_school_by_id(school_id, school_name, school_address, city, province, country, postal_code, school_status, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())
    _c.execute("UPDATE SCHOOL_DIRECTORY SET school_name = ?, school_address = ?, city = ?, province = ?, country = ?, zip_code = ?, school_status = ?, last_updated_by = ?, last_updated_date = ? WHERE school_id = ?", (school_name, school_address, city, province, country, postal_code, school_status, current_user_id, current_timestamp, school_id))

    _conn.commit()
    _conn.close()


# add a new school to school_directory
def add_school(school_name, school_address, city, province, country, zipcode, created_by, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    _c.execute(
        "insert into SCHOOL_DIRECTORY (school_name, school_address, city, province, country, zip_code, created_by) values(?, ?, ?, ?, ?, ?, ?)",
        (school_name, school_address, city, province, country, zipcode, created_by))

    school_id = _c.lastrowid

    _conn.commit()
    _conn.close()

    return school_id


def add_team_member(team_id, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())
    _c.execute(
        "insert into team_member (team_id, team_member_user_id, MEMBER_STATUS, CREATED_DATE, CREATED_BY) values(?, ?, 'Requested', ?, ?)",
        (team_id, current_user_id, current_timestamp, current_user_id))

    _conn.commit()
    _conn.close()


# Search teams that are joined by a specific team member user Id
def search_teams_joinedbyme(event_id, team_member_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "EVENT_ID, EVENT_NAME, " \
              "TEAM_MEMBER_ID, TEAM_MEMBER_USER_ID, IS_CAPTAIN, MEMBER_STATUS, COMMENTS, " \
              "TEAM_ID, TEAM_NAME, TEAM_STATUS, " \
              "SCHOOL_ID, SCHOOL_NAME, SCHOOL_ADDRESS, SCHOOL_CITY, SCHOOL_PROVINCE, SCHOOL_COUNTRY, " \
              "TEAM_LEAD_ID, TEAM_LEAD_FIRST_NAME, TEAM_LEAD_LAST_NAME, TEAM_LEAD_EMAIL " \
              "FROM V_TEAM_MEMBER " \
              "WHERE EVENT_ID=" + str(event_id) + " " \
              "AND TEAM_MEMBER_USER_ID=" + str(team_member_user_id) + " " \
              "ORDER by TEAM_MEMBER_USER_ID, SCHOOL_NAME, TEAM_NAME " \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    # count number of team that I got approved
    myteams_count_joined_approved = 0
    myteams_joined = []
    for item in result:
        myteams_joined.append(item)
        if item[5] == "Approved":
            myteams_count_joined_approved += 1

    return (myteams_joined, myteams_count_joined_approved)


# Search all the team members for a specific event
def search_team_members_all(event_id, team_member_status, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    if team_member_status is None or len(team_member_status) < 1:
        command = "SELECT " \
                  "EVENT_ID, EVENT_NAME, " \
                  "TEAM_MEMBER_ID, TEAM_MEMBER_USER_ID, IS_CAPTAIN, MEMBER_STATUS, COMMENTS, " \
                  "TEAM_ID, TEAM_NAME, TEAM_STATUS, " \
                  "SCHOOL_ID, SCHOOL_NAME, SCHOOL_ADDRESS, SCHOOL_CITY, SCHOOL_PROVINCE, SCHOOL_COUNTRY, " \
                  "TEAM_LEAD_ID, TEAM_LEAD_FIRST_NAME, TEAM_LEAD_LAST_NAME, TEAM_LEAD_EMAIL, " \
                  "TEAM_MEMBER_FIRST_NAME, TEAM_MEMBER_LAST_NAME, TEAM_MEMBER_EMAIL, strftime('%Y-%m-%d',TEAM_MEMBER_DOB), " \
                  "strftime('%Y-%m-%d',TEAM_MEMBER_APPLY_DATE)  " \
                  "FROM V_TEAM_MEMBER " \
                  "WHERE EVENT_ID=" + str(event_id) + " " \
                  "ORDER by TEAM_MEMBER_FIRST_NAME, TEAM_MEMBER_LAST_NAME, SCHOOL_NAME " \
                  ";"
    else:
        command = "SELECT " \
                  "EVENT_ID, EVENT_NAME, " \
                  "TEAM_MEMBER_ID, TEAM_MEMBER_USER_ID, IS_CAPTAIN, MEMBER_STATUS, COMMENTS, " \
                  "TEAM_ID, TEAM_NAME, TEAM_STATUS, " \
                  "SCHOOL_ID, SCHOOL_NAME, SCHOOL_ADDRESS, SCHOOL_CITY, SCHOOL_PROVINCE, SCHOOL_COUNTRY, " \
                  "TEAM_LEAD_ID, TEAM_LEAD_FIRST_NAME, TEAM_LEAD_LAST_NAME, TEAM_LEAD_EMAIL, " \
                  "TEAM_MEMBER_FIRST_NAME, TEAM_MEMBER_LAST_NAME, TEAM_MEMBER_EMAIL, strftime('%Y-%m-%d',TEAM_MEMBER_DOB), " \
                  "strftime('%Y-%m-%d',TEAM_MEMBER_APPLY_DATE)  " \
                  "FROM V_TEAM_MEMBER " \
                  "WHERE EVENT_ID=" + str(event_id) + " " \
                  "AND MEMBER_STATUS = '" + team_member_status + "' " \
                  "ORDER by TEAM_MEMBER_FIRST_NAME, TEAM_MEMBER_LAST_NAME, SCHOOL_NAME " \
                  ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


def add_event_participant(event_id, ppant_user_id, current_user_id, ppant_role_type, has_coi, teleconferencing, tslot1, tslot2, tslot3, tslot4, app_db_web_location, juror_experience):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())
    ppant_status = "Requested"
    if ppant_role_type.lower() == 'volunteer':
        ppant_status = "Approved"
    _c.execute(
        "insert into event_participant (event_id, ppant_user_id, participant_role_type, ppant_status, has_coi, CREATED_BY, teleconference, TSLOT1, TSLOT2, TSLOT3, TSLOT4, juror_experience, created_date) "
        "values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (event_id, ppant_user_id, ppant_role_type, ppant_status, has_coi, current_user_id, teleconferencing, tslot1, tslot2, tslot3, tslot4, juror_experience, current_timestamp))

    ppant_id = _c.lastrowid

    _conn.commit()
    _conn.close()

    return ppant_id


def add_event_participant_with_coi(event_id, ppant_user_id, current_user_id, ppant_role_type, has_coi, coi_schools, teleconferencing, tslot1, tslot2, tslot3, tslot4, app_db_web_location, juror_experience):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())
    ppant_status = "Requested"
    if ppant_role_type.lower() == 'volunteer':
        ppant_status = "Approved"
    # add event participant
    _c.execute(
        "insert into event_participant (event_id, ppant_user_id, participant_role_type, ppant_status, has_coi, CREATED_BY, teleconference, TSLOT1, TSLOT2, TSLOT3, TSLOT4, juror_experience, created_date) "
        "values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (event_id, ppant_user_id, ppant_role_type, ppant_status, has_coi, current_user_id, teleconferencing, tslot1, tslot2, tslot3, tslot4, juror_experience, current_timestamp))

    # get participant id
    ppant_id = _c.lastrowid
    for item in coi_schools:
        school_id = int(item)
        _c.execute(
            "insert into conflict_of_interest (participant_id, coi_school_id, CREATED_BY, created_date) values(?, ?, ?, ?)",
            (ppant_id, school_id, current_user_id, current_timestamp))

    _conn.commit()
    _conn.close()


# add juror who is the team leader
def add_event_juror_as_tl(event_id, ppant_user_id, current_user_id, ppant_role_type, has_coi, coi_schools, teleconferencing, tslot1, tslot2, tslot3, tslot4, is_tl, tl_school_id, juror_experience, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())
    ppant_status = "Requested"
    # add event participant
    _c.execute(
        "insert into event_participant (event_id, ppant_user_id, participant_role_type, ppant_status, has_coi, CREATED_BY, teleconference, TSLOT1, TSLOT2, TSLOT3, TSLOT4, IS_TL, TL_SCHOOL_ID, juror_experience, created_date) "
        "values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (event_id, ppant_user_id, ppant_role_type, ppant_status, has_coi, current_user_id, teleconferencing, tslot1, tslot2, tslot3, tslot4, is_tl, tl_school_id, juror_experience, current_timestamp))

    # get participant id
    ppant_id = _c.lastrowid

    # add COI schools
    for item in coi_schools:
        school_id = int(item)
        _c.execute(
            "insert into conflict_of_interest (participant_id, coi_school_id, CREATED_BY, created_date) values(?, ?, ?, ?)",
            (ppant_id, school_id, current_user_id, current_timestamp))

    # update event_team table: team lead's juror id
    if is_tl == 1:
        _c.execute("UPDATE event_team SET tl1_juror_id = ?, last_updated_by = ?, last_updated_date = ? "
                   "WHERE event_id = ? and team_lead_id = ? and school_id = ?",
                   (ppant_id, current_user_id, current_timestamp, event_id, current_user_id, tl_school_id))
    elif is_tl == 2:
        pass

    _conn.commit()
    _conn.close()


def update_event_participant(event_id, ppant_id, teleconferencing, tslot1, tslot2, tslot3, tslot4, new_coi_schools, last_coi_count, current_user_id, juror_experience, app_db_web_location):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())

    # deal with last coi data if applicable
    if last_coi_count > 0:
        # remove original coi
        _c.execute("DELETE FROM conflict_of_interest WHERE participant_id = " + str(ppant_id) + ";")
    # deal with new coi data if applicable
    has_coi = 0
    if new_coi_schools is None or len(new_coi_schools) < 1:
        has_coi = 0
    else:
        has_coi = 1
        # add new_coi_schools to coi table
        for item in new_coi_schools:
            school_id = int(item)
            _c.execute("insert into conflict_of_interest (participant_id, coi_school_id, CREATED_BY, created_date) "
                       "values(?, ?, ?, ?)", (ppant_id, school_id, current_user_id, current_timestamp))

    # update participant base table
    _c.execute("UPDATE event_participant SET has_coi = ?, teleconference = ?, tslot1 = ?, tslot2 = ?, tslot3 = ?, "
               "tslot4 = ?, last_updated_by = ?, last_updated_date = ?, juror_experience=? WHERE participant_id = ?",
               (has_coi, teleconferencing, tslot1, tslot2, tslot3, tslot4, current_user_id, current_timestamp, juror_experience, ppant_id))

    _conn.commit()
    _conn.close()


def add_ppant_coi_team_members(participant_id, current_user_id, coi_team_members, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    for item in coi_team_members:
        tmp_list = list(item.split("-"))
        team_id = int(tmp_list[0])
        team_member_id = int(tmp_list[1])
        _c.execute(
            "insert into conflict_of_interest (participant_id, coi_team_id, coi_team_member_id, CREATED_BY) values(?, ?, ?, ?)",
            (participant_id, team_id, team_member_id, current_user_id))

    _conn.commit()
    _conn.close()


# Search participants that are under specific event and participant
def search_events_participatedbyme(event_id, curretn_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "EVENT_ID, EVENT_NAME, " \
              "PARTICIPANT_ID, HAS_COI, PARTICIPANT_ROLE_TYPE, PPANT_STATUS, " \
              "PARTICIPANT_FIRST_NAME, PARTICIPANT_LAST_NAME, PARTICIPANT_EMAIL " \
              "FROM V_EVENT_PARTICIPANT " \
              "WHERE EVENT_ID=" + str(event_id) + " " \
              "AND PPANT_USER_ID=" + str(curretn_user_id) + " " \
              "ORDER by PARTICIPANT_ROLE_TYPE " \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# Search participants and cois if applicable for specific event and participant
def search_events_ppant_n_cois(event_id, participant_user_id, ppant_id=0, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    if ppant_id == 0:
        command = "SELECT " \
                  "EVENT_ID, EVENT_NAME, " \
                  "PARTICIPANT_ID, HAS_COI, PARTICIPANT_ROLE_TYPE, PPANT_STATUS, " \
                  "PPANT_FIRST_NAME, PPANT_LAST_NAME, PPANT_EMAIL, " \
                  "COI_ID, COI_SCHOOL_ID, COI_SCHOOL_NAME, COI_SCHOOL_ADDRESS, COI_SCHOOL_CITY, COI_SCHOOL_PROVINCE, " \
                  "COI_SCHOOL_COUNTRY, COI_SCHOOL_POSTAL_CODE, COI_SCHOOL_STATUS, COI_SCHOOL_WEBSITE, COI_COMMENTS, " \
                  "PPANT_TELEC, TSLOT1, TSLOT2, TSLOT3, TSLOT4, TL_SCHOOL_ID, IS_TL, JUROR_LEVEL, JUROR_EXPERIENCE, IS_CHAIR " \
                  "FROM v_event_participant_cois_schools " \
                  "WHERE EVENT_ID=" + str(event_id) + " AND PPANT_USER_ID=" + str(participant_user_id) + \
                  " ORDER by PARTICIPANT_ROLE_TYPE, COI_SCHOOL_NAME COLLATE NOCASE;"
    else:
        command = "SELECT " \
                  "EVENT_ID, EVENT_NAME, " \
                  "PARTICIPANT_ID, HAS_COI, PARTICIPANT_ROLE_TYPE, PPANT_STATUS, " \
                  "PPANT_FIRST_NAME, PPANT_LAST_NAME, PPANT_EMAIL, " \
                  "COI_ID, COI_SCHOOL_ID, COI_SCHOOL_NAME, COI_SCHOOL_ADDRESS, COI_SCHOOL_CITY, COI_SCHOOL_PROVINCE, " \
                  "COI_SCHOOL_COUNTRY, COI_SCHOOL_POSTAL_CODE, COI_SCHOOL_STATUS, COI_SCHOOL_WEBSITE, COI_COMMENTS, " \
                  "PPANT_TELEC, TSLOT1, TSLOT2, TSLOT3, TSLOT4, TL_SCHOOL_ID, IS_TL, JUROR_LEVEL, JUROR_EXPERIENCE, IS_CHAIR " \
                  "FROM v_event_participant_cois_schools " \
                  "WHERE EVENT_ID=" + str(event_id) + " AND PPANT_USER_ID=" + str(participant_user_id) + \
                  " AND PARTICIPANT_ID=" + str(ppant_id) + \
                  " ORDER by PARTICIPANT_ROLE_TYPE, COI_SCHOOL_NAME COLLATE NOCASE;"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get event participant and associated cois for specific event and participant
def get_event_ppant_n_mycois(event_id, current_user_id, ppant_id=0, app_db_web_location=app_db_web_location_default):
    result_rows = search_events_ppant_n_cois(event_id, current_user_id, ppant_id, app_db_web_location)
    event_ppant_n_mycois = list()
    tmp_role_type = None
    tmp_has_coi = 0
    tmp_ppant_status = None
    tmp_coi_schools = list()
    tmp_telec = None
    tmp_tslot1 = None
    tmp_tslot2 = None
    tmp_tslot3 = None
    tmp_tslot4 = None
    tmp_juror_experience = None
    tmp_tl_school_id = 0
    tmp_ppant_id = 0
    tmp_is_chair = None

    for row in result_rows:
        if row[4] != tmp_role_type:
            if tmp_role_type is not None:
                tmp_tuple2 = (tmp_role_type, tmp_has_coi, tmp_ppant_status, tmp_coi_schools, tmp_telec, tmp_tslot1, tmp_tslot2, tmp_tslot3, tmp_tslot4, tmp_ppant_id, tmp_tl_school_id, tmp_juror_experience, tmp_is_chair)
                event_ppant_n_mycois.append(tmp_tuple2)
            tmp_role_type = row[4]
            tmp_has_coi = row[3]
            tmp_ppant_status = row[5]
            tmp_coi_schools = list()
            tmp_telec = row[20]
            tmp_tslot1 = row[21]
            tmp_tslot2 = row[22]
            tmp_tslot3 = row[23]
            tmp_tslot4 = row[24]
            tmp_ppant_id = row[2]
            tmp_tl_school_id = row[25]
            tmp_juror_experience = row[28]
            tmp_is_chair = row[29]

        if tmp_has_coi == 1:
            tmp_tuple_school = (row[9], row[10], row[11], row[12], row[13], row[14], row[19])
            tmp_coi_schools.append(tmp_tuple_school)

    if tmp_role_type is not None:
        tmp_tuple2 = (tmp_role_type, tmp_has_coi, tmp_ppant_status, tmp_coi_schools, tmp_telec, tmp_tslot1, tmp_tslot2, tmp_tslot3, tmp_tslot4, tmp_ppant_id, tmp_tl_school_id, tmp_juror_experience, tmp_is_chair)
        event_ppant_n_mycois.append(tmp_tuple2)

    return event_ppant_n_mycois


# Search all the participants and cois for specific event for data entry
def search_events_ppant_n_cois_for_data_entry(event_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    ppant_status = "Approved"
    ppant_role_type = "Volunteer"
    ppan_subtype = 99 # don't select sub_type=99 volunteers who are system side volunteer
    has_coi = 0
    timeslot = "Yes"
    _c = _conn.cursor()

    command = "SELECT " \
              "EVENT_ID, PARTICIPANT_ID, HAS_COI, PARTICIPANT_ROLE_TYPE, PPANT_STATUS, " \
              "PPANT_FIRST_NAME, PPANT_LAST_NAME, PPANT_EMAIL, PPANT_SUBTYPE, " \
              "TSLOT1, TSLOT2, TSLOT3, TSLOT4 " \
              "FROM v_event_participant_cois_schools " \
              "WHERE EVENT_ID=" + str(event_id) + " " \
              "AND PPANT_STATUS='" + ppant_status + "' " \
              "AND (PPANT_SUBTYPE <> " + str(ppan_subtype) + " OR PPANT_SUBTYPE IS NULL) " \
              "AND HAS_COI=" + str(has_coi) + " " \
              "AND TSLOT1='" + timeslot + "' " \
              "AND TSLOT2='" + timeslot + "' " \
              "AND TSLOT3='" + timeslot + "' " \
              "AND TSLOT4='" + timeslot + "' " \
              "AND PARTICIPANT_ROLE_TYPE='" + ppant_role_type + "' " \
              "ORDER by PARTICIPANT_ID" \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# Search all the participants and cois for specific event
def search_events_ppant_n_cois_for_volunteer(event_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    ppant_status = "Approved"
    ppant_role_type = "Volunteer"
    ppan_subtype = 99 # don't select sub_type=99 volunteers who are system side volunteer
    _c = _conn.cursor()

    command = "SELECT " \
              "EVENT_ID, EVENT_NAME, " \
              "PARTICIPANT_ID, HAS_COI, PARTICIPANT_ROLE_TYPE, PPANT_STATUS, " \
              "PPANT_FIRST_NAME, PPANT_LAST_NAME, PPANT_EMAIL, " \
              "COI_ID, COI_SCHOOL_ID, COI_SCHOOL_NAME, COI_SCHOOL_ADDRESS, COI_SCHOOL_CITY, COI_SCHOOL_PROVINCE, " \
              "COI_SCHOOL_COUNTRY, COI_SCHOOL_POSTAL_CODE, COI_SCHOOL_STATUS, COI_SCHOOL_WEBSITE, COI_COMMENTS, " \
              "PPANT_BACKGROUND, strftime('%Y-%m-%d',PPANT_DOB), strftime('%Y-%m-%d',PPANT_RQUEST_DATE), PPANT_INSTITUTION, " \
              "PHYSICS_BACKGROUND, TSLOT1, TSLOT2, TSLOT3, TSLOT4, PPANT_TELEC, TL_SCHOOL_ID, JUROR_EXPERIENCE, IS_CHAIR, PPANT_SUBTYPE " \
              "FROM v_event_participant_cois_schools " \
              "WHERE EVENT_ID=" + str(event_id) + " " \
              "AND PPANT_STATUS='" + ppant_status + "' " \
              "AND (PPANT_SUBTYPE <> " + str(ppan_subtype) + " OR PPANT_SUBTYPE IS NULL) " \
              "AND PARTICIPANT_ROLE_TYPE='" + ppant_role_type + "' " \
              "ORDER by PARTICIPANT_ID, COI_SCHOOL_NAME COLLATE NOCASE" \
              ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get event's all the qualified volunteers and associated cois for specific event
def get_event_ppant_n_cois_for_volunteer(event_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_events_ppant_n_cois_for_volunteer(event_id, app_db_web_location)
    event_ppant_n_mycois = list()
    tmp_coi_count = 0
    tmp_ppant_id = 0
    tmp_has_coi = 0
    tmp_ppant_status = None
    tmp_ppant_name = None
    tmp_ppant_background = None
    tmp_ppant_dob = None
    tmp_ppant_request_date = None
    tmp_ppant_institution = None
    tmp_ppant_physics_bg = None
    tmp_ppant_tslot1 = None
    tmp_ppant_tslot2 = None
    tmp_ppant_tslot3 = None
    tmp_ppant_tslot4 = None
    tmp_coi_schools = list()
    tmp_ppant_email = None
    tmp_ppant_telec = None
    tmp_tl_school_id = 0
    tmp_juror_expereince = None
    tmp_is_chair = None
    tmp_ppant_subtype = 0

    for row in result_rows:
        if row[2] != tmp_ppant_id:
            if tmp_ppant_id > 0:
                tmp_tuple2 = (tmp_ppant_id, tmp_has_coi, tmp_ppant_status, tmp_coi_schools, tmp_coi_count, tmp_ppant_name,
                              tmp_ppant_background, tmp_ppant_dob, tmp_ppant_request_date, tmp_ppant_institution,
                              tmp_ppant_physics_bg, tmp_ppant_tslot1, tmp_ppant_tslot2, tmp_ppant_tslot3, tmp_ppant_tslot4,
                              tmp_ppant_email, tmp_ppant_telec, tmp_tl_school_id, tmp_juror_expereince, tmp_is_chair, tmp_ppant_subtype)
                event_ppant_n_mycois.append(tmp_tuple2)
            tmp_ppant_id = row[2]
            tmp_has_coi = row[3]
            tmp_ppant_status = row[5]
            tmp_ppant_name = row[6] + " " + row[7]
            tmp_ppant_background = convert_background_text(row[20])
            tmp_ppant_dob = row[21]
            tmp_ppant_request_date = row[22]
            tmp_ppant_institution = row[23]
            tmp_ppant_physics_bg = row[24]
            tmp_ppant_tslot1 = row[25]
            tmp_ppant_tslot2 = row[26]
            tmp_ppant_tslot3 = row[27]
            tmp_ppant_tslot4 = row[28]
            tmp_coi_schools = list()
            tmp_ppant_email = row[8]
            tmp_ppant_telec = row[29]
            tmp_tl_school_id = row[30]
            tmp_juror_expereince = row[31]
            tmp_is_chair = row[32]
            tmp_ppant_subtype = row[33]
            tmp_coi_count = 0

        if tmp_has_coi == 1:
            tmp_tuple_school = (row[9], row[10], row[11], row[12], row[13], row[14], row[19])
            tmp_coi_count = tmp_coi_count + 1
            tmp_coi_schools.append(tmp_tuple_school)

    if tmp_ppant_id > 0:
        tmp_tuple2 = (tmp_ppant_id, tmp_has_coi, tmp_ppant_status, tmp_coi_schools, tmp_coi_count, tmp_ppant_name,
                      tmp_ppant_background, tmp_ppant_dob, tmp_ppant_request_date, tmp_ppant_institution, tmp_ppant_physics_bg,
                      tmp_ppant_tslot1, tmp_ppant_tslot2, tmp_ppant_tslot3, tmp_ppant_tslot4, tmp_ppant_email, tmp_ppant_telec, tmp_tl_school_id, tmp_juror_expereince, tmp_is_chair, tmp_ppant_subtype)
        event_ppant_n_mycois.append(tmp_tuple2)

    return event_ppant_n_mycois


# Search all the participants and cois for specific event
def search_events_ppant_n_cois_by_roletype(event_id, ppant_status, ppant_role_type, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    if ppant_status is None or len(ppant_status) < 1:
        command = "SELECT " \
                  "EVENT_ID, EVENT_NAME, " \
                  "PARTICIPANT_ID, HAS_COI, PARTICIPANT_ROLE_TYPE, PPANT_STATUS, " \
                  "PPANT_FIRST_NAME, PPANT_LAST_NAME, PPANT_EMAIL, " \
                  "COI_ID, COI_SCHOOL_ID, COI_SCHOOL_NAME, COI_SCHOOL_ADDRESS, COI_SCHOOL_CITY, COI_SCHOOL_PROVINCE, " \
                  "COI_SCHOOL_COUNTRY, COI_SCHOOL_POSTAL_CODE, COI_SCHOOL_STATUS, COI_SCHOOL_WEBSITE, COI_COMMENTS, " \
                  "PPANT_BACKGROUND, strftime('%Y-%m-%d',PPANT_DOB), strftime('%Y-%m-%d',PPANT_RQUEST_DATE), PPANT_INSTITUTION, " \
                  "PHYSICS_BACKGROUND, TSLOT1, TSLOT2, TSLOT3, TSLOT4, PPANT_TELEC, TL_SCHOOL_ID, JUROR_EXPERIENCE, IS_CHAIR, PPANT_SUBTYPE " \
                  "FROM v_event_participant_cois_schools " \
                  "WHERE EVENT_ID=" + str(event_id) + " " \
                  "AND PARTICIPANT_ROLE_TYPE='" + ppant_role_type + "' " \
                  "ORDER by IS_CHAIR DESC, PPANT_SUBTYPE DESC, PARTICIPANT_ID, COI_SCHOOL_NAME COLLATE NOCASE" \
                  ";"
    else:
        command = "SELECT " \
                  "EVENT_ID, EVENT_NAME, " \
                  "PARTICIPANT_ID, HAS_COI, PARTICIPANT_ROLE_TYPE, PPANT_STATUS, " \
                  "PPANT_FIRST_NAME, PPANT_LAST_NAME, PPANT_EMAIL, " \
                  "COI_ID, COI_SCHOOL_ID, COI_SCHOOL_NAME, COI_SCHOOL_ADDRESS, COI_SCHOOL_CITY, COI_SCHOOL_PROVINCE, " \
                  "COI_SCHOOL_COUNTRY, COI_SCHOOL_POSTAL_CODE, COI_SCHOOL_STATUS, COI_SCHOOL_WEBSITE, COI_COMMENTS, " \
                  "PPANT_BACKGROUND, strftime('%Y-%m-%d',PPANT_DOB), strftime('%Y-%m-%d',PPANT_RQUEST_DATE), PPANT_INSTITUTION, " \
                  "PHYSICS_BACKGROUND, TSLOT1, TSLOT2, TSLOT3, TSLOT4, PPANT_TELEC, TL_SCHOOL_ID, JUROR_EXPERIENCE, IS_CHAIR, PPANT_SUBTYPE " \
                  "FROM v_event_participant_cois_schools " \
                  "WHERE EVENT_ID=" + str(event_id) + " " \
                  "AND PPANT_STATUS='" + ppant_status + "' " \
                  "AND PARTICIPANT_ROLE_TYPE='" + ppant_role_type + "' " \
                  "ORDER by IS_CHAIR DESC, PPANT_SUBTYPE DESC, PARTICIPANT_ID, COI_SCHOOL_NAME COLLATE NOCASE" \
                  ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get event's all the participants and associated cois for specific event
def get_event_ppant_n_cois_by_roletype(event_id, ppant_status, ppant_role_type, app_db_web_location=app_db_web_location_default):
    result_rows = search_events_ppant_n_cois_by_roletype(event_id, ppant_status, ppant_role_type, app_db_web_location)
    event_ppant_n_mycois = list()
    tmp_coi_count = 0
    tmp_ppant_id = 0
    tmp_has_coi = 0
    tmp_ppant_status = None
    tmp_ppant_name = None
    tmp_ppant_background = None
    tmp_ppant_dob = None
    tmp_ppant_request_date = None
    tmp_ppant_institution = None
    tmp_ppant_physics_bg = None
    tmp_ppant_tslot1 = None
    tmp_ppant_tslot2 = None
    tmp_ppant_tslot3 = None
    tmp_ppant_tslot4 = None
    tmp_coi_schools = list()
    tmp_ppant_email = None
    tmp_ppant_telec = None
    tmp_tl_school_id = 0
    tmp_juror_expereince = None
    tmp_is_chair = None
    tmp_ppant_subtype = 0

    for row in result_rows:
        if row[2] != tmp_ppant_id:
            if tmp_ppant_id > 0:
                tmp_tuple2 = (tmp_ppant_id, tmp_has_coi, tmp_ppant_status, tmp_coi_schools, tmp_coi_count, tmp_ppant_name,
                              tmp_ppant_background, tmp_ppant_dob, tmp_ppant_request_date, tmp_ppant_institution,
                              tmp_ppant_physics_bg, tmp_ppant_tslot1, tmp_ppant_tslot2, tmp_ppant_tslot3, tmp_ppant_tslot4,
                              tmp_ppant_email, tmp_ppant_telec, tmp_tl_school_id, tmp_juror_expereince, tmp_is_chair, tmp_ppant_subtype)
                event_ppant_n_mycois.append(tmp_tuple2)
            tmp_ppant_id = row[2]
            tmp_has_coi = row[3]
            tmp_ppant_status = row[5]
            tmp_ppant_name = row[6] + " " + row[7]
            tmp_ppant_background = convert_background_text(row[20])
            tmp_ppant_dob = row[21]
            tmp_ppant_request_date = row[22]
            tmp_ppant_institution = row[23]
            tmp_ppant_physics_bg = row[24]
            tmp_ppant_tslot1 = row[25]
            tmp_ppant_tslot2 = row[26]
            tmp_ppant_tslot3 = row[27]
            tmp_ppant_tslot4 = row[28]
            tmp_coi_schools = list()
            tmp_ppant_email = row[8]
            tmp_ppant_telec = row[29]
            tmp_tl_school_id = row[30]
            tmp_juror_expereince = row[31]
            tmp_is_chair = row[32]
            tmp_ppant_subtype = row[33]
            tmp_coi_count = 0

        if tmp_has_coi == 1:
            tmp_tuple_school = (row[9], row[10], row[11], row[12], row[13], row[14], row[19])
            tmp_coi_count = tmp_coi_count + 1
            tmp_coi_schools.append(tmp_tuple_school)

    if tmp_ppant_id > 0:
        tmp_tuple2 = (tmp_ppant_id, tmp_has_coi, tmp_ppant_status, tmp_coi_schools, tmp_coi_count, tmp_ppant_name,
                      tmp_ppant_background, tmp_ppant_dob, tmp_ppant_request_date, tmp_ppant_institution, tmp_ppant_physics_bg,
                      tmp_ppant_tslot1, tmp_ppant_tslot2, tmp_ppant_tslot3, tmp_ppant_tslot4, tmp_ppant_email, tmp_ppant_telec, tmp_tl_school_id, tmp_juror_expereince, tmp_is_chair, tmp_ppant_subtype)
        event_ppant_n_mycois.append(tmp_tuple2)

    return event_ppant_n_mycois


# Search all the jurors and cois for specific event if is chair or not
def search_events_juror_n_cois_by_chair(event_id, is_chair, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    ppant_status = "Approved"
    ppant_role_type = "Juror"
    _c = _conn.cursor()

    if is_chair is None or len(is_chair) < 1:
        command = "SELECT " \
                  "EVENT_ID, EVENT_NAME, " \
                  "PARTICIPANT_ID, HAS_COI, PARTICIPANT_ROLE_TYPE, PPANT_STATUS, " \
                  "PPANT_FIRST_NAME, PPANT_LAST_NAME, PPANT_EMAIL, " \
                  "COI_ID, COI_SCHOOL_ID, COI_SCHOOL_NAME, COI_SCHOOL_ADDRESS, COI_SCHOOL_CITY, COI_SCHOOL_PROVINCE, " \
                  "COI_SCHOOL_COUNTRY, COI_SCHOOL_POSTAL_CODE, COI_SCHOOL_STATUS, COI_SCHOOL_WEBSITE, COI_COMMENTS, " \
                  "PPANT_BACKGROUND, strftime('%Y-%m-%d',PPANT_DOB), strftime('%Y-%m-%d',PPANT_RQUEST_DATE), PPANT_INSTITUTION, " \
                  "PHYSICS_BACKGROUND, TSLOT1, TSLOT2, TSLOT3, TSLOT4, PPANT_TELEC, TL_SCHOOL_ID, JUROR_EXPERIENCE, IS_CHAIR, PPANT_SUBTYPE " \
                  "FROM v_event_participant_cois_schools " \
                  "WHERE EVENT_ID=" + str(event_id) + " " \
                  "AND PARTICIPANT_ROLE_TYPE='" + ppant_role_type + "' " \
                  "ORDER by PARTICIPANT_ID, COI_SCHOOL_NAME COLLATE NOCASE" \
                  ";"
    else:
        command = "SELECT " \
                  "EVENT_ID, EVENT_NAME, " \
                  "PARTICIPANT_ID, HAS_COI, PARTICIPANT_ROLE_TYPE, PPANT_STATUS, " \
                  "PPANT_FIRST_NAME, PPANT_LAST_NAME, PPANT_EMAIL, " \
                  "COI_ID, COI_SCHOOL_ID, COI_SCHOOL_NAME, COI_SCHOOL_ADDRESS, COI_SCHOOL_CITY, COI_SCHOOL_PROVINCE, " \
                  "COI_SCHOOL_COUNTRY, COI_SCHOOL_POSTAL_CODE, COI_SCHOOL_STATUS, COI_SCHOOL_WEBSITE, COI_COMMENTS, " \
                  "PPANT_BACKGROUND, strftime('%Y-%m-%d',PPANT_DOB), strftime('%Y-%m-%d',PPANT_RQUEST_DATE), PPANT_INSTITUTION, " \
                  "PHYSICS_BACKGROUND, TSLOT1, TSLOT2, TSLOT3, TSLOT4, PPANT_TELEC, TL_SCHOOL_ID, JUROR_EXPERIENCE, IS_CHAIR, PPANT_SUBTYPE " \
                  "FROM v_event_participant_cois_schools " \
                  "WHERE EVENT_ID=" + str(event_id) + " " \
                  "AND PPANT_STATUS='" + ppant_status + "' " \
                  "AND IS_CHAIR='" + is_chair + "' " \
                  "AND PARTICIPANT_ROLE_TYPE='" + ppant_role_type + "' " \
                  "ORDER by PARTICIPANT_ID, COI_SCHOOL_NAME COLLATE NOCASE" \
                  ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get event's all the participants and associated cois for specific event - juror and if is chair or not
def get_event_juror_n_cois_by_chair(event_id, is_chair, app_db_web_location=app_db_web_location_default):
    result_rows = search_events_juror_n_cois_by_chair(event_id, is_chair, app_db_web_location)
    event_ppant_n_mycois = list()
    tmp_coi_count = 0
    tmp_ppant_id = 0
    tmp_has_coi = 0
    tmp_ppant_status = None
    tmp_ppant_name = None
    tmp_ppant_background = None
    tmp_ppant_dob = None
    tmp_ppant_request_date = None
    tmp_ppant_institution = None
    tmp_ppant_physics_bg = None
    tmp_ppant_tslot1 = None
    tmp_ppant_tslot2 = None
    tmp_ppant_tslot3 = None
    tmp_ppant_tslot4 = None
    tmp_coi_schools = list()
    tmp_ppant_email = None
    tmp_ppant_telec = None
    tmp_tl_school_id = 0
    tmp_juror_expereince = None
    tmp_is_chair = None
    tmp_ppant_subtype = 0

    for row in result_rows:
        if row[2] != tmp_ppant_id:
            if tmp_ppant_id > 0:
                tmp_tuple2 = (tmp_ppant_id, tmp_has_coi, tmp_ppant_status, tmp_coi_schools, tmp_coi_count, tmp_ppant_name,
                              tmp_ppant_background, tmp_ppant_dob, tmp_ppant_request_date, tmp_ppant_institution,
                              tmp_ppant_physics_bg, tmp_ppant_tslot1, tmp_ppant_tslot2, tmp_ppant_tslot3, tmp_ppant_tslot4,
                              tmp_ppant_email, tmp_ppant_telec, tmp_tl_school_id, tmp_juror_expereince, tmp_is_chair, tmp_ppant_subtype)
                event_ppant_n_mycois.append(tmp_tuple2)
            tmp_ppant_id = row[2]
            tmp_has_coi = row[3]
            tmp_ppant_status = row[5]
            tmp_ppant_name = row[6] + " " + row[7]
            tmp_ppant_background = convert_background_text(row[20])
            tmp_ppant_dob = row[21]
            tmp_ppant_request_date = row[22]
            tmp_ppant_institution = row[23]
            tmp_ppant_physics_bg = row[24]
            tmp_ppant_tslot1 = row[25]
            tmp_ppant_tslot2 = row[26]
            tmp_ppant_tslot3 = row[27]
            tmp_ppant_tslot4 = row[28]
            tmp_coi_schools = list()
            tmp_ppant_email = row[8]
            tmp_ppant_telec = row[29]
            tmp_tl_school_id = row[30]
            tmp_juror_expereince = row[31]
            tmp_is_chair = row[32]
            tmp_ppant_subtype = row[33]
            tmp_coi_count = 0

        if tmp_has_coi == 1:
            tmp_tuple_school = (row[9], row[10], row[11], row[12], row[13], row[14], row[19])
            tmp_coi_count = tmp_coi_count + 1
            tmp_coi_schools.append(tmp_tuple_school)

    if tmp_ppant_id > 0:
        tmp_tuple2 = (tmp_ppant_id, tmp_has_coi, tmp_ppant_status, tmp_coi_schools, tmp_coi_count, tmp_ppant_name,
                      tmp_ppant_background, tmp_ppant_dob, tmp_ppant_request_date, tmp_ppant_institution, tmp_ppant_physics_bg,
                      tmp_ppant_tslot1, tmp_ppant_tslot2, tmp_ppant_tslot3, tmp_ppant_tslot4, tmp_ppant_email, tmp_ppant_telec, tmp_tl_school_id, tmp_juror_expereince, tmp_is_chair, tmp_ppant_subtype)
        event_ppant_n_mycois.append(tmp_tuple2)

    return event_ppant_n_mycois


def search_event_rooms(event_id, usage_num=0, status_type=None, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    if status_type is not None and usage_num > 0:
        command = "SELECT " \
                  "EVENT_ROOM_ID, EVENT_ID, ROOM_NUMBER, ROOM_STATUS, ROOM_USAGE_NUM, ROOM_PURPOSE, ROOM_TELEC, " \
                  "ROOM_CAPACITY, ROOM_TYPE, ROOM_NOTES, ROOM_BUILDING, ROOM_ADDRESS " \
                  "FROM EVENT_ROOM " \
                  "WHERE EVENT_ID = " + str(event_id) + " " \
                  "AND ROOM_STATUS = '" + status_type + "' " \
                  "AND ROOM_USAGE_NUM = " + str(usage_num) + " " \
                  ";"
    elif status_type is not None:
        command = "SELECT " \
                  "EVENT_ROOM_ID, EVENT_ID, ROOM_NUMBER, ROOM_STATUS, ROOM_USAGE_NUM, ROOM_PURPOSE, ROOM_TELEC, " \
                  "ROOM_CAPACITY, ROOM_TYPE, ROOM_NOTES, ROOM_BUILDING, ROOM_ADDRESS " \
                  "FROM EVENT_ROOM " \
                  "WHERE EVENT_ID = " + str(event_id) + " " \
                  "AND ROOM_STATUS = '" + status_type + "' " \
                  ";"
    elif usage_num > 0:
        command = "SELECT " \
                  "EVENT_ROOM_ID, EVENT_ID, ROOM_NUMBER, ROOM_STATUS, ROOM_USAGE_NUM, ROOM_PURPOSE, ROOM_TELEC, " \
                  "ROOM_CAPACITY, ROOM_TYPE, ROOM_NOTES, ROOM_BUILDING, ROOM_ADDRESS " \
                  "FROM EVENT_ROOM " \
                  "WHERE EVENT_ID = " + str(event_id) + " " \
                  "AND ROOM_USAGE_NUM = " + str(usage_num) + " " \
                  ";"
    else:
        command = "SELECT " \
                  "EVENT_ROOM_ID, EVENT_ID, ROOM_NUMBER, ROOM_STATUS, ROOM_USAGE_NUM, ROOM_PURPOSE, ROOM_TELEC, " \
                  "ROOM_CAPACITY, ROOM_TYPE, ROOM_NOTES, ROOM_BUILDING, ROOM_ADDRESS " \
                  "FROM EVENT_ROOM " \
                  "WHERE EVENT_ID = " + str(event_id) + " " \
                  ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# This function is to update the plan status to Active
# And also update the following tables' status to Active for the selected plan_id
# - MTEAM, MROOM, MJUROR, MVOLUNTEER
# - MPAIR, MPAIR_TEAM, MAPIR_JUROR
def update_plan_status(plan_id, plan_status, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()
    current_timestamp = str(datetime.datetime.now())

    # update plan status to Active
    _c.execute("UPDATE EVENT_PLAN SET EVENT_PLAN_STATUS = ?, ACCEPTED_BY = ?, last_updated_by = ?, last_updated_date = ? WHERE EVENT_PLAN_ID = ?",
               (plan_status, current_user_id, current_user_id, current_timestamp, plan_id))
    # - MTEAM, MROOM, MJUROR, MVOLUNTEER
    _c.execute("UPDATE MTEAM SET MTEAM_STATUS = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ?",
               (plan_status, current_user_id, current_timestamp, plan_id))
    _c.execute("UPDATE MROOM SET MROOM_STATUS = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ?",
               (plan_status, current_user_id, current_timestamp, plan_id))
    _c.execute("UPDATE MJUROR SET MJUROR_STATUS = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ?",
               (plan_status, current_user_id, current_timestamp, plan_id))
    _c.execute("UPDATE MVOLUNTEER SET MVOLUNTEER_STATUS = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ?",
               (plan_status, current_user_id, current_timestamp, plan_id))
    # - MPAIR, MPAIR_TEAM, MAPIR_JUROR
    _c.execute("UPDATE MPAIR SET MPAIR_STATUS = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ?",
               (plan_status, current_user_id, current_timestamp, plan_id))
    _c.execute("UPDATE MPAIR_TEAM SET MPAIR_TEAM_STATUS = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ?",
               (plan_status, current_user_id, current_timestamp, plan_id))
    _c.execute("UPDATE MPAIR_JUROR SET MPAIR_JUROR_STATUS = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ?",
               (plan_status, current_user_id, current_timestamp, plan_id))

    _conn.commit()
    _conn.close()


# This function is to update the plan sub status to Released
def release_sm_plan(plan_id, plan_sub_status, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()
    current_timestamp = str(datetime.datetime.now())

    # update plan sub status
    _c.execute("UPDATE EVENT_PLAN SET EVENT_PLAN_SUB_STATUS = ?, ACCEPTED_BY = ?, last_updated_by = ?, last_updated_date = ? WHERE EVENT_PLAN_ID = ?",
               (plan_sub_status, current_user_id, current_user_id, current_timestamp, plan_id))

    # get mvolunteer list
    command = "SELECT DISTINCT " \
              "PLAN_ID, MVOLUNTEER_ID, PPANT_ID, PPANT_USER_ID, DATA_ENTRY " \
              "FROM v_mvolunteers " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "AND MVOLUNTEER_STATUS='Active' " \
              "ORDER by PPANT_ID" \
              ";"
    _c.execute(command)
    mvolunteer_result = _c.fetchall()

    for row in mvolunteer_result:
        current_ppant_id = row[2]
        current_ppant_user_id = row[3]
        ppant_subtype = 8
        if row[4] == "Yes":
            ppant_subtype = 9
            # add data entry role to user roles
            _c.execute(
                "insert into users_roles (user_id, role_id) values(?, ?)",
                (current_ppant_user_id, 3))
        # update ppant subtype at EVENT_PARTICIPANT table - do these when this plan is finalized
        _c.execute("UPDATE EVENT_PARTICIPANT SET SUB_TYPE = ?, last_updated_by = ?, last_updated_date = ? WHERE PARTICIPANT_ID = ?",
                   (ppant_subtype, current_user_id, current_timestamp, current_ppant_id))

    _conn.commit()
    _conn.close()


# This function is to update the plan sub status for publish or un-publish
def update_plan_sub_status_by_id(plan_id, plan_sub_status, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()
    current_timestamp = str(datetime.datetime.now())

    # update plan sub status
    _c.execute("UPDATE EVENT_PLAN SET EVENT_PLAN_SUB_STATUS = ?, last_updated_by = ?, last_updated_date = ? WHERE EVENT_PLAN_ID = ?",
               (plan_sub_status, current_user_id, current_timestamp, plan_id))

    _conn.commit()
    _conn.close()


# This function is to delete the proposed plan
# which will automatically delete the following tables' record that referenced to the selected plan_id
# - MTEAM, MROOM, MJUROR, (for SM)
# - MPAIR, MPAIR_TEAM, MPAIR_JUROR (for SM and FM)
def admin_delete_plan(event_id, plan_id, plan_status, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()
    current_timestamp = str(datetime.datetime.now())

    # delete the selected plan
    _c.execute("PRAGMA foreign_keys = ON")
    _c.execute("DELETE FROM EVENT_PLAN WHERE EVENT_ID = ? AND EVENT_PLAN_ID = ? AND EVENT_PLAN_STATUS = ?",
               (event_id, plan_id, plan_status))

    _conn.commit()
    _conn.close()


# This function is to save the proposed plan to the database:
# - Insert to EVENT_PLAN: return plan_id
# - insert to MTEAM: return mteam_id
# - insert to MROOM: return mroom_id
# - insert to MJUROR (CHAIR and moved juror)
# - insert to MVOLUNTEER
# - insert to MPAIR: return mpair_id
# - insert to MPAIRE_TEAM
# - insert to MPAIR_JUROR (CHAIR and moved juror)
def db_save_proposal(event_id, round_room_team_plan, juror_plan, volunteer_plan, moved_jurors_plan, current_user_id,
                     app_db_web_location=app_db_web_location_default, last_event_round_id=0):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()
    current_timestamp = str(datetime.datetime.now())
    round_plan = round_room_team_plan[0]
    room_plan = round_room_team_plan[1]
    team_plan = round_room_team_plan[2]

    # - Insert to EVENT_PLAN: return plan_id
    print("***1: Insert to EVENT_PLAN: return plan_id")
    _c.execute(
        "insert into EVENT_PLAN (EVENT_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?)",
        (event_id, current_user_id, current_timestamp))
    new_plan_id = _c.lastrowid

    # - insert to MTEAM: return mteam_id
    print("***2: insert to MTEAM: return mteam_id")
    new_mteam_id_list = []
    for team in team_plan:
        _c.execute(
            "insert into MTEAM (EVENT_TEAM_ID, MTEAM_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?)",
            (team['team_id'], team['team_code'], new_plan_id, current_user_id, current_timestamp))
        new_mteam_id = _c.lastrowid
        new_mteam_id_list.append(new_mteam_id)

    # - insert to MROOM: return mroom_id
    print("***3: insert to MROOM: return mroom_id")
    alpha = 'A'
    new_mroom_id_list = []
    for room in room_plan:
        tmp_school_id_list = None
        for school_id in room['room_cois']:
            if tmp_school_id_list is None:
                tmp_school_id_list = "-" + str(school_id)
            else:
                tmp_school_id_list = tmp_school_id_list + "-" + str(school_id)

        _c.execute(
            "insert into MROOM (EVENT_ROOM_ID, MROOM_CODE, MROOM_LABEL, MROOM_COI_SIDS, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?)",
            (room['room_id'], room['room_code'], alpha, tmp_school_id_list, new_plan_id, current_user_id, current_timestamp))
        new_mroom_id = _c.lastrowid
        new_mroom_id_list.append(new_mroom_id)
        alpha = chr(ord(alpha) + 1)

    # - insert to MJUROR for chair
    print("***4-1. insert to MJUROR for chairs")
    is_chair = "Yes"
    new_mjuror_id_list = []
    for juror in juror_plan:
        current_juror_code = juror['juror_code']
        current_ppant_id = juror['juror_info'][0]
        current_mroom_id = new_mroom_id_list[juror['room_code'] - 1]
        current_juror_timeslots = juror['juror_info'][11] + "-" + juror['juror_info'][12]+ "-" + juror['juror_info'][13] + "-" + juror['juror_info'][14]
        current_juror_cois = None
        for coi_school in juror['juror_info'][3]:
            if current_juror_cois is None:
                current_juror_cois = "-" + str(coi_school[1])
            else:
                current_juror_cois = current_juror_cois + "-" + str(coi_school[1])
        _c.execute(
            "insert into MJUROR (MJUROR_CODE, PPANT_ID, MROOM_ID, MJUROR_COI_SIDS, MJUROR_TIMESLOTS, PLAN_ID, IS_CHAIR, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (current_juror_code, current_ppant_id, current_mroom_id, current_juror_cois, current_juror_timeslots, new_plan_id, is_chair, current_user_id, current_timestamp))
        new_mjuror_id = _c.lastrowid
        new_mjuror_id_list.append(new_mjuror_id)

    # - insert to MJUROR for moved jurors
    print("***4-2. insert to MJUROR for moved jurors and associated MPAIR_JUROR")
    is_chair = "No"
    moved_juror_type = "Moved"
    #new_moved_juror_id_list = []
    for moved_juror in moved_jurors_plan:
        current_moved_juror_code = moved_juror['juror_code']
        current_moved_ppant_id = moved_juror['juror_info'][0]
        current_moved_juror_timeslots = moved_juror['juror_info'][11] + "-" + moved_juror['juror_info'][12]+ "-" + moved_juror['juror_info'][13] + "-" + moved_juror['juror_info'][14]
        current_moved_juror_cois = None
        for coi_school in moved_juror['juror_info'][3]:
            if current_moved_juror_cois is None:
                current_jmoved_uror_cois = "-" + str(coi_school[1])
            else:
                current_moved_juror_cois = current_moved_juror_cois + "-" + str(coi_school[1])
        _c.execute(
            "insert into MJUROR (MJUROR_CODE, PPANT_ID, MJUROR_COI_SIDS, MJUROR_TIMESLOTS, PLAN_ID, IS_CHAIR, MJUROR_TYPE, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (current_moved_juror_code, current_moved_ppant_id, current_moved_juror_cois, current_moved_juror_timeslots, new_plan_id, is_chair, moved_juror_type, current_user_id, current_timestamp))
        new_moved_juror_id = _c.lastrowid
        #new_mjuror_id_list.append(new_moved_juror_id)
        round_index = -1
        for room_code in moved_juror['round_room_codes']:
            round_index += 1
            if room_code > 0:
                current_round_code = round_index + 1
                current_event_round_id = last_event_round_id + current_round_code
                current_mroom_id = new_mroom_id_list[room_code - 1]
                _c.execute("insert into MPAIR_JUROR (MJUROR_ID, MJUROR_CODE, EVENT_ROUND_ID2, MROOM_ID2, PLAN_ID, MPAIR_JUROR_TYPE, CREATED_BY, CREATED_DATE) "
                           "values(?, ?, ?, ?, ?, ?, ?, ?)",
                           (new_moved_juror_id, current_moved_juror_code, current_event_round_id, current_mroom_id, new_plan_id, moved_juror_type, current_user_id, current_timestamp))

    # - insert to MJUROR for chair
    print("***5. insert to MVOLUNTEER for both data entriers and other volunteers")
    data_entry = "No"
    new_mvolunteer_id_list = []
    for volunteer in volunteer_plan:
        current_volunteer_code = volunteer['mvolunteer_code']
        current_ppant_id = volunteer['ppant_id']
        current_mroom_id = new_mroom_id_list[volunteer['mroom_code'] - 1]
        current_volunteer_timeslots = volunteer['timeslots']
        data_entry = volunteer['data_entry']
        ppant_subtype = volunteer['ppant_subtype']
        current_volunteer_cois = None
        for coi_school_id in volunteer['cois']:
            if current_volunteer_cois is None:
                current_volunteer_cois = "-" + str(coi_school_id)
            else:
                current_volunteer_cois = current_volunteer_cois + "-" + str(coi_school_id)
        _c.execute(
            "insert into MVOLUNTEER (MVOLUNTEER_CODE, PPANT_ID, MROOM_ID, MVOLUNTEER_COI_SIDS, MVOLUNTEER_TIMESLOTS, PLAN_ID, DATA_ENTRY, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (current_volunteer_code, current_ppant_id, current_mroom_id, current_volunteer_cois, current_volunteer_timeslots, new_plan_id, data_entry, current_user_id, current_timestamp))
        new_mvolunteer_id = _c.lastrowid
        new_mvolunteer_id_list.append(new_mvolunteer_id)

    # - insert to MPAIR, MAPIR TEAM, MPAIR JUROR for chairs
    print("***6. insert to insert to MPAIR, MAPIR TEAM, MPAIR JUROR for chairs")
    round_count = len(round_plan)
    for room in room_plan:
        current_room_code = room['room_code']
        current_room_jurors_code = room['jurors']
        current_mroom_id = new_mroom_id_list[current_room_code - 1]
        for round_index in range(round_count):
            current_round_code = round_index + 1
            current_event_round_id = last_event_round_id + current_round_code
            if room['room_team_matches_codes'][round_index] is not None:
                # get the team pair at the current room and current round
                current_team_pair_codes = room['room_team_matches_codes'][round_index]
                team_code_a = current_team_pair_codes[0]
                team_code_b = current_team_pair_codes[1]
                current_mpair_code_label = "-" + str(team_code_a) + "-" + str(team_code_b)
                current_mteam_a_id = new_mteam_id_list[team_code_a - 1]
                current_mteam_b_id = new_mteam_id_list[team_code_b - 1]
                tmp_school_ids_str = "-" + str(team_plan[team_code_a - 1]['school_id']) + "-" + str(
                    team_plan[team_code_b - 1]['school_id'])
                # add record to MPAIR
                _c.execute(
                    "insert into MPAIR (EVENT_ROUND_ID, MROOM_ID, MPAIR_CODE_LABEL, MPAIR_SIDS, PLAN_ID, CREATED_BY, CREATED_DATE) "
                    "values(?, ?, ?, ?, ?, ?, ?)",
                    (current_event_round_id, current_mroom_id, current_mpair_code_label, tmp_school_ids_str, new_plan_id, current_user_id, current_timestamp))
                new_mpair_id = _c.lastrowid
                # - insert to MPAIR_TEAM for team a and team b
                _c.execute(
                    "insert into MPAIR_TEAM (MPAIR_ID, MTEAM_ID, MTEAM_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?)",
                    (new_mpair_id, current_mteam_a_id, team_code_a, new_plan_id, current_user_id, current_timestamp))
                _c.execute(
                    "insert into MPAIR_TEAM (MPAIR_ID, MTEAM_ID, MTEAM_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?)",
                    (new_mpair_id, current_mteam_b_id, team_code_b, new_plan_id, current_user_id, current_timestamp))

                # - insert to MPAIR_JUROR for chairs
                for juror_code in current_room_jurors_code:
                    current_mjuror_id = new_mjuror_id_list[juror_code-1]
                    _c.execute(
                        "insert into MPAIR_JUROR (MPAIR_ID, MJUROR_ID, MJUROR_CODE, EVENT_ROUND_ID2, MROOM_ID2, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
                        (new_mpair_id, current_mjuror_id, juror_code, current_event_round_id, current_mroom_id, new_plan_id, current_user_id, current_timestamp))
            else:
                # no pair assigned to current room and current round
                # - insert to MPAIR_JUROR
                for juror_code in current_room_jurors_code:
                    current_mjuror_id = new_mjuror_id_list[juror_code-1]
                    _c.execute(
                        "insert into MPAIR_JUROR (MJUROR_ID, MJUROR_CODE, EVENT_ROUND_ID2, MROOM_ID2, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?)",
                        (current_mjuror_id, juror_code, current_event_round_id, current_mroom_id, new_plan_id, current_user_id, current_timestamp))

    _conn.commit()
    _conn.close()


# This function is to save the final match plan to the database:
# - Insert to EVENT_PLAN: return plan_id (type = fm)
# - mteam_id, mroom_id, mjuror_id
# - insert to MPAIR: return mpair_id
# - insert to MPAIRE_TEAM
# - insert to MPAIR_JUROR (CHAIR and moved juror)
def db_save_fm_proposal(event_id, fm_round_id, fm_room_id, jury, fm_teams, current_user_id,
                     app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()
    current_timestamp = str(datetime.datetime.now())

    # - Insert to EVENT_PLAN (2-fm, proposed): return plan_id
    print("***1: Insert to EVENT_PLAN: return plan_id")
    _c.execute(
        "insert into EVENT_PLAN (EVENT_ID, EVENT_PLAN_TYPE, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?)",
        (event_id, 2, current_user_id, current_timestamp))
    new_fm_plan_id = _c.lastrowid

    # - insert to MTEAM: return mteam_id
    # - insert to MROOM: return mroom_id
    # - insert to MJUROR for chair
    # - insert to MJUROR for moved jurors
    # - insert to MPAIR, MAPIR TEAM, MPAIR JUROR
    print("***2. insert to insert to MPAIR, MAPIR TEAM, MPAIR JUROR")
    # get team a, b, c
    team_code_a = fm_teams[0][1]
    team_code_b = fm_teams[1][1]
    team_code_c = fm_teams[2][1]
    current_mpair_code_label = "-" + str(team_code_a) + "-" + str(team_code_b) + "-" + str(team_code_c)
    tmp_school_ids_str = "-" + str(fm_teams[0][2]) + "-" + str(fm_teams[1][2]) + "-" + str(fm_teams[2][2])
    # add record to MPAIR - 1 new record
    _c.execute(
        "insert into MPAIR (EVENT_ROUND_ID, MROOM_ID, MPAIR_CODE_LABEL, MPAIR_SIDS, PLAN_ID, CREATED_BY, CREATED_DATE) "
        "values(?, ?, ?, ?, ?, ?, ?)",
        (fm_round_id, fm_room_id, current_mpair_code_label, tmp_school_ids_str, new_fm_plan_id,
         current_user_id, current_timestamp))
    new_fm_mpair_id = _c.lastrowid
    # - insert to MPAIR_TEAM for team a, team b and team c - 3 new records with same mpair_id
    _c.execute(
        "insert into MPAIR_TEAM (MPAIR_ID, MTEAM_ID, MTEAM_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?)",
        (new_fm_mpair_id, fm_teams[0][0], team_code_a, new_fm_plan_id, current_user_id, current_timestamp))
    _c.execute(
        "insert into MPAIR_TEAM (MPAIR_ID, MTEAM_ID, MTEAM_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?)",
        (new_fm_mpair_id, fm_teams[1][0], team_code_b, new_fm_plan_id, current_user_id, current_timestamp))
    _c.execute(
        "insert into MPAIR_TEAM (MPAIR_ID, MTEAM_ID, MTEAM_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?)",
        (new_fm_mpair_id, fm_teams[2][0], team_code_c, new_fm_plan_id, current_user_id, current_timestamp))

    # - insert to MPAIR_JUROR for current mpair- multiple new records with same mpair_id
    for juror in jury:
        current_mjuror_id = juror[0]
        juror_code = juror[1]
        _c.execute(
            "insert into MPAIR_JUROR (MPAIR_ID, MJUROR_ID, MJUROR_CODE, EVENT_ROUND_ID2, MROOM_ID2, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
            (new_fm_mpair_id, current_mjuror_id, juror_code, fm_round_id, fm_room_id, new_fm_plan_id, current_user_id, current_timestamp))

    _conn.commit()
    _conn.close()


# This function is to save the proposed plan to the database:
# - Insert to EVENT_PLAN: return plan_id
# - insert to MTEAM: return mteam_id
# - insert to MROOM: return mroom_id
# - insert to MPAIR: return mpair_id
# - insert to MPAIRE_TEAM
# - insert to MJUROR
# - insert to MPAIR_JUROR
def db_save_proposal_old(event_id, round_room_team_plan, juror_plan, juror_alternatives, current_user_id, app_db_web_location=app_db_web_location_default, last_event_round_id=0):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()
    current_timestamp = str(datetime.datetime.now())
    round_plan = round_room_team_plan[0]
    room_plan = round_room_team_plan[1]
    team_plan = round_room_team_plan[2]

    # - Insert to EVENT_PLAN: return plan_id
    print("***1: Insert to EVENT_PLAN: return plan_id")
    _c.execute(
        "insert into EVENT_PLAN (EVENT_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?)",
        (event_id, current_user_id, current_timestamp))
    new_plan_id = _c.lastrowid
    print("***--- new plan id = ", new_plan_id)

    # - insert to MTEAM: return mteam_id
    print("***2: insert to MTEAM: return mteam_id")
    new_mteam_id_list = []
    for team in team_plan:
        _c.execute(
            "insert into MTEAM (EVENT_TEAM_ID, MTEAM_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?)",
            (team['team_id'], team['team_code'], new_plan_id, current_user_id, current_timestamp))
        new_mteam_id = _c.lastrowid
        print("***--- new mteam_id = ", new_mteam_id)
        new_mteam_id_list.append(new_mteam_id)

    # - insert to MROOM: return mroom_id
    print("***3: insert to MROOM: return mroom_id")
    alpha = 'A'
    new_mroom_id_list = []
    for room in room_plan:
        tmp_school_id_list = None
        for school_id in room['room_cois']:
            if tmp_school_id_list is None:
                tmp_school_id_list = "-" + str(school_id)
            else:
                tmp_school_id_list = tmp_school_id_list + "-" + str(school_id)

        _c.execute(
            "insert into MROOM (EVENT_ROOM_ID, MROOM_CODE, MROOM_LABEL, MROOM_COI_SIDS, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?)",
            (room['room_id'], room['room_code'], alpha, tmp_school_id_list, new_plan_id, current_user_id, current_timestamp))
        new_mroom_id = _c.lastrowid
        print("***--- new mteam_id = ", new_mroom_id)
        new_mroom_id_list.append(new_mroom_id)
        alpha = chr(ord(alpha) + 1)

    # - insert to MJUROR
    print("***4. insert to insert to MJUROR")
    new_mjuror_id_list = []
    for juror in juror_plan:
        current_juror_code = juror['juror_code']
        current_ppant_id = juror['juror_info'][0]
        current_mroom_id = new_mroom_id_list[juror['room_code'] - 1]
        current_juror_timeslots = juror['juror_info'][11] + "-" + juror['juror_info'][12]+ "-" + juror['juror_info'][13] + "-" + juror['juror_info'][14]
        current_juror_cois = None
        for coi_school in juror['juror_info'][3]:
            if current_juror_cois is None:
                current_juror_cois = "-" + str(coi_school[1])
            else:
                current_juror_cois = current_juror_cois + "-" + str(coi_school[1])
        _c.execute(
            "insert into MJUROR (MJUROR_CODE, PPANT_ID, MROOM_ID, MJUROR_COI_SIDS, MJUROR_TIMESLOTS, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
            (current_juror_code, current_ppant_id, current_mroom_id, current_juror_cois, current_juror_timeslots, new_plan_id, current_user_id, current_timestamp))
        new_mjuror_id = _c.lastrowid
        print("***--- new mjuror_id = ", new_mjuror_id)
        new_mjuror_id_list.append(new_mjuror_id)

    # - insert to MPAIR: return mpair_id
    print("***5. insert to MPAIR: return mpair_id")
    for round in round_plan:
        current_event_round_id = last_event_round_id + round['round_code']

        i = -1
        for team in round['round_team_matches_code']:
            i += 1
            team_code_a = team[0]
            team_code_b = team[1]
            current_mroom_code_label = "-" + str(team_code_a) + "-" + str(team_code_b)
            current_mteam_a_id = new_mteam_id_list[team_code_a-1]
            current_mteam_b_id = new_mteam_id_list[team_code_b-1]
            current_mroom_id = new_mroom_id_list[round['round_team_matches_room_codes'][i] - 1]
            tmp_school_ids_str = "-" + str(round['round_team_matches_school_ids'][i][0]) + "-" + str(round['round_team_matches_school_ids'][i][1])
            # add record to MPAIR
            _c.execute(
                "insert into MPAIR (EVENT_ROUND_ID, MROOM_ID, MPAIR_CODE_LABEL, MPAIR_SIDS, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?)",
                (current_event_round_id, current_mroom_id, current_mroom_code_label, tmp_school_ids_str, new_plan_id, current_user_id, current_timestamp))
            new_mpair_id = _c.lastrowid
            # - insert to MPAIRE_TEAM for team a and team b
            print("***6. insert to MPAIRE_TEAM for team a and team b")
            _c.execute(
                "insert into MPAIR_TEAM (MPAIR_ID, MTEAM_ID, MTEAM_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?)",
                (new_mpair_id, current_mteam_a_id, team_code_a, new_plan_id, current_user_id, current_timestamp))
            _c.execute(
                "insert into MPAIR_TEAM (MPAIR_ID, MTEAM_ID, MTEAM_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?)",
                (new_mpair_id, current_mteam_b_id, team_code_b, new_plan_id, current_user_id, current_timestamp))

    _conn.commit()
    _conn.close()


# Search all the plans for specific event with optional status
def search_event_plan(event_id, plan_status, plan_type, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    if plan_type == 0:
        if plan_status is None or len(plan_status) < 1:
            command = "SELECT " \
                      "EVENT_ID, EVENT_PLAN_ID, EVENT_PLAN_STATUS, EVENT_PLAN_TYPE, EVENT_PLAN_SUB_STATUS " \
                      "FROM EVENT_PLAN " \
                      "WHERE EVENT_ID=" + str(event_id) + " " \
                      "ORDER by EVENT_PLAN_ID" \
                      ";"
        else:
            command = "SELECT " \
                      "EVENT_ID, EVENT_PLAN_ID, EVENT_PLAN_STATUS, EVENT_PLAN_TYPE, EVENT_PLAN_SUB_STATUS " \
                      "FROM EVENT_PLAN " \
                      "WHERE EVENT_ID=" + str(event_id) + " " \
                      "AND EVENT_PLAN_STATUS='" + plan_status + "' " \
                      "ORDER by EVENT_PLAN_ID" \
                      ";"
    else:
        if plan_status is None or len(plan_status) < 1:
            command = "SELECT " \
                      "EVENT_ID, EVENT_PLAN_ID, EVENT_PLAN_STATUS, EVENT_PLAN_TYPE, EVENT_PLAN_SUB_STATUS " \
                      "FROM EVENT_PLAN " \
                      "WHERE EVENT_ID=" + str(event_id) + " " \
                      "AND EVENT_PLAN_TYPE=" + str(plan_type) + " " \
                      "ORDER by EVENT_PLAN_ID" \
                      ";"
        else:
            command = "SELECT " \
                      "EVENT_ID, EVENT_PLAN_ID, EVENT_PLAN_STATUS, EVENT_PLAN_TYPE, EVENT_PLAN_SUB_STATUS " \
                      "FROM EVENT_PLAN " \
                      "WHERE EVENT_ID=" + str(event_id) + " " \
                      "AND EVENT_PLAN_STATUS='" + plan_status + "' " \
                      "AND EVENT_PLAN_TYPE=" + str(plan_type) + " " \
                      "ORDER by EVENT_PLAN_ID" \
                      ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# Search all the pairs for specific plan order to by round and room
def search_mpair(plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "PLAN_ID, MPAIR_ID, EVENT_ROUND_ID, MROOM_ID, MPAIR_CODE_LABEL, MPAIR_SIDS, MPAIR_LABEL " \
              "FROM MPAIR " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "ORDER by PLAN_ID, EVENT_ROUND_ID, MROOM_ID" \
              ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the pairs for specific event by room and by round
def get_mpair_by_room_round(plan_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_mpair(plan_id, app_db_web_location) # the search_mpair is by round and by room, need to create a new search function
    current_mroom_id = 0
    mpair_list = []
    tmp_round_list = []
    tmp_round_id = 0
    tmp_mpair_code_label = None
    tmp_mpair_sids = []
    for row in result_rows:
        if row[3] != current_mroom_id:
            if current_mroom_id >0:
                tmp_tuple2 = (current_mroom_id, tmp_round_list)
                mpair_list.append(tmp_tuple2)

            current_mroom_id = row[3]
            tmp_round_list = []

        tmp_tuple_round = (row[2], row[4], row[5]) # round_id, mpair_code_label, mpair_sids
        tmp_round_list.append(tmp_tuple_round)

    if current_mroom_id >0:
        tmp_tuple2 = (current_mroom_id, tmp_round_list)
        mpair_list.append(tmp_tuple2)

    return mpair_list


# get all the pairs for specific event by round and by room
def get_mpair_by_round_room(plan_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_mpair(plan_id, app_db_web_location)
    current_round_id = 0
    mpair_list = []
    tmp_round_list = []
    tmp_room_id = 0
    tmp_mpair_code_label = None
    tmp_mpair_sids = []
    for row in result_rows:
        if row[2] != current_round_id:
            if current_round_id >0:
                tmp_tuple2 = (current_round_id, tmp_round_list)
                mpair_list.append(tmp_tuple2)

            current_round_id = row[2]
            tmp_round_list = []

        tmp_tuple_round = (row[3], row[4], row[5]) # room_id, mpair_code_label, mpair_sids
        tmp_round_list.append(tmp_tuple_round)

    if current_round_id >0:
        tmp_tuple2 = (current_round_id, tmp_round_list)
        mpair_list.append(tmp_tuple2)

    return mpair_list


# Search all the pairs for specific plan order to by round and room code
def search_mpair_by_code(plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "PLAN_ID, MPAIR_ID, ROUND_CODE, MROOM_CODE, MPAIR_CODE_LABEL, MPAIR_SIDS, MPAIR_LABEL, " \
              "EVENT_ROUND_ID, MROOM_ID " \
              "FROM v_mpair " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "ORDER by PLAN_ID, EVENT_ROUND_ID, MROOM_ID" \
              ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the pairs for specific event by round and by room code
def get_mpair_by_round_room_code(plan_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_mpair(plan_id, app_db_web_location)
    current_round_id = 0
    mpair_list = []
    tmp_round_list = []
    tmp_room_id = 0
    tmp_mpair_code_label = None
    tmp_mpair_sids = []
    for row in result_rows:
        if row[2] != current_round_id:
            if current_round_id >0:
                tmp_tuple2 = (current_round_id, tmp_round_list)
                mpair_list.append(tmp_tuple2)

            current_round_id = row[2]
            tmp_round_list = []

        tmp_tuple_round = (row[3], row[4], row[5]) # room_id, mpair_code_label, mpair_sids
        tmp_round_list.append(tmp_tuple_round)

    if current_round_id >0:
        tmp_tuple2 = (current_round_id, tmp_round_list)
        mpair_list.append(tmp_tuple2)

    return mpair_list


# Search all the paired teams for specific plan order by round and team code
def search_mpair_team_by_round_team(plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "PLAN_ID, MPAIR_TEAM_ID, MPAIR_ID, EVENT_ROUND_ID, MROOM_ID, MPAIR_CODE_LABEL, " \
              "MTEAM_CODE, MTEAM_ID, MROOM_CODE, MROOM_LABEL, ROUND_CODE " \
              "FROM v_mpair_team " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "ORDER by PLAN_ID, ROUND_CODE, MTEAM_CODE" \
              ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the MPAIR TEAMS for specific plan by round and by team code
def get_mpair_team_by_round_team(plan_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_mpair_team_by_round_team(plan_id, app_db_web_location)
    current_round_id = 0
    mpair_list = []
    tmp_round_list = []
    for row in result_rows:
        if row[3] != current_round_id:
            if current_round_id >0:
                tmp_tuple2 = (current_round_id, tmp_round_list)
                mpair_list.append(tmp_tuple2)

            current_round_id = row[3]
            tmp_round_list = []

        tmp_tuple_round = (row[1], row[7], row[2], row[6], row[4]) # mpair_team_id, mteam_id, mpair_id, team_code, mroom_id
        tmp_round_list.append(tmp_tuple_round)

    if current_round_id >0:
        tmp_tuple2 = (current_round_id, tmp_round_list)
        mpair_list.append(tmp_tuple2)

    return mpair_list


# Search all the rooms for specific plan order by rooom_id
def search_mroom(plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "PLAN_ID, MROOM_ID, EVENT_ROOM_ID, MROOM_CODE, MROOM_LABEL, MROOM_COI_SIDS " \
              "FROM MROOM " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "ORDER by PLAN_ID, MROOM_ID" \
              ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# Search all the rooms for specific plan order by rooom_id
def search_mroom_assigned_to_data_entry(plan_id, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()
    data_entry = "Yes"
    ppant_user_id = current_user_id

    command = "SELECT DISTINCT " \
              "PLAN_ID, PPANT_USER_ID, MROOM_ID, MROOM_CODE, MROOM_LABEL, DATA_ENTRY " \
              "FROM v_mvolunteers " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "AND PPANT_USER_ID=" + str(ppant_user_id) + " " \
              "AND DATA_ENTRY='" + data_entry + "' " \
              "ORDER by PLAN_ID, PPANT_USER_ID, MROOM_CODE" \
              ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the mvolunteers for specific event by room
def get_mvolunteer_by_room(plan_id, mvolunteer_type=None, app_db_web_location=app_db_web_location_default):
    result_rows = search_mvolunteer_by_room(plan_id, mvolunteer_type, app_db_web_location)
    current_room_id = 0
    mvolunteer_list = []
    tmp_volunteer_list = []
    for row in result_rows:
        if row[3] != current_room_id:
            if current_room_id >0:
                tmp_tuple2 = (current_room_id, tmp_volunteer_list)
                mvolunteer_list.append(tmp_tuple2)

            current_room_id = row[3]
            tmp_volunteer_list = []
        # PLAN_ID, MVOLUNTEER_ID, MVOLUNTEER_CODE, MROOM_ID, MVOLUNTEER_TYPE, MVOLUNTEER_COI_SIDS, DATA_ENTRY
        tmp_tuple_volunteer = (row[1], row[2], row[3], row[4], row[5], row[6])
        tmp_volunteer_list.append(tmp_tuple_volunteer)

    if current_room_id >0:
        tmp_tuple2 = (current_room_id, tmp_volunteer_list)
        mvolunteer_list.append(tmp_tuple2)

    return mvolunteer_list


# Search all the jurors for specific plan order by room id
def search_mvolunteer_by_room(plan_id, mvolunteer_type=None, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    if mvolunteer_type is None:
        command = "SELECT " \
                  "PLAN_ID, MVOLUNTEER_ID, MVOLUNTEER_CODE, MROOM_ID, MVOLUNTEER_TYPE, MVOLUNTEER_COI_SIDS, DATA_ENTRY " \
                  "FROM MVOLUNTEER " \
                  "WHERE PLAN_ID=" + str(plan_id) + " " \
                  "ORDER by PLAN_ID, MROOM_ID, MVOLUNTEER_CODE" \
                  ";"
    else:
        command = "SELECT " \
                  "PLAN_ID, MVOLUNTEER_ID, MVOLUNTEER_CODE, MROOM_ID, MVOLUNTEER_TYPE, MVOLUNTEER_COI_SIDS, DATA_ENTRY " \
                  "FROM MVOLUNTEER " \
                  "WHERE PLAN_ID=" + str(plan_id) + " " \
                  "AND MVOLUNTEER_TYPE='" + mvolunteer_type + "' " \
                  "ORDER by PLAN_ID, MROOM_ID, MVOLUNTEER_CODE" \
                  ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the plans for specific event by round and by room
def get_mjuror_by_room(plan_id, mjuror_type=None, app_db_web_location=app_db_web_location_default):
    result_rows = search_mjuror_by_room(plan_id, mjuror_type, app_db_web_location)
    current_room_id = 0
    mjuror_list = []
    tmp_juror_list = []
    for row in result_rows:
        if row[3] != current_room_id:
            if current_room_id >0:
                tmp_tuple2 = (current_room_id, tmp_juror_list)
                mjuror_list.append(tmp_tuple2)

            current_room_id = row[3]
            tmp_juror_list = []

        tmp_tuple_juror = (row[1], row[2], row[3], row[4], row[5]) # MJUROR_ID, MJUROR_CODE, MROOM_ID, MJUROR_TYPE, MJUROR_COI_SIDS
        tmp_juror_list.append(tmp_tuple_juror)

    if current_room_id >0:
        tmp_tuple2 = (current_room_id, tmp_juror_list)
        mjuror_list.append(tmp_tuple2)

    return mjuror_list


# Search all the jurors for specific plan order by room id
def search_mjuror_by_room(plan_id, mjuror_type=None, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    if mjuror_type is None:
        command = "SELECT " \
                  "PLAN_ID, MJUROR_ID, MJUROR_CODE, MROOM_ID, MJUROR_TYPE, MJUROR_COI_SIDS " \
                  "FROM MJUROR " \
                  "WHERE PLAN_ID=" + str(plan_id) + " " \
                  "ORDER by PLAN_ID, MROOM_ID, MJUROR_CODE" \
                  ";"
    else:
        command = "SELECT " \
                  "PLAN_ID, MJUROR_ID, MJUROR_CODE, MROOM_ID, MJUROR_TYPE, MJUROR_COI_SIDS " \
                  "FROM MJUROR " \
                  "WHERE PLAN_ID=" + str(plan_id) + " " \
                  "AND MJUROR_TYPE='" + mjuror_type + "' " \
                  "ORDER by PLAN_ID, MROOM_ID, MJUROR_CODE" \
                  ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result

# Search all the mteams for specific plan order by mteam code
def search_mteam_by_code(plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "PLAN_ID, MTEAM_CODE, MTEAM_ID, EVENT_TEAM_ID, TEAM_NAME, SCHOOL_ID, SCHOOL_NAME " \
              "FROM v_team_mteam " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "ORDER by PLAN_ID, MTEAM_CODE" \
              ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# Search all the mpair_jurors for specific plan order by round and room id for specific type of juror: chair or moved juror
def search_mpair_jurors_by_round_room(plan_id, mjuror_type=None, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    if mjuror_type is None:
        command = "SELECT " \
                  "PLAN_ID, EVENT_ROUND_ID2, MROOM_ID2, MPAIR_ID, " \
                  "MPAIR_JUROR_ID, MJUROR_ID, MJUROR_CODE, MPAIR_JUROR_STATUS, MPAIR_JUROR_TYPE " \
                  "FROM MPAIR_JUROR " \
                  "WHERE PLAN_ID=" + str(plan_id) + " " \
                  "ORDER by PLAN_ID, EVENT_ROUND_ID2, MROOM_ID2, MJUROR_CODE" \
                  ";"
    else:
        command = "SELECT " \
                  "PLAN_ID, EVENT_ROUND_ID2, MROOM_ID2, MPAIR_ID, " \
                  "MPAIR_JUROR_ID, MJUROR_ID, MJUROR_CODE, MPAIR_JUROR_STATUS, MPAIR_JUROR_TYPE " \
                  "FROM MPAIR_JUROR " \
                  "WHERE PLAN_ID=" + str(plan_id) + " " \
                  "AND MPAIR_JUROR_TYPE='" + mjuror_type + "' " \
                  "ORDER by PLAN_ID, EVENT_ROUND_ID2, MROOM_ID2, MJUROR_CODE" \
                  ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# Search all the mpair_jurors for specific plan order by round and room id for specific type of juror: chair or moved juror
def get_mpair_jurors_by_round_room(plan_id, mjuror_type=None, app_db_web_location=app_db_web_location_default):
    result_rows = search_mpair_jurors_by_round_room(plan_id, mjuror_type, app_db_web_location)
    current_round_id = 0
    tmp_room_id = 0
    tmp_room_juror_code_list = []
    mjuror_list = []
    tmp_room_jurors = []
    tmp_juror_list = []
    for row in result_rows:
        if row[1] != current_round_id:
            if tmp_room_id > 0:
                tmp_tuple1 = (tmp_room_id, tmp_juror_list, tmp_room_juror_code_list)
                tmp_room_jurors.append(tmp_tuple1)

            if current_round_id >0:
                tmp_tuple2 = (current_round_id, tmp_room_jurors)
                mjuror_list.append(tmp_tuple2)

            current_round_id = row[1]
            tmp_room_id = row[2]
            tmp_room_jurors = []
            tmp_juror_list = []
            tmp_room_juror_code_list = []

        if row[2] != tmp_room_id:
            if tmp_room_id > 0:
                tmp_tuple1 = (tmp_room_id, tmp_juror_list, tmp_room_juror_code_list)
                tmp_room_jurors.append(tmp_tuple1)

            tmp_juror_list=[]
            tmp_room_juror_code_list = []
            tmp_room_id = row[2]

        #PLAN_ID, EVENT_ROUND_ID2, MROOM_ID2, MPAIR_ID
        #MPAIR_JUROR_ID, MJUROR_ID, MJUROR_CODE, MPAIR_JUROR_STATUS, MPAIR_JUROR_TYPE
        tmp_tuple_juror = (row[4], row[5], row[6], row[7], row[8])
        tmp_juror_list.append(tmp_tuple_juror)
        tmp_room_juror_code_list.append(row[6])

    if tmp_room_id > 0:
        tmp_tuple1 = (tmp_room_id, tmp_juror_list, tmp_room_juror_code_list)
        tmp_room_jurors.append(tmp_tuple1)

    if current_round_id > 0:
        tmp_tuple2 = (current_round_id, tmp_room_jurors)
        mjuror_list.append(tmp_tuple2)

    return mjuror_list


# Search all the mteams for specific plan order by mteam code from view
def search_mteams(plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "EVENT_ID, PLAN_ID, MTEAM_CODE, MTEAM_ID, EVENT_TEAM_ID, TEAM_NAME, " \
              "SCHOOL_ID, SCHOOL_NAME, SCHOOL_CITY, SCHOOL_PROVINCE, " \
              "TEAM_MEMBER_ID, TEAM_MEMBER_USER_ID, TEAM_MEMBER_FIRST_NAME, TEAM_MEMBER_LAST_NAME, TEAM_MEMBER_DOB, " \
              "TEAM_LEAD_ID, TEAM_LEAD_FIRST_NAME, TEAM_LEAD_LAST_NAME, TEAM_LEAD_EMAIL, TEAM_LEAD_TELEC " \
              "FROM v_mteams " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "AND MEMBER_STATUS='Approved' " \
              "ORDER by PLAN_ID, MTEAM_CODE, TEAM_MEMBER_ID" \
              ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the mteams for specific plan order by mteam code from view
def get_mteams(plan_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_mteams(plan_id, app_db_web_location)
    current_mteam_code = 0
    tmp_mteam_name = None
    mteam_list = []
    tmp_member_list = []
    tmp_team_info = ()
    for row in result_rows:
        if row[2] != current_mteam_code:
            if current_mteam_code >0:
                tmp_tuple2 = (current_mteam_code, tmp_mteam_name, tmp_team_info, tmp_member_list)
                mteam_list.append(tmp_tuple2)

            current_mteam_code = row[2]
            tmp_mteam_name = row[5]
            #EVENT_ID, PLAN_ID, MTEAM_CODE, MTEAM_ID, EVENT_TEAM_ID, TEAM_NAME 0-5
            # team lead info: 15-19
            tmp_team_info = (row[0], row[1], row[3], row[4], row[15], row[16] + " " + row[17], row[18], row[19], row[6], row[7], row[8], row[9])
            tmp_member_list = []
        #"SCHOOL_ID, SCHOOL_NAME, SCHOOL_CITY, SCHOOL_PROVINCE, " - index 6-9
        #"TEAM_MEMBER_ID, TEAM_MEMBER_USER_ID, TEAM_MEMBER_FIRST_NAME, TEAM_MEMBER_LAST_NAME, TEAM_MEMBER_DOB, " - index 10-14
        # old good version: tmp_tuple_member = (row[10], row[11], row[12] + " " + row[13], row[14], row[6], row[7], row[8], row[9])
        tmp_tuple_member = (row[10], row[11], row[12] + " " + row[13], row[14], row[6], row[7], row[8], row[9])
        tmp_member_list.append(tmp_tuple_member)

    if current_mteam_code >0:
        tmp_tuple2 = (current_mteam_code, tmp_mteam_name, tmp_team_info, tmp_member_list)
        mteam_list.append(tmp_tuple2)

    return mteam_list


# Search all the mrooms for specific plan order by mroom code from view
def search_mrooms(plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "EVENT_ID, PLAN_ID, EVENT_ROOM_ID, MROOM_CODE, MROOM_LABEL, MROOM_COI_SIDS, MROOM_STATUS, " \
              "ROOM_NUMBER, ROOM_PURPOSE, ROOM_STATUS, ROOM_TELEC, ROOM_TYPE, ROOM_USAGE_NUM, MROOM_ID " \
              "FROM v_mrooms " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "ORDER by PLAN_ID, MROOM_CODE" \
              ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the mrooms for specific plan order by mroom code from view
def get_mrooms(plan_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_mrooms(plan_id, app_db_web_location)
    current_mteam_code = 0
    tmp_mteam_name = None
    mroom_list = []
    tmp_member_list = []
    tmp_team_info = ()
    for row in result_rows:
        #"EVENT_ID, PLAN_ID, EVENT_ROOM_ID, MROOM_CODE, MROOM_LABEL, MROOM_COI_SIDS, MROOM_STATUS, " - 0-
        #"ROOM_NUMBER, ROOM_PURPOSE, ROOM_STATUS, ROOM_TELEC, ROOM_TYPE, ROOM_USAGE_NUM, MROOM_ID " 7-13
        tmp_room_info = (row[0], row[1], row[2], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13])
        tmp_room = (row[3], row[4], tmp_room_info)
        mroom_list.append(tmp_room)

    return mroom_list


# Search all the mjuros for specific plan order by mjuror code from view
def search_mjurors(plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "EVENT_ID, PLAN_ID, MJUROR_ID, MJUROR_CODE, PPANT_ID, PPANT_USER_ID, " \
              "MJUROR_STATUS, MJUROR_TIMESLOTS, MJUROR_TYPE, PPANT_FIRST_NAME, PPANT_LAST_NAME, " \
              "IS_CHAIR, CHAIR_ROOM_ID, " \
              "HAS_COI, MJUROR_COI_SIDS, COI_SCHOOL_ID, COI_SCHOOL_NAME, COI_SCHOOL_CITY, COI_SCHOOL_PROVINCE, " \
              "IS_TL, JUROR_EXPERIENCE, PARTICIPANT_ROLE_TYPE " \
              "FROM v_mjurors " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "ORDER by PLAN_ID, MJUROR_CODE, IS_CHAIR DESC, COI_SCHOOL_ID" \
              ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the mjuros for specific plan order by mjuror code from view
def get_mjurors(plan_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_mjurors(plan_id, app_db_web_location)
    current_mjuror_code = 0
    tmp_mjuror_name = None
    tmp_has_cois = 0
    mjuror_list = []
    tmp_juror_cois_list = []
    tmp_juror_info = ()
    for row in result_rows:
        if row[3] != current_mjuror_code:
            if current_mjuror_code >0:
                tmp_tuple2 = (current_mjuror_code, tmp_mjuror_name, tmp_juror_info, tmp_has_cois, tmp_juror_cois_list)
                mjuror_list.append(tmp_tuple2)

            current_mjuror_code = row[3]
            tmp_mjuror_name = row[9] + " " + row[10]
            tmp_has_cois = row[13]
            #"EVENT_ID, PLAN_ID, MJUROR_ID, MJUROR_CODE, PPANT_ID, PPANT_USER_ID, " \ 0-5
            #"MJUROR_STATUS, MJUROR_TIMESLOTS, MJUROR_TYPE, PPANT_FIRST_NAME, PPANT_LAST_NAME, " \ 6-10
            #"IS_CHAIR, CHAIR_ROOM_ID, **CHAIR_ROOM_CODE, CHAIR_ROOM_LABEL,** " \ 11-14 **- 2: 11-12
            #"HAS_COI, MJUROR_COI_SIDS, COI_SCHOOL_ID, COI_SCHOOL_NAME, COI_SCHOOL_CITY, COI_SCHOOL_PROVINCE, " \ 15-20 ** 13-18
            #"IS_TL, JUROR_EXPERIENCE, PARTICIPANT_ROLE_TYPE " \ 21-23 ** 19-21
            tmp_juror_info = (row[0], row[1], row[2], row[4], row[5], row[7], row[8], row[11], row[12], row[14], row[19], row[21])
            tmp_juror_cois_list = []
        # "HAS_COI, MJUROR_COI_SIDS, COI_SCHOOL_ID, COI_SCHOOL_NAME, COI_SCHOOL_CITY, COI_SCHOOL_PROVINCE, " 15-20 ** 13-18
        tmp_tuple_juror_cois = (row[15], row[16], row[17], row[18])
        tmp_juror_cois_list.append(tmp_tuple_juror_cois)

    if current_mjuror_code >0:
        tmp_tuple2 = (current_mjuror_code, tmp_mjuror_name, tmp_juror_info, tmp_has_cois, tmp_juror_cois_list)
        mjuror_list.append(tmp_tuple2)

    return mjuror_list


# Search all the mvolunteers for specific plan order by mroom code from view
def search_mvolunteers(plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "EVENT_ID, PLAN_ID, MROOM_ID, MROOM_CODE, MROOM_LABEL, MVOLUNTEER_ID, MVOLUNTEER_CODE, PPANT_ID, PPANT_USER_ID, " \
              "HAS_COI, MVOLUNTEER_COI_SIDS, COI_SCHOOL_ID, COI_SCHOOL_NAME, COI_SCHOOL_CITY, COI_SCHOOL_PROVINCE, " \
              "DATA_ENTRY, MVOLUNTEER_STATUS, MVOLUNTEER_TIMESLOTS, MVOLUNTEER_TYPE, PPANT_DOB, " \
              "PPANT_FIRST_NAME, PPANT_LAST_NAME, IS_TL, PARTICIPANT_ROLE_TYPE " \
              "FROM v_mvolunteers " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "ORDER by PLAN_ID, MROOM_CODE, DATA_ENTRY DESC, MVOLUNTEER_ID, COI_SCHOOL_ID" \
              ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the mvolunteers for specific plan order by mroom code from view
def get_mvolunteers(plan_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_mvolunteers(plan_id, app_db_web_location)
    current_mroom_code = 0
    tmp_mroom_label = None
    tmp_mvolunteer_id = 0
    mvolunteer_list = []
    tmp_room_volunteers = []
    tmp_volunteer_cois_list = []
    tmp_mvolunteer_code = 0
    tmp_has_cois = 0
    tmp_mvolunteer_info = ()
    tmp_mvolunteer_name = None
    for row in result_rows:
        if row[3] != current_mroom_code:
            if tmp_mvolunteer_id > 0:
                tmp_tuple1 = (tmp_mvolunteer_id, tmp_mvolunteer_code, tmp_mvolunteer_name, tmp_mvolunteer_info, tmp_has_cois, tmp_volunteer_cois_list)
                tmp_room_volunteers.append(tmp_tuple1)

            if current_mroom_code >0:
                tmp_tuple2 = (current_mroom_code, tmp_mroom_label, tmp_room_volunteers)
                mvolunteer_list.append(tmp_tuple2)

            current_mroom_code = row[3]
            tmp_room_volunteers = []
            tmp_volunteer_cois_list = []
            tmp_mroom_label = row[4]
            tmp_mvolunteer_id = row[5]
            tmp_mvolunteer_code = row[6]
            tmp_has_cois = row[9]
            tmp_mvolunteer_name = row[20] + " " + row[21]
            #"EVENT_ID, PLAN_ID, MROOM_ID, MROOM_CODE, MROOM_LABEL, MVOLUNTEER_ID, MVOLUNTEER_CODE, PPANT_ID, PPANT_USER_ID, " 0-8
            #"HAS_COI, MVOLUNTEER_COI_SIDS, COI_SCHOOL_ID, COI_SCHOOL_NAME, COI_SCHOOL_CITY, COI_SCHOOL_PROVINCE, " \ 9-14
            #"DATA_ENTRY, MVOLUNTEER_STATUS, MVOLUNTEER_TIMESLOTS, MVOLUNTEER_TYPE, PPANT_DOB, " \ 15-19
            #"PPANT_FIRST_NAME, PPANT_LAST_NAME, IS_TL, PARTICIPANT_ROLE_TYPE " 20-23
            tmp_mvolunteer_info = (row[0], row[1], row[2], row[7], row[8], row[10], row[15], row[16], row[17], row[18], row[23])

        if row[5] != tmp_mvolunteer_id:
            if tmp_mvolunteer_id > 0:
                tmp_tuple1 = (tmp_mvolunteer_id, tmp_mvolunteer_code, tmp_mvolunteer_name, tmp_mvolunteer_info, tmp_has_cois, tmp_volunteer_cois_list)
                tmp_room_volunteers.append(tmp_tuple1)

            tmp_volunteer_cois_list=[]
            tmp_mvolunteer_id = row[5]
            tmp_mvolunteer_code = row[6]
            tmp_has_cois = row[9]
            tmp_mvolunteer_name = row[20] + " " + row[21]
            tmp_mvolunteer_info = (row[0], row[1], row[2], row[7], row[8], row[10], row[15], row[16], row[17], row[18], row[23])

        #"HAS_COI, MVOLUNTEER_COI_SIDS, COI_SCHOOL_ID, COI_SCHOOL_NAME, COI_SCHOOL_CITY, COI_SCHOOL_PROVINCE, " - 9-14
        tmp_tuple_cois = (row[11], row[12], row[13], row[14])
        tmp_volunteer_cois_list.append(tmp_tuple_cois)

    if tmp_mvolunteer_id > 0:
        tmp_tuple1 = (tmp_mvolunteer_id, tmp_mvolunteer_code, tmp_mvolunteer_name, tmp_mvolunteer_info, tmp_has_cois, tmp_volunteer_cois_list)
        tmp_room_volunteers.append(tmp_tuple1)

    if current_mroom_code > 0:
        tmp_tuple2 = (current_mroom_code, tmp_mroom_label, tmp_room_volunteers)
        mvolunteer_list.append(tmp_tuple2)

    return mvolunteer_list


# Get and search volunteer schedule based on ppant_user_id
def get_volunteer_schedue(event_id, plan_id, ppant_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()
    # search MJUROR_CODE by PPANT_USER_ID
    command = "SELECT DISTINCT MVOLUNTEER_CODE, MROOM_CODE, MROOM_LABEL, DATA_ENTRY, PPANT_FIRST_NAME, PPANT_LAST_NAME " \
              "FROM v_mvolunteers " \
              "WHERE EVENT_ID=" + str(event_id) + " " \
              "AND PLAN_ID=" + str(plan_id) + " " \
              "AND PPANT_USER_ID=" + str(ppant_user_id) + ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    volunteer_schedule = None
    for row in result:
        volunteer_schedule = (row[0], row[1], row[2], row[3], row[4], row[5])
        break

    return volunteer_schedule


# Search juror schedule based on ppant_user_id
def search_juror_schedue(event_id, plan_id, ppant_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()
    # search MJUROR_CODE by PPANT_USER_ID
    command = "SELECT DISTINCT MJUROR_CODE " \
              "FROM v_mjurors " \
              "WHERE EVENT_ID=" + str(event_id) + " " \
              "AND PLAN_ID=" + str(plan_id) + " " \
              "AND PPANT_USER_ID=" + str(ppant_user_id) + ";"

    _c.execute(command)
    result = _c.fetchall()
    juror_code = 0
    for row in result:
        juror_code = row[0]
        break

    if juror_code > 0:
        command = "SELECT " \
                  "MPAIR_ID, EVENT_ROUND_ID2, MROOM_ID2, " \
                  "ROUND_CODE, MROOM_CODE, MJUROR_CODE, MJUROR_ID, MPAIR_JUROR_TYPE " \
                  "FROM v_mpair_juror " \
                  "WHERE PLAN_ID=" + str(plan_id) + " " \
                  "AND MJUROR_CODE=" + str(juror_code) + " " \
                  "ORDER by ROUND_CODE, MROOM_CODE" \
                  ";"
        _c.execute(command)
        result = _c.fetchall()

        _conn.commit()
        _conn.close()

        return result
    else:
        return None


# get juror schedule based on ppant_user_id
def get_juror_schedue(event_id, plan_id, ppant_user_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_juror_schedue(event_id, plan_id, ppant_user_id, app_db_web_location)
    juror_schedule = []
    juror_code = result_rows[0][5]
    for row in result_rows:
        juror_schedule.append(row[4])

    return (juror_code, juror_schedule)


# Search my team schedule based on ppant_user_id
def search_my_team_schedue(event_id, plan_id, ppant_user_id, schedule_type, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()
    command = None
    if schedule_type == 1 or schedule_type == 13:
        # search mteam_code(s) by team_lead_id
        command = "SELECT DISTINCT MTEAM_CODE " \
                  "FROM v_mteams " \
                  "WHERE EVENT_ID=" + str(event_id) + " " \
                  "AND PLAN_ID=" + str(plan_id) + " " \
                  "AND TEAM_LEAD_ID=" + str(ppant_user_id) + " " \
                  "AND MTEAM_STATUS='Active' " \
                  "ORDER by MTEAM_CODE;"
    elif schedule_type == 2:
        # search mteam_code by team_member_user_id
        command = "SELECT DISTINCT MTEAM_CODE " \
                  "FROM v_mteams " \
                  "WHERE EVENT_ID=" + str(event_id) + " " \
                  "AND PLAN_ID=" + str(plan_id) + " " \
                  "AND TEAM_MEMBER_USER_ID=" + str(ppant_user_id) + " " \
                  "AND MTEAM_STATUS='Active' " \
                  "ORDER by MTEAM_CODE;"
    else:
        return None

    _c.execute(command)
    result = _c.fetchall()
    my_team_codes = []
    for row in result:
        my_team_codes.append(row[0])

    if my_team_codes is not None and len(my_team_codes) > 0:
        if len(my_team_codes) == 1:
            mteam_code = my_team_codes[0]
            command = "SELECT " \
                      "PLAN_ID, MPAIR_TEAM_ID, MPAIR_ID, EVENT_ROUND_ID, MROOM_ID, MPAIR_CODE_LABEL, " \
                      "MTEAM_CODE, MTEAM_ID, MROOM_CODE, MROOM_LABEL, ROUND_CODE " \
                      "FROM v_mpair_team " \
                      "WHERE PLAN_ID=" + str(plan_id) + " " \
                      "AND MTEAM_CODE=" + str(mteam_code) + " " \
                      "ORDER by PLAN_ID, MTEAM_CODE, ROUND_CODE, MROOM_CODE" \
                      ";"
        else:
            command = "SELECT " \
                      "PLAN_ID, MPAIR_TEAM_ID, MPAIR_ID, EVENT_ROUND_ID, MROOM_ID, MPAIR_CODE_LABEL, " \
                      "MTEAM_CODE, MTEAM_ID, MROOM_CODE, MROOM_LABEL, ROUND_CODE " \
                      "FROM v_mpair_team " \
                      "WHERE PLAN_ID=" + str(plan_id) + " "
            i = 0
            for mteam_code in my_team_codes:
                i += 1
                if i == 1:
                    command = command + "AND (MTEAM_CODE=" + str(mteam_code) + " "
                else:
                    command = command + "OR MTEAM_CODE=" + str(mteam_code) + " "
            command = command + ") " \
                      "ORDER by PLAN_ID, MTEAM_CODE, ROUND_CODE, MROOM_CODE" \
                      ";"

        _c.execute(command)
        result = _c.fetchall()

        _conn.commit()
        _conn.close()

        return result
    else:
        return None


# get my team schedule based on ppant_user_id
def get_my_team_schedue(event_id, plan_id, ppant_user_id, schedule_type, app_db_web_location=app_db_web_location_default):
    result_rows = search_my_team_schedue(event_id, plan_id, ppant_user_id, schedule_type, app_db_web_location)
    current_mteam_code = 0
    my_team_schedule = []
    tmp_team_round_room = []
    for row in result_rows:
        if row[6] != current_mteam_code:
            if current_mteam_code >0:
                tmp_tuple2 = (current_mteam_code, tmp_team_round_room)
                my_team_schedule.append(tmp_tuple2)

            current_mteam_code = row[6]
            tmp_team_round_room = []
        tmp_team_round_room.append(row[8])

    if current_mteam_code >0:
        tmp_tuple2 = (current_mteam_code, tmp_team_round_room)
        my_team_schedule.append(tmp_tuple2)

    return my_team_schedule


# Search all the paired teams for specific plan order to by team code
def search_mpair_by_team(plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "PLAN_ID, MPAIR_TEAM_ID, MPAIR_ID, EVENT_ROUND_ID, MROOM_ID, MPAIR_CODE_LABEL, " \
              "MTEAM_CODE, MTEAM_ID, MROOM_CODE, MROOM_LABEL, ROUND_CODE, " \
              "MPAIR_STAGE_STATUS_CODE, SP, FIGHT_WON " \
              "FROM v_mpair_team " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "ORDER by MTEAM_CODE, MPAIR_TEAM_ID" \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the teams' ranking for specific plan id and selective matches
def get_sm_team_rank(plan_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_mpair_by_team(plan_id, app_db_web_location)
    current_mteam_code = 0
    tmp_mteam_total_scores = 0
    tmp_mteam_total_rounds_counted = 0
    tmp_mteam_total_won_times = 0
    tmp_mteam_id = 0
    sm_team_rank = []
    tmp_mteam_list = []
    tmp_mteam_total_score_list = []
    tmp_team_mpairs = []
    for row in result_rows:
        if row[6] != current_mteam_code:
            if current_mteam_code >0:
                tmp_tuple2 = (current_mteam_code, tmp_mteam_id, round(tmp_mteam_total_scores,1), tmp_mteam_total_won_times, tmp_mteam_total_rounds_counted, tmp_team_mpairs)
                tmp_mteam_list.append(tmp_tuple2)
                tmp_mteam_total_score_list.append(round(tmp_mteam_total_scores,1))

            current_mteam_code = row[6]
            tmp_mteam_id = row[7]
            tmp_team_mpairs = []
            tmp_mteam_total_scores = 0
            tmp_mteam_total_won_times = 0
            tmp_mteam_total_rounds_counted = 0

        #"PLAN_ID, MPAIR_TEAM_ID, MPAIR_ID, EVENT_ROUND_ID, MROOM_ID, MPAIR_CODE_LABEL, " \ 0-5
        #"MTEAM_CODE, MTEAM_ID, MROOM_CODE, MROOM_LABEL, ROUND_CODE, " \ 6-10
        #"MPAIR_STAGE_STATUS_CODE, SP, FIGHT_WON " \ 11-13
        tmp_tuple_team = (row[0], row[1], row[2], row[8], row[10], row[11], row[12], row[13])
        tmp_team_mpairs.append(tmp_tuple_team)
        if row[11] == 99:
            tmp_mteam_total_rounds_counted += 1
            tmp_mteam_total_scores += row[12]
        if row[13] is not None:
            tmp_mteam_total_won_times += row[13]

    if current_mteam_code > 0:
        tmp_tuple2 = (current_mteam_code, tmp_mteam_id, round(tmp_mteam_total_scores,1), tmp_mteam_total_won_times, tmp_mteam_total_rounds_counted, tmp_team_mpairs)
        tmp_mteam_list.append(tmp_tuple2)
        tmp_mteam_total_score_list.append(round(tmp_mteam_total_scores,1))

    # re-order the list by scores
    while True:
        max_value = max(tmp_mteam_total_score_list)
        max_index = tmp_mteam_total_score_list.index(max_value)
        sm_team_rank.append(tmp_mteam_list[max_index])
        tmp_mteam_total_score_list.pop(max_index)
        tmp_mteam_list.pop(max_index)
        if tmp_mteam_total_score_list is None or len(tmp_mteam_total_score_list) < 1:
            break
    return sm_team_rank


# Search all the paired teams for specific plan order to by team code
def search_mpair_by_team_round(plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "PLAN_ID, MPAIR_TEAM_ID, MPAIR_ID, EVENT_ROUND_ID, MROOM_ID, MPAIR_CODE_LABEL, " \
              "MTEAM_CODE, MTEAM_ID, MROOM_CODE, MROOM_LABEL, ROUND_CODE, " \
              "MPAIR_STAGE_STATUS_CODE, SP, FIGHT_WON " \
              "FROM v_mpair_team " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "ORDER by MTEAM_CODE, ROUND_CODE, MPAIR_TEAM_ID" \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the teams' ranking for specific plan id and selective matches by each round
def get_sm_team_rank_by_round(plan_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_mpair_by_team_round(plan_id, app_db_web_location)
    current_mteam_code = 0
    tmp_round_code = 0
    tmp_mteam_total_scores = 0
    tmp_mteam_total_rounds_counted = 0
    tmp_mteam_total_won_times = 0
    tmp_mteam_id = 0
    sm_team_rank = []
    tmp_mteam_list = []
    tmp_mteam_total_score_list = []
    tmp_team_mpairs = []
    tmp_team_rounds = []
    tmp_mteam_round_score = 0
    for row in result_rows:
        if row[6] != current_mteam_code:
            if tmp_round_code > 0:
                tmp_tuple1 = (tmp_round_code, tmp_mteam_round_score)
                tmp_team_rounds.append(tmp_tuple1)

            if current_mteam_code >0:
                tmp_tuple2 = (current_mteam_code, tmp_mteam_id, round(tmp_mteam_total_scores,1), tmp_mteam_total_won_times, tmp_mteam_total_rounds_counted, tmp_team_mpairs, tmp_team_rounds)
                tmp_mteam_list.append(tmp_tuple2)
                tmp_mteam_total_score_list.append(round(tmp_mteam_total_scores,1))

            current_mteam_code = row[6]
            tmp_mteam_id = row[7]
            tmp_team_mpairs = []
            tmp_mteam_total_scores = 0
            tmp_mteam_round_score = 0
            tmp_mteam_total_won_times = 0
            tmp_mteam_total_rounds_counted = 0
            tmp_team_rounds = []
            tmp_round_code = row[10]

        if row[10] != tmp_round_code:
            if tmp_round_code > 0:
                tmp_tuple1 = (tmp_round_code, tmp_mteam_round_score)
                tmp_team_rounds.append(tmp_tuple1)
            tmp_round_code = row[10]
            tmp_mteam_round_score = 0

        #"PLAN_ID, MPAIR_TEAM_ID, MPAIR_ID, EVENT_ROUND_ID, MROOM_ID, MPAIR_CODE_LABEL, " \ 0-5
        #"MTEAM_CODE, MTEAM_ID, MROOM_CODE, MROOM_LABEL, ROUND_CODE, " \ 6-10
        #"MPAIR_STAGE_STATUS_CODE, SP, FIGHT_WON " \ 11-13
        tmp_tuple_team = (row[0], row[1], row[2], row[8], row[10], row[11], row[12], row[13])
        tmp_team_mpairs.append(tmp_tuple_team)
        if row[11] == 99:
            tmp_mteam_total_rounds_counted += 1
            tmp_mteam_total_scores += row[12]
            tmp_mteam_round_score += row[12]
        if row[13] is not None:
            tmp_mteam_total_won_times += row[13]

    if tmp_round_code > 0:
        tmp_tuple1 = (tmp_round_code, tmp_mteam_round_score)
        tmp_team_rounds.append(tmp_tuple1)

    if current_mteam_code > 0:
        tmp_tuple2 = (current_mteam_code, tmp_mteam_id, round(tmp_mteam_total_scores,1), tmp_mteam_total_won_times, tmp_mteam_total_rounds_counted, tmp_team_mpairs, tmp_team_rounds)
        tmp_mteam_list.append(tmp_tuple2)
        tmp_mteam_total_score_list.append(round(tmp_mteam_total_scores,1))

    # re-order the list by scores
    while True:
        max_value = max(tmp_mteam_total_score_list)
        max_index = tmp_mteam_total_score_list.index(max_value)
        sm_team_rank.append(tmp_mteam_list[max_index])
        tmp_mteam_total_score_list.pop(max_index)
        tmp_mteam_list.pop(max_index)
        if tmp_mteam_total_score_list is None or len(tmp_mteam_total_score_list) < 1:
            break
    return sm_team_rank


# Search all the paired teams for specific plan order to by team code
def search_dstage_member_by_round(plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "TEAM_MEMBER_ID, TEAM_MEMBER_NAME, MTEAM_CODE, ROUND_CODE, MROOM_CODE, STAGE_CODE, " \
              "POINT_WITH_FACTOR, MPAIR_STAGE_STATUS_CODE " \
              "FROM v_dstage_teams " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "ORDER by TEAM_MEMBER_ID, ROUND_CODE" \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the teams' ranking for specific plan id and selective matches by each round
def get_sm_member_rank_by_round(plan_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_dstage_member_by_round(plan_id, app_db_web_location)
    current_member_id = 0
    tmp_round_code = 0
    tmp_member_total_scores = 0
    tmp_member_total_fight_counted = 0
    tmp_member_name = None
    tmp_mteam_code = 0
    sm_member_rank = []
    tmp_member_list = []
    tmp_member_total_score_list = []
    tmp_member_rounds = []
    tmp_member_round_score = 0
    for row in result_rows:
        if row[0] != current_member_id:
            if tmp_round_code > 0:
                tmp_tuple1 = (tmp_round_code, tmp_member_round_score)
                tmp_member_rounds.append(tmp_tuple1)

            if current_member_id >0:
                tmp_tuple2 = (current_member_id, tmp_member_name, tmp_mteam_code, round(tmp_member_total_scores/tmp_member_total_fight_counted,1), tmp_member_total_fight_counted, tmp_member_rounds)
                tmp_member_list.append(tmp_tuple2)
                tmp_member_total_score_list.append(round(tmp_member_total_scores/tmp_member_total_fight_counted,1))

            current_member_id = row[0]
            tmp_member_name = row[1]
            tmp_mteam_code = row[2]
            tmp_member_total_scores = 0
            tmp_member_round_score = 0
            tmp_member_total_fight_counted = 0
            tmp_member_rounds = []
            tmp_round_code = row[3]

        if row[3] != tmp_round_code:
            if tmp_round_code > 0:
                tmp_tuple1 = (tmp_round_code, tmp_member_round_score)
                tmp_member_rounds.append(tmp_tuple1)
            tmp_round_code = row[3]
            tmp_member_round_score = 0

        if row[7] == 99:
            tmp_member_total_fight_counted += 1
            tmp_member_total_scores += row[6]
            tmp_member_round_score += row[6]

    if tmp_round_code > 0:
        tmp_tuple1 = (tmp_round_code, tmp_member_round_score)
        tmp_member_rounds.append(tmp_tuple1)

    if current_member_id > 0:
        tmp_tuple2 = (current_member_id, tmp_member_name, tmp_mteam_code, round(tmp_member_total_scores/tmp_member_total_fight_counted,1), tmp_member_total_fight_counted, tmp_member_rounds)
        tmp_member_list.append(tmp_tuple2)
        tmp_member_total_score_list.append(round(tmp_member_total_scores/tmp_member_total_fight_counted,1))

    # re-order the list by scores
    while True:
        max_value = max(tmp_member_total_score_list)
        max_index = tmp_member_total_score_list.index(max_value)
        sm_member_rank.append(tmp_member_list[max_index])
        tmp_member_total_score_list.pop(max_index)
        tmp_member_list.pop(max_index)
        if tmp_member_total_score_list is None or len(tmp_member_total_score_list) < 1:
            break

    for row in sm_member_rank:
        print("***---", row[0], row[1])
    return sm_member_rank


# Search all the paired teams for specific plan order to by round and room code
def search_schedue_by_round_room(plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "PLAN_ID, MPAIR_TEAM_ID, MPAIR_ID, EVENT_ROUND_ID, MROOM_ID, MPAIR_CODE_LABEL, " \
              "MTEAM_CODE, MTEAM_ID, MROOM_CODE, MROOM_LABEL, ROUND_CODE, " \
              "MPAIR_STAGE_STATUS_CODE, SP, FIGHT_WON, Field14 " \
              "FROM v_mpair_team " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "ORDER by PLAN_ID, ROUND_CODE, MROOM_CODE, MPAIR_ID, SP DESC" \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the paired teams for specific plan order to by round and room code
def get_schedue_by_round_room(plan_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_schedue_by_round_room(plan_id, app_db_web_location)
    current_round_code = 0
    tmp_room_code = 0
    event_schedule = []
    tmp_room_teams = []
    tmp_team_list = []
    tmp_mpair_stage_status = 0
    tmp_mpair_problem_guide = None
    tmp_mpair_id = 0
    for row in result_rows:
        if row[10] != current_round_code:
            if tmp_room_code > 0:
                tmp_tuple1 = (tmp_room_code, tmp_team_list, tmp_mpair_stage_status, tmp_mpair_id, tmp_mpair_problem_guide)
                tmp_room_teams.append(tmp_tuple1)

            if current_round_code >0:
                tmp_tuple2 = (current_round_code, tmp_room_teams)
                event_schedule.append(tmp_tuple2)

            current_round_code = row[10]
            tmp_room_code = row[8]
            tmp_mpair_stage_status = row[11]
            tmp_mpair_problem_guide = row[14]
            tmp_mpair_id = row[2]
            tmp_room_teams = []
            tmp_team_list = []

        if row[8] != tmp_room_code:
            if tmp_room_code > 0:
                tmp_tuple1 = (tmp_room_code, tmp_team_list, tmp_mpair_stage_status, tmp_mpair_id, tmp_mpair_problem_guide)
                tmp_room_teams.append(tmp_tuple1)

            tmp_team_list=[]
            tmp_room_code = row[8]
            tmp_mpair_stage_status = row[11]
            tmp_mpair_problem_guide = row[14]
            tmp_mpair_id = row[2]

        #"PLAN_ID, MPAIR_TEAM_ID, MPAIR_ID, EVENT_ROUND_ID, MROOM_ID, MPAIR_CODE_LABEL, " 0-5
        #"MTEAM_CODE, MTEAM_ID, MROOM_CODE, MROOM_LABEL, ROUND_CODE " 6-10
        tmp_tuple_team = (row[0], row[1], row[2], row[7], row[6], row[12], row[13])
        tmp_team_list.append(tmp_tuple_team)

    if tmp_room_code > 0:
        tmp_tuple1 = (tmp_room_code, tmp_team_list, tmp_mpair_stage_status, tmp_mpair_id, tmp_mpair_problem_guide)
        tmp_room_teams.append(tmp_tuple1)

    if current_round_code > 0:
        tmp_tuple2 = (current_round_code, tmp_room_teams)
        event_schedule.append(tmp_tuple2)

    return event_schedule


# Search all the paired teams for specific plan order to by room and round code
def search_mpairs_by_room_round(plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "PLAN_ID, MPAIR_TEAM_ID, MPAIR_ID, EVENT_ROUND_ID, MROOM_ID, MPAIR_CODE_LABEL, " \
              "MTEAM_CODE, MTEAM_ID, MROOM_CODE, MROOM_LABEL, ROUND_CODE, MPAIR_STAGE_STATUS_CODE, " \
              "DRAW_NUM, SP, FIGHT_WON, Field15, Field14 " \
              "FROM v_mpair_team " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "ORDER by PLAN_ID, MROOM_CODE, ROUND_CODE, DRAW_NUM, MTEAM_CODE" \
              ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the paired teams for specific plan order to by round and room code
def get_mpairs_by_room_round(plan_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_mpairs_by_room_round(plan_id, app_db_web_location)
    current_room_code = 0
    tmp_mpair_id = 0
    tmp_mpair_problem_guide = None
    mpair_list = []
    tmp_mroom_label = None
    tmp_mround_code = 0 #(round=row[10])
    tmp_stage_status_code = 0
    tmp_round_list = []
    tmp_team_list = []
    for row in result_rows:
        if row[8] != current_room_code:
            if tmp_mround_code > 0:
                tmp_tuple1 = (tmp_mround_code, tmp_team_list, tmp_stage_status_code, tmp_mpair_id, tmp_mpair_problem_guide)
                tmp_round_list.append(tmp_tuple1)

            if current_room_code >0:
                tmp_tuple2 = (current_room_code, tmp_mroom_label, tmp_round_list)
                mpair_list.append(tmp_tuple2)

            current_room_code = row[8]
            tmp_round_list = []
            tmp_team_list = []
            tmp_mroom_label = row[9]
            tmp_mround_code = row[10]
            tmp_stage_status_code = row[11]
            tmp_mpair_problem_guide = row[16]
            tmp_mpair_id = row[2]

        if row[10] != tmp_mround_code:
            if tmp_mround_code > 0:
                tmp_tuple1 = (tmp_mround_code, tmp_team_list, tmp_stage_status_code, tmp_mpair_id, tmp_mpair_problem_guide)
                tmp_round_list.append(tmp_tuple1)

            tmp_team_list = []
            tmp_mround_code = row[10]
            tmp_stage_status_code = row[11]
            tmp_mpair_problem_guide = row[16]
            tmp_mpair_id = row[2]

        #"PLAN_ID, MPAIR_TEAM_ID, MPAIR_ID, EVENT_ROUND_ID, MROOM_ID, MPAIR_CODE_LABEL, " 0-5
        #"MTEAM_CODE, MTEAM_ID, MROOM_CODE, MROOM_LABEL, ROUND_CODE, MPAIR_STAGE_STATUS_CODE, DRAW_NUM, SP, FIGHT_WON, Field15, Field14 " 6-12 + 13-14, 15, 16
        tmp_tuple_team = (row[0], row[1], row[2], row[7], row[6], row[12], row[13], row[14], row[15])
        tmp_team_list.append(tmp_tuple_team)

    if tmp_mround_code > 0:
        tmp_tuple1 = (tmp_mround_code, tmp_team_list, tmp_stage_status_code, tmp_mpair_id, tmp_mpair_problem_guide)
        tmp_round_list.append(tmp_tuple1)

    if current_room_code > 0:
        tmp_tuple2 = (current_room_code, tmp_mroom_label, tmp_round_list)
        mpair_list.append(tmp_tuple2)

    return mpair_list


# Search stage agenda for specific plan and pair (aka. at specific room and round)
def search_stage_agenda(plan_id, mpair_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "PLAN_ID, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, STAGE_PROGRESS_STATUS_CODE, " \
              "MTEAM_CODE, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, TEAM_MEMBER_ID, TEAM_MEMBER_NAME " \
              "FROM DSTAGE_TEAM " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "AND MPAIR_ID=" + str(mpair_id) + " " \
              "ORDER by STAGE_CODE, STAGE_ROLE_CODE" \
              ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get stage agenda for specific plan and pair (aka. at specific room and round)
def get_sm_stage_agenda(plan_id, mpair_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_stage_agenda(plan_id, mpair_id, app_db_web_location)
    current_stage_code = 0
    stage_agenda = []
    tmp_role_list = []
    tmp_role_info = ()
    for row in result_rows:
        if row[2] != current_stage_code:
            if current_stage_code >0:
                tmp_tuple2 = (current_stage_code, mpair_id, tmp_role_list)
                stage_agenda.append(tmp_tuple2)

            current_stage_code = row[2]
            tmp_role_list = []
        #"PLAN_ID, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, STAGE_PROGRESS_STATUS_CODE, " \ 0-4
        #"MTEAM_CODE, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, TEAM_MEMBER_ID, TEAM_MEMBER_NAME " \ 5-9
        tmp_role_info = (row[0], row[1], row[4], row[6], row[7], row[8], row[9])
        tmp_tuple_role = (row[3], row[5], tmp_role_info)
        tmp_role_list.append(tmp_tuple_role)

    if current_stage_code >0:
        tmp_tuple2 = (current_stage_code, mpair_id, tmp_role_list)
        stage_agenda.append(tmp_tuple2)

    return stage_agenda


# initilize stage agenda for selective match
# insert new records in DSTAGE_TEAM table
# - FK: MPAIR_ID, MPAIR_TEAM_ID, PLAN_ID
# - for each mpair_team, add two records: stage 1, reporter/opponent, stage 2, opponent/reporter
# update MPAIR stage_status_code
# update MPAIR_TEAM draw number
# parameters:
# - sm_current_room_round_pairs e.g. (1, [(26, 1251, 626, 254, 4, 1), (26, 1252, 626, 255, 5, 2)], 1, 626)
# (stage_code, [reporter, opponent], stage-status_code, mpair_id)
# - PLAN_ID, MPAIR_TEAM_ID, MPAIR_ID, MTEAM_ID, MTEAM_CODE, DRAW_NUM
def initialize_sm_stage_agenda(plan_id, sm_current_room_round_pairs, team1_code, team2_code, current_jury, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())
    mpair_id = 0
    # initialize stage agenca in DSTAGE_TEAM table
    for team in sm_current_room_round_pairs[1]:
        mpair_team_id = team[1]
        mpair_id = team[2]
        mteam_code = team[4]
        # insert new records in DSTAGE_TEAM table
        if mteam_code == team1_code:
            # insert new records in DSTAGE_TEAM table - team1
            # insert: stage 1, reporter, stage 2, opponent
            stage_code = 1
            stage_role_codde = 1 # reporter
            _c.execute(
                "insert into DSTAGE_TEAM (MPAIR_TEAM_ID, MPAIR_ID, MTEAM_CODE, STAGE_CODE, STAGE_ROLE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
                (mpair_team_id, mpair_id, mteam_code, stage_code, stage_role_codde, plan_id, current_user_id, current_timestamp))
            stage_code = 2
            stage_role_codde = 2 # OPPONENT
            _c.execute(
                "insert into DSTAGE_TEAM (MPAIR_TEAM_ID, MPAIR_ID, MTEAM_CODE, STAGE_CODE, STAGE_ROLE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
                (mpair_team_id, mpair_id, mteam_code, stage_code, stage_role_codde, plan_id, current_user_id, current_timestamp))
            # update MPAIR_TEAM draw_num - 2
            _c.execute("UPDATE MPAIR_TEAM SET DRAW_NUM = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND MPAIR_TEAM_ID = ?",
                       (1, current_user_id, current_timestamp, plan_id, mpair_team_id))
        elif mteam_code == team2_code:
            # insert new records in DSTAGE_TEAM table - team2
            # insert: stage 1, opponent , stage 2, reporter
            stage_code = 1
            stage_role_codde = 2
            _c.execute(
                "insert into DSTAGE_TEAM (MPAIR_TEAM_ID, MPAIR_ID, MTEAM_CODE, STAGE_CODE, STAGE_ROLE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
                (mpair_team_id, mpair_id, mteam_code, stage_code, stage_role_codde, plan_id, current_user_id, current_timestamp))
            stage_code = 2
            stage_role_codde = 1
            _c.execute(
                "insert into DSTAGE_TEAM (MPAIR_TEAM_ID, MPAIR_ID, MTEAM_CODE, STAGE_CODE, STAGE_ROLE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
                (mpair_team_id, mpair_id, mteam_code, stage_code, stage_role_codde, plan_id, current_user_id, current_timestamp))
            # update MPAIR_TEAM draw_num - 2
            _c.execute("UPDATE MPAIR_TEAM SET DRAW_NUM = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND MPAIR_TEAM_ID = ?",
                       (2, current_user_id, current_timestamp, plan_id, mpair_team_id))

    #insert new records in DSTAGE_JUROR table for stage 1 and stage 2
    for juror in current_jury:
        mjuror_code = juror[0]
        mjuror_id = juror[2]
        mpair_juror_id = juror[1]
        if mpair_juror_id == 0:
            mpair_juror_id = None
        _c.execute(
            "insert into DSTAGE_JUROR (MJUROR_ID, MPAIR_JUROR_ID, MPAIR_ID, MJUROR_CODE, STAGE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
            (mjuror_id, mpair_juror_id, mpair_id, mjuror_code, 1, plan_id, current_user_id, current_timestamp))
        _c.execute(
            "insert into DSTAGE_JUROR (MJUROR_ID, MPAIR_JUROR_ID, MPAIR_ID, MJUROR_CODE, STAGE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
            (mjuror_id, mpair_juror_id, mpair_id, mjuror_code, 2, plan_id, current_user_id, current_timestamp))

    # update MPAIR stage_status_code
    _c.execute("UPDATE MPAIR SET MPAIR_STAGE_STATUS_CODE = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND MPAIR_ID = ?",
               (1, current_user_id, current_timestamp, plan_id, mpair_id))

    _conn.commit()
    _conn.close()


# initilize stage agenda for final match
# insert new records in DSTAGE_TEAM table
# - FK: MPAIR_ID, MPAIR_TEAM_ID, PLAN_ID
# - for each mpair_team, add three records: stage 1, reporter/opponent/reviewer, stage 2, reviewer/reporter/opponent, stage 3, opponent/reviewer/reporter
# update MPAIR stage_status_code
# update MPAIR_TEAM draw number
# parameters:
# - fm_plan e.g. (teams, jurors, mpair, round, room)
# (stage_code, [reporter, opponent], stage-status_code, mpair_id)
# - PLAN_ID, MPAIR_TEAM_ID, MPAIR_ID, MTEAM_ID, MTEAM_CODE, DRAW_NUM
#    round_info = (row[2], row[1])  # roound_id, round_code
#    room_info = (row[3], row[4], row[5])  # mroom_id, mroom_code, mroom_label
#    pair_info = (row[0], row[9], row[10])  # mpair_id, MPAIR_SIDS, MPAIR_STAGE_STATUS_CODE
#fm_plan_teams.append((row[6], row[7], row[8]))  # mpair_team_id, mteam_code, mteam_id
def initialize_fm_stage_agenda(fm_plan_id, fm_plan, draw_numbers, fm_team_problem_codes, current_jury, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())
    mpair_id = fm_plan[2][0]
    # initialize stage agenca in DSTAGE_TEAM table
    i = 0
    for team in fm_plan[0]:
        i += 1
        mpair_team_id = team[0]
        mteam_id = team[2]
        mteam_code = team[1]
        draw_number = draw_numbers[i-1]
        selected_problem_code = fm_team_problem_codes[i-1]
        # insert new records in DSTAGE_TEAM table
        if draw_number == 1:
            # insert new records in DSTAGE_TEAM table - sm ranking #1 team
            # insert: stage 1, reporter, stage 2, reviewer, stage 3, opponent
            stage_code = 1
            stage_role_codde = 1 # reporter
            _c.execute(
                "insert into DSTAGE_TEAM (MPAIR_TEAM_ID, MPAIR_ID, MTEAM_CODE, STAGE_CODE, STAGE_ROLE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
                (mpair_team_id, mpair_id, mteam_code, stage_code, stage_role_codde, fm_plan_id, current_user_id, current_timestamp))
            stage_code = 2
            stage_role_codde = 3 # REVIEWER
            _c.execute(
                "insert into DSTAGE_TEAM (MPAIR_TEAM_ID, MPAIR_ID, MTEAM_CODE, STAGE_CODE, STAGE_ROLE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
                (mpair_team_id, mpair_id, mteam_code, stage_code, stage_role_codde, fm_plan_id, current_user_id, current_timestamp))
            stage_code = 3
            stage_role_codde = 2 # OPPONENT
            _c.execute(
                "insert into DSTAGE_TEAM (MPAIR_TEAM_ID, MPAIR_ID, MTEAM_CODE, STAGE_CODE, STAGE_ROLE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
                (mpair_team_id, mpair_id, mteam_code, stage_code, stage_role_codde, fm_plan_id, current_user_id, current_timestamp))
            # update MPAIR_TEAM draw_num - 2
            _c.execute("UPDATE MPAIR_TEAM SET DRAW_NUM = ?, Field15=?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND MPAIR_TEAM_ID = ?",
                       (draw_number, selected_problem_code, current_user_id, current_timestamp, fm_plan_id, mpair_team_id))
        elif draw_number == 2:
            # insert new records in DSTAGE_TEAM table - sm ranking #2 team
            # insert: stage 1, reporter, stage 2, reviewer, stage 3, opponent
            stage_code = 1
            stage_role_codde = 2 # OPPONENT
            _c.execute(
                "insert into DSTAGE_TEAM (MPAIR_TEAM_ID, MPAIR_ID, MTEAM_CODE, STAGE_CODE, STAGE_ROLE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
                (mpair_team_id, mpair_id, mteam_code, stage_code, stage_role_codde, fm_plan_id, current_user_id, current_timestamp))
            stage_code = 2
            stage_role_codde = 1 # reporter
            _c.execute(
                "insert into DSTAGE_TEAM (MPAIR_TEAM_ID, MPAIR_ID, MTEAM_CODE, STAGE_CODE, STAGE_ROLE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
                (mpair_team_id, mpair_id, mteam_code, stage_code, stage_role_codde, fm_plan_id, current_user_id, current_timestamp))
            stage_code = 3
            stage_role_codde = 3 # REVIEWER
            _c.execute(
                "insert into DSTAGE_TEAM (MPAIR_TEAM_ID, MPAIR_ID, MTEAM_CODE, STAGE_CODE, STAGE_ROLE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
                (mpair_team_id, mpair_id, mteam_code, stage_code, stage_role_codde, fm_plan_id, current_user_id, current_timestamp))
            # update MPAIR_TEAM draw_num - 2
            _c.execute("UPDATE MPAIR_TEAM SET DRAW_NUM = ?, Field15=?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND MPAIR_TEAM_ID = ?",
                       (draw_number, selected_problem_code, current_user_id, current_timestamp, fm_plan_id, mpair_team_id))
        elif draw_number == 3:
            # insert new records in DSTAGE_TEAM table - sm ranking #3 team
            # insert: stage 1, reporter, stage 2, reviewer, stage 3, opponent
            stage_code = 1
            stage_role_codde = 3 #REVIEWER
            _c.execute(
                "insert into DSTAGE_TEAM (MPAIR_TEAM_ID, MPAIR_ID, MTEAM_CODE, STAGE_CODE, STAGE_ROLE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
                (mpair_team_id, mpair_id, mteam_code, stage_code, stage_role_codde, fm_plan_id, current_user_id, current_timestamp))
            stage_code = 2
            stage_role_codde = 2 #OPPONENT
            _c.execute(
                "insert into DSTAGE_TEAM (MPAIR_TEAM_ID, MPAIR_ID, MTEAM_CODE, STAGE_CODE, STAGE_ROLE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
                (mpair_team_id, mpair_id, mteam_code, stage_code, stage_role_codde, fm_plan_id, current_user_id, current_timestamp))
            stage_code = 3
            stage_role_codde = 1 # reporter
            _c.execute(
                "insert into DSTAGE_TEAM (MPAIR_TEAM_ID, MPAIR_ID, MTEAM_CODE, STAGE_CODE, STAGE_ROLE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
                (mpair_team_id, mpair_id, mteam_code, stage_code, stage_role_codde, fm_plan_id, current_user_id, current_timestamp))
            # update MPAIR_TEAM draw_num - 2
            _c.execute("UPDATE MPAIR_TEAM SET DRAW_NUM = ?, Field15=?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND MPAIR_TEAM_ID = ?",
                       (draw_number, selected_problem_code, current_user_id, current_timestamp, fm_plan_id, mpair_team_id))

    #insert new records in DSTAGE_JUROR table for stage 1, stage 2 and stage 3
    for juror in current_jury:
        mjuror_code = juror[0]
        mjuror_id = juror[2]
        mpair_juror_id = juror[1]
        if mpair_juror_id == 0:
            mpair_juror_id = None
        _c.execute(
            "insert into DSTAGE_JUROR (MJUROR_ID, MPAIR_JUROR_ID, MPAIR_ID, MJUROR_CODE, STAGE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
            (mjuror_id, mpair_juror_id, mpair_id, mjuror_code, 1, fm_plan_id, current_user_id, current_timestamp))
        _c.execute(
            "insert into DSTAGE_JUROR (MJUROR_ID, MPAIR_JUROR_ID, MPAIR_ID, MJUROR_CODE, STAGE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
            (mjuror_id, mpair_juror_id, mpair_id, mjuror_code, 2, fm_plan_id, current_user_id, current_timestamp))
        _c.execute(
            "insert into DSTAGE_JUROR (MJUROR_ID, MPAIR_JUROR_ID, MPAIR_ID, MJUROR_CODE, STAGE_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?)",
            (mjuror_id, mpair_juror_id, mpair_id, mjuror_code, 3, fm_plan_id, current_user_id, current_timestamp))

    # update MPAIR stage_status_code
    _c.execute("UPDATE MPAIR SET MPAIR_STAGE_STATUS_CODE = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND MPAIR_ID = ?",
               (1, current_user_id, current_timestamp, fm_plan_id, mpair_id))

    _conn.commit()
    _conn.close()


# save stage members and jurors for selective match
# update team_member_id and name in DSTAGE_TEAM table for reporter and opponent
# update MPAIR stage_status_code to 11 or 21
# parameters:
def save_stage_members(plan_id, current_pair_id, stage_code, reporter, opponent, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())

    # update team_member_id and name in DSTAGE_TEAM table
    # reporter's team member: role code = 1
    stage_role_code = 1
    team_member_id = reporter.split("--", 1)[0]
    team_member_name = reporter.split("--", 1)[1]
    _c.execute(
        "UPDATE DSTAGE_TEAM SET TEAM_MEMBER_ID = ?, TEAM_MEMBER_NAME=?, last_updated_by = ?, last_updated_date = ? "
        "WHERE PLAN_ID = ? AND MPAIR_ID = ? AND STAGE_CODE = ? AND STAGE_ROLE_CODE = ?",
        (team_member_id, team_member_name, current_user_id, current_timestamp, plan_id, current_pair_id, stage_code, stage_role_code))
    # opponent's team member: role code = 2
    stage_role_code = 2
    team_member_id = opponent.split("--", 1)[0]
    team_member_name = opponent.split("--", 1)[1]
    _c.execute(
        "UPDATE DSTAGE_TEAM SET TEAM_MEMBER_ID = ?, TEAM_MEMBER_NAME=?, last_updated_by = ?, last_updated_date = ? "
        "WHERE PLAN_ID = ? AND MPAIR_ID = ? AND STAGE_CODE = ? AND STAGE_ROLE_CODE = ?",
        (team_member_id, team_member_name, current_user_id, current_timestamp, plan_id, current_pair_id, stage_code, stage_role_code))

    # update MPAIR stage_status_code
    stage_status_code = 1
    if stage_code == 1:
        stage_status_code = 11
    elif stage_code == 2:
        stage_status_code = 21
    _c.execute("UPDATE MPAIR SET MPAIR_STAGE_STATUS_CODE = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND MPAIR_ID = ?",
               (stage_status_code, current_user_id, current_timestamp, plan_id, current_pair_id))

    _conn.commit()
    _conn.close()


# save stage members and jurors for final match
# update team_member_id and name in DSTAGE_TEAM table for reporter and opponent, reviewer
# insert one new records in DSTAGE_problem table
# update MPAIR stage_status_code to 11 or 21, 31
# parameters:
def save_fm_stage_members(plan_id, current_pair_id, stage_code, reporter, opponent, reviewer, reporter_problem,
                          current_reporter_dstage_team_id, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())

    # update team_member_id and name in DSTAGE_TEAM table
    # reporter's team member: role code = 1
    stage_role_code = 1
    team_member_id = reporter.split("--", 1)[0]
    team_member_name = reporter.split("--", 1)[1]
    _c.execute(
        "UPDATE DSTAGE_TEAM SET TEAM_MEMBER_ID = ?, TEAM_MEMBER_NAME=?, last_updated_by = ?, last_updated_date = ? "
        "WHERE PLAN_ID = ? AND MPAIR_ID = ? AND STAGE_CODE = ? AND STAGE_ROLE_CODE = ?",
        (team_member_id, team_member_name, current_user_id, current_timestamp, plan_id, current_pair_id, stage_code, stage_role_code))

    # insert reporter problem to DSTAGE_PROBLEM - one record
    _c.execute(
        "insert into DSTAGE_PROBLEM (DSTAGE_TEAM_ID_FROM, DSTAGE_TEAM_ID_TO, PROBLEM_ID, STAGE_CODE, PROBLEM_CODE, PROBLEM_LABEL_CODE, DSTAGE_PROBLEM_SUB_STATUS_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (current_reporter_dstage_team_id, current_reporter_dstage_team_id, reporter_problem['problem_id'], stage_code, reporter_problem['problem_code'],
         reporter_problem['problem_label_code'], 3, plan_id, current_user_id, current_timestamp))

    # opponent's team member: role code = 2
    stage_role_code = 2
    team_member_id = opponent.split("--", 1)[0]
    team_member_name = opponent.split("--", 1)[1]
    _c.execute(
        "UPDATE DSTAGE_TEAM SET TEAM_MEMBER_ID = ?, TEAM_MEMBER_NAME=?, last_updated_by = ?, last_updated_date = ? "
        "WHERE PLAN_ID = ? AND MPAIR_ID = ? AND STAGE_CODE = ? AND STAGE_ROLE_CODE = ?",
        (team_member_id, team_member_name, current_user_id, current_timestamp, plan_id, current_pair_id, stage_code, stage_role_code))

    # reviewer's team member: role code = 3
    stage_role_code = 3
    team_member_id = reviewer.split("--", 1)[0]
    team_member_name = reviewer.split("--", 1)[1]
    _c.execute(
        "UPDATE DSTAGE_TEAM SET TEAM_MEMBER_ID = ?, TEAM_MEMBER_NAME=?, last_updated_by = ?, last_updated_date = ? "
        "WHERE PLAN_ID = ? AND MPAIR_ID = ? AND STAGE_CODE = ? AND STAGE_ROLE_CODE = ?",
        (team_member_id, team_member_name, current_user_id, current_timestamp, plan_id, current_pair_id, stage_code, stage_role_code))

    # update MPAIR stage_status_code
    stage_status_code = 1
    if stage_code == 1:
        stage_status_code = 11
    elif stage_code == 2:
        stage_status_code = 21
    elif stage_code == 3:
        stage_status_code = 31
    _c.execute("UPDATE MPAIR SET MPAIR_STAGE_STATUS_CODE = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND MPAIR_ID = ?",
               (stage_status_code, current_user_id, current_timestamp, plan_id, current_pair_id))

    #update DSTAGE_TEAM table to set the accepted problem
    rep_coefficince = 3.0
    opp_coefficince = 2.0
    rev_coefficince = 1.0
    reporter_current_stage_rejection_credit_g1 = 0
    reporter_current_stage_rejection_credit_g2 = 0
    reporter_current_stage_rejection_times = 0
    _c.execute(
        "UPDATE DSTAGE_TEAM SET STAGE_MATCH_PROBLEM_ID = ?, STAGE_MATCH_PROBLEM_CODE=?, REP_COEFFICIENCE=?, OPP_COEFFICIENCE = ?, REV_COEFFICIENCE = ?, "
        "REP_REJECTION_CREIDT_G1 = ?, REP_REJECTION_CREIDT_G2 = ?, TOTAL_REJECTED_TIMES = ?, last_updated_by = ?, last_updated_date = ? "
        "WHERE PLAN_ID = ? AND MPAIR_ID = ? AND STAGE_CODE = ?",
        (reporter_problem['problem_id'], reporter_problem['problem_code'], rep_coefficince, opp_coefficince, rev_coefficince,
         reporter_current_stage_rejection_credit_g1, reporter_current_stage_rejection_credit_g2, reporter_current_stage_rejection_times,
         current_user_id, current_timestamp, plan_id, current_pair_id, stage_code))

    _conn.commit()
    _conn.close()


# Search all the jurors that attended a specific stage for specific plan and pair (aka. at specific room and round)
def search_stage_jurors(plan_id, mpair_id, stage_code, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "PLAN_ID, MPAIR_ID, STAGE_CODE, DSTAGE_JUROR_ID, MJUROR_ID, MPAIR_JUROR_ID, MJUROR_CODE, " \
              "IS_CHAIR, MJUROR_COI_SIDS, MJUROR_TIMESLOTS " \
              "FROM v_dstage_jurors " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "AND MPAIR_ID=" + str(mpair_id) + " " \
              "AND STAGE_CODE=" + str(stage_code) + " " \
              "AND DSTAGE_JUROR_STATUS='Active' " \
              "ORDER by IS_CHAIR DESC" \
              ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the jurors that attended a specific stage for specific plan and pair (aka. at specific room and round)
def get_stage_jurors(plan_id, mpair_id, stage_code, app_db_web_location=app_db_web_location_default):
    result_rows = search_stage_jurors(plan_id, mpair_id, stage_code, app_db_web_location)
    stage_jurors = list()
    for row in result_rows:
        #"PLAN_ID, MPAIR_ID, STAGE_CODE, DSTAGE_JUROR_ID, MJUROR_ID, MPAIR_JUROR_ID, MJUROR_CODE, " \ 0-6
        #"IS_CHAIR, MJUROR_COI_SIDS, MJUROR_TIMESLOTS " \ 7-9
        tmp_tuple_juror = (row[6], row[5], row[4], (row[1], row[2], row[3], row[7], row[8], row[9]))
        stage_jurors.append(tmp_tuple_juror)

    return stage_jurors


# Search all the problems for specific plan order by group and problem label
def search_master_problems(event_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "PROBLEM_ID, EVENT_ID, PROBLEM_LABEL, PROBLEM_LABEL_CODE, PROBLEM_DESCRIPTION, " \
              "PROBLEM_GROUP, PROBLEM_NOTES, PROBLEM_CODE " \
              "FROM EVENT_PROBLEM " \
              "WHERE EVENT_ID=" + str(event_id) + " " \
              "AND PROBLEM_STATUS='Active' " \
              "ORDER by PROBLEM_GROUP, PROBLEM_CODE" \
              ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the problems in a group for specific plan order by group and problem code
def get_event_group_problems(event_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_master_problems(event_id, app_db_web_location)
    group_code = 0
    problem_list = []
    tmp_problem_list = []
    for row in result_rows:
        if row[5] != group_code:
            if group_code >0:
                tmp_problem_group = [group_code, tmp_problem_list]
                problem_list.append(tmp_problem_group)

            group_code = row[5]
            tmp_problem_list = []
        #"PROBLEM_ID, EVENT_ID, PROBLEM_LABEL, PROBLEM_LABEL_CODE, PROBLEM_DESCRIPTION, " 0-4
        # problem status code: 1-proposed, 2-rejected, 3-accepted
        tmp_problem_info = {
            "problem_code": row[7],
            "problem_id": row[0],
            "problem_label_code": row[3],
            "problem_label": row[2],
            "problem_description": row[4],
            "problem_status": 0,
            "group_code" : group_code
        }
        tmp_problem_list.append(tmp_problem_info)

    if group_code >0:
        tmp_problem_group = [group_code, tmp_problem_list]
        problem_list.append(tmp_problem_group)

    return problem_list


# get all the problems in a group for specific plan order by group and problem code
def get_event_master_problems(event_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_master_problems(event_id, app_db_web_location)
    group_code = 0
    problem_list = []
    for row in result_rows:
        #"PROBLEM_ID, EVENT_ID, PROBLEM_LABEL, PROBLEM_LABEL_CODE, PROBLEM_DESCRIPTION, " 0-4
        # problem status code: 1-proposed, 2-rejected, 3-accepted
        tmp_problem_info = {
            "problem_code": row[7],
            "problem_id": row[0],
            "problem_label_code": row[3],
            "problem_label": row[2],
            "problem_description": row[4],
            "problem_status": 0,
            "group_code" : group_code
        }
        tmp_problem = [row[7], tmp_problem_info]
        problem_list.append(tmp_problem)

    return problem_list


# save the selected problems at one stage for selective match
# insert new records in DSTAGE_PROBLEM table
# - FK: DSTAGE_TEAM_ID, EVENT_PROBLEM_ID, PLAN_ID
# - for each accepted/rejected problem, add one records
# current_stage_agenda: (current_stage_code, mpair_id, tmp_role_list)
# "PLAN_ID, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, STAGE_PROGRESS_STATUS_CODE, " \ 0-4
# "MTEAM_CODE, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, TEAM_MEMBER_ID, TEAM_MEMBER_NAME " \ 5-9
#tmp_role_info = (row[0], row[1], row[4], row[6], row[7], row[8], row[9])
#tmp_tuple_role = (row[3], row[5], tmp_role_info)
# update DSTAGE_TEAM table to set the accepted problem
# parameters:
def save_stage_problems(plan_id, stage_code, current_stage_agenda, current_stage_problems, current_group_code, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())
    mpair_id = 0
    accepted_problem_id = 0
    accepted_problem_code = 0

    # initiate coefficience
    reduction_for_each_rejection = 0.2
    rep_coefficince = 3.0
    opp_coefficince = 2.0
    reporter_mteam_rejection_credit_g1 = 0
    reporter_mteam_rejection_credit_g2 = 0
    reporter_current_stage_rejection_credit_g1 = 0
    reporter_current_stage_rejection_credit_g2 = 0
    reporter_current_stage_rejection_times = 0
    reporter_mteam_code = current_stage_agenda[2][0][1]
    # check if the reporter team has taken the credit for one rejection of each group problem
    command = "SELECT " \
              "REP_REJECTION_CREDIT_G1, REP_REJECTION_CREDIT_G2 " \
              "FROM MTEAM " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "AND MTEAM_CODE=" + str(reporter_mteam_code) + " " \
              ";"

    _c.execute(command)
    result = _c.fetchall()
    for row in result:
        reporter_mteam_rejection_credit_g1 = row[0]
        reporter_mteam_rejection_credit_g2 = row[1]
        break
    #insert new records TO DSTAGE_problem table
    for problem in current_stage_problems[1]:
        # mpair_id
        mpair_id = current_stage_agenda[1]
        # opponent team's DSTAGE_TEAM_ID
        problem_proposed_by = current_stage_agenda[2][1][2][4]
        # reporter team's DSTAGE_TEAM_ID
        problem_proposed_to = current_stage_agenda[2][0][2][4]
        if problem['problem_status'] == 3:
            accepted_problem_id = problem['problem_id']
            accepted_problem_code = problem['problem_code']

        if problem['problem_status'] == 2:
            reporter_current_stage_rejection_times += 1

        if problem['problem_status'] > 0:
            _c.execute(
                "insert into DSTAGE_PROBLEM (DSTAGE_TEAM_ID_FROM, DSTAGE_TEAM_ID_TO, PROBLEM_ID, STAGE_CODE, PROBLEM_CODE, PROBLEM_LABEL_CODE, DSTAGE_PROBLEM_SUB_STATUS_CODE, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (problem_proposed_by, problem_proposed_to, problem['problem_id'], stage_code, problem['problem_code'], problem['problem_label_code'], problem['problem_status'], plan_id, current_user_id, current_timestamp))

    # calculate reporter team rejection credit
    if reporter_current_stage_rejection_times > 0:
        # has rejections
        if current_group_code == 1:
            # check group 1 credit
            if reporter_mteam_rejection_credit_g1 is None or reporter_mteam_rejection_credit_g1 == 0:
                # give credit to this stage's 1st rejection
                reporter_current_stage_rejection_credit_g1 = 1
                reporter_mteam_rejection_credit_g1 = 1
        else:
            #check group 2 credit
            if reporter_mteam_rejection_credit_g2 is None or reporter_mteam_rejection_credit_g2 == 0:
                # give credit to this stage's 1st rejection
                reporter_current_stage_rejection_credit_g2 = 1
                reporter_mteam_rejection_credit_g2 = 1
        # calculate reporter coefficience - removed on Jan 28th, 2020 because keep reporter coefficience as standard value
        # calculate on the fly: reporter coefficience - (total rejected time - group1/group2 allowance
        # update MTEAM REP_REJECTION_CREDIT_G1, REP_REJECTION_CREDIT_G2
        _c.execute(
            "UPDATE MTEAM SET REP_REJECTION_CREDIT_G1 = ?, REP_REJECTION_CREDIT_G2=?, last_updated_by = ?, last_updated_date = ? "
            "WHERE PLAN_ID = ? AND MTEAM_CODE = ?",
            (reporter_mteam_rejection_credit_g1, reporter_mteam_rejection_credit_g2, current_user_id, current_timestamp, plan_id, reporter_mteam_code))
    else:
        # no rejection
        pass
    #update DSTAGE_TEAM table to set the accepted problem
    if accepted_problem_id > 0:
        _c.execute(
            "UPDATE DSTAGE_TEAM SET STAGE_MATCH_PROBLEM_ID = ?, STAGE_MATCH_PROBLEM_CODE=?, REP_COEFFICIENCE=?, OPP_COEFFICIENCE = ?, "
            "REP_REJECTION_CREIDT_G1 = ?, REP_REJECTION_CREIDT_G2 = ?, TOTAL_REJECTED_TIMES = ?, last_updated_by = ?, last_updated_date = ? "
            "WHERE PLAN_ID = ? AND MPAIR_ID = ? AND STAGE_CODE = ?",
            (accepted_problem_id, accepted_problem_code, rep_coefficince, opp_coefficince,
             reporter_current_stage_rejection_credit_g1, reporter_current_stage_rejection_credit_g2, reporter_current_stage_rejection_times,
             current_user_id, current_timestamp, plan_id, mpair_id, stage_code))

    # update MPAIR stage_status_code
    stage_status_code = 1
    if stage_code == 1:
        stage_status_code = 11
    elif stage_code == 2:
        stage_status_code = 21
    _c.execute("UPDATE MPAIR SET MPAIR_STAGE_STATUS_CODE = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND MPAIR_ID = ?",
               (stage_status_code, current_user_id, current_timestamp, plan_id, mpair_id))

    _conn.commit()
    _conn.close()


def update_mpair_stage_status(plan_id, mpair_id, mpair_stage_status_code, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())

    # update MPAIR stage_status_code
    _c.execute("UPDATE MPAIR SET MPAIR_STAGE_STATUS_CODE = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND MPAIR_ID = ?",
               (mpair_stage_status_code, current_user_id, current_timestamp, plan_id, mpair_id))

    _conn.commit()
    _conn.close()


# save scores for specifc stage, pair, juror
# insert new record to DSTAGE_SCORE
# - FK: DSTAGE_JUROR_ID, DSTAGE_TEAM_ID
# - for each key/value: find DSTAGE_JUROR_ID
# - from current_stage_agenda: find rep's DSTAGE_TEAM_ID and opp's DSTAGE_TEAM_ID
# update MPAIR stage_status_code to 13 or 23
# parameters:
def save_stage_scores(plan_id, current_pair_id, stage_scores, current_stage_agenda, stage_code, room_code, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())

    # get volunteer id and code for data entrier
    command = "SELECT " \
              "MVOLUNTEER_ID, MVOLUNTEER_CODE " \
              "FROM v_mvolunteers " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "AND MROOM_CODE=" + str(room_code) + " " \
              "AND PPANT_USER_ID=" + str(current_user_id) + " " \
              ";"
    _c.execute(command)
    result = _c.fetchall()
    mvolunteer_id = None
    mvolunteer_code = 0
    for row in result:
        mvolunteer_id = row[0]
        mvolunteer_code = row[1]
        break

    # get reporter and oppoent DSTAGE_TEAM_ID
    reporter_dstage_team_id = current_stage_agenda[2][0][2][4]
    reporter_team_code = current_stage_agenda[2][0][1]
    opponent_dstage_team_id = current_stage_agenda[2][1][2][4]
    opponent_team_code = current_stage_agenda[2][1][1]
    #insert new records in DSTAGE_SCORE table
    team_score_key = None
    key_str = None
    mjuror_code = 0
    team_role = 0
    mjuror_score_element_id = 0
    dstage_juror_id = 0
    dstage_team_id = None
    team_code = 0
    team_sc1 = 0
    team_sc2 = 0
    team_sc3 = 0
    team_sc4 = 0
    team_sc5 = 0
    for item in stage_scores:
        # key: j_4_opp_3_92
        key_str = item[0].split("_", 4)
        tmp_team_score_key = key_str[1] + "_" + key_str[2]
        if team_score_key != tmp_team_score_key:
            if team_score_key != None:
                # previous values are for the new record
                total_score = team_sc1 + team_sc2 + team_sc3 + team_sc4 + team_sc5
                # insert into DSTAGE_SCORE table
                _c.execute(
                    "insert into DSTAGE_SCORE (DSTAGE_TEAM_ID, DSTAGE_JUROR_ID, MTEAM_CODE, MJUROR_CODE, STAGE_CODE, "
                    "SCORE_MVOLUNTEER_ID, SCORE_MVOLUNTEER_CODE, SCORE_ENTER_BY, TOTAL_SCORE, "
                    "SC1, SC2, SC3, SC4, SC5, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (dstage_team_id, dstage_juror_id, team_code, mjuror_code, stage_code, mvolunteer_id, mvolunteer_code,
                     current_user_id, total_score, team_sc1 , team_sc2 , team_sc3 , team_sc4 , team_sc5,
                     plan_id, current_user_id, current_timestamp))
            # reset data
            team_score_key = tmp_team_score_key
            team_sc1 = 0
            team_sc2 = 0
            team_sc3 = 0
            team_sc4 = 0
            team_sc5 = 0
            mjuror_code = key_str[1]
            team_role = key_str[2]
            dstage_juror_id = key_str[4]
            dstage_team_id = None
            if team_role == "rep":
                dstage_team_id = reporter_dstage_team_id
                team_code = reporter_team_code
            elif team_role == "opp":
                dstage_team_id = opponent_dstage_team_id
                team_code = opponent_team_code
        mjuror_score_element_id = key_str[3]
        if mjuror_score_element_id == "1":
            team_sc1 = float(item[1])
        elif mjuror_score_element_id == "2":
            team_sc2 = float(item[1])
        elif mjuror_score_element_id == "3":
            team_sc3 = float(item[1])
        elif mjuror_score_element_id == "4":
            team_sc4 = float(item[1])
        elif mjuror_score_element_id == "5":
            team_sc5 = float(item[1])

    if team_score_key != None:
        # previous values are for the new record
        total_score = team_sc1 + team_sc2 + team_sc3 + team_sc4 + team_sc5
        # insert into DSTAGE_SCORE table
        _c.execute(
            "insert into DSTAGE_SCORE (DSTAGE_TEAM_ID, DSTAGE_JUROR_ID, MTEAM_CODE, MJUROR_CODE, STAGE_CODE, "
            "SCORE_MVOLUNTEER_ID, SCORE_MVOLUNTEER_CODE, SCORE_ENTER_BY, TOTAL_SCORE, "
            "SC1, SC2, SC3, SC4, SC5, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (dstage_team_id, dstage_juror_id, team_code, mjuror_code, stage_code, mvolunteer_id, mvolunteer_code,
             current_user_id, total_score, team_sc1 , team_sc2 , team_sc3 , team_sc4 , team_sc5,
             plan_id, current_user_id, current_timestamp))

    # update MPAIR stage_status_code
    stage_status_code = 99
    if stage_code == 1:
        stage_status_code = 13
    elif stage_code == 2:
        stage_status_code = 23
    _c.execute("UPDATE MPAIR SET MPAIR_STAGE_STATUS_CODE = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND MPAIR_ID = ?",
               (stage_status_code, current_user_id, current_timestamp, plan_id, current_pair_id))

    _conn.commit()
    _conn.close()


# save scores for specifc stage, pair, juror - final match
# insert new record to DSTAGE_SCORE
# - FK: DSTAGE_JUROR_ID, DSTAGE_TEAM_ID
# - for each key/value: find DSTAGE_JUROR_ID
# - from current_stage_agenda: find rep's DSTAGE_TEAM_ID and opp's DSTAGE_TEAM_ID
# update MPAIR stage_status_code to 13 or 23, 33
# parameters:
def save_fm_stage_scores(plan_id, sm_plan_id, current_pair_id, stage_scores, current_stage_agenda, stage_code, room_code, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())

    # get volunteer id and code for data entrier
    command = "SELECT " \
              "MVOLUNTEER_ID, MVOLUNTEER_CODE " \
              "FROM v_mvolunteers " \
              "WHERE PLAN_ID=" + str(sm_plan_id) + " " \
              "AND MROOM_CODE=" + str(room_code) + " " \
              "AND PPANT_USER_ID=" + str(current_user_id) + " " \
              ";"
    _c.execute(command)
    result = _c.fetchall()
    mvolunteer_id = None
    mvolunteer_code = 0
    for row in result:
        mvolunteer_id = row[0]
        mvolunteer_code = row[1]
        break

    # get reporter and oppoent DSTAGE_TEAM_ID + reviewer
    reporter_dstage_team_id = current_stage_agenda[2][0][2][4]
    reporter_team_code = current_stage_agenda[2][0][1]
    opponent_dstage_team_id = current_stage_agenda[2][1][2][4]
    opponent_team_code = current_stage_agenda[2][1][1]
    reviewer_dstage_team_id = current_stage_agenda[2][2][2][4]
    reviewer_team_code = current_stage_agenda[2][2][1]
    #insert new records in DSTAGE_SCORE table
    team_score_key = None
    key_str = None
    mjuror_code = 0
    team_role = 0
    mjuror_score_element_id = 0
    dstage_juror_id = 0
    dstage_team_id = None
    team_code = 0
    team_sc1 = 0
    team_sc2 = 0
    team_sc3 = 0
    team_sc4 = 0
    team_sc5 = 0
    team_sc6 = 0
    team_sc7 = 0
    for item in stage_scores:
        # key: j_4_opp_3_92
        key_str = item[0].split("_", 4)
        tmp_team_score_key = key_str[1] + "_" + key_str[2]
        if team_score_key != tmp_team_score_key:
            if team_score_key != None:
                # previous values are for the new record
                total_score = team_sc1 + team_sc2 + team_sc3 + team_sc4 + team_sc5 + team_sc6 + team_sc7
                # insert into DSTAGE_SCORE table
                _c.execute(
                    "insert into DSTAGE_SCORE (DSTAGE_TEAM_ID, DSTAGE_JUROR_ID, MTEAM_CODE, MJUROR_CODE, STAGE_CODE, "
                    "SCORE_MVOLUNTEER_ID, SCORE_MVOLUNTEER_CODE, SCORE_ENTER_BY, TOTAL_SCORE, "
                    "SC1, SC2, SC3, SC4, SC5, SC6, SC7, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (dstage_team_id, dstage_juror_id, team_code, mjuror_code, stage_code, mvolunteer_id, mvolunteer_code,
                     current_user_id, total_score, team_sc1 , team_sc2 , team_sc3 , team_sc4 , team_sc5, team_sc6, team_sc7,
                     plan_id, current_user_id, current_timestamp))
            # reset data
            team_score_key = tmp_team_score_key
            team_sc1 = 0
            team_sc2 = 0
            team_sc3 = 0
            team_sc4 = 0
            team_sc5 = 0
            team_sc6 = 0
            team_sc7 = 0
            mjuror_code = key_str[1]
            team_role = key_str[2]
            dstage_juror_id = key_str[4]
            dstage_team_id = None
            if team_role == "rep":
                dstage_team_id = reporter_dstage_team_id
                team_code = reporter_team_code
            elif team_role == "opp":
                dstage_team_id = opponent_dstage_team_id
                team_code = opponent_team_code
            elif team_role == "rev":
                dstage_team_id = reviewer_dstage_team_id
                team_code = reviewer_team_code
        mjuror_score_element_id = key_str[3]
        if mjuror_score_element_id == "1":
            team_sc1 = float(item[1])
        elif mjuror_score_element_id == "2":
            team_sc2 = float(item[1])
        elif mjuror_score_element_id == "3":
            team_sc3 = float(item[1])
        elif mjuror_score_element_id == "4":
            team_sc4 = float(item[1])
        elif mjuror_score_element_id == "5":
            team_sc5 = float(item[1])
        elif mjuror_score_element_id == "6":
            team_sc6 = float(item[1])
        elif mjuror_score_element_id == "7":
            team_sc7 = float(item[1])

    if team_score_key != None:
        # previous values are for the new record
        total_score = team_sc1 + team_sc2 + team_sc3 + team_sc4 + team_sc5 + team_sc6 + team_sc7
        # insert into DSTAGE_SCORE table
        _c.execute(
            "insert into DSTAGE_SCORE (DSTAGE_TEAM_ID, DSTAGE_JUROR_ID, MTEAM_CODE, MJUROR_CODE, STAGE_CODE, "
            "SCORE_MVOLUNTEER_ID, SCORE_MVOLUNTEER_CODE, SCORE_ENTER_BY, TOTAL_SCORE, "
            "SC1, SC2, SC3, SC4, SC5, SC6, SC7, PLAN_ID, CREATED_BY, CREATED_DATE) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (dstage_team_id, dstage_juror_id, team_code, mjuror_code, stage_code, mvolunteer_id, mvolunteer_code,
             current_user_id, total_score, team_sc1, team_sc2, team_sc3, team_sc4, team_sc5, team_sc6, team_sc7,
             plan_id, current_user_id, current_timestamp))

    # update MPAIR stage_status_code
    stage_status_code = 99
    if stage_code == 1:
        stage_status_code = 13
    elif stage_code == 2:
        stage_status_code = 23
    elif stage_code == 3:
        stage_status_code = 33
    _c.execute("UPDATE MPAIR SET MPAIR_STAGE_STATUS_CODE = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND MPAIR_ID = ?",
               (stage_status_code, current_user_id, current_timestamp, plan_id, current_pair_id))

    _conn.commit()
    _conn.close()


# Search all the team members' roles at each stage and the problem taken
def search_team_member_roles(plan_id, team_code=0, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    if team_code > 0:
        command = "SELECT " \
                  "EVENT_ID, PLAN_ID, MTEAM_CODE, TEAM_MEMBER_ID, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, " \
                  "MROOM_ID, MROOM_CODE, EVENT_ROUND_ID, ROUND_CODE, ROUND_TYPE, MPAIR_STAGE_STATUS_CODE, " \
                  "TEAM_MEMBER_USER_ID, TEAM_MEMBER_FIRST_NAME, TEAM_MEMBER_LAST_NAME, IS_CAPTAIN, " \
                  "STAGE_MATCH_PROBLEM_CODE, STAGE_MATCH_PROBLEM_ID, STAGE_PROGRESS_STATUS_CODE, MROOM_LABEL, " \
                  "TEAM_ID, TEAM_NAME " \
                  "FROM v_team_member_roles " \
                  "WHERE PLAN_ID=" + str(plan_id) + " " \
                  "AND MTEAM_CODE=" + str(team_code) + " " \
                  "AND MEMBER_STATUS='Approved' " \
                  "AND TEAM_STATUS='Approved' " \
                  "ORDER by TEAM_MEMBER_ID, ROUND_CODE" \
                  ";"
    else:
        command = "SELECT " \
                  "EVENT_ID, PLAN_ID, MTEAM_CODE, TEAM_MEMBER_ID, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, " \
                  "MROOM_ID, MROOM_CODE, EVENT_ROUND_ID, ROUND_CODE, ROUND_TYPE, MPAIR_STAGE_STATUS_CODE, " \
                  "TEAM_MEMBER_USER_ID, TEAM_MEMBER_FIRST_NAME, TEAM_MEMBER_LAST_NAME, IS_CAPTAIN, " \
                  "STAGE_MATCH_PROBLEM_CODE, STAGE_MATCH_PROBLEM_ID, STAGE_PROGRESS_STATUS_CODE, MROOM_LABEL, " \
                  "TEAM_ID, TEAM_NAME " \
                  "FROM v_team_member_roles " \
                  "WHERE PLAN_ID=" + str(plan_id) + " " \
                  "AND MEMBER_STATUS='Approved' " \
                  "AND TEAM_STATUS='Approved' " \
                  "ORDER by MTEAM_CODE, TEAM_MEMBER_ID, ROUND_CODE" \
                  ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the team members' roles at each stage and the problem taken
def get_team_member_roles(plan_id, team_code=0, app_db_web_location=app_db_web_location_default):
    result_rows = search_team_member_roles(plan_id, team_code, app_db_web_location)
    current_team_code = 0
    tmp_is_captain = 0
    team_member_role_list = []
    tmp_team_name = None
    tmp_team_member_id = 0
    tmp_team_member_name = None
    tmp_member_list = []
    tmp_dstage_team_list = []
    tmp_member_id_list = []
    tmp_member_take_floor_times = 0
    for row in result_rows:
        if row[2] != current_team_code:
            if tmp_team_member_id > 0:
                tmp_tuple1 = (tmp_team_member_id, tmp_team_member_name, tmp_is_captain, tmp_dstage_team_list, tmp_member_take_floor_times)
                tmp_member_list.append(tmp_tuple1)
                tmp_member_id_list.append(tmp_team_member_id)

            if current_team_code >0:
                tmp_tuple2 = (current_team_code, tmp_team_name, tmp_member_list, tmp_member_id_list)
                team_member_role_list.append(tmp_tuple2)

            current_team_code = row[2]
            tmp_member_list = []
            tmp_member_id_list = []
            tmp_dstage_team_list = []
            tmp_member_take_floor_times = 0
            tmp_team_name = row[24]
            tmp_team_member_id = row[3]
            tmp_team_member_name = row[16] + " " + row[17]
            tmp_is_captain = row[18]

        if row[3] != tmp_team_member_id:
            if tmp_team_member_id > 0:
                tmp_tuple1 = (tmp_team_member_id, tmp_team_member_name, tmp_is_captain, tmp_dstage_team_list, tmp_member_take_floor_times)
                tmp_member_list.append(tmp_tuple1)
                tmp_member_id_list.append(tmp_team_member_id)

            tmp_dstage_team_list = []
            tmp_member_take_floor_times = 0
            tmp_team_member_id = row[3]
            tmp_team_member_name = row[16] + " " + row[17]
            tmp_is_captain = row[18]

        #"EVENT_ID, PLAN_ID, MTEAM_CODE, TEAM_MEMBER_ID, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, " \ 0-8
        #"MROOM_ID, MROOM_CODE, EVENT_ROUND_ID, ROUND_CODE, ROUND_TYPE, MPAIR_STAGE_STATUS_CODE, " \ 9-14
        #"TEAM_MEMBER_USER_ID, TEAM_MEMBER_FIRST_NAME, TEAM_MEMBER_LAST_NAME, IS_CAPTAIN, " \ 15-18
        #"STAGE_MATCH_PROBLEM_CODE, STAGE_MATCH_PROBLEM_ID, STAGE_PROGRESS_STATUS_CODE, MROOM_LABEL, " \ 19-22
        # info: MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, \ 0-4
        # + MROOM_CODE, MROOM_LABEL, ROUND_CODE, MPAIR_STAGE_STATUS_CODE, STAGE_MATCH_PROBLEM_CODE, STAGE_MATCH_PROBLEM_ID \ 5-10
        # + problem_label \ 11
        problem_label = None
        if row[19] is not None:
            problem_label = chr(ord('A') + row[19] - 1)
        tmp_tuple_dstage_team_info = (row[4], row[5], row[6], row[7], row[8], row[10], row[22], row[12], row[14], row[19], row[20], problem_label)
        tmp_dstage_team_list.append(tmp_tuple_dstage_team_info)
        if row[6] == 1:
            tmp_member_take_floor_times += 1

    if tmp_team_member_id > 0:
        tmp_tuple1 = (tmp_team_member_id, tmp_team_member_name, tmp_is_captain, tmp_dstage_team_list, tmp_member_take_floor_times)
        tmp_member_list.append(tmp_tuple1)
        tmp_member_id_list.append(tmp_team_member_id)

    if current_team_code > 0:
        tmp_tuple2 = (current_team_code, tmp_team_name, tmp_member_list, tmp_member_id_list)
        team_member_role_list.append(tmp_tuple2)

    return team_member_role_list


# search all the problems for specific pair of teams that have been challenged (2-rejected, 3-accepted)
def search_reporter_problems(plan_id, reporter_team_code, oppenent_team_code, reviewer_team_code, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    if reviewer_team_code == 0:
        command = "SELECT " \
                  "PLAN_ID, MTEAM_CODE, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, " \
                  "MROOM_ID, MROOM_CODE, EVENT_ROUND_ID, ROUND_CODE, ROUND_TYPE, MPAIR_STAGE_STATUS_CODE, " \
                  "PROBLEM_GROUP, PROBLEM_ID, PROBLEM_CODE, PROBLEM_LABEL_CODE, DSTAGE_PROBLEM_SUB_STATUS_CODE, " \
                  "STAGE_MATCH_PROBLEM_CODE, STAGE_MATCH_PROBLEM_ID, STAGE_PROGRESS_STATUS_CODE, MROOM_LABEL " \
                  "FROM v_dstage_problems_reporter " \
                  "WHERE PLAN_ID=" + str(plan_id) + " " \
                  "AND (MTEAM_CODE=" + str(reporter_team_code) + " OR MTEAM_CODE=" + str(oppenent_team_code) + " ) " \
                  "ORDER by MTEAM_CODE, PROBLEM_CODE, ROUND_CODE, STAGE_CODE" \
                  ";"
    else:
        command = "SELECT " \
                  "PLAN_ID, MTEAM_CODE, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, " \
                  "MROOM_ID, MROOM_CODE, EVENT_ROUND_ID, ROUND_CODE, ROUND_TYPE, MPAIR_STAGE_STATUS_CODE, " \
                  "PROBLEM_GROUP, PROBLEM_ID, PROBLEM_CODE, PROBLEM_LABEL_CODE, DSTAGE_PROBLEM_SUB_STATUS_CODE, " \
                  "STAGE_MATCH_PROBLEM_CODE, STAGE_MATCH_PROBLEM_ID, STAGE_PROGRESS_STATUS_CODE, MROOM_LABEL " \
                  "FROM v_dstage_problems_reporter " \
                  "WHERE PLAN_ID=" + str(plan_id) + " " \
                  "AND (MTEAM_CODE=" + str(reporter_team_code) + \
                  " OR MTEAM_CODE=" + str(oppenent_team_code) + " OR MTEAM_CODE=" + str(reviewer_team_code) + " ) " \
                  "ORDER by MTEAM_CODE, PROBLEM_CODE, ROUND_CODE, STAGE_CODE" \
                  ";"
    #print("***___", command)
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the problems for specific pair of teams that have been challenged (2-rejected, 3-accepted)
def get_reporter_problems(plan_id, reporter_team_code, oppenent_team_code, reviewer_team_code=0, app_db_web_location=app_db_web_location_default):
    result_rows = search_reporter_problems(plan_id, reporter_team_code, oppenent_team_code, reviewer_team_code, app_db_web_location)
    if result_rows is not None and len(result_rows) > 0:
        current_team_code = 0
        tmp_team_problem_list = []
        reporter_problems = []
        tmp_problem_code = 0
        tmp_problem_label_code = 0
        tmp_dstage_problem_list = []
        for row in result_rows:
            if row[1] != current_team_code:
                if tmp_problem_code > 0:
                    tmp_tuple1 = (tmp_problem_code, tmp_dstage_problem_list, tmp_problem_label_code)
                    tmp_team_problem_list.append(tmp_tuple1)

                if current_team_code >0:
                    tmp_tuple2 = (current_team_code, tmp_team_problem_list)
                    reporter_problems.append(tmp_tuple2)

                current_team_code = row[1]
                tmp_team_problem_list = []
                tmp_dstage_problem_list = []
                tmp_problem_code = row[15]
                tmp_problem_label_code = row[16]

            if row[15] != tmp_problem_code:
                if tmp_problem_code > 0:
                    tmp_tuple1 = (tmp_problem_code, tmp_dstage_problem_list, tmp_problem_label_code)
                    tmp_team_problem_list.append(tmp_tuple1)

                tmp_dstage_problem_list = []
                tmp_problem_code = row[15]
                tmp_problem_label_code = row[16]

            #"PLAN_ID, MTEAM_CODE, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, " \ 0-6
            #"MROOM_ID, MROOM_CODE, EVENT_ROUND_ID, ROUND_CODE, ROUND_TYPE, MPAIR_STAGE_STATUS_CODE, " \ 7-12
            #"PROBLEM_GROUP, PROBLEM_ID, PROBLEM_CODE, PROBLEM_LABEL_CODE, DSTAGE_PROBLEM_SUB_STATUS_CODE, " \ 13-17
            #"STAGE_MATCH_PROBLEM_CODE, STAGE_MATCH_PROBLEM_ID, STAGE_PROGRESS_STATUS_CODE, MROOM_LABEL " \ 18-21
            # info: ROUND_CODE, MROOM_CODE, STAGE_CODE, STAGE_ROLE_CODE, DSTAGE_PROBLEM_SUB_STATUS_CODE,\
            tmp_tuple_dstage_problem_info = (row[10], row[8], row[3], row[4], row[17])
            tmp_dstage_problem_list.append(tmp_tuple_dstage_problem_info)

        if tmp_problem_code > 0:
            tmp_tuple1 = (tmp_problem_code, tmp_dstage_problem_list, tmp_problem_label_code)
            tmp_team_problem_list.append(tmp_tuple1)

        if current_team_code > 0:
            tmp_tuple2 = (current_team_code, tmp_team_problem_list)
            reporter_problems.append(tmp_tuple2)

        return reporter_problems
    else:
        return None


# search all the problems for all teams that have been challenged (2-rejected, 3-accepted)
def search_all_reporter_problems(plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "PLAN_ID, MTEAM_CODE, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, " \
              "MROOM_ID, MROOM_CODE, EVENT_ROUND_ID, ROUND_CODE, ROUND_TYPE, MPAIR_STAGE_STATUS_CODE, " \
              "PROBLEM_GROUP, PROBLEM_ID, PROBLEM_CODE, PROBLEM_LABEL_CODE, DSTAGE_PROBLEM_SUB_STATUS_CODE, " \
              "STAGE_MATCH_PROBLEM_CODE, STAGE_MATCH_PROBLEM_ID, STAGE_PROGRESS_STATUS_CODE, MROOM_LABEL " \
              "FROM v_dstage_problems_reporter " \
              "WHERE PLAN_ID=" + str(plan_id) + " " + \
              "UNION SELECT " \
              "PLAN_ID, MTEAM_CODE, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, " \
              "MROOM_ID, MROOM_CODE, EVENT_ROUND_ID, ROUND_CODE, ROUND_TYPE, MPAIR_STAGE_STATUS_CODE, " \
              "PROBLEM_GROUP, PROBLEM_ID, PROBLEM_CODE, PROBLEM_LABEL_CODE, DSTAGE_PROBLEM_SUB_STATUS_CODE, " \
              "STAGE_MATCH_PROBLEM_CODE, STAGE_MATCH_PROBLEM_ID, STAGE_PROGRESS_STATUS_CODE, MROOM_LABEL " \
              "FROM v_dstage_problems_opponent " \
              "WHERE PLAN_ID=" + str(plan_id) + " " + \
              "ORDER by MTEAM_CODE, PROBLEM_CODE, ROUND_CODE, STAGE_CODE, STAGE_ROLE_CODE" \
              ";"
    #print("***___", command)
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the problems for all teams that have been challenged (2-rejected, 3-accepted)
def get_all_reporter_problems(plan_id, app_db_web_location=app_db_web_location_default):
    result_rows = search_all_reporter_problems(plan_id, app_db_web_location)
    if result_rows is not None and len(result_rows) > 0:
        current_team_code = 0
        tmp_team_problem_list = []
        reporter_problems = []
        tmp_problem_code = 0
        tmp_problem_label_code = 0
        tmp_dstage_problem_list = []
        for row in result_rows:
            if row[1] != current_team_code:
                if tmp_problem_code > 0:
                    tmp_tuple1 = (tmp_problem_code, tmp_dstage_problem_list, tmp_problem_label_code)
                    tmp_team_problem_list.append(tmp_tuple1)

                if current_team_code >0:
                    tmp_tuple2 = (current_team_code, tmp_team_problem_list)
                    reporter_problems.append(tmp_tuple2)

                current_team_code = row[1]
                tmp_team_problem_list = []
                tmp_dstage_problem_list = []
                tmp_problem_code = row[15]
                tmp_problem_label_code = row[16]

            if row[15] != tmp_problem_code:
                if tmp_problem_code > 0:
                    tmp_tuple1 = (tmp_problem_code, tmp_dstage_problem_list, tmp_problem_label_code)
                    tmp_team_problem_list.append(tmp_tuple1)

                tmp_dstage_problem_list = []
                tmp_problem_code = row[15]
                tmp_problem_label_code = row[16]

            #"PLAN_ID, MTEAM_CODE, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, " \ 0-6
            #"MROOM_ID, MROOM_CODE, EVENT_ROUND_ID, ROUND_CODE, ROUND_TYPE, MPAIR_STAGE_STATUS_CODE, " \ 7-12
            #"PROBLEM_GROUP, PROBLEM_ID, PROBLEM_CODE, PROBLEM_LABEL_CODE, DSTAGE_PROBLEM_SUB_STATUS_CODE, " \ 13-17
            #"STAGE_MATCH_PROBLEM_CODE, STAGE_MATCH_PROBLEM_ID, STAGE_PROGRESS_STATUS_CODE, MROOM_LABEL " \ 18-21
            # info: ROUND_CODE, MROOM_CODE, STAGE_CODE, STAGE_ROLE_CODE, DSTAGE_PROBLEM_SUB_STATUS_CODE,\
            tmp_tuple_dstage_problem_info = (row[10], row[8], row[3], row[4], row[17])
            tmp_dstage_problem_list.append(tmp_tuple_dstage_problem_info)

        if tmp_problem_code > 0:
            tmp_tuple1 = (tmp_problem_code, tmp_dstage_problem_list, tmp_problem_label_code)
            tmp_team_problem_list.append(tmp_tuple1)

        if current_team_code > 0:
            tmp_tuple2 = (current_team_code, tmp_team_problem_list)
            reporter_problems.append(tmp_tuple2)

        return reporter_problems
    else:
        return None


# search all the problems that reporter team has been challenged (2-rejected, 3-accepted)
def search_reporter_team_problems(plan_id, current_reporter_team_code, problem_reject_accept_code, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "PLAN_ID, MTEAM_CODE, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, " \
              "MROOM_ID, MROOM_CODE, EVENT_ROUND_ID, ROUND_CODE, ROUND_TYPE, MPAIR_STAGE_STATUS_CODE, " \
              "PROBLEM_GROUP, PROBLEM_ID, PROBLEM_CODE, PROBLEM_LABEL_CODE, DSTAGE_PROBLEM_SUB_STATUS_CODE, " \
              "STAGE_MATCH_PROBLEM_CODE, STAGE_MATCH_PROBLEM_ID, STAGE_PROGRESS_STATUS_CODE, MROOM_LABEL " \
              "FROM v_dstage_problems_reporter " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "AND DSTAGE_PROBLEM_SUB_STATUS_CODE=" + str(problem_reject_accept_code) + " " \
              "AND MTEAM_CODE=" + str(current_reporter_team_code) + " " \
              "ORDER by PROBLEM_GROUP, PROBLEM_CODE, ROUND_CODE" \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the problems that reporter team has been challenged (2-rejected, 3-accepted)
def get_reporter_team_problems(plan_id, current_reporter_team_code, problem_reject_accept_code, app_db_web_location=app_db_web_location_default):
    result_rows = search_reporter_team_problems(plan_id, current_reporter_team_code, problem_reject_accept_code, app_db_web_location)
    if result_rows is not None and len(result_rows) > 0:
        current_problem_group_code = 0
        tmp_total_rejected_times = 0
        reporter_problems_rejected = []
        tmp_problem_code = 0
        tmp_group_problem_list = []
        tmp_dstage_problem_list = []
        tmp_prolem_rejected_times = 0
        for row in result_rows:
            if row[13] != current_problem_group_code:
                if tmp_problem_code > 0:
                    tmp_tuple1 = (tmp_problem_code, tmp_dstage_problem_list, tmp_prolem_rejected_times)
                    tmp_group_problem_list.append(tmp_tuple1)

                if current_problem_group_code >0:
                    tmp_tuple2 = (current_problem_group_code, tmp_group_problem_list, tmp_total_rejected_times)
                    reporter_problems_rejected.append(tmp_tuple2)

                current_problem_group_code = row[13]
                tmp_group_problem_list = []
                tmp_dstage_problem_list = []
                tmp_prolem_rejected_times = 0
                tmp_total_rejected_times = 0
                tmp_problem_code = row[15]

            if row[15] != tmp_problem_code:
                if tmp_problem_code > 0:
                    tmp_tuple1 = (tmp_problem_code, tmp_dstage_problem_list, tmp_prolem_rejected_times)
                    tmp_group_problem_list.append(tmp_tuple1)

                tmp_dstage_problem_list = []
                tmp_prolem_rejected_times = 0
                tmp_problem_code = row[15]

            #"PLAN_ID, MTEAM_CODE, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, " \ 0-6
            #"MROOM_ID, MROOM_CODE, EVENT_ROUND_ID, ROUND_CODE, ROUND_TYPE, MPAIR_STAGE_STATUS_CODE, " \ 7-12
            #"PROBLEM_GROUP, PROBLEM_ID, PROBLEM_CODE, PROBLEM_LABEL_CODE, DSTAGE_PROBLEM_SUB_STATUS_CODE, " \ 13-17
            #"STAGE_MATCH_PROBLEM_CODE, STAGE_MATCH_PROBLEM_ID, STAGE_PROGRESS_STATUS_CODE, MROOM_LABEL " \ 18-21
            # info: MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, MROOM_CODE, MROOM_LABEL, ROUND_CODE \ 0-7
            # + PROBLEM_ID, PROBLEM_CODE, PROBLEM_LABEL_CODE, DSTAGE_PROBLEM_SUB_STATUS_CODE,\ 8-11
            tmp_tuple_dstage_problem_info = (row[2], row[3], row[4], row[5], row[6], row[8], row[21], row[10], row[14], row[15], row[16], row[17])
            tmp_dstage_problem_list.append(tmp_tuple_dstage_problem_info)
            tmp_prolem_rejected_times += 1
            tmp_total_rejected_times += 1

        if tmp_problem_code > 0:
            tmp_tuple1 = (tmp_problem_code, tmp_dstage_problem_list, tmp_prolem_rejected_times)
            tmp_group_problem_list.append(tmp_tuple1)

        if current_problem_group_code > 0:
            tmp_tuple2 = (current_problem_group_code, tmp_group_problem_list, tmp_total_rejected_times)
            reporter_problems_rejected.append(tmp_tuple2)

        return reporter_problems_rejected
    else:
        return None


# Search all the teams' scores for specific pair (aka round and room)
def search_mpair_scores(plan_id, mpair_id=0, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    if mpair_id > 0:
        command = "SELECT " \
                  "EVENT_ID, PLAN_ID, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, MTEAM_CODE, TEAM_MEMBER_ID, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, " \
                  "ROUND_CODE, ROUND_TYPE, MROOM_CODE, MPAIR_STAGE_STATUS_CODE, POINT_WITH_FACTOR, " \
                  "DSTAGE_JUROR_ID, DSTAGE_SCORE_ID, MJUROR_CODE, TOTAL_SCORE, AVERAGE_POINT, " \
                  "REP_COEFFICIENCE, OPP_COEFFICIENCE, REP_REJECTION_CREIDT_G1, REP_REJECTION_CREIDT_G2, " \
                  "STAGE_MATCH_PROBLEM_CODE, DSTAGE_JUROR_ID, ROUND_TYPE, MROOM_LABEL, " \
                  "SC1, SC2, SC3, SC4, SC5, TEAM_MEMBER_ID, TEAM_MEMBER_NAME, TOTAL_REJECTED_TIMES, " \
                  "SC6, SC7, REV_COEFFICIENCE " \
                  "FROM v_dstage_team_scores " \
                  "WHERE PLAN_ID=" + str(plan_id) + " " \
                  "AND MPAIR_ID=" + str(mpair_id) + " " \
                  "ORDER by STAGE_CODE, STAGE_ROLE_CODE, MJUROR_CODE" \
                  ";"
    else:
        command = "SELECT " \
                  "EVENT_ID, PLAN_ID, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, MTEAM_CODE, TEAM_MEMBER_ID, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, " \
                  "ROUND_CODE, ROUND_TYPE, MROOM_CODE, MPAIR_STAGE_STATUS_CODE, POINT_WITH_FACTOR, " \
                  "DSTAGE_JUROR_ID, DSTAGE_SCORE_ID, MJUROR_CODE, TOTAL_SCORE, AVERAGE_POINT, " \
                  "REP_COEFFICIENCE, OPP_COEFFICIENCE, REP_REJECTION_CREIDT_G1, REP_REJECTION_CREIDT_G2, " \
                  "STAGE_MATCH_PROBLEM_CODE, DSTAGE_JUROR_ID, ROUND_TYPE, MROOM_LABEL, " \
                  "SC1, SC2, SC3, SC4, SC5, TEAM_MEMBER_ID, TEAM_MEMBER_NAME, TOTAL_REJECTED_TIMES, " \
                  "SC6, SC7, REV_COEFFICIENCE " \
                  "FROM v_dstage_team_scores " \
                  "WHERE PLAN_ID=" + str(plan_id) + " " \
                  "ORDER by ROUND_CODE, MROOM_CODE, STAGE_CODE, STAGE_ROLE_CODE, MJUROR_CODE" \
                  ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the teams' scores for specific pair (aka round and room)
def get_mpair_scores_4validate(plan_id, mpair_id, current_team_codes, app_db_web_location=app_db_web_location_default):
    result_rows = search_mpair_scores(plan_id, mpair_id, app_db_web_location)
    current_stage_code = 0
    tmp_stage_role_scores = None
    tmp_stage_role_team_member = None
    mpair_stage_role_score_list = []
    tmp_mpair_info = None
    tmp_stage_role_code = 0
    tmp_mteam_code = 0
    tmp_mteam_1 = current_team_codes[0]
    tmp_mteam_2 = current_team_codes[1]
    tmp_mteam_1_SP = 0
    tmp_mteam_2_SP = 0
    tmp_stage_role_list = []
    tmp_dstage_score_list = []
    tmp_dstage_role_jscores = []
    for row in result_rows:
        if row[3] != current_stage_code:
            if tmp_stage_role_code > 0:
                # calculate average point
                tmp_max_score = max(tmp_dstage_role_jscores)
                tmp_min_score = min(tmp_dstage_role_jscores)
                tmp_average_score = (tmp_max_score + tmp_min_score) / 2
                tmp_score_count = 1
                for jscore in tmp_dstage_role_jscores:
                    if jscore == tmp_min_score:
                        tmp_min_score = -100
                    elif jscore == tmp_max_score:
                        tmp_max_score = 100
                    else:
                        tmp_score_count += 1
                        tmp_average_score = tmp_average_score + jscore
                tmp_average_score = round(tmp_average_score / tmp_score_count, 1)
                tmp_deduction = 0
                if tmp_stage_role_scores[8] is not None and tmp_stage_role_scores[8] > 0:
                    tmp_deduction = (tmp_stage_role_scores[8] - tmp_stage_role_scores[6] - tmp_stage_role_scores[
                        7]) * 0.2
                tmp_points = 0
                if tmp_stage_role_code == 1:
                    tmp_points = tmp_average_score * (tmp_stage_role_scores[4] - tmp_deduction)
                elif tmp_stage_role_code == 2:
                    tmp_points = tmp_average_score * (tmp_stage_role_scores[5])
                # calcuate SP at mpair_team level
                if tmp_mteam_code == tmp_mteam_1:
                    tmp_mteam_1_SP = tmp_mteam_1_SP + round(tmp_points, 1)
                elif tmp_mteam_code == tmp_mteam_2:
                    tmp_mteam_2_SP = tmp_mteam_2_SP + round(tmp_points, 1)

                tmp_tuple1 = (tmp_stage_role_code, tmp_mteam_code, tmp_stage_role_scores, tmp_dstage_score_list,
                              tmp_stage_role_team_member, round(tmp_average_score, 1), round(tmp_points, 1),
                              round(tmp_deduction, 1))
                tmp_stage_role_list.append(tmp_tuple1)

            if current_stage_code >0:
                tmp_tuple2 = (current_stage_code, tmp_mpair_info, tmp_stage_role_list)
                mpair_stage_role_score_list.append(tmp_tuple2)

            current_stage_code = row[3]
            tmp_stage_role_list = []
            tmp_dstage_score_list = []
            tmp_dstage_role_jscores = []
            tmp_mpair_info = (row[2], row[9], row[11], row[26], row[23]) # mpair_id, round_code, room_code, romm_code_label)
            tmp_stage_role_code = row[4]
            tmp_mteam_code = row[5]
            # MPAIR_TEAM_ID, DSTAGE_TEAM_ID, ap_with_factor, average_point, REP_COEFFICIENCE, OPP_COEFFICIENCE, REP_REJECTION_CREIDT_G1, REP_REJECTION_CREIDT_G2, TOTAL_REJECTED_TIMES
            tmp_stage_role_scores = (row[7], row[8], row[13], row[18], row[19], row[20], row[21], row[22], row[34])
            tmp_stage_role_team_member = (row[32], row[33]) # TEAM_MEMBER_ID, TEAM_MEMBER_NAME

        if row[4] != tmp_stage_role_code:
            if tmp_stage_role_code > 0:
                # calculate average point
                tmp_max_score = max(tmp_dstage_role_jscores)
                tmp_min_score = min(tmp_dstage_role_jscores)
                tmp_average_score = (tmp_max_score + tmp_min_score) / 2
                tmp_score_count = 1
                for jscore in tmp_dstage_role_jscores:
                    if jscore == tmp_min_score:
                        tmp_min_score = -100
                    elif jscore == tmp_max_score:
                        tmp_max_score = 100
                    else:
                        tmp_score_count += 1
                        tmp_average_score = tmp_average_score + jscore
                tmp_average_score = round(tmp_average_score / tmp_score_count, 1)
                tmp_deduction = 0
                if tmp_stage_role_scores[8] is not None and tmp_stage_role_scores[8] > 0:
                    tmp_deduction = (tmp_stage_role_scores[8] - tmp_stage_role_scores[6] - tmp_stage_role_scores[
                        7]) * 0.2
                tmp_points = 0
                if tmp_stage_role_code == 1:
                    tmp_points = tmp_average_score * (tmp_stage_role_scores[4] - tmp_deduction)
                elif tmp_stage_role_code == 2:
                    tmp_points = tmp_average_score * (tmp_stage_role_scores[5])
                # calcuate SP at mpair_team level
                if tmp_mteam_code == tmp_mteam_1:
                    tmp_mteam_1_SP = tmp_mteam_1_SP + round(tmp_points, 1)
                elif tmp_mteam_code == tmp_mteam_2:
                    tmp_mteam_2_SP = tmp_mteam_2_SP + round(tmp_points, 1)

                tmp_tuple1 = (tmp_stage_role_code, tmp_mteam_code, tmp_stage_role_scores, tmp_dstage_score_list,
                              tmp_stage_role_team_member, round(tmp_average_score, 1), round(tmp_points, 1),
                              round(tmp_deduction, 1))
                tmp_stage_role_list.append(tmp_tuple1)

            tmp_dstage_score_list = []
            tmp_dstage_role_jscores = []
            tmp_stage_role_code = row[4]
            tmp_mteam_code = row[5]
            # MPAIR_TEAM_ID, DSTAGE_TEAM_ID, ap_with_factor, average_point, REP_COEFFICIENCE, OPP_COEFFICIENCE, REP_REJECTION_CREIDT_G1, REP_REJECTION_CREIDT_G2, TOTAL_REJECTED_TIMES
            tmp_stage_role_scores = (row[7], row[8], row[13], row[18], row[19], row[20], row[21], row[22], row[34])
            tmp_stage_role_team_member = (row[32], row[33]) # TEAM_MEMBER_ID, TEAM_MEMBER_NAME

        #"EVENT_ID, PLAN_ID, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, MTEAM_CODE, TEAM_MEMBER_ID, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, " \ 0-8
        #"ROUND_CODE, ROUND_TYPE, MROOM_CODE, MPAIR_STAGE_STATUS_CODE, POINT_WITH_FACTOR, " \ 9-13
        #"DSTAGE_JUROR_ID, DSTAGE_SCORE_ID, MJUROR_CODE, TOTAL_SCORE, AVERAGE_POINT, " \ 14-18
        #"REP_COEFFICIENCE, OPP_COEFFICIENCE, REP_REJECTION_CREIDT_G1, REP_REJECTION_CREIDT_G2, " \ 19-22
        #"STAGE_MATCH_PROBLEM_CODE, DSTAGE_JUROR_ID, ROUND_TYPE, MROOM_LABEL, " \ 23-26
        #"SC1, SC2, SC3, SC4, SC5, TEAM_MEMBER_ID, TEAM_MEMBER_NAME, TOTAL_REJECTED_TIMES " \ 27-34
        # info: DSTAGE_SCORE_ID, MJUROR_CODE, TOTAL_SCORE, SC1, SC2, SC3, SC4, SC5 \ 0-4
        tmp_dstage_juror_score = (row[15], row[16], row[17], row[27], row[28], row[29], row[30], row[31])
        tmp_dstage_score_list.append(tmp_dstage_juror_score)
        tmp_dstage_role_jscores.append(row[17])

    if tmp_stage_role_code > 0:
        # calculate average point
        tmp_max_score = max(tmp_dstage_role_jscores)
        tmp_min_score = min(tmp_dstage_role_jscores)
        tmp_average_score = (tmp_max_score + tmp_min_score) / 2
        tmp_score_count = 1
        for jscore in tmp_dstage_role_jscores:
            if jscore == tmp_min_score:
                tmp_min_score = -100
            elif jscore == tmp_max_score:
                tmp_max_score = 100
            else:
                tmp_score_count += 1
                tmp_average_score = tmp_average_score + jscore
        tmp_average_score = round(tmp_average_score / tmp_score_count, 1)
        tmp_deduction = 0
        if tmp_stage_role_scores[8] is not None and tmp_stage_role_scores[8] > 0:
            tmp_deduction = (tmp_stage_role_scores[8] - tmp_stage_role_scores[6] - tmp_stage_role_scores[7]) * 0.2
        tmp_points = 0
        if tmp_stage_role_code == 1:
            tmp_points = tmp_average_score * (tmp_stage_role_scores[4] - tmp_deduction)
        elif tmp_stage_role_code == 2:
            tmp_points = tmp_average_score * (tmp_stage_role_scores[5])
        # calcuate SP at mpair_team level
        if tmp_mteam_code == tmp_mteam_1:
            tmp_mteam_1_SP = tmp_mteam_1_SP + round(tmp_points, 1)
        elif tmp_mteam_code == tmp_mteam_2:
            tmp_mteam_2_SP = tmp_mteam_2_SP + round(tmp_points, 1)

        tmp_tuple1 = (tmp_stage_role_code, tmp_mteam_code, tmp_stage_role_scores, tmp_dstage_score_list, tmp_stage_role_team_member, round(tmp_average_score,1), round(tmp_points,1), round(tmp_deduction,1))
        tmp_stage_role_list.append(tmp_tuple1)

    if current_stage_code > 0:
        tmp_tuple2 = (current_stage_code, tmp_mpair_info, tmp_stage_role_list)
        mpair_stage_role_score_list.append(tmp_tuple2)

    return ( mpair_stage_role_score_list, (round(tmp_mteam_1_SP,1), round(tmp_mteam_2_SP,1)) )


# get all the teams' scores for final match
def get_fm_mpair_scores_4validate(plan_id, mpair_id, current_team_codes, app_db_web_location=app_db_web_location_default):
    result_rows = search_mpair_scores(plan_id, mpair_id, app_db_web_location)
    current_stage_code = 0
    tmp_stage_role_scores = None
    tmp_stage_role_team_member = None
    mpair_stage_role_score_list = []
    tmp_mpair_info = None
    tmp_stage_role_code = 0
    tmp_mteam_code = 0
    tmp_mteam_1 = current_team_codes[0]
    tmp_mteam_2 = current_team_codes[1]
    tmp_mteam_3 = current_team_codes[2]
    tmp_mteam_1_SP = 0
    tmp_mteam_2_SP = 0
    tmp_mteam_3_SP = 0
    tmp_stage_role_list = []
    tmp_dstage_score_list = []
    tmp_dstage_role_jscores = []
    for row in result_rows:
        if row[3] != current_stage_code:
            if tmp_stage_role_code > 0:
                # calculate average point
                tmp_max_score = max(tmp_dstage_role_jscores)
                tmp_min_score = min(tmp_dstage_role_jscores)
                tmp_average_score = (tmp_max_score + tmp_min_score) / 2
                tmp_score_count = 1
                for jscore in tmp_dstage_role_jscores:
                    if jscore == tmp_min_score:
                        tmp_min_score = -100
                    elif jscore == tmp_max_score:
                        tmp_max_score = 100
                    else:
                        tmp_score_count += 1
                        tmp_average_score = tmp_average_score + jscore
                tmp_average_score = round(tmp_average_score / tmp_score_count, 1)
                tmp_deduction = 0
                if tmp_stage_role_scores[8] > 0:
                    tmp_deduction = (tmp_stage_role_scores[8] - tmp_stage_role_scores[6] - tmp_stage_role_scores[
                        7]) * 0.2
                tmp_points = 0
                if tmp_stage_role_code == 1:
                    tmp_points = tmp_average_score * (tmp_stage_role_scores[4] - tmp_deduction)
                elif tmp_stage_role_code == 2:
                    tmp_points = tmp_average_score * (tmp_stage_role_scores[5])
                elif tmp_stage_role_code == 3:
                    tmp_points = tmp_average_score * (tmp_stage_role_scores[9])
                # calcuate SP at mpair_team level
                if tmp_mteam_code == tmp_mteam_1:
                    tmp_mteam_1_SP = tmp_mteam_1_SP + round(tmp_points, 1)
                elif tmp_mteam_code == tmp_mteam_2:
                    tmp_mteam_2_SP = tmp_mteam_2_SP + round(tmp_points, 1)
                elif tmp_mteam_code == tmp_mteam_3:
                    tmp_mteam_3_SP = tmp_mteam_3_SP + round(tmp_points, 1)

                tmp_tuple1 = (tmp_stage_role_code, tmp_mteam_code, tmp_stage_role_scores, tmp_dstage_score_list,
                              tmp_stage_role_team_member, round(tmp_average_score, 1), round(tmp_points, 1),
                              round(tmp_deduction, 1))
                tmp_stage_role_list.append(tmp_tuple1)

            if current_stage_code >0:
                tmp_tuple2 = (current_stage_code, tmp_mpair_info, tmp_stage_role_list)
                mpair_stage_role_score_list.append(tmp_tuple2)

            current_stage_code = row[3]
            tmp_stage_role_list = []
            tmp_dstage_score_list = []
            tmp_dstage_role_jscores = []
            tmp_mpair_info = (row[2], row[9], row[11], row[26], row[23]) # mpair_id, round_code, room_code, romm_code_label)
            tmp_stage_role_code = row[4]
            tmp_mteam_code = row[5]
            # MPAIR_TEAM_ID, DSTAGE_TEAM_ID, ap_with_factor, average_point, REP_COEFFICIENCE, OPP_COEFFICIENCE,
            # REP_REJECTION_CREIDT_G1, REP_REJECTION_CREIDT_G2, TOTAL_REJECTED_TIMES
            tmp_stage_role_scores = (row[7], row[8], row[13], row[18], row[19], row[20], row[21], row[22], row[34], row[37])
            tmp_stage_role_team_member = (row[32], row[33]) # TEAM_MEMBER_ID, TEAM_MEMBER_NAME

        if row[4] != tmp_stage_role_code:
            if tmp_stage_role_code > 0:
                # calculate average point
                tmp_max_score = max(tmp_dstage_role_jscores)
                tmp_min_score = min(tmp_dstage_role_jscores)
                tmp_average_score = (tmp_max_score + tmp_min_score) / 2
                tmp_score_count = 1
                for jscore in tmp_dstage_role_jscores:
                    if jscore == tmp_min_score:
                        tmp_min_score = -100
                    elif jscore == tmp_max_score:
                        tmp_max_score = 100
                    else:
                        tmp_score_count += 1
                        tmp_average_score = tmp_average_score + jscore
                tmp_average_score = round(tmp_average_score / tmp_score_count, 1)
                tmp_deduction = 0
                if tmp_stage_role_scores[8] > 0:
                    tmp_deduction = (tmp_stage_role_scores[8] - tmp_stage_role_scores[6] - tmp_stage_role_scores[
                        7]) * 0.2
                tmp_points = 0
                if tmp_stage_role_code == 1:
                    tmp_points = tmp_average_score * (tmp_stage_role_scores[4] - tmp_deduction)
                elif tmp_stage_role_code == 2:
                    tmp_points = tmp_average_score * (tmp_stage_role_scores[5])
                elif tmp_stage_role_code == 3:
                    tmp_points = tmp_average_score * (tmp_stage_role_scores[9])
                # calcuate SP at mpair_team level
                if tmp_mteam_code == tmp_mteam_1:
                    tmp_mteam_1_SP = tmp_mteam_1_SP + round(tmp_points, 1)
                elif tmp_mteam_code == tmp_mteam_2:
                    tmp_mteam_2_SP = tmp_mteam_2_SP + round(tmp_points, 1)
                elif tmp_mteam_code == tmp_mteam_3:
                    tmp_mteam_3_SP = tmp_mteam_3_SP + round(tmp_points, 1)

                tmp_tuple1 = (tmp_stage_role_code, tmp_mteam_code, tmp_stage_role_scores, tmp_dstage_score_list,
                              tmp_stage_role_team_member, round(tmp_average_score, 1), round(tmp_points, 1),
                              round(tmp_deduction, 1))
                tmp_stage_role_list.append(tmp_tuple1)

            tmp_dstage_score_list = []
            tmp_dstage_role_jscores = []
            tmp_stage_role_code = row[4]
            tmp_mteam_code = row[5]
            # MPAIR_TEAM_ID, DSTAGE_TEAM_ID, ap_with_factor, average_point, REP_COEFFICIENCE, OPP_COEFFICIENCE,
            # REP_REJECTION_CREIDT_G1, REP_REJECTION_CREIDT_G2, TOTAL_REJECTED_TIMES
            tmp_stage_role_scores = (row[7], row[8], row[13], row[18], row[19], row[20], row[21], row[22], row[34], row[37])
            tmp_stage_role_team_member = (row[32], row[33]) # TEAM_MEMBER_ID, TEAM_MEMBER_NAME

        #"EVENT_ID, PLAN_ID, MPAIR_ID, STAGE_CODE, STAGE_ROLE_CODE, MTEAM_CODE, TEAM_MEMBER_ID, MPAIR_TEAM_ID, DSTAGE_TEAM_ID, " \ 0-8
        #"ROUND_CODE, ROUND_TYPE, MROOM_CODE, MPAIR_STAGE_STATUS_CODE, POINT_WITH_FACTOR, " \ 9-13
        #"DSTAGE_JUROR_ID, DSTAGE_SCORE_ID, MJUROR_CODE, TOTAL_SCORE, AVERAGE_POINT, " \ 14-18
        #"REP_COEFFICIENCE, OPP_COEFFICIENCE, REP_REJECTION_CREIDT_G1, REP_REJECTION_CREIDT_G2, " \ 19-22
        #"STAGE_MATCH_PROBLEM_CODE, DSTAGE_JUROR_ID, ROUND_TYPE, MROOM_LABEL, " \ 23-26
        #"SC1, SC2, SC3, SC4, SC5, TEAM_MEMBER_ID, TEAM_MEMBER_NAME, TOTAL_REJECTED_TIMES " \ 27-34
        # SC6, SC7, REV_COEFFICIENCE \ 35-37
        # info: DSTAGE_SCORE_ID, MJUROR_CODE, TOTAL_SCORE, SC1, SC2, SC3, SC4, SC5, SC6, SC7 \ 0-4
        tmp_dstage_juror_score = (row[15], row[16], row[17], row[27], row[28], row[29], row[30], row[31], row[35], row[36])
        tmp_dstage_score_list.append(tmp_dstage_juror_score)
        tmp_dstage_role_jscores.append(row[17])

    if tmp_stage_role_code > 0:
        # calculate average point
        tmp_max_score = max(tmp_dstage_role_jscores)
        tmp_min_score = min(tmp_dstage_role_jscores)
        tmp_average_score = (tmp_max_score + tmp_min_score) / 2
        tmp_score_count = 1
        for jscore in tmp_dstage_role_jscores:
            if jscore == tmp_min_score:
                tmp_min_score = -100
            elif jscore == tmp_max_score:
                tmp_max_score = 100
            else:
                tmp_score_count += 1
                tmp_average_score = tmp_average_score + jscore
        tmp_average_score = round(tmp_average_score / tmp_score_count, 1)
        tmp_deduction = 0
        if tmp_stage_role_scores[8] > 0:
            tmp_deduction = (tmp_stage_role_scores[8] - tmp_stage_role_scores[6] - tmp_stage_role_scores[7]) * 0.2
        tmp_points = 0
        if tmp_stage_role_code == 1:
            tmp_points = tmp_average_score * (tmp_stage_role_scores[4] - tmp_deduction)
        elif tmp_stage_role_code == 2:
            tmp_points = tmp_average_score * (tmp_stage_role_scores[5])
        elif tmp_stage_role_code == 3:
            tmp_points = tmp_average_score * (tmp_stage_role_scores[9])
        # calcuate SP at mpair_team level
        if tmp_mteam_code == tmp_mteam_1:
            tmp_mteam_1_SP = tmp_mteam_1_SP + round(tmp_points, 1)
        elif tmp_mteam_code == tmp_mteam_2:
            tmp_mteam_2_SP = tmp_mteam_2_SP + round(tmp_points, 1)
        elif tmp_mteam_code == tmp_mteam_3:
            tmp_mteam_3_SP = tmp_mteam_3_SP + round(tmp_points, 1)

        tmp_tuple1 = (tmp_stage_role_code, tmp_mteam_code, tmp_stage_role_scores, tmp_dstage_score_list, tmp_stage_role_team_member, round(tmp_average_score,1), round(tmp_points,1), round(tmp_deduction,1))
        tmp_stage_role_list.append(tmp_tuple1)

    if current_stage_code > 0:
        tmp_tuple2 = (current_stage_code, tmp_mpair_info, tmp_stage_role_list)
        mpair_stage_role_score_list.append(tmp_tuple2)

    return ( mpair_stage_role_score_list, (round(tmp_mteam_1_SP,1), round(tmp_mteam_2_SP,1), round(tmp_mteam_3_SP,1)) )


# Search all the teams' problems for specific pair (aka round and room)
def search_mpair_problems(plan_id, mpair_id=0, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    if mpair_id > 0:
        command = "SELECT DISTINCT " \
                  "PLAN_ID, MPAIR_ID, ROUND_CODE, MROOM_CODE, STAGE_CODE, " \
                  "DSTAGE_PROBLEM_ID, PROBLEM_CODE, PROBLEM_LABEL_CODE, PROBLEM_LABEL, DSTAGE_PROBLEM_SUB_STATUS_CODE " \
                  "FROM v_dstage_problems_reporter " \
                  "WHERE PLAN_ID=" + str(plan_id) + " " \
                  "AND MPAIR_ID=" + str(mpair_id) + " " \
                  "ORDER by STAGE_CODE, PROBLEM_CODE, DSTAGE_PROBLEM_SUB_STATUS_CODE" \
                  ";"
    else:
        command = "SELECT DISTINCT " \
                  "PLAN_ID, MPAIR_ID, ROUND_CODE, MROOM_CODE, STAGE_CODE, " \
                  "DSTAGE_PROBLEM_ID, PROBLEM_CODE, PROBLEM_LABEL_CODE, PROBLEM_LABEL, DSTAGE_PROBLEM_SUB_STATUS_CODE " \
                  "FROM v_dstage_problems_reporter " \
                  "WHERE PLAN_ID=" + str(plan_id) + " " \
                  "ORDER by ROUND_CODE, MROOM_CODE, STAGE_CODE, PROBLEM_CODE, DSTAGE_PROBLEM_SUB_STATUS_CODE" \
                  ";"

    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result


# get all the teams' problems for specific pair (aka round and room)
def get_mpair_problems_simmple(plan_id, mpair_id=0, app_db_web_location=app_db_web_location_default):
    result_rows = search_mpair_problems(plan_id, mpair_id, app_db_web_location)
    if result_rows is not None and len(result_rows) > 0:
        current_stage_code = 0
        tmp_total_rejected_times = 0
        tmp_dstage_problem_list = []
        mpair_problem_list = []
        for row in result_rows:
            if row[4] != current_stage_code:
                if current_stage_code >0:
                    tmp_tuple2 = (current_stage_code, tmp_dstage_problem_list, tmp_total_rejected_times)
                    mpair_problem_list.append(tmp_tuple2)

                current_stage_code = row[4]
                tmp_dstage_problem_list = []
                tmp_prolem_rejected_times = 0

            #"PLAN_ID, MPAIR_ID, ROUND_CODE, MROOM_CODE, STAGE_CODE, " \ 0-4
            #"DSTAGE_PROBLEM_ID, PROBLEM_CODE, PROBLEM_LABEL_CODE, PROBLEM_LABEL, DSTAGE_PROBLEM_SUB_STATUS_CODE " \ 5-9
            tmp_tuple_dstage_problem_info = (row[5], row[6], row[7], row[8], row[9])
            tmp_dstage_problem_list.append(tmp_tuple_dstage_problem_info)
            if row[9] == 2:
                tmp_total_rejected_times += 1

        if current_stage_code > 0:
            tmp_tuple2 = (current_stage_code, tmp_dstage_problem_list, tmp_total_rejected_times)
            mpair_problem_list.append(tmp_tuple2)

        return mpair_problem_list
    else:
        return None


def update_dstage_score_by_id(plan_id, dstage_score_id, dstage_scores, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())

    # update MPAIR stage_status_code
    if len(dstage_scores) > 6:
        _c.execute(
            "UPDATE DSTAGE_SCORE SET TOTAL_SCORE = ?, SC1=?, SC2=?, SC3=?, SC4=?, SC5=?, SC6=?, SC7=?, SCORE_ENTER_BY = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND DSTAGE_SCORE_ID = ?",
            (dstage_scores[0], dstage_scores[1], dstage_scores[2], dstage_scores[3], dstage_scores[4], dstage_scores[5],
             dstage_scores[6], dstage_scores[7],
             current_user_id, current_user_id, current_timestamp, plan_id, dstage_score_id))
    else:
        _c.execute("UPDATE DSTAGE_SCORE SET TOTAL_SCORE = ?, SC1=?, SC2=?, SC3=?, SC4=?, SC5=?, SCORE_ENTER_BY = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND DSTAGE_SCORE_ID = ?",
                   (dstage_scores[0], dstage_scores[1], dstage_scores[2], dstage_scores[3], dstage_scores[4], dstage_scores[5],
                    current_user_id, current_user_id, current_timestamp, plan_id, dstage_score_id))

    _conn.commit()
    _conn.close()


# update the calculated scores for the dstage_team and mpair_team, also update the mpair stage status to 99-completed
def validate_dstage_score(plan_id, mpair_id, mpair_team_records, dstage_team_records, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())

    # update four dstage_teams of the current mpair_id: Average Point, Point (POINT_WITH_FACTOR)
    # stage 1/2/3: rep and opp, rev
    for row in dstage_team_records:
        _c.execute("UPDATE DSTAGE_TEAM SET AVERAGE_POINT = ?, POINT_WITH_FACTOR=?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND DSTAGE_TEAM_ID = ?",
                   (row[1], row[2], current_user_id, current_timestamp, plan_id, row[0]))

    # update three mpair_teams of the current mpair_id: SP and FW=1 or 0
    # winner is the first record
    # use mteam_code and mpair_id to find mpair_team_id (PK)
    for row in mpair_team_records:
        _c.execute("UPDATE MPAIR_TEAM SET SP = ?, FIGHT_WON=?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND MPAIR_ID = ? AND MTEAM_CODE = ?",
                   (row[1], row[2], current_user_id, current_timestamp, plan_id, mpair_id, row[0]))

    #update the mpair stage status by mpair id
    _c.execute(
        "UPDATE MPAIR SET MPAIR_STAGE_STATUS_CODE = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND MPAIR_ID = ?",
        (99, current_user_id, current_timestamp, plan_id, mpair_id))

    _conn.commit()
    _conn.close()


# search the round information for final match for a specific event
def search_fm_round(event_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT " \
              "EVENT_ID, ROUND_CODE, EVENT_ROUND_ID, ROUND_TYPE, ROUND_LABEL, ROUND_STATUS, ROUND_DAY_NUM " \
              "FROM EVENT_ROUND " \
              "WHERE EVENT_ID=" + str(event_id) + " " \
              "AND ROUND_TYPE='FM' " \
              "AND ROUND_STATUS='Active' " \
              "ORDER by ROUND_CODE" \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    fm_round = None
    for row in result:
        fm_round = (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        break

    return fm_round


# search the final match plan for a specific fm plan id
def search_fm_plan(event_id, fm_plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    # search fm_plan_teams
    command = "SELECT " \
              "MPAIR_ID, ROUND_CODE, EVENT_ROUND_ID, MROOM_ID, MROOM_CODE, MROOM_LABEL, " \
              "MPAIR_TEAM_ID, MTEAM_CODE, MTEAM_ID, MPAIR_SIDS, MPAIR_STAGE_STATUS_CODE " \
              "FROM v_mpair_team " \
              "WHERE PLAN_ID=" + str(fm_plan_id) + " " \
              "AND ROUND_TYPE='FM' " \
              "ORDER by MPAIR_TEAM_ID" \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    fm_plan_teams = list()
    pair_info = None
    round_info = None
    room_info = None
    i = 0
    for row in result:
        i += 1
        if i == 1:
            round_info = (row[2], row[1]) # roound_id, round_code
            room_info = (row[3], row[4], row[5]) # mroom_id, mroom_code, mroom_label
            pair_info = (row[0], row[9], row[10]) # mpair_id, MPAIR_SIDS, MPAIR_STAGE_STATUS_CODE
        fm_plan_teams.append((row[6], row[7], row[8])) # mpair_team_id, mteam_code, mteam_id

    # search fm_plan_jurors
    command = "SELECT " \
              "MPAIR_JUROR_ID, MJUROR_CODE, MJUROR_ID " \
              "FROM MPAIR_JUROR " \
              "WHERE PLAN_ID=" + str(fm_plan_id) + " " \
              "ORDER by MPAIR_JUROR_ID" \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    fm_plan_jurors = list()
    for row in result:
        fm_plan_jurors.append((row[0], row[1], row[2]))

    _conn.commit()
    _conn.close()

    return (fm_plan_teams, fm_plan_jurors, pair_info, round_info, room_info)


# check if all the sm stages completed for a specific event and sm_plan_id
def check_sm_status(plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    command = "SELECT count(*) " \
              "FROM MPAIR " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "AND MPAIR_STAGE_STATUS_CODE!=99 " \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result[0][0]


# check if final match score is ready for public for a specific fm_plan_id
def check_fm_status(plan_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    fm_status = []

    command = "SELECT MPAIR_ID, MPAIR_STAGE_STATUS_CODE " \
              "FROM MPAIR " \
              "WHERE PLAN_ID=" + str(plan_id) + " " \
              "AND MPAIR_STAGE_STATUS_CODE=99 " \
              ";"
    _c.execute(command)
    result = _c.fetchall()

    if result is not None and len(result) > 0:
        print("***___ result ", result)
        mpair_id = result[0][0]
        fm_status.append(mpair_id)
        # get final match scores
        command = "SELECT MPAIR_TEAM_ID, MTEAM_ID, MTEAM_CODE, SP, FIGHT_WON " \
                  "FROM MPAIR_TEAM " \
                  "WHERE PLAN_ID=" + str(plan_id) + " " \
                  "AND MPAIR_ID=" + str(mpair_id) + " " \
                  "ORDER BY SP DESC, FIGHT_WON DESC " \
                  ";"
        _c.execute(command)
        result = _c.fetchall()
        fm_status.append(result)
    else:
        fm_status = None

    _conn.commit()
    _conn.close()

    return fm_status


# add quick comments to mpair.field as temporary solution
def add_problem_guide(plan_id, mpair_id, problem_guide, current_user_id, app_db_web_location=app_db_web_location_default):
    _conn = sqlite3.connect(app_db_web_location)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())

    _c.execute("UPDATE MPAIR SET Field14 = ?, last_updated_by = ?, last_updated_date = ? WHERE PLAN_ID = ? AND MPAIR_ID = ? ",
               (problem_guide, current_user_id, current_timestamp, plan_id, mpair_id))

    _conn.commit()
    _conn.close()
