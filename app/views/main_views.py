# Copyright StemFellowship
#
# Authors: Andrew Mao


from flask import Blueprint, redirect, render_template, flash, session
from flask import request, url_for
from flask_user import current_user, login_required, roles_required
from flask import current_app
from app.models.app_db_handler import get_school_list, search_teams_ledbyme, add_team, add_school, add_team_member, \
    get_current_teams_options, get_schools_has_event_team, search_teams_joinedbyme, get_school_teams_n_members, \
    add_event_participant, add_event_participant_with_coi, get_event_ppant_n_mycois, search_event_teams, \
    get_event_teams_n_members_ledbyme, count_team_group_by_status, count_team_member_group_by_status, \
    count_juror_group_by_status, count_volunteer_group_by_status, get_event_teams_n_members_all, update_a_team_status, \
    search_schools_by_id, update_a_school_by_id, get_event_ppant_n_cois_by_roletype, update_a_ppant_status, \
    search_team_members_all, update_a_team_member_status, get_schools_for_ppant, update_event_participant, \
    add_event_juror_as_tl, search_event_rooms, db_save_proposal, search_event_plan, get_mpair_by_round_room, \
    search_mroom, get_mjuror_by_room, search_mteam_by_code, get_mpair_team_by_round_team, \
    get_mpair_jurors_by_round_room, \
    update_plan_status, admin_delete_plan, set_juror_chair, search_events_ppant_n_cois_for_data_entry, \
    get_event_ppant_n_cois_for_volunteer, search_event_teams_inorder, get_mvolunteer_by_room, \
    get_event_juror_n_cois_by_chair, release_sm_plan, get_mteams, get_mrooms, get_mjurors, get_mvolunteers, \
    search_mroom_assigned_to_data_entry, get_mpairs_by_room_round, initialize_sm_stage_agenda, get_sm_stage_agenda, \
    save_stage_members, get_event_group_problems, save_stage_problems, update_mpair_stage_status, \
    get_stage_jurors, save_stage_scores, get_event_master_problems, get_team_member_roles, get_reporter_team_problems, \
    get_schedue_by_round_room, get_mpair_scores_4validate, get_mpair_problems_simmple, update_dstage_score_by_id, \
    validate_dstage_score, get_my_team_schedue, get_juror_schedue, get_volunteer_schedue, update_plan_sub_status_by_id, \
    get_sm_team_rank, search_fm_round, db_save_fm_proposal, search_fm_plan, check_sm_status, get_reporter_problems, \
    initialize_fm_stage_agenda, save_fm_stage_members, save_fm_stage_scores, get_all_reporter_problems, \
    get_fm_mpair_scores_4validate, add_problem_guide, get_sm_team_rank_by_round, get_sm_member_rank_by_round, \
    check_fm_status
from app import db
from app.utilities.app_utilities import calculate_age_from_datetime, count_by_status, convert_background_text, \
    team_matching_2, assign_team_code_randomly, assign_room_juror_code_randomly, assign_room_to_team, \
    tournament_plan_cleanup, get_sm_performance_order, assign_volunteer, assign_team_code_inorder, assign_chair_room, \
    assign_room_to_team_wt_chair, assign_moved_jurors, assign_volunteers, get_fm_performance_order, check_ranking3, \
    check_ranking2, get_2days_timeslots
from app.models.user_models import UserProfileForm
from app.forms.app_forms import CreateTeamForm, JoinTeamForm, ApproveRegistForm, SchoolForm, PpantForm, EventPlanForm, \
    EventStageForm, EventFinalPlanForm
import secrets
#from flask_weasyprint import render_pdf, HTML


main_blueprint = Blueprint('main', __name__, template_folder='templates')


@main_blueprint.app_errorhandler(400)
def FUN_400(error):
    return render_template("main/page_400.html"), 401


@main_blueprint.app_errorhandler(401)
def FUN_401(error):
    return render_template("main/page_401.html"), 401


@main_blueprint.app_errorhandler(403)
def FUN_403(error):
    return render_template("main/page_403.html"), 403


@main_blueprint.app_errorhandler(404)
def FUN_404(error):
    return render_template("main/page_404.html"), 404


@main_blueprint.app_errorhandler(405)
def FUN_405(error):
    return render_template("main/page_405.html"), 405


@main_blueprint.app_errorhandler(413)
def FUN_413(error):
    return render_template("main/page_413.html"), 413


# The Public page is accessible to all
@main_blueprint.route('/public', methods=['GET', 'POST'])
def public_page():
    return render_template('main/how_to_apply.html')


# The Public page is accessible to all
@main_blueprint.route('/training', methods=['GET', 'POST'])
def training():
    return render_template('main/training1.html')


# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']

    # manual turn on/off the system, remember to update the member_page()
    #app_available = False # system is NOT avaiailable, it is under maintain
    app_available = True # system is available
    if app_available:
        active_pan_list = search_event_plan(1, "Active", 1, app_db_web_location)
        plan_sub_status = 0
        for plan in active_pan_list:
            #plan_id = plan[1]
            plan_sub_status = plan[4]  # 1-released 2-published
            break
        return render_template('main/home_page.html', plan_sub_status=plan_sub_status)
    else:
        return render_template('main/system_not_available.html')


# The Member page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/member', methods=['GET', 'POST'])
@login_required  # Limits access to authenticated users
def member_page():
    # manual turn on/off the system, remember to update the home_page()
    #app_available = False # system is NOT avaiailable, it is under maintain
    app_available = True  # system is available
    if not app_available:
        # reditect to logout
        flash_msg = "System is under maintainance, please try again in two hours."
        flash(flash_msg, 'error')
        return redirect(url_for('user.logout'))

    # before starting the tournament plan, you should manually disable all the members to update his/her informaiton
    #member_editable = False # member is Not allowed to be updated from now on
    member_editable = True  # member is ok to update his/her information

    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    event_id = current_app.config['CURRENT_EVENT']

    # check if current event plan has been activated
    plan_status = "Inactive" # plan is not ready
    active_pan_list = search_event_plan(event_id, "Active", 0, app_db_web_location)
    for plan in active_pan_list:
        plan_status = plan[2]
        break
    # Initialize form
    form = CreateTeamForm(request.form)

    # Process valid POST
    if request.method == 'POST':
        team_lead_id = current_user.id
        team_school_id = request.form['school_id']
        team_name = request.form['team_name']
        teleconferencing = request.form['teleconferencing']

        if int(team_school_id) > 0:
            add_team(event_id, team_lead_id, team_school_id, team_name, teleconferencing, app_db_web_location)
        else:
            print("*****--- no school id, something wrong")

        # Redirect to member dashboard page
        return redirect(url_for('main.member_page'))
    else:
        # calculate current user's age
        age = round(calculate_age_from_datetime(current_user.dob), 1)

        my_background_text = None
        my_background = 0
        try:
            my_background = int(current_user.background)
            my_background_text = convert_background_text(current_user.background)
        except:
            pass

        # Retrieve database settings from app.config
        app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']

        myteams_list = get_event_teams_n_members_ledbyme(event_id, current_user.id, app_db_web_location)
        myteams_count_led = len(myteams_list)

        # initialize team school info
        if myteams_count_led > 0:
            for row in myteams_list:
                form.school_name.process_data(row[3])
                form.school_id.process_data(row[7])
                form.submit.label.text = "Add one more team"
                break

        myteams_table_led = zip([x[0] for x in myteams_list], \
                            [x[1] for x in myteams_list], \
                            [x[2] for x in myteams_list], \
                            [x[3] for x in myteams_list], \
                            [x[4] for x in myteams_list], \
                            [x[5] for x in myteams_list], \
                            [x[6] for x in myteams_list], \
                            [x[7] for x in myteams_list], \
                            [x[8] for x in myteams_list], \
                            [x[9] for x in myteams_list], \
                            [x[10] for x in myteams_list], \
                            [x[11] for x in myteams_list], \
                            [x[12] for x in myteams_list])

        results = search_teams_joinedbyme(event_id, current_user.id, app_db_web_location)
        myteams_table_joined = results[0]
        myteams_count_joined_approved = results[1]
        myteams_count_joined = len(myteams_table_joined)
        # get participant info
        myparticipation_list = get_event_ppant_n_mycois(event_id, current_user.id, 0, app_db_web_location)
        myparticipation_count = len(myparticipation_list)
        two_day_timeslots = get_2days_timeslots()
        if plan_status == "Active":
            return render_template('main/member_page_tournament.html', member_age=age, data_entry=1, two_day_timeslots=two_day_timeslots,
                               myparticipation_list=myparticipation_list, myparticipation_count=myparticipation_count,
                               led_teams_list=myteams_table_led, led_teams_count=myteams_count_led, plan_status=plan_status,
                               joined_teams_list=myteams_table_joined, joined_teams_count=myteams_count_joined, form=form, my_background=my_background, my_background_text=my_background_text)
        else:
            return render_template('main/member_page.html', member_age=age, myteams_count_joined_approved=myteams_count_joined_approved,
                               myparticipation_list=myparticipation_list, myparticipation_count=myparticipation_count,
                               led_teams_list=myteams_table_led, led_teams_count=myteams_count_led, member_editable=member_editable,
                               joined_teams_list=myteams_table_joined, joined_teams_count=myteams_count_joined, form=form,
                                   my_background=my_background, my_background_text=my_background_text, two_day_timeslots=two_day_timeslots)


@main_blueprint.route('/register_team', methods=['GET', 'POST'])
@login_required  # Limits access to authenticated users
def register_team():
    #initialize form
    form = CreateTeamForm(request.form)
    db_created_by_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']

    if request.method == 'POST' and form.validate():
        team_lead_id = current_user.id
        team_school_id = request.form['school_id']
        team_name = request.form['team_name']
        teleconferencing = request.form['teleconferencing']

        if int(team_school_id) > 0:
            add_team(event_id, team_lead_id, team_school_id, team_name, teleconferencing, app_db_web_location)
        else:
            # add a new school and then add a new team for the new school
            school_name = request.form['school_name']
            school_address = request.form['address']
            country = 'CA'
            province = request.form['province']
            city = request.form['city']
            postal_code = request.form['postal_code']
            team_lead_id = current_user.id

            try:
                new_school_id = add_school(school_name, school_address, city, province, country, postal_code,
                                           db_created_by_id, app_db_web_location)
                add_team(event_id, team_lead_id, new_school_id, team_name, teleconferencing, app_db_web_location)
            except:
                flash_msg = "Duplicted school name or incorrect school info"
                flash(flash_msg, 'error')
                return redirect(url_for('main.member_page'))

        # reditect to member dashboard
        flash_msg = "Your request is approved."
        flash(flash_msg, 'success')
        return redirect(url_for('main.member_page'))
    else:
        # select SCHOOL_ID, SCHOOL_NAME, PROVINCE, CITY, SCHOOL_ADDRESS, ZIP_CODE from SCHOOL_DIRECTORY
        school_list = get_school_list(app_db_web_location)

        form.school_id.choices = school_list

        # Process GET or invalid POST
        return render_template('main/register_team.html', form=form)


@main_blueprint.route('/be_juror', methods=['GET', 'POST'])
@login_required  # Limits access to authenticated users
def be_juror():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']

    db_created_by_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = JoinTeamForm(request.form) # change to BeJurorForm later

    # Process valid POST
    if request.method == 'POST':
        selected_schools = request.form.getlist("school")
        teleconferencing = request.form.get("teleconferencing")
        juror_experience = request.form.get("juror_experience")
        selected_times = request.form.getlist("timeslot")
        tslot1 = "No"
        tslot2 = "No"
        tslot3 = "No"
        tslot4 = "No"
        print(selected_times)
        for timeslot in selected_times:
            if timeslot == "1":
                tslot1 = "Yes"
            elif timeslot == "2":
                tslot2 = "Yes"
            elif timeslot == "3":
                tslot3 = "Yes"
            elif timeslot == "4":
                tslot4 = "Yes"
        if selected_schools is None or len(selected_schools) < 1:
            add_event_participant(event_id, current_user.id, db_created_by_id, "Juror", 0, teleconferencing, tslot1, tslot2, tslot3, tslot4, app_db_web_location, juror_experience)
        else:
            add_event_participant_with_coi(event_id, current_user.id, db_created_by_id, "Juror", 1, selected_schools, teleconferencing, tslot1, tslot2, tslot3, tslot4, app_db_web_location, juror_experience)

        # Redirect to home page
        flash_msg = "Your request is under review, please sign to check after two days."
        flash(flash_msg, 'success')

        return redirect(url_for('main.member_page'))
    else:
        school_list = get_schools_for_ppant(event_id, app_db_web_location)

        # Process GET or invalid POST
        two_day_timeslots = get_2days_timeslots()
        return render_template('main/be_juror.html', form=form, current_school_list=school_list, two_day_timeslots=two_day_timeslots)


@main_blueprint.route('/be_juror_as_tl', methods=['GET', 'POST'])
@login_required  # Limits access to authenticated users
def be_juror_as_tl():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']

    db_created_by_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = JoinTeamForm(request.form) # change to BeJurorForm later

    # Process valid POST
    if request.method == 'POST':
        selected_schools = request.form.getlist("school")
        teleconferencing = request.form.get("teleconferencing")
        juror_experience = request.form.get("juror_experience")
        selected_times = request.form.getlist("timeslot")
        tl_school_id = int(request.form.get('tl_school_id'))
        tslot1 = "No"
        tslot2 = "No"
        tslot3 = "No"
        tslot4 = "No"
        for timeslot in selected_times:
            if timeslot == "1":
                tslot1 = "Yes"
            elif timeslot == "2":
                tslot2 = "Yes"
            elif timeslot == "3":
                tslot3 = "Yes"
            elif timeslot == "4":
                tslot4 = "Yes"
        if selected_schools is None or len(selected_schools) < 1:
            selected_schools = [tl_school_id]
        else:
            if tl_school_id in selected_schools:
                pass
            else:
                selected_schools.append(tl_school_id)
        add_event_juror_as_tl(event_id, current_user.id, db_created_by_id, "Juror", 1, selected_schools, teleconferencing, tslot1, tslot2, tslot3, tslot4, 1, tl_school_id, juror_experience, app_db_web_location)

        # Redirect to home page
        flash_msg = "Your request is under review, please sign to check after two days."
        flash(flash_msg, 'success')

        return redirect(url_for('main.member_page'))
    else:
        tl_school_id = int(request.args.get('school'))
        school_list = get_schools_for_ppant(event_id, app_db_web_location)

        # Process GET or invalid POST
        return render_template('main/be_juror_as_tl.html', form=form, current_school_list=school_list, tl_school_id=tl_school_id)


@main_blueprint.route('/be_volunteer', methods=['GET', 'POST'])
@login_required  # Limits access to authenticated users
def be_volunteer():
    #prepare parameter
    event_id = current_app.config['CURRENT_EVENT']
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    # Initialize form
    form = JoinTeamForm(request.form) # change to BeJurorForm later
    if request.method == 'POST':
        selected_schools = request.form.getlist('school')
        selected_times = request.form.getlist("timeslot")
        tslot1 = "No"
        tslot2 = "No"
        tslot3 = "No"
        tslot4 = "No"
        for timeslot in selected_times:
            if timeslot == "1":
                tslot1 = "Yes"
            elif timeslot == "2":
                tslot2 = "Yes"
            elif timeslot == "3":
                tslot3 = "Yes"
            elif timeslot == "4":
                tslot4 = "Yes"

        if selected_schools is None or len(selected_schools)<1:
            add_event_participant(event_id, current_user.id, current_user.id, 'Volunteer', 0, 'Not Applicable', tslot1, tslot2, tslot3, tslot4, app_db_web_location, None)
        else:
            add_event_participant_with_coi(event_id, current_user.id, current_user.id, 'Volunteer', 1, selected_schools,'-----', tslot1, tslot2, tslot3, tslot4, app_db_web_location, None)
        flash_msg = "Your request is approved."
        flash(flash_msg, 'success')
        return redirect(url_for('main.member_page'))
    else:
        #call function
        two_day_timeslots = get_2days_timeslots()
        school_list = get_schools_for_ppant(event_id, app_db_web_location)
        return render_template('main/be_volunteer.html', form = form, school_list = school_list,
                               two_day_timeslots=two_day_timeslots)


# join a team as student
@main_blueprint.route('/join_team', methods=['GET', 'POST'])
@login_required  # Limits access to authenticated users
def join_team():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']

    db_created_by_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = JoinTeamForm(request.form)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        team_id = request.form['team_id']
        if int(team_id) > 0:
            add_team_member(team_id, db_created_by_id, app_db_web_location)
        else:
            # something is wrong
            pass

        # Redirect to home page
        flash_msg = "Your request is under review by your team lead, please sign to check after two days."
        flash(flash_msg, 'success')
        return redirect(url_for('main.member_page'))
    else:
        school_list = get_schools_has_event_team(event_id, app_db_web_location)

        form.team_school_id.choices = school_list

        # get current year's teams
        current_teams_options = get_current_teams_options(event_id, app_db_web_location)
        # get the teams that current user has already joined (even though that could be rejected)
        myteams_table_joined = search_teams_joinedbyme(event_id, current_user.id, app_db_web_location)[0]
        # add all the team id into a list
        myteams_table_joined_ids = []
        for item in myteams_table_joined:
            myteams_table_joined_ids.append(item[7])

        # removed the teams tht I have already joined from the option list
        #print(myteams_table_joined_ids)
        current_teams_table = []
        for school in current_teams_options:
            school_team_options = []
            for team in school[2]:
                #print(team, team[2] in myteams_table_joined_ids)
                if not (team[2] in myteams_table_joined_ids):
                    school_team_options.append(team)
            if school_team_options is not None and len(school_team_options) > 0:
                current_teams_table.append([school[0], school[1], school_team_options])
        """  
        current_teams_table = zip([x[0] for x in current_teams_options], \
                            [x[1] for x in current_teams_options], \
                            [x[2] for x in current_teams_options])
        """
        # Process GET or invalid POST
        return render_template('main/join_team.html', form=form, current_team_options=current_teams_table, current_school_list=school_list)


# approve team member by team lead
@main_blueprint.route('/team_member_approval')
@login_required  # Limits access to authenticated users
def team_member_approval():
    event_id = current_app.config['CURRENT_EVENT']
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    db_user_id = current_user.id

    member_approval_type = request.args.get('type')
    team_lead_id_str = request.args.get('lead_id')
    member_name = request.args.get('member_name')
    member_id = request.args.get('member_id')
    is_captain = request.args.get('captain')

    if team_lead_id_str is None or len(team_lead_id_str) < 1:
        flash_msg = "No team lead selected, please double check your data."
        flash(flash_msg, 'error')
    else:
        team_lead_id = int(team_lead_id_str)
        if team_lead_id != current_user.id:
            flash_msg = "Invalid access, please double check your data."
            flash(flash_msg, 'error')
        else:
            if member_approval_type.lower() == "approve":
                # approve a team member
                update_a_team_member_status(member_id, "Approved", is_captain, db_user_id, app_db_web_location)
                flash_msg = "Team member #" + str(member_id) + "-" + member_name + " has been approved."
                flash(flash_msg, 'success')
            elif member_approval_type.lower() == "reject":
                # reject a team member
                # force is_captain == 0
                is_captain = 0
                update_a_team_member_status(member_id, "Rejected", is_captain, db_user_id, app_db_web_location)
                flash_msg = "Team member #" + str(member_id) + "-" + member_name + " has been rejected."
                flash(flash_msg, 'success')
            else:
                flash_msg = "No record updated, please double check your data."
                flash(flash_msg, 'error')

    return redirect(url_for('main.member_page'))


# Member updates availability and coi
@main_blueprint.route('/update_ppant', methods=['GET', 'POST'])
@login_required  # Limits access to authenticated users
def update_ppant():
    event_id = current_app.config['CURRENT_EVENT']
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    db_user_id = current_user.id

    # Initialize form
    form = PpantForm(request.form)
    role_type = request.args.get('type')
    ppant_id_str = request.args.get('ppant_id')

    # Process valid POST
    if request.method == 'POST' and form.validate():
        ppant_id = int(form.ppant_id.data)
        last_coi_count = int(form.last_coi_count.data)
        selected_schools = request.form.getlist("school")
        teleconferencing = request.form.get("teleconferencing")
        selected_times = request.form.getlist("timeslot")
        tl_school_id = int(request.form.get('tl_school_id'))
        tslot1 = "No"
        tslot2 = "No"
        tslot3 = "No"
        tslot4 = "No"
        juror_experience = request.form.get("juror_experience")
        for timeslot in selected_times:
            if timeslot == "1":
                tslot1 = "Yes"
            elif timeslot == "2":
                tslot2 = "Yes"
            elif timeslot == "3":
                tslot3 = "Yes"
            elif timeslot == "4":
                tslot4 = "Yes"
        if tl_school_id > 0:
            if selected_schools is None or len(selected_schools) < 1:
                selected_schools = [tl_school_id]
            else:
                if tl_school_id in selected_schools:
                    pass
                else:
                    selected_schools.append(tl_school_id)
        update_event_participant(event_id, ppant_id, teleconferencing, tslot1, tslot2, tslot3, tslot4, selected_schools, last_coi_count, db_user_id, juror_experience, app_db_web_location)
        flash_msg = "Updated successfully. (Participant #" + str(ppant_id) + ")"
        flash(flash_msg, 'success')
    else:
        if ppant_id_str is None or len(ppant_id_str) < 1:
            flash_msg = "No participant selected, please double check your data."
            flash(flash_msg, 'error')
        else:
            ppant_id = int(ppant_id_str)
            tl_school_id = int(request.args.get('tl_school_id'))
            # get participant info
            myparticipation_list = get_event_ppant_n_mycois(event_id, current_user.id, ppant_id, app_db_web_location)
            myparticipation_count = len(myparticipation_list)
            my_coi = None
            if myparticipation_list is not None:
                for item in myparticipation_list:
                    #SCHOOL_ID, SCHOOL_NAME, PROVINCE, CITY, SCHOOL_ADDRESS, ZIP_CODE
                    form.role_type.data = item[0]
                    form.ppant_id.data = item[9]
                    form.time_slot1.data = item[5]
                    form.time_slot2.data = item[6]
                    form.time_slot3.data = item[7]
                    form.time_slot4.data = item[8]
                    form.teleconferencing.data = item[4]
                    form.juror_experience.data = item[11]
                    # form.is_chair.data = item[12]
                    my_coi = item[3]
                    form.last_coi_count.data = len(my_coi)
                    break
                school_list = get_schools_for_ppant(event_id, app_db_web_location)
                my_coi_ids = []
                for coi_school in my_coi:
                    my_coi_ids.append(coi_school[1])

                two_day_timeslots = get_2days_timeslots()
                return render_template('main/update_ppant.html', form=form, current_school_list=school_list,
                                       my_coi_ids=my_coi_ids, tl_school_id=tl_school_id, two_day_timeslots=two_day_timeslots)
            else:
                flash_msg = "No record updated, please double check your data."
                flash(flash_msg, 'error')
    return redirect(url_for('main.member_page'))


# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_page():
    event_id = current_app.config['CURRENT_EVENT']
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']

    # prepare team number summary by status
    team_counts = count_team_group_by_status(event_id, app_db_web_location)
    team_counts_total = team_counts[0]
    team_count_data = [0,0,0]
    if team_counts_total > 0:
        team_count_data = [count_by_status(team_counts[1], "Approved"),
                           count_by_status(team_counts[1], "Requested"),
                           count_by_status(team_counts[1], "Rejected")]

    # prepare team member number summary by status
    team_member_counts = count_team_member_group_by_status(event_id, app_db_web_location)
    team_member_counts_total = team_member_counts[0]
    team_member_count_data = [0,0,0]
    if team_member_counts_total > 0:
        team_member_count_data = [count_by_status(team_member_counts[1], "Approved"),
                                  count_by_status(team_member_counts[1], "Requested"),
                                  count_by_status(team_member_counts[1], "Rejected")]

    # prepare juror number summary by status
    juror_counts = count_juror_group_by_status(event_id, app_db_web_location)
    juror_counts_total = juror_counts[0]
    juror_count_data = [0,0,0]
    if juror_counts_total > 0:
        juror_count_data = [count_by_status(juror_counts[1], "Approved"),
                           count_by_status(juror_counts[1], "Requested"),
                           count_by_status(juror_counts[1], "Rejected")]

    # prepare volunteer number summary by status
    volunteer_counts = count_volunteer_group_by_status(event_id, app_db_web_location)
    volunteer_counts_total = volunteer_counts[0]
    volunteer_count_data = [0,0,0]
    if volunteer_counts_total > 0:
        volunteer_count_data = [count_by_status(volunteer_counts[1], "Approved"),
                           count_by_status(volunteer_counts[1], "Requested"),
                           count_by_status(volunteer_counts[1], "Rejected")]

    return render_template('main/admin_page.html', team_count_data = team_count_data, team_count_total=team_counts_total,
                           team_member_count_data = team_member_count_data, team_member_count_total=team_member_counts_total,
                           juror_count_data = juror_count_data, juror_count_total=juror_counts_total,
                           volunteer_count_data = volunteer_count_data, volunteer_count_total=volunteer_counts_total)


# The Admin - view registration of team, student, juror and volunteer page is accessible to users with the 'admin' role
@main_blueprint.route('/admin_view_regist')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_view_regist():
    event_id = current_app.config['CURRENT_EVENT']
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    sm_active_pan_list = search_event_plan(event_id, "Active", 1, app_db_web_location)
    sm_plan_sub_status = 0
    sm_plan_id = 0
    for plan in sm_active_pan_list:
        sm_plan_id = plan[1]
        sm_plan_sub_status = plan[4] # 1-released 2-published
        break

    # Initialize form
    form = ApproveRegistForm(request.form)
    regist_type = request.args.get('type')
    regist_lable = request.args.get('label')

    if regist_type is None or len(regist_type) < 1:
        return redirect(url_for('main.admin_page'))
    else:
        if regist_type.lower() == 'team':
            team_list = []
            if regist_lable is None or len(regist_lable) < 1:
                team_list = get_event_teams_n_members_all(event_id, None, app_db_web_location)
                regist_lable = "in the system"
            else:
                team_list = get_event_teams_n_members_all(event_id, regist_lable, app_db_web_location)

            teams_count = len(team_list)

            return render_template('main/admin_view_team.html', team_list = team_list, teams_count = teams_count,
                                   team_status = regist_lable, sm_plan_sub_status=sm_plan_sub_status)
        elif regist_type.lower() == 'student':
            if regist_lable is None or len(regist_lable) < 1:
                student_list = search_team_members_all(event_id, None, app_db_web_location)
                regist_lable = "in the system"
            else:
                student_list = search_team_members_all(event_id, regist_lable, app_db_web_location)

            students_count = len(student_list)
            student_list_table = zip([x[0] for x in student_list], \
                                   [x[1] for x in student_list], \
                                   [x[2] for x in student_list], \
                                   [x[3] for x in student_list], \
                                   [x[4] for x in student_list], \
                                   [x[5] for x in student_list], \
                                   [x[6] for x in student_list], \
                                   [x[7] for x in student_list], \
                                   [x[8] for x in student_list], \
                                   [x[9] for x in student_list], \
                                   [x[10] for x in student_list], \
                                   [x[11] for x in student_list], \
                                   [x[12] for x in student_list], \
                                   [x[13] for x in student_list], \
                                   [x[14] for x in student_list], \
                                   [x[15] for x in student_list], \
                                   [x[16] for x in student_list], \
                                   [x[17] for x in student_list], \
                                   [x[18] for x in student_list], \
                                   [x[19] for x in student_list], \
                                   [x[20] for x in student_list], \
                                   [x[21] for x in student_list], \
                                   [x[22] for x in student_list], \
                                   [x[23] for x in student_list], \
                                   [x[24] for x in student_list])

            return render_template('main/admin_view_student.html', student_list=student_list_table, students_count=students_count,
                                   student_status=regist_lable)
        elif regist_type.lower() == 'juror':
            if regist_lable is None or len(regist_lable) < 1:
                juror_list = get_event_ppant_n_cois_by_roletype(event_id, None, "Juror", app_db_web_location)
                regist_lable = "in the system"
            else:
                juror_list = get_event_ppant_n_cois_by_roletype(event_id, regist_lable, "Juror", app_db_web_location)
            jurors_count = len(juror_list)
            return render_template('main/admin_view_juror.html', juror_list=juror_list, jurors_count=jurors_count,
                                   juror_status=regist_lable, sm_plan_sub_status=sm_plan_sub_status)
        elif regist_type.lower() == 'volunteer':
            if regist_lable is None or len(regist_lable) < 1:
                #call function
                volunteer_list = get_event_ppant_n_cois_by_roletype(event_id, None, 'Volunteer', app_db_web_location)
                regist_lable = 'In the System'
            else:
                #call function
                volunteer_list = get_event_ppant_n_cois_by_roletype(event_id, regist_lable, 'Volunteer', app_db_web_location)
            volunteer_count = len(volunteer_list)
            return render_template('main/admin_view_volunteer.html', volunteer_list = volunteer_list, volunteer_status = regist_lable, volunteer_count = volunteer_count)
        else:
            return render_template('main/public_page.html')


# The Admin - team approval page is accessible to users with the 'admin' role
@main_blueprint.route('/admin_team_approval')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_team_approval():
    event_id = current_app.config['CURRENT_EVENT']
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    db_user_id = current_user.id

    team_approval_type = request.args.get('type')
    team_id_str = request.args.get('team_id')
    team_name = request.args.get('team_name')

    if team_id_str is None or len(team_id_str) < 1:
        flash_msg = "No team selected, please double check your data."
        flash(flash_msg, 'error')
    else:
        team_id = int(team_id_str)
        if team_approval_type.lower() == "approve":
            # approve a team
            update_a_team_status(event_id, team_id, "Approved", db_user_id, app_db_web_location)
            flash_msg = "Team #" + str(team_id) + "-" + team_name + " has been approved."
            flash(flash_msg, 'success')
        elif team_approval_type.lower() == "reject":
                # approve a team
                update_a_team_status(event_id, team_id, "Rejected", db_user_id, app_db_web_location)
                flash_msg = "Team #" + str(team_id) + "-" + team_name + " has been rejected."
                flash(flash_msg, 'error')
        else:
            flash_msg = "No record updated, please double check your data."
            flash(flash_msg, 'error')
    return redirect(url_for('main.admin_page'))


# The Admin - team approval page is accessible to users with the 'admin' role
@main_blueprint.route('/admin_review_school', methods=['GET', 'POST'])
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_review_school():
    event_id = current_app.config['CURRENT_EVENT']
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    db_user_id = current_user.id

    # Initialize form
    form = SchoolForm(request.form)
    review_type = request.args.get('type')
    school_id_str = request.args.get('school_id')

    # Process valid POST
    if request.method == 'POST' and form.validate():
        school_id = int(form.school_id.data)
        school_name = form.school_name.data
        update_a_school_by_id(school_id, school_name, form.address.data, form.city.data, form.province.data,
                              form.country.data, form.postal_code.data, form.school_status.data, db_user_id,
                              app_db_web_location)
        flash_msg = "School #" + str(school_id) + "-" + school_name + " has been reviewed and status is: " + form.school_status.data
        flash(flash_msg, 'success')
    else:
        if school_id_str is None or len(school_id_str) < 1:
            flash_msg = "No school selected, please double check your data."
            flash(flash_msg, 'error')
        else:
            school_id = int(school_id_str)
            if review_type.lower() == "review":
                # review a team
                school_result = search_schools_by_id(school_id, app_db_web_location)
                if school_result is not None:
                    for item in school_result:
                        #SCHOOL_ID, SCHOOL_NAME, PROVINCE, CITY, SCHOOL_ADDRESS, ZIP_CODE
                        form.school_id.data = item[0]
                        form.school_name.data = item[1]
                        form.province.data = item[2]
                        form.city.data = item[3]
                        form.address.data = item[4]
                        form.postal_code.data = item[5]
                        form.country.data = item[6]
                        form.school_status.data = item[7]
                        break
                return render_template('main/admin_review_school.html', form=form)
            else:
                flash_msg = "No record updated, please double check your data."
                flash(flash_msg, 'error')
    return redirect(url_for('main.admin_page'))


# The Admin - juror approval page is accessible to users with the 'admin' role
@main_blueprint.route('/admin_juror_approval')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_juror_approval():
    event_id = current_app.config['CURRENT_EVENT']
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    db_user_id = current_user.id

    juror_approval_type = request.args.get('type')
    juror_id_str = request.args.get('juror_id')
    juror_name = request.args.get('juror_name')

    if juror_id_str is None or len(juror_id_str) < 1:
        flash_msg = "No juror selected, please double check your data."
        flash(flash_msg, 'error')
    else:
        juror_id = int(juror_id_str)
        if juror_approval_type.lower() == "approve":
            # approve a juror
            update_a_ppant_status(event_id, juror_id, "Approved", db_user_id, app_db_web_location)
            flash_msg = "Juror #" + str(juror_id) + "-" + juror_name + " has been approved."
            flash(flash_msg, 'success')
        elif juror_approval_type.lower() == "reject":
            # reject a juror
            update_a_ppant_status(event_id, juror_id, "Rejected", db_user_id, app_db_web_location)
            flash_msg = "Juror #" + str(juror_id) + "-" + juror_name + " has been rejected."
            flash(flash_msg, 'error')
        elif juror_approval_type.lower() == "assign_chair":
            # assign juror as chair
            set_juror_chair(event_id, juror_id, "Yes", db_user_id, app_db_web_location)
            flash_msg = "Juror #" + str(juror_id) + "-" + juror_name + " has been assigned as Chair."
            flash(flash_msg, 'success')
        elif juror_approval_type.lower() == "not_assign_chair":
            # assign juror back to normal
            set_juror_chair(event_id, juror_id, "No", db_user_id, app_db_web_location)
            flash_msg = "Juror #" + str(juror_id) + "-" + juror_name + " has been re-assigned as normal juror, NOT chair."
            flash(flash_msg, 'success')
        else:
            flash_msg = "No record updated, please double check your data."
            flash(flash_msg, 'error')
    return redirect(url_for('main.admin_page'))


# The Admin - volunteer approval page is accessible to users with the 'admin' role
@main_blueprint.route('/admin_volunteer_approval')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_volunteer_approval():
    event_id = current_app.config['CURRENT_EVENT']
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    db_user_id = current_user.id

    volunteer_approval_type = request.args.get('type')
    volunteer_id_str = request.args.get('volunteer_id')
    volunteer_name = request.args.get('volunteer_name')

    if volunteer_id_str is None or len(volunteer_id_str) < 1:
        flash_msg = "No volunteer selected, please double check your data."
        flash(flash_msg, 'error')
    else:
        volunteer_id = int(volunteer_id_str)
        if volunteer_approval_type.lower() == "approve":
            # approve a team
            update_a_ppant_status(event_id, volunteer_id, "Approved", db_user_id, app_db_web_location)
            flash_msg = "volunteer #" + str(volunteer_id) + "-" + volunteer_name + " has been approved."
            flash(flash_msg, 'success')
        elif volunteer_approval_type.lower() == "reject":
                # approve a team
                update_a_ppant_status(event_id, volunteer_id, "Rejected", db_user_id, app_db_web_location)
                flash_msg = "Volunteer #" + str(volunteer_id) + "-" + volunteer_name + " has been rejected."
                flash(flash_msg, 'error')
        else:
            flash_msg = "No record updated, please double check your data."
            flash(flash_msg, 'error')
    return redirect(url_for('main.admin_page'))


@main_blueprint.route('/admin_plan_view', methods=['GET', 'POST'])
@roles_required('super')  # Limits access to users with 'super' role
def admin_plan_view():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    event_id = current_app.config['CURRENT_EVENT']
    plan_id = request.args.get('plan_id')
    plan_status = request.args.get('plan_status')
    plan_sub_status = int(request.args.get('plan_sub_status'))
    activable = int(request.args.get('activable'))
    # Initialize form
    form = EventPlanForm(request.form)

    if request.method == 'POST':
        deactivate = request.form.get("deactivate")
        release = request.form.get("release")
        if deactivate == "Deactivate":
            # De-Activate Plan (change status to proposed)
            update_plan_status(plan_id, "Proposed", current_user.id, app_db_web_location)
            flash_msg = "Proposed plan has been deactivated."
        elif release == "Release":
                # Release Plan (change sub status to Released), plan is forzen, no more change allowed
                # get all volunteers
                release_sm_plan(plan_id, 1, current_user.id, app_db_web_location)
                flash_msg = "Proposed plan has been released."
        else:
            update_plan_status(plan_id, "Active", current_user.id, app_db_web_location)
            flash_msg = "Proposed plan has been activated successfully. Participants can't be updated anymore."
        flash(flash_msg, 'success')
        return redirect(url_for('main.admin_mgmt'))
    else:
        # get mteam for the selected plan_id
        mteam_list = search_mteam_by_code(plan_id, app_db_web_location)
        # get mroom for the selected plan_id
        mroom_list = search_mroom(plan_id, app_db_web_location)
        # get mjuror for the selected plan_id for juror chairs
        mjuror_list = get_mjuror_by_room(plan_id, "Base", app_db_web_location)
        # get moved juror for the selected plan_id
        moved_juror_list = get_mpair_jurors_by_round_room(plan_id, "Moved", app_db_web_location)
        # get mvolunteer for the selected plan_id
        mvolunteer_list = get_mvolunteer_by_room(plan_id, "Base", app_db_web_location)
        # (mjuror_code, mjuror_name, mjuror_info, has_cois, juror_cois_list)
        master_mjurors = get_mjurors(plan_id, app_db_web_location)
        # (mroom_code, mroom_label, room_volunteers)
        master_room_mvolunteers = get_mvolunteers(plan_id, app_db_web_location)
        # get mpair team
        mpair_team_list = get_mpair_team_by_round_team(plan_id, app_db_web_location)
        # get round, room and pair from MPAIR table
        mpair_list = get_mpair_by_round_room(plan_id, app_db_web_location)
        mround_list = []
        for round in mpair_list:
            tmp_pair_list = []
            for room in mroom_list:
                # find pair at current round and current room
                found_pair_at_round_room = False
                for pair in round[1]:
                    if pair[0] == room[1]:
                        tmp_pair_list.append(pair)
                        found_pair_at_round_room = True
                        break
                if not found_pair_at_round_room:
                    tmp_pair_list.append(None)
            tmp_tuple3 = (round[0], tmp_pair_list)
            mround_list.append(tmp_tuple3)

        return render_template('main/admin_plan_view.html', form=form, plan_status=plan_status, plan_id=plan_id, mround_list=mround_list,
                               mroom_list=mroom_list, mjuror_list=mjuror_list, mteam_list=mteam_list, mpair_team_list=mpair_team_list,
                               activable=activable, master_room_mvolunteers=master_room_mvolunteers, moved_juror_list=moved_juror_list,
                               plan_sub_status=plan_sub_status, master_mjurors=master_mjurors)


@main_blueprint.route('/admin_plan_download', methods=['GET', 'POST'])
@roles_required('admin', 'super')  # Limits access to users with the 'admin' role and 'super' role
def admin_plan_download():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    event_id = current_app.config['CURRENT_EVENT']
    plan_id = request.args.get('plan_id')
    plan_status = request.args.get('plan_status')
    # Initialize form
    form = EventPlanForm(request.form)

    # get mteam for the selected plan_id
    mteam_list = search_mteam_by_code(plan_id, app_db_web_location)
    # get mroom for the selected plan_id
    mroom_list = search_mroom(plan_id, app_db_web_location)
    # get mjuror for the selected plan_id for juror chairs
    mjuror_list = get_mjuror_by_room(plan_id, "Base", app_db_web_location)
    # get moved juror for the selected plan_id
    moved_juror_list = get_mpair_jurors_by_round_room(plan_id, "Moved", app_db_web_location)
    # get mvolunteer for the selected plan_id
    mvolunteer_list = get_mvolunteer_by_room(plan_id, "Base", app_db_web_location)
    # (mjuror_code, mjuror_name, mjuror_info, has_cois, juror_cois_list)
    master_mjurors = get_mjurors(plan_id, app_db_web_location)
    # (mroom_code, mroom_label, room_volunteers)
    master_room_mvolunteers = get_mvolunteers(plan_id, app_db_web_location)
    # get mpair team
    mpair_team_list = get_mpair_team_by_round_team(plan_id, app_db_web_location)
    # get round, room and pair from MPAIR table
    mpair_list = get_mpair_by_round_room(plan_id, app_db_web_location)
    mround_list = []
    for round in mpair_list:
        tmp_pair_list = []
        for room in mroom_list:
            # find pair at current round and current room
            found_pair_at_round_room = False
            for pair in round[1]:
                if pair[0] == room[1]:
                    tmp_pair_list.append(pair)
                    found_pair_at_round_room = True
                    break
            if not found_pair_at_round_room:
                tmp_pair_list.append(None)
        tmp_tuple3 = (round[0], tmp_pair_list)
        mround_list.append(tmp_tuple3)

    response_html_string= render_template('main/admin_plan_view_pdf.html', form=form, plan_status=plan_status, plan_id=plan_id,
                           mround_list=mround_list, mroom_list=mroom_list, mjuror_list=mjuror_list, mteam_list=mteam_list,
                           mpair_team_list=mpair_team_list, master_mjurors=master_mjurors,
                           master_room_mvolunteers=master_room_mvolunteers, moved_juror_list=moved_juror_list)
    pdf_filename = plan_status + "_Plan_" + str(plan_id)
    return render_pdf(HTML(string=response_html_string), download_filename=pdf_filename, automatic_download=False)


# delete event plan for either SM or FM
@main_blueprint.route('/admin_plan_delete')
@roles_required('admin', 'super')  # Limits access to users with the 'admin' role and 'super' role
def admin_plan_delete():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    event_id = current_app.config['CURRENT_EVENT']
    plan_id = request.args.get('plan_id')
    plan_status = request.args.get('plan_status')
    if plan_status == 'Proposed':
        # delete the selected plan and the related six "M" tables
        admin_delete_plan(event_id, plan_id, plan_status, app_db_web_location)
        flash_msg = plan_status + "Plan # " + str(plan_id) + "has been deleted!"
        flash(flash_msg, 'success')
        return redirect(url_for('main.admin_mgmt'))
    else:
        flash_msg = plan_status + "Plan # " + str(plan_id) + "can NOT be deleted!"
        flash(flash_msg, 'error')
        return redirect(url_for('main.admin_mgmt'))


@main_blueprint.route('/admin_save_proposal', methods=['GET', 'POST'])
@roles_required('admin', 'super')  # Limits access to users with the 'admin' role and 'super' role
def admin_save_proposal():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    event_id = current_app.config['CURRENT_EVENT']

    round_room_team_plan = session['round_room_team_plan']
    juror_plan = session['juror_plan']
    volunteer_plan = session['volunteer_plan']
    moved_jurors_plan = session['moved_jurors_plan']
    db_save_proposal(event_id, round_room_team_plan, juror_plan, volunteer_plan, moved_jurors_plan, current_user.id, app_db_web_location)
    session.pop('round_room_team_plan')
    session.pop('juror_plan')
    session.pop('volunteer_plan')
    session.pop('moved_jurors_plan')
    flash_msg = "Proposed plan has been saved successfully."
    flash(flash_msg, 'success')
    return redirect(url_for('main.admin_mgmt'))


@main_blueprint.route('/admin_mgmt', methods=['GET', 'POST'])
@roles_required('admin', 'super')  # Limits access to users with the 'admin' role and 'super' role
def admin_mgmt():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']

    db_created_by_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = EventPlanForm(request.form)

    # get plan from database
    plan_status = "Active"
    active_sm_plan_list = search_event_plan(event_id, plan_status, 1, app_db_web_location)
    active_fm_plan_list = search_event_plan(event_id, plan_status, 2, app_db_web_location)
    if active_sm_plan_list is not None and len(active_sm_plan_list) > 0:
        # plan has already been activated, no changes to the plan are allowed
        pass
    else:
        # plan has not been finalized, can view, re-plan or manual change the plan
        plan_status = "Proposed"

    plan_list = search_event_plan(event_id, None, 0, app_db_web_location)

    return render_template('main/admin_mgmt.html', plan_list=plan_list, plan_count=len(plan_list), active_sm_plan_count=len(active_sm_plan_list),
                           active_fm_plan_count=len(active_fm_plan_list), plan_status=plan_status)


@main_blueprint.route('/admin_planning', methods=['GET', 'POST'])
@roles_required('admin', 'super')  # Limits access to users with the 'admin' role and 'super' role
def admin_planning():
    # Retrieve database settings from app.config
    global team_plan
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']

    db_created_by_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = EventPlanForm(request.form)
    current_event_teams = search_event_teams_inorder(event_id, app_db_web_location, 'Approved')
    form.teams_total_number.data = len(current_event_teams)

    # Process valid POST
    if request.method == 'POST': #and form.validate():
        # get parameters
        rounds_total_number = int(request.form['rounds_total_number'])
        teams_total_number = int(request.form['teams_total_number'])
        teams_mini_number = int(request.form['teams_mini_number'])
        rooms_for_each_round = int(request.form['rooms_for_each_round'])
        max_re_do_times = int(request.form['max_re_do_times'])
        max_repeated_rooms = int(request.form['max_repeated_rooms'])
        open_last_round = int(request.form['last_round_repeatable'])
        accept_proposal_str = request.form.get('accept_proposal')
        accept_proposal = 0
        if accept_proposal_str is not None:
            accept_proposal = int(accept_proposal_str)
        if accept_proposal == 1:
            # get juror alternative room assignment from flask form
            juror_alternatives = request.form
            session['juror_alternatives'] = juror_alternatives
            return redirect(url_for('main.admin_save_proposal'))
        else:
            if teams_mini_number < 6:
                teams_mini_number = 6
            if teams_total_number < teams_mini_number:
                teams_total_number = teams_mini_number
            elif teams_total_number % 2 != 0:
                teams_total_number += 1
            re_do_from_beginning = False
            re_do_from_beginning_tried_times = 0
            room_plan = []
            juror_plan = []
            round_plan = []
            volunteer_plan = []
            moved_jurors_plan = []
            not_assigned_volunteers = None
            team_pair_count_per_round = int((teams_total_number+1)/2)
            current_event_rooms_usage1 = search_event_rooms(event_id, 1, 'Active', app_db_web_location)
            if len(current_event_rooms_usage1) < team_pair_count_per_round or len(current_event_rooms_usage1) < rooms_for_each_round:
                flash_msg = "No enough PM rooms! Only total " + str(len(current_event_rooms_usage1)) + \
                            " ACTIVE PM rooms in the database. Please contact admin to release backup rooms."
                flash(flash_msg, 'error')
                return redirect(url_for('main.admin_mgmt'))
            else:
                while re_do_from_beginning_tried_times < max_re_do_times and (re_do_from_beginning_tried_times == 0 or re_do_from_beginning):
                    # plan team
                    print("***2-1***team plan - start here")
                    team_plan= team_matching_2(teams_total_number, rounds_total_number)
                    if team_plan is None:
                        flash_msg = "Please try again." + str(teams_total_number)
                        flash(flash_msg, 'error')
                        return render_template('main/admin_planning.html', form=form, round_count = 0)
                    else:
                        current_teams_number_assignment = assign_team_code_inorder(current_event_teams, teams_total_number)
                        i = 0
                        for team in current_teams_number_assignment:
                            team_plan[i]['team_id'] = team[1][0] # team_id
                            team_plan[i]['team_name'] = team[1][1] # team_name
                            team_plan[i]['school_id'] = team[1][2] # school_id
                            team_plan[i]['school_name'] = team[1][3] # school_name
                            i += 1
                        print("***2-end***team plan - end here")
                        print("***New 3-1***room and chair plan - start here")
                        #plan chair
                        chairs_room_assignment = list()
                        chair_list = get_event_juror_n_cois_by_chair(event_id,"Yes", app_db_web_location)
                        if chair_list is None or len(chair_list) != rooms_for_each_round:
                            flash_msg = "Juror chairs's total number is not matching the total number of rooms."
                            flash(flash_msg, 'error')
                            return redirect(url_for('main.admin_mgmt'))
                        else:
                            # assign chair to room firstly
                            chairs_room_assignment = assign_chair_room(chair_list, rooms_for_each_round)
                            juror_plan = chairs_room_assignment[0]
                        print("***New 3-end***room and chair plan - end here")
                        print("***New 4-1***round, room and team plan - start here")
                        round_room_plan = assign_room_to_team_wt_chair(rounds_total_number, team_plan, teams_total_number ,
                                                                       rooms_for_each_round, chairs_room_assignment, max_repeated_rooms, open_last_round)
                        round_plan = round_room_plan[0]
                        room_plan = round_room_plan[1]
                        planing_so_far_status = round_room_plan[2]
                        print("***New 4-end***round, room and team plan - end here")
                        re_do_from_beginning = False
                        for round in round_plan:
                            if len(round['round_team_matches_room_codes']) != team_pair_count_per_round:
                                re_do_from_beginning = True
                                break
                        re_do_from_beginning_tried_times += 1
                        print("!!!!!!!! total re-do from beginning times: ", re_do_from_beginning_tried_times)
                # clean the data
                if not re_do_from_beginning:
                    print("***5. Clean up------")
                    round_room_team_plan = tournament_plan_cleanup(round_plan, room_plan, team_plan, current_event_rooms_usage1)
                    round_plan = round_room_team_plan[0]
                    room_plan = round_room_team_plan[1]
                    team_plan = round_room_team_plan[2]
                    print("***6. assign other jurors to each round each room------")
                    # assign other jurors to each round each room is_char=No
                    moved_juror_list = get_event_juror_n_cois_by_chair(event_id,"No", app_db_web_location)
                    moved_jurors_plan = assign_moved_jurors(moved_juror_list, round_plan, rooms_for_each_round)
                    # assign volunteer to do the data entry for each room
                    room_count = len(room_plan)
                    print("***7. assign other volunteers to each room------")
                    data_entry_volunteer_results = search_events_ppant_n_cois_for_data_entry(event_id, app_db_web_location)
                    if data_entry_volunteer_results is not None and len(data_entry_volunteer_results) >= room_count:
                        # convert search results to list
                        data_entry_volunteer_list = zip([x[0] for x in data_entry_volunteer_results], \
                                                [x[1] for x in data_entry_volunteer_results], \
                                                [x[2] for x in data_entry_volunteer_results], \
                                                [x[3] for x in data_entry_volunteer_results], \
                                                [x[4] for x in data_entry_volunteer_results], \
                                                [x[5] for x in data_entry_volunteer_results], \
                                                [x[6] for x in data_entry_volunteer_results], \
                                                [x[7] for x in data_entry_volunteer_results], \
                                                [x[8] for x in data_entry_volunteer_results], \
                                                [x[9] for x in data_entry_volunteer_results], \
                                                [x[10] for x in data_entry_volunteer_results], \
                                                [x[11] for x in data_entry_volunteer_results], \
                                                [x[12] for x in data_entry_volunteer_results])
                        # select all the approved volunteer that is not subtype 99
                        volunteer_list = get_event_ppant_n_cois_for_volunteer(event_id, app_db_web_location)
                        # do the volunteer plan
                        volunteer_assignment_results = assign_volunteers(data_entry_volunteer_list, volunteer_list, room_plan)
                        volunteer_plan = volunteer_assignment_results[0]
                        not_assigned_volunteers = volunteer_assignment_results[1]
                        # mapping volunteer to room_plan
                        for volunteer in volunteer_plan:
                            vol_room_code = volunteer['mroom_code']
                            room_plan[vol_room_code - 1]['volunteers'].append(volunteer['mvolunteer_code'])
                    else:
                        flash_msg = "Qualified volunteers for data entry are not enough."
                        flash(flash_msg, 'error')
                        return redirect(url_for('main.admin_mgmt'))
                    revise_juror_room = True
                    session['round_room_team_plan'] = round_room_team_plan
                    session['juror_plan'] = juror_plan
                    session['volunteer_plan'] = volunteer_plan
                    session['moved_jurors_plan'] = moved_jurors_plan
                else:
                    revise_juror_room = False
                    session['round_room_team_plan'] = None
                    session['juror_plan'] = None
                    session['volunteer_plan'] = None
                    session['moved_jurors_plan'] = None
            return render_template('main/admin_planning.html', form=form, team_plan=team_plan, round_count=rounds_total_number,
                               revise_juror_room=revise_juror_room, room_plan=room_plan, juror_plan=juror_plan, round_plan=round_plan,
                                   volunteer_plan=volunteer_plan, moved_jurors_plan=moved_jurors_plan, not_assigned_volunteers=not_assigned_volunteers)
    else:
        # Process GET or invalid POST
        return render_template('main/admin_planning.html', form=form, round_count = 0)


# this is the start point of the selective match
# save all the master tables in session
# get pair information for room and round
@main_blueprint.route('/sm_mgmt', methods=['GET', 'POST'])
@roles_required('data')  # Limits access to users with the 'data' role
def sm_mgmt():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    current_user_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # get active plan_id for current event selective match-1
    plan_id = 0
    plan_sub_status = 0
    plan_status = "Active"
    plan_type = 1 #"SM"
    #EVENT_ID, EVENT_PLAN_ID, EVENT_PLAN_STATUS, EVENT_PLAN_TYPE, EVENT_PLAN_SUB_STATUS
    active_sm_plan_list = search_event_plan(event_id, plan_status, plan_type, app_db_web_location)
    for sm_plan in active_sm_plan_list:
        plan_id = sm_plan[1]
        plan_sub_status = sm_plan[4]
        break
    # redirect to member page if staging is not ready
    if plan_sub_status > 0:
        if plan_sub_status == 1 and not current_user.has_roles('super'):
            flash_msg = "Staging will be open on Tournament Day! Please contact Information Team if you have any questions."
            flash(flash_msg, 'error')
            return redirect(url_for('main.member_page'))
        else:
            pass
    else:
        flash_msg = "Staging is not ready yet! Please contact Information Team if you have any questions."
        flash(flash_msg, 'error')
        return redirect(url_for('main.member_page'))

    # Initialize form
    form = EventStageForm(request.form)

    # save master tables to session
    master_mteams = None
    master_mrooms = None
    master_mjurors = None
    master_room_mvolunteers = None
    try:
        # get master table from session
        master_mteams = session['master_mteams']
        master_mrooms = session['master_mrooms']
        master_mjurors = session['master_mjurors']
        master_room_mvolunteers = session['master_room_mvolunteers']
    except:
        # first time, save master tables to session
        master_mteams = get_mteams(plan_id, app_db_web_location) #(mteam_code, mteam_name, team_info, team_member_list)
        master_mrooms = get_mrooms(plan_id, app_db_web_location) #(mroom_code, mroom_label, mroom_info)
        master_mjurors = get_mjurors(plan_id, app_db_web_location) #(mjuror_code, mjuror_name, mjuror_info, has_cois, juror_cois_list)
        master_room_mvolunteers = get_mvolunteers(plan_id, app_db_web_location) #(mroom_code, mroom_label, room_volunteers)
        session['master_mteams'] = master_mteams
        session['master_mrooms'] = master_mrooms
        session['master_mjurors'] = master_mjurors
        session['master_room_mvolunteers'] = master_room_mvolunteers

    current_room_code = 0
    if request.method == 'POST':
        # Process valid POST
        current_room_code = int(request.form.get("current_room_code"))
    else:
        # Process valid GET'
        if current_user.has_roles('super'):
            # let super user select room code
            pass
        else:
            # search the room code that assigned to the data entrier
            #PLAN_ID, PPANT_USER_ID, MROOM_ID, MROOM_CODE, MROOM_LABEL, DATA_ENTRY
            assigned_rooms = search_mroom_assigned_to_data_entry(plan_id, current_user_id, app_db_web_location)
            for room in assigned_rooms:
                current_room_code = room[3]
                break
    sm_current_room_pairs = None
    if current_room_code > 0:
        # get up to date mpair fight status
        sm_room_pairs = get_mpairs_by_room_round(plan_id, app_db_web_location)
        sm_current_room_pairs = sm_room_pairs[current_room_code-1] #(current_room_code, tmp_mroom_label, tmp_round_list)

    return render_template('main/sm_mgmt.html', form=form, current_room_code=current_room_code, master_mrooms=master_mrooms,
                           sm_current_room_pairs=sm_current_room_pairs, master_mteams=master_mteams, plan_id=plan_id,
                           is_super=current_user.has_roles('super'))


@main_blueprint.route('/sm_draw', methods=['GET', 'POST'])
@roles_required('data')  # Limits access to users with the 'data' role
def sm_draw():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    current_user_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = EventStageForm(request.form)

    # Initialize parameters from request and session
    current_room_code = 0
    current_round_code = 0
    current_plan_id = 0
    sm_current_room_round_pairs = None
    master_mteams = None
    master_mrooms = None
    master_mjurors = None
    master_room_mvolunteers = None
    current_pair_assigned_jurors = None
    current_pair_assigned_juror_codes = None
    team1 = 0
    team2 = 0
    try:
        # get master table from session
        master_mteams = session['master_mteams']
        master_mrooms = session['master_mrooms']
        master_mjurors = session['master_mjurors']
        master_room_mvolunteers = session['master_room_mvolunteers']
    except:
        flash_msg = "Invalid access to get session!"
        flash(flash_msg, 'error')
        return redirect(url_for('main.sm_mgmt'))

    if request.method == 'POST':
        # Process valid POST
        try:
            current_room_code = int(request.form.get('current_room_code'))
            current_round_code = int(request.form.get('current_round_code'))
            current_plan_id = int(request.form.get('current_plan_id'))
            team1 = int(request.form.get('team1'))
            team2 = int(request.form.get('team2'))
            jury = request.form.getlist("jury")
            # get up to date mpair fight status
            sm_room_pairs = get_mpairs_by_room_round(current_plan_id, app_db_web_location)
            sm_current_room_round_pairs = sm_room_pairs[current_room_code - 1][2][
                current_round_code - 1]  # (current_room_code, tmp_mroom_label, tmp_round_list)
        except:
            flash_msg = "Invalid access in POST!"
            flash(flash_msg, 'error')
            return redirect(url_for('main.sm_mgmt'))

        if sm_current_room_round_pairs[2] < 2:
            # initilize stage agenda
            if team1>0 and team2>0 and team1 != team2 and jury is not None and len(jury) >2:
                # initilize stage agenda for selective match
                if sm_current_room_round_pairs[2] == 0:
                    current_jury = list()
                    for juror in jury:
                        tmp_juror_code = juror.split("--", 2)[0]
                        tmp_mpair_juror_id = juror.split("--", 2)[1]
                        tmp_mjuror_id = juror.split("--", 2)[2]
                        tmp_turple = (int(tmp_juror_code),int(tmp_mpair_juror_id), int(tmp_mjuror_id))
                        current_jury.append(tmp_turple )
                    #save_stage_members_jurors(current_plan_id, current_jury, current_pair_id, current_stage_code, reporter, opponent, current_user_id, app_db_web_location)
                    initialize_sm_stage_agenda(current_plan_id, sm_current_room_round_pairs, team1, team2, current_jury, current_user_id, app_db_web_location)
                    # get up to date mpair fight status
                    sm_room_pairs = get_mpairs_by_room_round(current_plan_id, app_db_web_location)
                    sm_current_room_round_pairs = sm_room_pairs[current_room_code - 1][2][
                        current_round_code - 1]  # (current_room_code, tmp_mroom_label, tmp_round_list)
            else:
                flash_msg = "Invalid data entry for the draw and or jury!"
                flash(flash_msg, 'error')
                return redirect(url_for('main.sm_mgmt'))
        else:
            flash_msg = "Another volunteer is working on the same pair, please contact the Information Team!"
            flash(flash_msg, 'error')
            return redirect(url_for('main.sm_mgmt'))
    else:
        # Process valid GET
        try:
            current_room_code = int(request.args.get('room'))
            current_round_code = int(request.args.get('round'))
            current_plan_id = int(request.args.get('plan'))
            # get up to date mpair fight status
            sm_room_pairs = get_mpairs_by_room_round(current_plan_id, app_db_web_location)
            sm_current_room_round_pairs = sm_room_pairs[current_room_code - 1][2][
                current_round_code - 1]  # (current_room_code, tmp_mroom_label, tmp_round_list)
            # get assigned juror for current pair
            tmp_juror_list = get_mpair_jurors_by_round_room(current_plan_id, None, app_db_web_location)
            current_pair_assigned_jurors = tmp_juror_list[current_round_code - 1][1][current_room_code - 1][1]
            current_pair_assigned_juror_codes = tmp_juror_list[current_round_code - 1][1][current_room_code - 1][2]
        except:
            flash_msg = "Invalid access in get!"
            flash(flash_msg, 'error')
            return redirect(url_for('main.sm_mgmt'))

    return render_template('main/sm_draw.html', form=form, current_room_code=current_room_code, master_mrooms=master_mrooms,
                           sm_current_room_round_pairs=sm_current_room_round_pairs, master_mteams=master_mteams,
                           plan_id=current_plan_id, team1=team1, team2=team2, master_mjurors=master_mjurors,
                           current_pair_assigned_jurors=current_pair_assigned_jurors, current_pair_assigned_juror_codes=current_pair_assigned_juror_codes)


# assign team member
@main_blueprint.route('/sm_select', methods=['GET', 'POST'])
@roles_required('data')  # Limits access to users with the 'data' role
def sm_select():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    current_user_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = EventStageForm(request.form)

    # Initialize parameters from request and session
    current_room_code = 0
    current_round_code = 0
    current_plan_id = 0
    sm_current_room_round_pairs = None
    master_mteams = None
    master_mrooms = None
    master_mjurors = None
    master_room_mvolunteers = None
    current_stage_code = 0
    stage_agenda = None
    current_pair_assigned_jurors = None
    current_pair_assigned_juror_codes = None
    current_pair_id = 0
    master_problems = None
    opponent_team_members_roles = None
    reporter_team_members_roles = None
    current_pair_team_problems = None
    problem_label_codes = None
    team_problems = []
    current_day_pair_problems = []
    #current_pair_problem_guide = None
    try:
        # get master prolbem tables from session
        master_problems = session['master_problems']
    except:
        # search master table of event problems from database
        master_problems= get_event_master_problems(event_id, app_db_web_location)

    try:
        # get master table from session
        master_mteams = session['master_mteams']
        master_mrooms = session['master_mrooms']
        master_mjurors = session['master_mjurors']
        master_room_mvolunteers = session['master_room_mvolunteers']
    except:
        flash_msg = "Invalid access to get session!"
        flash(flash_msg, 'error')
        return redirect(url_for('main.sm_mgmt'))

    try:
        current_room_code = int(request.args.get('room'))
        current_round_code = int(request.args.get('round'))
        current_plan_id = int(request.args.get('plan'))
        current_stage_code = int(request.args.get('stage'))
    except:
        flash_msg = "Invalid access in switching to timer!"
        flash(flash_msg, 'error')
        return redirect(url_for('main.sm_mgmt'))

    # get up to date mpair fight status
    sm_room_pairs = get_mpairs_by_room_round(current_plan_id, app_db_web_location)
    # (current_room_code, tmp_mroom_label, tmp_round_list)
    sm_current_room_round_pairs = sm_room_pairs[current_room_code - 1][2][current_round_code - 1]
    #current_pair_problem_guide = sm_current_room_round_pairs[4]
    current_pair_id = sm_current_room_round_pairs[3]

    # get up to date stage_agenda for specific mpair
    # stage_agenda: (stage_code, role_list)
    # role_list: (reporter, opponent)
    stage_agenda = get_sm_stage_agenda(current_plan_id, sm_current_room_round_pairs[3],
                                       app_db_web_location)

    session['sm_current_room_round_pairs'] = sm_current_room_round_pairs
    session['current_stage_agenda'] = stage_agenda[current_stage_code -1]
    session['current_codes'] = (current_room_code, current_round_code, current_stage_code, current_pair_id, current_plan_id)

    return redirect(url_for('main.sm_timing'))


#route('/user/id/<int:user_id>')
# conduct one selective match using timer
#@main_blueprint.route('/sm_timing/<int:current_room_code>/<int:current_round_code>/<int:current_stage_code>/<int:current_pair_id>/<int:current_plan_id>', methods=['GET', 'POST'])
@main_blueprint.route('/sm_timing', methods=['GET', 'POST'])
@roles_required('data')  # Limits access to users with the 'data' role
def sm_timing():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    current_user_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = EventStageForm(request.form)

    # Initialize parameters from request and session
    master_mteams = None
    master_mrooms = None
    master_mjurors = None
    master_room_mvolunteers = None

    current_stage_agenda = None
    sm_current_room_round_pairs = None

    current_room_code = 0
    current_round_code = 0
    current_stage_code = 0
    current_pair_id = 0
    current_plan_id = 0

    step_number = 0
    sm_steps = None
    current_stage_problems = None
    reporter_problems_rejected = None
    stage_agenda = None
    current_reporter_team_members_roles = None
    current_opponent_team_members_roles = None

    try:
        # get master table from session
        master_mteams = session['master_mteams']
        master_mrooms = session['master_mrooms']
        master_mjurors = session['master_mjurors']
        master_room_mvolunteers = session['master_room_mvolunteers']
        current_stage_agenda = session['current_stage_agenda']
        sm_current_room_round_pairs = session['sm_current_room_round_pairs']
        tmp_current_codes = session['current_codes']
        current_room_code = tmp_current_codes[0]
        current_round_code = tmp_current_codes[1]
        current_stage_code = tmp_current_codes[2]
        current_pair_id = tmp_current_codes[3]
        current_plan_id = tmp_current_codes[4]
    except:
        flash_msg = "Invalid access to get session!"
        flash(flash_msg, 'error')
        return redirect(url_for('main.sm_mgmt'))

    # initial current stage problems
    try:
        current_stage_problems = session['current_stage_problems']
    except:
        # get problem master table
        stage_problems = get_event_group_problems(event_id, app_db_web_location)
        if current_round_code < 4:
            # round 1,2,3 is group 1
            current_stage_problems = stage_problems[0]
        else:
            # round 1,2,3 is group 2
            current_stage_problems = stage_problems[1]
        session['current_stage_problems'] = current_stage_problems

    # get the performance order in one stage of a selective match
    sm_steps = get_sm_performance_order()
    if request.method == 'POST':
        # Process valid POST
        # for step 1 and step 2: select problem
        # save problems proposed, and accepted/rejected in session and save to database before scoring
        # get parameters from request.form
        reporter = None
        opponent = None
        try:
            reporter = request.form.get('reporter')
            opponent = request.form.get('opponent')
        except:
            pass
        step_str = request.form.get("step")
        step_number = 1
        if step_str is not None and len(step_str) > 0:
            step_number = int(step_str)
        if reporter is not None and opponent is not None:
            if reporter != "0" and opponent != "0":
                save_stage_members(current_plan_id, current_pair_id, current_stage_code, reporter, opponent,
                                   current_user_id, app_db_web_location)
                # get up to date mpair fight status
                sm_room_pairs = get_mpairs_by_room_round(current_plan_id, app_db_web_location)
                # (current_room_code, tmp_mroom_label, tmp_round_list)
                sm_current_room_round_pairs = sm_room_pairs[current_room_code - 1][2][current_round_code - 1]

                # get up to date stage_agenda for specific mpair
                # stage_agenda: (stage_code, role_list)
                # role_list: (reporter, opponent)
                stage_agenda = get_sm_stage_agenda(current_plan_id, sm_current_room_round_pairs[3],
                                                   app_db_web_location)

                session['sm_current_room_round_pairs'] = sm_current_room_round_pairs
                current_stage_agenda = stage_agenda[current_stage_code - 1]
                session['current_stage_agenda'] = stage_agenda[current_stage_code - 1]
                flash_msg = "Team members have been selected successfully, you can start step 3 now!"
                flash(flash_msg, 'success')
            else:
                flash_msg = "Team member is missing!"
                flash(flash_msg, 'error')
        else:
            selected_problem_str = request.form.get("problem")
            if selected_problem_str is not None:
                problem_values = selected_problem_str.split("--", 1)
                selected_problem_code = int(problem_values[0])
                selected_problem_status_code = int(problem_values[1])
                # problem status code: 1-proposed, 2-rejected, 3-accepted
                selected_problem_index = selected_problem_code - 1 - 5 * (current_stage_problems[0]-1)
                current_stage_problems[1][selected_problem_index]['problem_status'] = selected_problem_status_code
                session['current_stage_problems'] = current_stage_problems

                if selected_problem_status_code == 3:
                    # at step 2, reporter accept/reject proposed question
                    current_group_code = 1
                    if current_round_code > 3:
                        current_group_code = 2
                    save_stage_problems(current_plan_id, current_stage_code, current_stage_agenda, current_stage_problems, current_group_code, current_user_id, app_db_web_location)
                elif selected_problem_status_code == 2:
                    # problem is rejected
                    step_number = 1
                    # get rejected problems by the reporter
                    problem_reject_accept_code = 2
                    current_reporter_team_code = current_stage_agenda[2][0][1]
                    reporter_problems_rejected = get_reporter_team_problems(current_plan_id, current_reporter_team_code,
                                                                            problem_reject_accept_code, app_db_web_location)
    else:
        # Process valid GET
        # get parameters from request
        step_str = request.args.get("step")
        step_number = 1
        if step_str is not None and len(step_str) > 0:
            step_number = int(step_str)

        # ensure there is one problem is accepted
        problem_accepted = False
        if step_number < 3:
            # get rejected problems by the reporter
            problem_reject_accept_code = 2
            current_reporter_team_code = current_stage_agenda[2][0][1]
            reporter_problems_rejected = get_reporter_team_problems(current_plan_id, current_reporter_team_code,
                                                                    problem_reject_accept_code, app_db_web_location)

            for problem in current_stage_problems[1]:
                if problem['problem_status'] == 3:
                    problem_accepted = True
                    break
            if problem_accepted:
                step_number = 3
                flash_msg = "Problem has already been accepted, can NOT re-do!"
                flash(flash_msg, 'error')
            else:
                pass
        elif step_number == 3:
            for problem in current_stage_problems[1]:
                if problem['problem_status'] == 3:
                    problem_accepted = True
                    break
            if problem_accepted:
                pass
            else:
                step_number = 1
                # get rejected problems by the reporter
                problem_reject_accept_code = 2
                current_reporter_team_code = current_stage_agenda[2][0][1]
                reporter_problems_rejected = get_reporter_team_problems(current_plan_id, current_reporter_team_code,
                                                                        problem_reject_accept_code, app_db_web_location)

                flash_msg = "Not any problem is accepted, please start from step 1!"
                flash(flash_msg, 'error')
        elif step_number == 4:
            if current_stage_agenda[2][0][2][6] is None or current_stage_agenda[2][1][2][6] is None:
                step_number = 3
                flash_msg = "Team members are missing!"
                flash(flash_msg, 'error')
        elif step_number > len(sm_steps):
            # completed all the steps, update mpair stage status to 12 or 22, but not enter the score yet
            mpair_stage_status_code = 0
            if current_stage_code == 1:
                mpair_stage_status_code = 12
            elif current_stage_code == 2:
                mpair_stage_status_code = 22
            update_mpair_stage_status(current_plan_id, current_pair_id, mpair_stage_status_code, current_user_id, app_db_web_location)
            return redirect(url_for('main.sm_scoring'))

    # get up to date stage_agenda for specific mpair
    stage_agenda = get_sm_stage_agenda(current_plan_id, current_pair_id, app_db_web_location)
    # get up to date team members' roles and problems
    reporter_team_members_roles = get_team_member_roles(current_plan_id, stage_agenda[current_stage_code-1][2][0][1], app_db_web_location)
    if reporter_team_members_roles is None or len(reporter_team_members_roles) < 1:
        reporter_team_members_roles = [0]
    opponent_team_members_roles = get_team_member_roles(current_plan_id, stage_agenda[current_stage_code-1][2][1][1], app_db_web_location)
    if opponent_team_members_roles is None or len(opponent_team_members_roles) < 1:
        opponent_team_members_roles = [0]

    team_problems = []
    current_day_pair_problems = []
    problem_label_codes = None
    if step_number < 2:
        current_pair_team_problems = get_reporter_problems(current_plan_id, current_stage_agenda[2][0][1], current_stage_agenda[2][1][1], 0, app_db_web_location)
        # re-arrange current_pair_team_problems
        if current_pair_team_problems is not None:
            for team in current_pair_team_problems:
                tmp_problem_code_list = []
                #print("*** team: ", team[0], team[1])
                for i in range(10):
                    tmp_problem_code = i + 1
                    #print("*** problem code: ", tmp_problem_code)
                    has_matched_problem = False
                    tmp_problme_list = []
                    for item in team[1]:
                        if item[0] == tmp_problem_code:
                            tmp_problme_list.append(item[1])
                            has_matched_problem = True
                    if has_matched_problem:
                        tmp_problem_code_list.append((tmp_problem_code, tmp_problme_list))
                    else:
                        tmp_problem_code_list.append((tmp_problem_code, None))
                team_problems.append((team[0], tmp_problem_code_list))

        if current_round_code < 4:
            problem_label_codes = ("A", "B", "C", "D", "E")
            current_day_pair_problems = team_problems[:5]
        else:
            problem_label_codes = ("F", "G", "H", "I", "J")
            current_day_pair_problems = team_problems[:5]

    return render_template('main/sm_timing.html', form=form, current_room_code=current_room_code, master_mrooms=master_mrooms,
                           sm_current_room_round_pairs=sm_current_room_round_pairs, master_mteams=master_mteams,
                           plan_id=current_plan_id, current_stage_code=current_stage_code, master_mjurors=master_mjurors,
                           current_stage_agenda=current_stage_agenda, current_stage_problems=current_stage_problems,
                           step_number=step_number, sm_steps=sm_steps, total_steps=len(sm_steps), team_problems=current_day_pair_problems,
                           reporter_problems_rejected=reporter_problems_rejected, problem_label_codes=problem_label_codes,
                           reporter_team_members_roles=reporter_team_members_roles[0], opponent_team_members_roles=opponent_team_members_roles[0])


@main_blueprint.route('/sm_scoring', methods=['GET', 'POST'])
@roles_required('data')  # Limits access to users with the 'data' role
def sm_scoring():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    current_user_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = EventStageForm(request.form)

    # Initialize parameters from request and session
    master_mteams = None
    master_mrooms = None
    master_mjurors = None
    master_room_mvolunteers = None

    current_stage_agenda = None
    sm_current_room_round_pairs = None

    current_room_code = 0
    current_round_code = 0
    current_stage_code = 0
    current_pair_id = 0
    current_plan_id = 0

    current_stage_problems = None
    current_stage_jurors = None

    try:
        # get master table from session
        master_mteams = session['master_mteams']
        master_mrooms = session['master_mrooms']
        master_mjurors = session['master_mjurors']
        master_room_mvolunteers = session['master_room_mvolunteers']
        current_stage_agenda = session['current_stage_agenda']
        sm_current_room_round_pairs = session['sm_current_room_round_pairs']
        tmp_current_codes = session['current_codes']
        current_room_code = tmp_current_codes[0]
        current_round_code = tmp_current_codes[1]
        current_stage_code = tmp_current_codes[2]
        current_pair_id = tmp_current_codes[3]
        current_plan_id = tmp_current_codes[4]
        current_stage_problems = session['current_stage_problems']
    except:
        flash_msg = "Invalid access to get session!"
        flash(flash_msg, 'error')
        return redirect(url_for('main.sm_mgmt'))

    if request.method == 'POST':
        # Process valid POST
        # get parameters from form
        stage_scores = list()
        stage_score_keys = list()
        data_received = request.form
        for key in data_received:
            stage_score_keys.append(key)
        sorted_keys = sorted(stage_score_keys)
        for key in sorted_keys:
            if key.startswith("j_"):
                #print('form key '+key+" "+ data_received[key])
                stage_scores.append((key, data_received[key]))
        # insert data to DSTAGE_SCORE
        save_stage_scores(current_plan_id, current_pair_id, stage_scores, current_stage_agenda, current_stage_code,
                          current_room_code, current_user_id, app_db_web_location)

        # clear session for stage specific values
        session.pop('current_stage_problems')
        session.pop('current_stage_agenda')
        session.pop('sm_current_room_round_pairs')
        session.pop('current_codes')
        return redirect(url_for('main.sm_mgmt'))
    else:
        # Process valid GET
        # get up to date jurors on board
        current_stage_jurors = get_stage_jurors(current_plan_id, current_pair_id, current_stage_code, app_db_web_location)

    return render_template('main/sm_scoring.html', form=form, current_room_code=current_room_code, master_mrooms=master_mrooms,
                           sm_current_room_round_pairs=sm_current_room_round_pairs, master_mteams=master_mteams,
                           plan_id=current_plan_id, current_stage_code=current_stage_code, master_mjurors=master_mjurors,
                           current_stage_agenda=current_stage_agenda, current_stage_problems=current_stage_problems,
                           current_jury=current_stage_jurors)


# validate score and calculate the total
@main_blueprint.route('/sm_validate', methods=['GET', 'POST'])
@roles_required('super')  # Limits access to users with the 'super' role
def sm_validate():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    current_user_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = EventStageForm(request.form)
    sm_current_pair_scores = None

    # Initialize parameters from request and session
    current_room_code = 0
    current_round_code = 0
    current_plan_id = 0
    sm_current_room_round_pairs = None
    master_mteams = None
    master_mrooms = None
    master_mjurors = None
    master_room_mvolunteers = None
    current_stage_code = 0
    stage_agenda = None
    current_pair_assigned_jurors = None
    current_pair_assigned_juror_codes = None
    current_pair_id = 0
    master_problems = None
    opponent_team_members_roles = None
    reporter_team_members_roles = None
    current_team_codes = None
    current_team_codes_SP = None
    current_stage_problems = None
    current_dstage_score_id = 0
    current_mpair_id = 0
    try:
        # get master prolbem tables from session
        master_problems = session['master_problems']
    except:
        # search master table of event problems from database
        master_problems= get_event_master_problems(event_id, app_db_web_location)

    try:
        # get master table from session
        master_mteams = session['master_mteams']
        master_mrooms = session['master_mrooms']
        master_mjurors = session['master_mjurors']
        master_room_mvolunteers = session['master_room_mvolunteers']

    except:
        flash_msg = "Invalid access to get session!"
        flash(flash_msg, 'error')
        return redirect(url_for('main.sm_mgmt'))

    if request.method == 'POST':
        # Process valid POST
        # check if the scoresheet is confirmed
        scoresheet_validate = request.form.get('validate')
        if scoresheet_validate is not None:
            if scoresheet_validate == "correct":
                # get calculated values
                #2_opp_dstage_team_P 2_rep_dstage_team_P 2_opp_dstage_team_AP 2_opp_dstage_team_id 2_rep_dstage_team_AP 2_rep_dstage_team_id
                #1_opp_dstage_team_P 1_rep_dstage_team_P 1_opp_dstage_team_AP 1_opp_dstage_team_id 1_rep_dstage_team_AP 1_rep_dstage_team_id
                #ds_fw_mteam_code ds_fw_mteam_code_SP ds_fl_mteam_code ds_fl_mteam_code_SP
                try:
                    current_room_code = int(request.form.get('current_room_code'))
                    current_round_code = int(request.form.get('current_round_code'))
                    current_plan_id = int(request.form.get('current_plan_id'))
                    current_mpair_id = int(request.form.get('current_mpair_id'))

                    ds2_opp_dstage_team_P = float(request.form.get("2_opp_dstage_team_P"))
                    ds2_rep_dstage_team_P = float(request.form.get("2_rep_dstage_team_P"))
                    ds2_opp_dstage_team_AP = float(request.form.get("2_opp_dstage_team_AP"))
                    ds2_opp_dstage_team_id = int(request.form.get("2_opp_dstage_team_id"))
                    ds2_rep_dstage_team_AP = float(request.form.get("2_rep_dstage_team_AP"))
                    ds2_rep_dstage_team_id = int(request.form.get("2_rep_dstage_team_id"))

                    ds1_opp_dstage_team_P = float(request.form.get("1_opp_dstage_team_P"))
                    ds1_rep_dstage_team_P = float(request.form.get("1_rep_dstage_team_P"))
                    ds1_opp_dstage_team_AP = float(request.form.get("1_opp_dstage_team_AP"))
                    ds1_opp_dstage_team_id = int(request.form.get("1_opp_dstage_team_id"))
                    ds1_rep_dstage_team_AP = float(request.form.get("1_rep_dstage_team_AP"))
                    ds1_rep_dstage_team_id = int(request.form.get("1_rep_dstage_team_id"))

                    ds_f1_mteam_code = int(request.form.get("ds_f1_mteam_code"))
                    ds_f1_mteam_code_SP = float(request.form.get("ds_f1_mteam_code_SP"))
                    ds_f1_mteam_code_fw = int(request.form.get("ds_f1_mteam_code_fw"))
                    ds_f2_mteam_code = int(request.form.get("ds_f2_mteam_code"))
                    ds_f2_mteam_code_SP = float(request.form.get("ds_f2_mteam_code_SP"))
                    ds_f2_mteam_code_fw = int(request.form.get("ds_f2_mteam_code_fw"))

                    # update two mpair_teams of the current mpair_id: SP and FW=1 or 0
                    # winner is the ranking #1 including tie scenario
                    # use mteam_code and mpair_id to find mpair_team_id (PK)
                    mpair_team_records = [
                        (ds_f1_mteam_code, ds_f1_mteam_code_SP, ds_f1_mteam_code_fw),
                        (ds_f2_mteam_code, ds_f2_mteam_code_SP, ds_f2_mteam_code_fw)
                    ]
                    # update four dstage_teams of the current mpair_id: Average Point, Point (POINT_WITH_FACTOR)
                    # stage 1: rep and opp, stage 2: rep and opp
                    dstage_team_records = [
                        (ds1_rep_dstage_team_id, ds1_rep_dstage_team_AP, ds1_rep_dstage_team_P),
                        (ds1_opp_dstage_team_id, ds1_opp_dstage_team_AP, ds1_opp_dstage_team_P),
                        (ds2_rep_dstage_team_id, ds2_rep_dstage_team_AP, ds2_rep_dstage_team_P),
                        (ds2_opp_dstage_team_id, ds2_opp_dstage_team_AP, ds2_opp_dstage_team_P)
                    ]

                    validate_dstage_score(current_plan_id, current_mpair_id, mpair_team_records, dstage_team_records, current_user_id,
                                          app_db_web_location)

                    flash_msg = "Room " + str(current_room_code) + " Round " + str(current_round_code) + "Scoresheet has been confirmed successfully!"
                    flash(flash_msg, 'success')
                    return redirect(url_for('main.sm_mgmt'))
                except:
                    flash_msg = "Scoresheet was not confirmed properly, please double check!"
                    flash(flash_msg, 'error')
                    return redirect(url_for('main.sm_mgmt'))
            else:
                flash_msg = "Scoresheet was not confirmed, please double check!"
                flash(flash_msg, 'error')
                return redirect(url_for('main.sm_mgmt'))
        else:
            try:
                current_room_code = int(request.form.get('current_room_code'))
                current_round_code = int(request.form.get('current_round_code'))
                current_plan_id = int(request.form.get('current_plan_id'))
                current_mpair_id = int(request.form.get('current_mpair_id'))
                dstage_score_id = int(request.form.get('ds_sc_id'))
                ds_sc_1 = float(request.form.get('ds_sc_1'))
                ds_sc_2 = float(request.form.get('ds_sc_2'))
                ds_sc_3 = float(request.form.get('ds_sc_3'))
                ds_sc_4 = float(request.form.get('ds_sc_4'))
                ds_sc_5 = float(request.form.get('ds_sc_5'))
            except:
                flash_msg = "Invalid access in post!"
                flash(flash_msg, 'error')
                return redirect(url_for('main.sm_mgmt'))

            # update dstage_score by dstage_score_id
            if dstage_score_id > 0:
                dstage_scores = (round(ds_sc_1 + ds_sc_2 + ds_sc_3 + ds_sc_4 + ds_sc_5, 1), ds_sc_1, ds_sc_2, ds_sc_3, ds_sc_4, ds_sc_5)
                update_dstage_score_by_id(current_plan_id, dstage_score_id, dstage_scores, current_user_id, app_db_web_location)

            # get up to date mpair fight status
            sm_room_pairs = get_mpairs_by_room_round(current_plan_id, app_db_web_location)
            sm_current_room_round_pairs = sm_room_pairs[current_room_code - 1][2][
                current_round_code - 1]  # (current_room_code, tmp_mroom_label, tmp_round_list)
            current_team_codes = (sm_current_room_round_pairs[1][0][4], sm_current_room_round_pairs[1][1][4])

            # get up to date mpair stage problem info
            current_stage_problems = get_mpair_problems_simmple(current_plan_id, current_mpair_id, app_db_web_location)
            # get up to date mpair stage score info
            validation_scores = get_mpair_scores_4validate(current_plan_id, current_mpair_id, current_team_codes, app_db_web_location)
            current_team_codes_SP = validation_scores[1]
            sm_current_pair_scores = validation_scores[0]

    else:
        # Process valid GET
        try:
            current_room_code = int(request.args.get('room'))
            current_round_code = int(request.args.get('round'))
            current_plan_id = int(request.args.get('plan'))
            current_mpair_id = int(request.args.get('pair'))
        except:
            flash_msg = "Invalid access in get!"
            flash(flash_msg, 'error')
            return redirect(url_for('main.sm_mgmt'))

        try:
            current_dstage_score_id = int(request.args.get('dss'))
        except:
            current_dstage_score_id = 0

        # get up to date mpair fight status
        sm_room_pairs = get_mpairs_by_room_round(current_plan_id, app_db_web_location)
        sm_current_room_round_pairs = sm_room_pairs[current_room_code - 1][2][
            current_round_code - 1]  # (current_room_code, tmp_mroom_label, tmp_round_list)
        current_team_codes = (sm_current_room_round_pairs[1][0][4], sm_current_room_round_pairs[1][1][4])

        # get up to date mpair stage problem info
        current_stage_problems = get_mpair_problems_simmple(current_plan_id, current_mpair_id, app_db_web_location)
        # get up to date mpair stage score info
        validation_scores = get_mpair_scores_4validate(current_plan_id, current_mpair_id, current_team_codes, app_db_web_location)
        current_team_codes_SP = validation_scores[1]
        sm_current_pair_scores = validation_scores[0]

    # compare who is the winner
    ranked_team_codes_SP = check_ranking2(current_team_codes_SP)

    return render_template('main/sm_validate.html', form=form, current_room_code=current_room_code, master_mrooms=master_mrooms,
                           current_round_code=current_round_code, master_mteams=master_mteams, current_plan_id=current_plan_id,
                           master_mjurors=master_mjurors, sm_current_pair_scores=sm_current_pair_scores, current_mpair_id=current_mpair_id,
                           current_team_codes_SP=current_team_codes_SP, current_team_codes=current_team_codes, ranked_team_codes_SP=ranked_team_codes_SP,
                           current_stage_problems=current_stage_problems, current_dstage_score_id=current_dstage_score_id)


# view mpair score
@main_blueprint.route('/sm_score_view', methods=['GET', 'POST'])
@roles_required('data')  # Limits access to users with the 'data' role
def sm_score_view():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    current_user_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = EventStageForm(request.form)
    sm_current_pair_scores = None

    # Initialize parameters from request and session
    current_room_code = 0
    current_round_code = 0
    current_plan_id = 0
    sm_current_room_round_pairs = None
    master_mteams = None
    master_mrooms = None
    master_mjurors = None
    master_room_mvolunteers = None
    current_stage_code = 0
    stage_agenda = None
    current_pair_assigned_jurors = None
    current_pair_assigned_juror_codes = None
    current_pair_id = 0
    master_problems = None
    opponent_team_members_roles = None
    reporter_team_members_roles = None
    current_team_codes = None
    current_team_codes_SP = None
    current_stage_problems = None
    current_dstage_score_id = 0
    current_mpair_id = 0
    view_type = 0
    try:
        # get master prolbem tables from session
        master_problems = session['master_problems']
    except:
        # search master table of event problems from database
        master_problems= get_event_master_problems(event_id, app_db_web_location)

    if request.method == 'POST':
        # Process valid POST
        pass
    else:
        # Process valid GET
        try:
            current_room_code = int(request.args.get('room'))
            current_round_code = int(request.args.get('round'))
            current_plan_id = int(request.args.get('plan'))
            current_mpair_id = int(request.args.get('pair'))
            view_type = int(request.args.get('type'))
        except:
            flash_msg = "Invalid access in get!"
            flash(flash_msg, 'error')
            return redirect(url_for('main.sm_mgmt'))

        try:
            # get master table from session
            master_mteams = session['master_mteams']
            master_mrooms = session['master_mrooms']
            master_mjurors = session['master_mjurors']
            master_room_mvolunteers = session['master_room_mvolunteers']
        except:
            # first time, save master tables to session
            # (mteam_code, mteam_name, team_info, team_member_list)
            master_mteams = get_mteams(current_plan_id, app_db_web_location)
            # (mroom_code, mroom_label, mroom_info)
            master_mrooms = get_mrooms(current_plan_id, app_db_web_location)
            # (mjuror_code, mjuror_name, mjuror_info, has_cois, juror_cois_list)
            master_mjurors = get_mjurors(current_plan_id, app_db_web_location)
            # (mroom_code, mroom_label, room_volunteers)
            master_room_mvolunteers = get_mvolunteers(current_plan_id, app_db_web_location)
            session['master_mteams'] = master_mteams
            session['master_mrooms'] = master_mrooms
            session['master_mjurors'] = master_mjurors
            session['master_room_mvolunteers'] = master_room_mvolunteers

        try:
            current_dstage_score_id = int(request.args.get('dss'))
        except:
            current_dstage_score_id = 0

        # get up to date mpair fight status
        sm_room_pairs = get_mpairs_by_room_round(current_plan_id, app_db_web_location)
        sm_current_room_round_pairs = sm_room_pairs[current_room_code - 1][2][
            current_round_code - 1]  # (current_room_code, tmp_mroom_label, tmp_round_list)
        current_team_codes = (sm_current_room_round_pairs[1][0][4], sm_current_room_round_pairs[1][1][4])

        # get up to date mpair stage problem info
        current_stage_problems = get_mpair_problems_simmple(current_plan_id, current_mpair_id, app_db_web_location)
        # get up to date mpair stage score info
        validation_scores = get_mpair_scores_4validate(current_plan_id, current_mpair_id, current_team_codes, app_db_web_location)
        current_team_codes_SP = validation_scores[1]
        sm_current_pair_scores = validation_scores[0]

    # compare who is the winner
    ranked_team_codes_SP = check_ranking2(current_team_codes_SP)

    return render_template('main/sm_score_view.html', form=form, view_type=view_type, current_room_code=current_room_code, master_mrooms=master_mrooms,
                           current_round_code=current_round_code, master_mteams=master_mteams, current_plan_id=current_plan_id,
                           master_mjurors=master_mjurors, sm_current_pair_scores=sm_current_pair_scores, current_mpair_id=current_mpair_id,
                           current_team_codes_SP=current_team_codes_SP, current_team_codes=current_team_codes, ranked_team_codes_SP=ranked_team_codes_SP,
                           current_stage_problems=current_stage_problems, current_dstage_score_id=current_dstage_score_id)


@main_blueprint.route('/round_schedule', methods=['GET', 'POST'])
def round_schedule():
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    event_id = current_app.config['CURRENT_EVENT']
    round_code = int(request.args.get('round'))
    active_pan_list = search_event_plan(event_id, "Active", 1, app_db_web_location)
    plan_id = 0
    plan_sub_status = 0
    for plan in active_pan_list:
        plan_id = plan[1]
        plan_sub_status = plan[4] # 1-released 2-published
        break

    if plan_sub_status > 0:
        round_schedule = get_schedue_by_round_room(plan_id, app_db_web_location)
        if round_schedule is None or len(round_schedule) < 1:
            flash_msg = "Schedule not available now, please check later."
            flash(flash_msg, 'error')
            return redirect(url_for('main.home_page'))
        else:
            master_mteams = get_mteams(plan_id, app_db_web_location)  # (mteam_code, mteam_name, team_info, team_member_list)
            master_mrooms = get_mrooms(plan_id, app_db_web_location)  # (mroom_code, mroom_label, mroom_info)
            round_room_jurors = get_mpair_jurors_by_round_room(plan_id, None, app_db_web_location)
            master_mjurors = get_mjurors(plan_id, app_db_web_location)  # (mjuror_code, mjuror_name, mjuror_info, has_cois, juror_cois_list)
            master_room_mvolunteers = get_mvolunteers(plan_id, app_db_web_location)  # (mroom_code, mroom_label, room_volunteers)

            fm_active_pan_list = search_event_plan(event_id, "Active", 2, app_db_web_location)
            fm_plan_id = 0
            fm_plan_sub_status = 0
            fm_schedule = None
            for plan in fm_active_pan_list:
                fm_plan_id = plan[1]
                fm_plan_sub_status = plan[4]  # 1-released 2-published
                break
            if fm_plan_id > 0 and fm_plan_sub_status >0:
                # (teams, jurors, mpair, round, room)
                fm_schedule = search_fm_plan(event_id, fm_plan_id, app_db_web_location)
            current_round_schedule = None
            current_round_room_jurors = None
            if round_code < 6:
                current_round_schedule = round_schedule[round_code - 1]
                current_round_room_jurors = round_room_jurors[round_code - 1]

            return render_template('main/round_schedule.html', round_schedule=current_round_schedule, master_mjurors=master_mjurors,
                                   master_room_mvolunteers=master_room_mvolunteers, round_room_jurors=current_round_room_jurors,
                                   master_mteams=master_mteams, round_code=round_code, master_mrooms=master_mrooms, fm_schedule=fm_schedule)
    else:
        flash_msg = "Schedule not available now, please check later."
        flash(flash_msg, 'error')
        return redirect(url_for('main.home_page'))


@main_blueprint.route('/event_schedule', methods=['GET', 'POST'])
def event_schedule():
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    event_id = current_app.config['CURRENT_EVENT']
    active_pan_list = search_event_plan(event_id, "Active", 1, app_db_web_location)
    plan_id = 0
    plan_sub_status = 0
    for plan in active_pan_list:
        plan_id = plan[1]
        plan_sub_status = plan[4] # 1-released 2-published
        break
    tmp_super = False
    try:
        if current_user.has_roles('super'):
            tmp_super = True
    except:
        pass

    if plan_sub_status > 0 or tmp_super:
        round_schedule = get_schedue_by_round_room(plan_id, app_db_web_location)
        if round_schedule is None or len(round_schedule) < 1:
            flash_msg = "Schedule not available now, please check later."
            flash(flash_msg, 'error')
            return redirect(url_for('main.home_page'))
        else:
            master_mteams = get_mteams(plan_id, app_db_web_location)  # (mteam_code, mteam_name, team_info, team_member_list)
            master_mrooms = get_mrooms(plan_id, app_db_web_location)  # (mroom_code, mroom_label, mroom_info)
            round_room_jurors = get_mpair_jurors_by_round_room(plan_id, None, app_db_web_location)
            master_mjurors = get_mjurors(plan_id, app_db_web_location)  # (mjuror_code, mjuror_name, mjuror_info, has_cois, juror_cois_list)
            master_room_mvolunteers = get_mvolunteers(plan_id, app_db_web_location)  # (mroom_code, mroom_label, room_volunteers)

            fm_active_pan_list = search_event_plan(event_id, "Active", 2, app_db_web_location)
            fm_plan_id = 0
            fm_plan_sub_status = 0
            fm_schedule = None
            for plan in fm_active_pan_list:
                fm_plan_id = plan[1]
                fm_plan_sub_status = plan[4]  # 1-released 2-published
                break
            if fm_plan_id > 0 and (fm_plan_sub_status >0 or tmp_super):
                # (teams, jurors, mpair, round, room)
                fm_schedule = search_fm_plan(event_id, fm_plan_id, app_db_web_location)

            return render_template('main/event_schedule.html', round_schedule=round_schedule, master_mjurors=master_mjurors,
                                   master_room_mvolunteers=master_room_mvolunteers, round_room_jurors=round_room_jurors,
                                   master_mteams=master_mteams, master_mrooms=master_mrooms, fm_schedule=fm_schedule)
    else:
        flash_msg = "Schedule not available now, please check later."
        flash(flash_msg, 'error')
        return redirect(url_for('main.home_page'))


@main_blueprint.route('/my_schedule', methods=['GET', 'POST'])
@login_required  # Limits access to authenticated users
def my_schedule():
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    active_pan_list = search_event_plan(1, "Active", 1, app_db_web_location)
    event_id = current_app.config['CURRENT_EVENT']
    current_user_id = current_user.id
    plan_sub_status = 0
    plan_id = 0
    for plan in active_pan_list:
        plan_id = plan[1]
        plan_sub_status = plan[4] # 1-released 2-published
        break

    if plan_sub_status > 0:
        try:
            schedule_type = int(request.args.get('type')) # 1-team, 2-team member, 3-juror, 4-volunteer
            team_schedules = None
            juror_schedule = None
            volunteer_schedule = None
            round_schedule = None
            if schedule_type == 1 or schedule_type == 2 or schedule_type == 13:
                team_schedules = get_my_team_schedue(event_id, plan_id, current_user_id, schedule_type, app_db_web_location)
                round_schedule = get_schedue_by_round_room(plan_id, app_db_web_location)
            if schedule_type == 3 or schedule_type == 13:
                juror_schedule = get_juror_schedue(event_id, plan_id, current_user_id, app_db_web_location)
            if schedule_type == 4:
                volunteer_schedule = get_volunteer_schedue(event_id, plan_id, current_user_id, app_db_web_location)
            master_mteams = get_mteams(plan_id,
                                       app_db_web_location)  # (mteam_code, mteam_name, team_info, team_member_list)
            master_mrooms = get_mrooms(plan_id, app_db_web_location)  # (mroom_code, mroom_label, mroom_info)
            round_room_jurors = get_mpair_jurors_by_round_room(plan_id, None, app_db_web_location)
            master_mjurors = get_mjurors(plan_id,
                                         app_db_web_location)  # (mjuror_code, mjuror_name, mjuror_info, has_cois, juror_cois_list)
            master_room_mvolunteers = get_mvolunteers(plan_id,
                                                      app_db_web_location)  # (mroom_code, mroom_label, room_volunteers)

            return render_template('main/my_schedule.html', schedule_type=schedule_type, team_schedules=team_schedules,
                                   juror_schedule=juror_schedule, volunteer_schedule=volunteer_schedule, round_schedule=round_schedule,
                                   master_mjurors=master_mjurors, master_room_mvolunteers=master_room_mvolunteers,
                                   round_room_jurors=round_room_jurors, master_mteams=master_mteams, master_mrooms=master_mrooms)
        except:
            flash_msg = "Invalid access."
            flash(flash_msg, 'error')
            return redirect(url_for('main.member_page'))
    else:
        flash_msg = "Schedule coming soon."
        flash(flash_msg, 'error')
        return redirect(url_for('main.member_page'))


@main_blueprint.route('/publish', methods=['GET', 'POST'])
@roles_required('super')  # Limits access to users with 'super' role
def admin_publish():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']

    current_user_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = EventPlanForm(request.form)

    # Process valid POST
    if request.method == 'POST':
        try:
            plan_id = int(request.form.get("plan_id"))
            plan_sub_status = int(request.form.get("plan_sub_status"))
            update_plan_sub_status_by_id(plan_id, plan_sub_status, current_user_id, app_db_web_location)
        except:
            flash_msg = "Plan Status Update failed, please re-try."
            flash(flash_msg, 'error')

    # get plan from database
    plan_status = "Active"
    sm_plan_id = 0
    sm_plan_sub_status = 0
    fm_plan_id = 0
    fm_plan_sub_status = 0
    active_sm_plan_list = search_event_plan(event_id, plan_status, 1, app_db_web_location)
    if active_sm_plan_list is not None and len(active_sm_plan_list) > 0:
        # plan has already been activated, changes to the plan are NOT allowed
        for plan in active_sm_plan_list:
            sm_plan_id = plan[1]
            sm_plan_sub_status = plan[4]  # 1-released 2-published
            break

        if sm_plan_sub_status > 0:
            active_fm_plan_list = search_event_plan(event_id, plan_status, 2, app_db_web_location)
            for plan in active_fm_plan_list:
                fm_plan_id = plan[1]
                fm_plan_sub_status = plan[4]  # 1-released 2-published
                break

            return render_template('main/admin_publish.html', form=form, plan_status=plan_status,
                                   sm_plan_sub_status=sm_plan_sub_status, sm_plan_id=sm_plan_id,
                                   fm_plan_sub_status=fm_plan_sub_status, fm_plan_id=fm_plan_id)

    flash_msg = "Plan is not ready yet."
    flash(flash_msg, 'error')
    return redirect(url_for('main.admin_mgmt'))


@main_blueprint.route('/sm_dashboard', methods=['GET', 'POST'])
@roles_required('super')  # Limits access to users with 'super' role
def sm_dashboard():
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    event_id = current_app.config['CURRENT_EVENT']

    try:
        sm_plan_id = int(request.args.get("plan_id"))
        sm_plan_sub_status = int(request.args.get("plan_sub_status"))
        sm_round_schedule = get_schedue_by_round_room(sm_plan_id, app_db_web_location)
        # (mteam_code, mteam_name, team_info, team_member_list)
        master_mteams = get_mteams(sm_plan_id, app_db_web_location)
        # (mroom_code, mroom_label, mroom_info)
        master_mrooms = get_mrooms(sm_plan_id, app_db_web_location)
        round_room_jurors = get_mpair_jurors_by_round_room(sm_plan_id, None, app_db_web_location)
        # (mjuror_code, mjuror_name, mjuror_info, has_cois, juror_cois_list)
        master_mjurors = get_mjurors(sm_plan_id, app_db_web_location)
        # (mroom_code, mroom_label, room_volunteers)
        master_room_mvolunteers = get_mvolunteers(sm_plan_id, app_db_web_location)

        return render_template('main/sm_dashboard.html', round_schedule=sm_round_schedule, master_mjurors=master_mjurors,
                               master_room_mvolunteers=master_room_mvolunteers, round_room_jurors=round_room_jurors,
                               master_mteams=master_mteams, master_mrooms=master_mrooms, plan_id=sm_plan_id)
    except:
        flash_msg = "Invalid access."
        flash(flash_msg, 'error')
        return redirect(url_for('main.admin_publish'))


@main_blueprint.route('/rank', methods=['GET', 'POST'])
def event_rank():
    return redirect(url_for('main.rank_final'))


@main_blueprint.route('/rank_final', methods=['GET', 'POST'])
def rank_final():
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    event_id = current_app.config['CURRENT_EVENT']
    plan_status = "Active"
    active_sm_plan_list = search_event_plan(event_id, plan_status, 1, app_db_web_location)
    active_fm_plan_list = search_event_plan(event_id, plan_status, 2, app_db_web_location)
    sm_plan_id = 0
    sm_plan_sub_status = 0
    for plan in active_sm_plan_list:
        sm_plan_id = plan[1]
        sm_plan_sub_status = plan[4] # 1-released 2-published
        break

    if sm_plan_sub_status > 0:
        fm_plan_sub_status = 0
        fm_plan_id = 0
        for plan in active_fm_plan_list:
            fm_plan_id = plan[1]
            fm_plan_sub_status = plan[4]  # 1-released 2-published
            break
        if fm_plan_sub_status > 0:
            # check if final_match validated
            fm_status = check_fm_status(fm_plan_id, app_db_web_location)
            if fm_status is not None:
                print("***___ fm_status ", fm_status)
                # (mteam_code, mteam_name, team_info, team_member_list)
                master_mteams = get_mteams(sm_plan_id, app_db_web_location)
                fm_team_rank = fm_status[1]
                return render_template('main/event_rank_final.html', fm_plan_sub_status=fm_plan_sub_status,
                                       master_mteams=master_mteams, fm_team_rank=fm_team_rank)
        # redirect to team ranking by round if final match score is not ready
        return redirect(url_for('main.rank_round'))
    else:
        flash_msg = "Ranking is coming soon."
        flash(flash_msg, 'error')
        return redirect(url_for('main.home_page'))


@main_blueprint.route('/rank_round', methods=['GET', 'POST'])
def rank_round():
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    event_id = current_app.config['CURRENT_EVENT']
    plan_status = "Active"
    active_sm_plan_list = search_event_plan(event_id, plan_status, 1, app_db_web_location)
    active_fm_plan_list = search_event_plan(event_id, plan_status, 2, app_db_web_location)
    sm_plan_id = 0
    sm_plan_sub_status = 0
    for plan in active_sm_plan_list:
        sm_plan_id = plan[1]
        sm_plan_sub_status = plan[4] # 1-released 2-published
        break

    if sm_plan_sub_status > 0:
        fm_plan_sub_status = 0
        for plan in active_fm_plan_list:
            fm_plan_id = plan[1]
            fm_plan_sub_status = plan[4]  # 1-released 2-published
            break
        # (mteam_code, mteam_name, team_info, team_member_list)
        master_mteams = get_mteams(sm_plan_id, app_db_web_location)
        sm_team_rank = get_sm_team_rank_by_round(sm_plan_id, app_db_web_location)
        return render_template('main/event_rank_round.html', fm_plan_sub_status=fm_plan_sub_status,
                               master_mteams=master_mteams, sm_team_rank=sm_team_rank)
    else:
        flash_msg = "Ranking is coming soon."
        flash(flash_msg, 'error')
        return redirect(url_for('main.home_page'))


@main_blueprint.route('/event_rank_member', methods=['GET', 'POST'])
def event_rank_member():
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    event_id = current_app.config['CURRENT_EVENT']
    plan_status = "Active"
    active_sm_plan_list = search_event_plan(event_id, plan_status, 1, app_db_web_location)
    active_fm_plan_list = search_event_plan(event_id, plan_status, 2, app_db_web_location)
    sm_plan_id = 0
    sm_plan_sub_status = 0
    for plan in active_sm_plan_list:
        sm_plan_id = plan[1]
        sm_plan_sub_status = plan[4] # 1-released 2-published
        break

    if sm_plan_sub_status > 0:
        fm_plan_sub_status = 0
        for plan in active_fm_plan_list:
            fm_plan_id = plan[1]
            fm_plan_sub_status = plan[4]  # 1-released 2-published
            break
        # (mteam_code, mteam_name, team_info, team_member_list)
        master_mteams = get_mteams(sm_plan_id, app_db_web_location)
        sm_member_rank = get_sm_member_rank_by_round(sm_plan_id, app_db_web_location)
        return render_template('main/event_rank_member.html', fm_plan_sub_status=fm_plan_sub_status,
                               master_mteams=master_mteams, sm_member_rank=sm_member_rank)
    else:
        flash_msg = "Ranking is coming soon."
        flash(flash_msg, 'error')
        return redirect(url_for('main.home_page'))


@main_blueprint.route('/main/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/user_profile_page.html',
                           form=form)


@main_blueprint.route('/fm_planning', methods=['GET', 'POST'])
@roles_required('super')  # Limits access to users with 'super' role
def fm_planning():
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    event_id = current_app.config['CURRENT_EVENT']
    current_user_id = current_user.id

    # Initialize form
    form = EventFinalPlanForm(request.form)

    # Process valid POST
    if request.method == 'POST':
        #get parameters:
        # hidden fields
        sm_plan_id = int(request.form.get("sm_plan_id"))
        fm_round_id = int(request.form.get("fm_round_id"))
        fm_round_code = int(request.form.get("fm_round_code"))
        # list of fm teams
        fm_teams = request.form.getlist("fm_teams")
        # selected room
        fm_room_id = int(request.form.get("fm_room"))
        # selected jurors
        jury = request.form.getlist("jury")
        print(fm_teams, fm_room_id, jury, len(fm_teams), len(jury))
        if fm_teams is not None and fm_room_id > 0 and jury is not None and len(fm_teams)==3 and len(jury) > 4:
            selected_fm_teams = list()
            for row in fm_teams:
                tmp_mteam_id = row.split("--", 2)[0]
                tmp_mteam_code = row.split("--", 2)[1]
                tmp_mteam_school_id = row.split("--", 2)[2]
                selected_fm_teams.append((tmp_mteam_id, tmp_mteam_code, tmp_mteam_school_id))
            selected_fm_jury = list()
            for row in jury:
                tmp_mjuror_id = row.split("--", 1)[0]
                tmp_mjuror_code = row.split("--", 1)[1]
                selected_fm_jury.append((tmp_mjuror_id, tmp_mjuror_code))

            db_save_fm_proposal(event_id, fm_round_id, fm_room_id, selected_fm_jury, selected_fm_teams, current_user_id, app_db_web_location)
            flash_msg = "Final Match Plan has been created successfully"
            flash(flash_msg, 'success')
            return redirect(url_for('main.admin_mgmt'))
        else:
            flash_msg = "Final Match Plan can't be created, please select the right data."
            flash(flash_msg, 'error')
            return redirect(url_for('main.admin_mgmt'))
    else:
        plan_status = "Active"
        active_sm_plan_list = search_event_plan(event_id, plan_status, 1, app_db_web_location)
        active_fm_plan_list = search_event_plan(event_id, plan_status, 2, app_db_web_location)
        sm_plan_id = 0
        sm_plan_sub_status = 0
        fm_round = 0
        for plan in active_sm_plan_list:
            sm_plan_id = plan[1]
            sm_plan_sub_status = plan[4] # 1-released 2-published
            break

        if sm_plan_sub_status > 0:
            fm_plan_sub_status = 0
            fm_plan_status = None
            for plan in active_fm_plan_list:
                fm_plan_id = plan[1]
                fm_plan_status = plan[2]
                fm_plan_sub_status = plan[4]  # 1-released 2-published
                break
            #get initial data
            # (mroom_code, mroom_label, mroom_info)
            master_mrooms = get_mrooms(sm_plan_id, app_db_web_location)
            # (mteam_code, mteam_name, team_info, team_member_list)
            master_mteams = get_mteams(sm_plan_id, app_db_web_location)
            # (mjuror_code, mjuror_name, mjuror_info, has_cois, juror_cois_list)
            master_mjurors = get_mjurors(sm_plan_id, app_db_web_location)
            # (mroom_code, mroom_label, room_volunteers)
            master_room_mvolunteers = get_mvolunteers(sm_plan_id, app_db_web_location)
            # get up to date selective match team ranking
            sm_team_rank = get_sm_team_rank(sm_plan_id, app_db_web_location)

            if fm_plan_status is not None and fm_plan_status == "Active":
                # final plan already active, display the plan
                flash_msg = "Final match plan has been activated, you can't create new one."
                flash(flash_msg, 'error')
                return redirect(url_for('main.admin_mgmt'))
            else:
                # final plan dosen't active or doesn't exist, start the final plan
                # get event_id and code for final match
                fm_round = search_fm_round(event_id, app_db_web_location)
                if fm_round is not None:
                    pass
                else:
                    flash_msg = "Final match round is not setup yet, please contact system administrator."
                    flash(flash_msg, 'error')
                    return redirect(url_for('main.admin_mgmt'))

            return render_template('main/admin_fm_planning.html', form=form, fm_plan_sub_status=fm_plan_sub_status,
                                   sm_plan_id=sm_plan_id, master_mrooms=master_mrooms,
                                   master_mteams=master_mteams, sm_team_rank=sm_team_rank, fm_round=fm_round,
                                   master_mjurors=master_mjurors, master_room_mvolunteers=master_room_mvolunteers)
        else:
            flash_msg = "Selective plan is not released yet, you can't start the final match planning."
            flash(flash_msg, 'error')
            return redirect(url_for('main.admin_mgmt'))


@main_blueprint.route('/fm_plan_view', methods=['GET', 'POST'])
@roles_required('super')  # Limits access to users with 'super' role
def fm_plan_view():
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    event_id = current_app.config['CURRENT_EVENT']
    current_user_id = current_user.id

    # Initialize form
    form = EventFinalPlanForm(request.form)
    fm_plan_id = int(request.args.get('plan_id'))

    # Process valid POST
    if request.method == 'POST':
        deactivate = request.form.get("deactivate")
        release = request.form.get("release")
        if deactivate == "Deactivate":
            # De-Activate Plan (change status to proposed)
            update_plan_status(fm_plan_id, "Proposed", current_user.id, app_db_web_location)
            flash_msg = "Proposed plan has been deactivated."
        elif release == "Release":
                # Release Plan (change sub status to Released), plan is forzen, no more change allowed
                # get all volunteers
                release_sm_plan(fm_plan_id, 1, current_user.id, app_db_web_location)
                flash_msg = "Proposed plan has been released."
        else:
            update_plan_status(fm_plan_id, "Active", current_user.id, app_db_web_location)
            flash_msg = "Proposed plan has been activated successfully. Participants can't be updated anymore."
        flash(flash_msg, 'success')
        return redirect(url_for('main.admin_mgmt'))
    else:
        fm_plan_status = request.args.get('plan_status')
        fm_plan_sub_status = int(request.args.get('plan_sub_status'))
        fm_activable = int(request.args.get('activable'))

        sm_plan_status = "Active"
        active_sm_plan_list = search_event_plan(event_id, sm_plan_status, 1, app_db_web_location)
        sm_plan_id = 0
        sm_plan_sub_status = 0
        fm_round = 0
        for plan in active_sm_plan_list:
            sm_plan_id = plan[1]
            sm_plan_sub_status = plan[4] # 1-released 2-published
            break
        if fm_plan_status is not None:
            #get initial data
            # (mroom_code, mroom_label, mroom_info)
            master_mrooms = get_mrooms(sm_plan_id, app_db_web_location)
            # (mteam_code, mteam_name, team_info, team_member_list)
            master_mteams = get_mteams(sm_plan_id, app_db_web_location)
            # (mjuror_code, mjuror_name, mjuror_info, has_cois, juror_cois_list)
            master_mjurors = get_mjurors(sm_plan_id, app_db_web_location)
            # (mroom_code, mroom_label, room_volunteers)
            master_room_mvolunteers = get_mvolunteers(sm_plan_id, app_db_web_location)
            # get up to date selective match team ranking
            sm_team_rank = get_sm_team_rank(sm_plan_id, app_db_web_location)
            # get fm_plan
            fm_plan = search_fm_plan(event_id, fm_plan_id, app_db_web_location) #(teams, jurors, mpair, round, room)
            fm_team_codes = list()
            fm_team_sids = list()
            for team in fm_plan[0]:
                fm_team_codes.append(team[1])
                fm_team_sids.append(master_mteams[team[1]-1][2][8])

            sm_left = check_sm_status(sm_plan_id, app_db_web_location)

            return render_template('main/admin_fm_plan_view.html', form=form, fm_plan_sub_status=fm_plan_sub_status,
                                   sm_plan_id=sm_plan_id, master_mrooms=master_mrooms, fm_plan=fm_plan,
                                   fm_plan_id=fm_plan_id, fm_plan_status=fm_plan_status, fm_activable=fm_activable,
                                   master_mteams=master_mteams, sm_team_rank=sm_team_rank, fm_round=fm_round,
                                   master_mjurors=master_mjurors, master_room_mvolunteers=master_room_mvolunteers,
                                   fm_team_codes=fm_team_codes, fm_team_sids=fm_team_sids, sm_left=sm_left)
        else:
            flash_msg = "Invalid access."
            flash(flash_msg, 'error')
            return redirect(url_for('main.admin_mgmt'))


@main_blueprint.route('/fm_mgmt', methods=['GET', 'POST'])
@roles_required('data')  # Limits access to users with the 'data' role
def fm_draw():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    current_user_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = EventStageForm(request.form)
    #fm_pair_teams = None
    fm_current_room_round_pairs = None
    fm_team_problem_codes = None

    if request.method == 'POST':
        # Process valid POST
        fm_plan_id = 0
        sm_plan_id = 0
        team1 = None
        team2 = None
        team3 = None
        jury = None
        fm_plan = None
        try:
            # get master table from session
            master_mteams = session['master_mteams']
            master_mrooms = session['master_mrooms']
            master_mjurors = session['master_mjurors']
            master_room_mvolunteers = session['master_room_mvolunteers']
            fm_plan = session['fm_plan']
            fm_plan_id = int(request.form.get('fm_plan_id'))
            sm_plan_id = int(request.form.get('sm_plan_id'))
            team_radio_1 = (request.form.get('team_radio_1'))
            team_radio_2 = (request.form.get('team_radio_2'))
            team_radio_3 = (request.form.get('team_radio_3'))
            #each team pick the problem"
            team_radio_1_problem_code = int(request.form.get('team_radio_1_problem'))
            team_radio_2_problem_code = int(request.form.get('team_radio_2_problem'))
            team_radio_3_problem_code = int(request.form.get('team_radio_3_problem'))
            fm_team_problem_codes = (team_radio_1_problem_code, team_radio_2_problem_code, team_radio_3_problem_code)
            print(team_radio_1, team_radio_2, team_radio_3)
            jury = request.form.getlist("jury")
            print(jury)
        except:
            flash_msg = "Invalid access to record team draw results!"
            flash(flash_msg, 'error')
            return redirect(url_for('main.sm_mgmt'))

        if team_radio_1 is not None and team_radio_2 is not None and team_radio_3 is not None and (int(team_radio_1) + int(team_radio_2) + int(team_radio_3)) == 6:
            if team_radio_1_problem_code>0 and team_radio_2_problem_code>0 and team_radio_3_problem_code>0 \
                    and team_radio_1_problem_code != team_radio_2_problem_code \
                    and team_radio_1_problem_code != team_radio_3_problem_code \
                    and team_radio_2_problem_code != team_radio_3_problem_code:
                if jury is not None and len(jury) > 4:
                    # get up to date mpair fight status
                    current_jury = list()
                    for juror in jury:
                        tmp_juror_code = juror.split("--", 2)[0]
                        tmp_mpair_juror_id = juror.split("--", 2)[1]
                        tmp_mjuror_id = juror.split("--", 2)[2]
                        tmp_turple = (int(tmp_juror_code), int(tmp_mpair_juror_id), int(tmp_mjuror_id))
                        current_jury.append(tmp_turple)
                    initialize_fm_stage_agenda(fm_plan_id, fm_plan,
                                               (int(team_radio_1), int(team_radio_2), int(team_radio_3)),
                                               fm_team_problem_codes, current_jury,
                                               current_user_id, app_db_web_location)
                    return redirect(url_for('main.fm_draw'))
                else:
                    flash_msg = "Don't have enough jurors (min 5)!"
            else:
                flash_msg = "Problem choice is missing or wrong!"
        else:
            flash_msg = "Draw number is wrong"
        flash(flash_msg, 'error')
        return redirect(url_for('main.fm_draw'))
    else:
        # Process valid GET
        plan_status = "Active"
        active_sm_plan_list = search_event_plan(event_id, plan_status, 1, app_db_web_location)
        active_fm_plan_list = search_event_plan(event_id, plan_status, 2, app_db_web_location)
        sm_plan_id = 0
        sm_plan_sub_status = 0
        fm_plan_id = 0
        fm_round = 0
        fm_plan_sub_status = 0
        current_room_code = 0
        fm_plan_status = None
        for plan in active_sm_plan_list:
            sm_plan_id = plan[1]
            sm_plan_sub_status = plan[4] # 1-released 2-published
            break
        for plan in active_fm_plan_list:
            fm_plan_id = plan[1]
            fm_plan_status = plan[2]
            fm_plan_sub_status = plan[4]  # 1-released 2-published
            break

        if sm_plan_sub_status > 0 and fm_plan_sub_status >0 and (fm_plan_sub_status == 2 or current_user.has_roles('super')):
            #get initial data
            # (mroom_code, mroom_label, mroom_info)
            master_mrooms = get_mrooms(sm_plan_id, app_db_web_location)
            # (mteam_code, mteam_name, team_info, team_member_list)
            master_mteams = get_mteams(sm_plan_id, app_db_web_location)
            # (mjuror_code, mjuror_name, mjuror_info, has_cois, juror_cois_list)
            master_mjurors = get_mjurors(sm_plan_id, app_db_web_location)
            # (mroom_code, mroom_label, room_volunteers)
            master_room_mvolunteers = get_mvolunteers(sm_plan_id, app_db_web_location)
            # get fm_plan
            # (teams, jurors, mpair, round, room)
            fm_plan = search_fm_plan(event_id, fm_plan_id, app_db_web_location)
            session['master_mteams'] = master_mteams
            session['master_mrooms'] = master_mrooms
            session['master_mjurors'] = master_mjurors
            session['master_room_mvolunteers'] = master_room_mvolunteers
            session['fm_plan'] = fm_plan
            current_room_code = fm_plan[4][1]
            fm_team_codes = list()
            fm_team_sids = list()
            for team in fm_plan[0]:
                fm_team_codes.append(team[1])
                fm_team_sids.append(master_mteams[team[1]-1][2][8])

            if current_user.has_roles('super'):
                # super user can access final match data entry
                pass
            else:
                # search the room code that assigned to the data entrier
                # PLAN_ID, PPANT_USER_ID, MROOM_ID, MROOM_CODE, MROOM_LABEL, DATA_ENTRY
                assigned_rooms = search_mroom_assigned_to_data_entry(sm_plan_id, current_user_id, app_db_web_location)
                can_access_fm = False
                for room in assigned_rooms:
                    if current_room_code == room[3]:
                        can_access_fm = True
                        break
                if not can_access_fm:
                    flash_msg = "Invalid access to final match!"
                    flash(flash_msg, 'error')
                    return redirect(url_for('main.sm_mgmt'))

            if fm_plan[2][2] > 0:
                fm_pairs = get_mpairs_by_room_round(fm_plan_id, app_db_web_location)
                # (current_room_code, tmp_mroom_label, tmp_round_list)
                fm_current_room_round_pairs = fm_pairs[0][2][0]
                print("**__", fm_current_room_round_pairs[2])

            current_pair_team_problems = get_reporter_problems(sm_plan_id, fm_plan[0][0][1], fm_plan[0][1][1], fm_plan[0][2][1], app_db_web_location)
            # re-arrange current_pair_team_problems
            team_problems = list()
            for team in current_pair_team_problems:
                tmp_problem_code_list = []
                for i in range(10):
                    tmp_problem_code = i + 1
                    has_matched_problem = False
                    tmp_problme_list = []
                    for item in team[1]:
                        if item[0] == tmp_problem_code:
                            tmp_problme_list.append(item[1])
                            has_matched_problem = True
                    if has_matched_problem:
                        tmp_problem_code_list.append((tmp_problem_code, tmp_problme_list))
                    else:
                        tmp_problem_code_list.append((tmp_problem_code, None))
                team_problems.append((team[0], tmp_problem_code_list))

            problem_label_codes = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")

            return render_template('main/fm_draw.html', form=form, fm_current_room_round_pairs=fm_current_room_round_pairs,
                                   sm_plan_id=sm_plan_id, master_mrooms=master_mrooms, fm_plan=fm_plan, problem_label_codes=problem_label_codes,
                                   fm_plan_id=fm_plan_id, master_mteams=master_mteams, team_problems=team_problems,
                                   master_mjurors=master_mjurors, master_room_mvolunteers=master_room_mvolunteers)
        else:
            flash_msg = "Final Match is not ready!"
            flash(flash_msg, 'error')
            return redirect(url_for('main.sm_mgmt'))


# assign team member
@main_blueprint.route('/fm_select', methods=['GET', 'POST'])
@roles_required('data')  # Limits access to users with the 'data' role
def fm_select():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    current_user_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = EventStageForm(request.form)

    # Initialize parameters from request and session
    current_room_code = 0
    current_round_code = 0
    current_plan_id = 0
    fm_current_room_round_pairs = None
    master_mteams = None
    master_mrooms = None
    master_mjurors = None
    master_room_mvolunteers = None
    current_stage_code = 0
    stage_agenda = None
    current_pair_assigned_jurors = None
    current_pair_assigned_juror_codes = None
    current_pair_id = 0
    master_problems = None
    opponent_team_members_roles = None
    reporter_team_members_roles = None
    reviewer_team_members_roles = None
    current_pair_team_problems = None
    problem_label_codes = None
    team_problems = []
    current_day_pair_problems = []
    try:
        # get master prolbem tables from session
        master_problems = session['master_problems']
    except:
        # search master table of event problems from database
        master_problems= get_event_master_problems(event_id, app_db_web_location)
        session['master_problems'] = master_problems

    try:
        # get master table from session
        master_mteams = session['master_mteams']
        master_mrooms = session['master_mrooms']
        master_mjurors = session['master_mjurors']
        master_room_mvolunteers = session['master_room_mvolunteers']
    except:
        flash_msg = "Invalid access to assign fm member!"
        flash(flash_msg, 'error')
        return redirect(url_for('main.fm_draw'))

    if request.method == 'POST':
        # Process valid POST
        try:
            current_room_code = int(request.form.get('current_room_code'))
            current_round_code = int(request.form.get('current_round_code'))
            current_plan_id = int(request.form.get('current_plan_id'))
            current_pair_id = int(request.form.get('current_pair_id'))
            current_stage_code = int(request.form.get('current_stage_code'))
            reporter_problem_code = int(request.form.get('reporter_problem'))
            reporter = request.form.get('reporter')
            opponent = request.form.get('opponent')
            reviewer = request.form.get('reviewer')
            # get up to date mpair fight status
            fm_room_pairs = get_mpairs_by_room_round(current_plan_id, app_db_web_location)
            # (current_room_code, tmp_mroom_label, tmp_round_list)
            fm_current_room_round_pairs = fm_room_pairs[0][2][0]
        except:
            flash_msg = "Invalid access in POST!"
            flash(flash_msg, 'error')
            return redirect(url_for('main.fm_draw'))

        # only the stage status code is 1 (initiated) or ?
        if fm_current_room_round_pairs[2] >0 :
            # assign members and problem
            if reporter is not None and opponent is not None and reviewer is not None \
                    and reporter != "0" and opponent != "0" and reviewer != "0":
                # add team members and jurors and update MPAIR stage status to 11 or 21
                if fm_current_room_round_pairs[2] == 1 or fm_current_room_round_pairs[2] == 13 or fm_current_room_round_pairs[2] == 23:
                    stage_agenda = get_sm_stage_agenda(current_plan_id, fm_current_room_round_pairs[3], app_db_web_location)
                    current_reporter_dstage_team_id = stage_agenda[current_stage_code - 1][2][0][2][4]
                    save_fm_stage_members(current_plan_id, current_pair_id, current_stage_code, reporter, opponent, reviewer,
                                          master_problems[reporter_problem_code-1][1], current_reporter_dstage_team_id, current_user_id, app_db_web_location)
                    # get up to date mpair fight status
                    fm_room_pairs = get_mpairs_by_room_round(current_plan_id, app_db_web_location)
                    # (current_room_code, tmp_mroom_label, tmp_round_list)
                    fm_current_room_round_pairs = fm_room_pairs[0][2][0]

                    # get up to date stage_agenda for specific mpair
                    # stage_agenda: (stage_code, role_list)
                    # role_list: (reporter, opponent)
                    stage_agenda = get_sm_stage_agenda(current_plan_id, fm_current_room_round_pairs[3], app_db_web_location)
                    # get on-board jurors order by is_chair
                    # to be added here, now use jury as place holder

                    session['fm_current_room_round_pairs'] = fm_current_room_round_pairs
                    session['current_stage_agenda'] = stage_agenda[current_stage_code -1]
                    session['current_codes'] = (current_room_code, current_round_code, current_stage_code, current_pair_id, current_plan_id)
                    session['fm_reporter_problem'] = master_problems[reporter_problem_code-1][1]
                    session.pop('fm_plan')
                    session.pop('master_room_mvolunteers')

                    return redirect(url_for('main.fm_timing'))
            else:
                flash_msg = "Reporter, Opponent and or Reviewer not valid!"
                flash(flash_msg, 'error')
                return redirect(url_for('main.fm_draw'))
        else:
            flash_msg = "Invalid access to assign team member!"
            flash(flash_msg, 'error')
            return redirect(url_for('main.fm_draw'))
    else:
        # Process valid GET
        try:
            current_room_code = int(request.args.get('room'))
            current_round_code = int(request.args.get('round'))
            current_plan_id = int(request.args.get('plan'))
            current_stage_code = int(request.args.get('stage'))
            sm_plan_id = int(request.args.get('sm_plan'))
        except:
            flash_msg = "Invalid access in get!"
            flash(flash_msg, 'error')
            return redirect(url_for('main.fm_draw'))

        # get up to date mpair fight status
        fm_room_pairs = get_mpairs_by_room_round(current_plan_id, app_db_web_location)
        # (current_room_code, tmp_mroom_label, tmp_round_list)
        fm_current_room_round_pairs = fm_room_pairs[0][2][0]
        # get up to date stage_agenda for specific mpair
        stage_agenda = get_sm_stage_agenda(current_plan_id, fm_current_room_round_pairs[3], app_db_web_location)
        # mpair_id = stage_agenda[0][1]
        current_pair_team_problems = get_reporter_problems(sm_plan_id, stage_agenda[current_stage_code-1][2][0][1], stage_agenda[current_stage_code-1][2][1][1], stage_agenda[current_stage_code-1][2][2][1], app_db_web_location)
        # get assigned juror
        tmp_juror_list = get_mpair_jurors_by_round_room(current_plan_id, None, app_db_web_location)
        current_pair_assigned_jurors = tmp_juror_list[0][1][0][1]
        current_pair_assigned_juror_codes = tmp_juror_list[0][1][0][2]
        # get up to date team members' roles and problems
        reporter_team_members_roles = get_team_member_roles(current_plan_id, stage_agenda[current_stage_code-1][2][0][1], app_db_web_location)
        if reporter_team_members_roles is None or len(reporter_team_members_roles) < 1:
            reporter_team_members_roles = [0]
        opponent_team_members_roles = get_team_member_roles(current_plan_id, stage_agenda[current_stage_code-1][2][1][1], app_db_web_location)
        if opponent_team_members_roles is None or len(opponent_team_members_roles) < 1:
            opponent_team_members_roles = [0]
        reviewer_team_members_roles = get_team_member_roles(current_plan_id, stage_agenda[current_stage_code-1][2][2][1], app_db_web_location)
        if reviewer_team_members_roles is None or len(reviewer_team_members_roles) < 1:
            reviewer_team_members_roles = [0]

        # re-arrange current_pair_team_problems
        for team in current_pair_team_problems:
            tmp_problem_code_list = []
            for i in range(10):
                tmp_problem_code = i + 1
                has_matched_problem = False
                tmp_problme_list = []
                for item in team[1]:
                    if item[0] == tmp_problem_code:
                        tmp_problme_list.append(item[1])
                        has_matched_problem = True
                if has_matched_problem:
                    tmp_problem_code_list.append((tmp_problem_code, tmp_problme_list))
                else:
                    tmp_problem_code_list.append((tmp_problem_code, None))
            team_problems.append((team[0], tmp_problem_code_list))

        problem_label_codes = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")

    return render_template('main/fm_select.html', form=form, current_room_code=current_room_code, master_mrooms=master_mrooms,
                           fm_current_room_round_pairs=fm_current_room_round_pairs, master_mteams=master_mteams,
                           reviewer_team_members_roles=reviewer_team_members_roles[0], master_problems=master_problems,
                           reporter_team_members_roles=reporter_team_members_roles[0], opponent_team_members_roles=opponent_team_members_roles[0],
                           plan_id=current_plan_id, current_stage_code=current_stage_code, master_mjurors=master_mjurors,
                           current_stage_agenda=stage_agenda[current_stage_code-1], current_pair_assigned_jurors=current_pair_assigned_jurors,
                           current_pair_assigned_juror_codes=current_pair_assigned_juror_codes)


@main_blueprint.route('/fm_timing', methods=['GET', 'POST'])
@roles_required('data')  # Limits access to users with the 'data' role
def fm_timing():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    current_user_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = EventStageForm(request.form)

    # Initialize parameters from request and session
    master_mteams = None
    master_mrooms = None
    master_mjurors = None

    current_stage_agenda = None
    sm_current_room_round_pairs = None
    fm_reporter_problem = None

    current_room_code = 0
    current_round_code = 0
    current_stage_code = 0
    current_pair_id = 0
    current_plan_id = 0

    step_number = 0
    sm_steps = None
    reporter_problems_rejected = None

    try:
        # get master table from session
        master_mteams = session['master_mteams']
        master_mrooms = session['master_mrooms']
        master_mjurors = session['master_mjurors']
        current_stage_agenda = session['current_stage_agenda']
        sm_current_room_round_pairs = session['fm_current_room_round_pairs']
        fm_reporter_problem = session['fm_reporter_problem']
        tmp_current_codes = session['current_codes']
        current_room_code = tmp_current_codes[0]
        current_round_code = tmp_current_codes[1]
        current_stage_code = tmp_current_codes[2]
        current_pair_id = tmp_current_codes[3]
        current_plan_id = tmp_current_codes[4]
    except:
        flash_msg = "Invalid access to get session!"
        flash(flash_msg, 'error')
        return redirect(url_for('main.fm_draw'))

    # get the performance order in one stage of a selective match
    fm_steps = get_fm_performance_order()
    if request.method == 'POST':
        # Process valid POST
        pass
    else:
        # Process valid GET
        # get parameters from request
        step_str = request.args.get("step")
        step_number = 1
        if step_str is not None and len(step_str) > 0:
            step_number = int(step_str)
        # skip first two steps for final match
        if step_number < 3:
            step_number = 3

        # ensure there is one problem is accepted
        problem_accepted = True
        if step_number > len(fm_steps):
            # completed all the steps, update mpair stage status to 12 or 22, but not enter the score yet
            mpair_stage_status_code = 0
            if current_stage_code == 1:
                mpair_stage_status_code = 12
            elif current_stage_code == 2:
                mpair_stage_status_code = 22
            elif current_stage_code == 3:
                mpair_stage_status_code = 32
            update_mpair_stage_status(current_plan_id, current_pair_id, mpair_stage_status_code, current_user_id, app_db_web_location)
            return redirect(url_for('main.fm_scoring'))

    return render_template('main/fm_timing.html', form=form, current_room_code=current_room_code, master_mrooms=master_mrooms,
                           sm_current_room_round_pairs=sm_current_room_round_pairs, master_mteams=master_mteams,
                           plan_id=current_plan_id, current_stage_code=current_stage_code, master_mjurors=master_mjurors,
                           current_stage_agenda=current_stage_agenda, fm_reporter_problem=fm_reporter_problem,
                           step_number=step_number, fm_steps=fm_steps, total_steps=len(fm_steps))


@main_blueprint.route('/fm_scoring', methods=['GET', 'POST'])
@roles_required('data')  # Limits access to users with the 'data' role
def fm_scoring():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    current_user_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = EventStageForm(request.form)

    # Initialize parameters from request and session
    master_mteams = None
    master_mrooms = None
    master_mjurors = None

    current_stage_agenda = None
    fm_current_room_round_pairs = None
    fm_reporter_problem = None

    current_room_code = 0
    current_round_code = 0
    current_stage_code = 0
    current_pair_id = 0
    current_plan_id = 0

    current_stage_jurors = None

    try:
        # get master table from session
        master_mteams = session['master_mteams']
        master_mrooms = session['master_mrooms']
        master_mjurors = session['master_mjurors']
        current_stage_agenda = session['current_stage_agenda']
        sm_current_room_round_pairs = session['fm_current_room_round_pairs']
        tmp_current_codes = session['current_codes']
        current_room_code = tmp_current_codes[0]
        current_round_code = tmp_current_codes[1]
        current_stage_code = tmp_current_codes[2]
        current_pair_id = tmp_current_codes[3]
        current_plan_id = tmp_current_codes[4]
        fm_reporter_problem = session['fm_reporter_problem']
    except:
        flash_msg = "Invalid access to enter scores!"
        flash(flash_msg, 'error')
        return redirect(url_for('main.fm_draw'))

    if request.method == 'POST':
        # Process valid POST
        # get parameters from form
        stage_scores = list()
        stage_score_keys = list()
        data_received = request.form
        for key in data_received:
            stage_score_keys.append(key)
        sorted_keys = sorted(stage_score_keys)
        for key in sorted_keys:
            if key.startswith("j_"):
                #print ('form key '+key+" "+ data_received[key])
                stage_scores.append((key, data_received[key]))

        # get sm plan id for volunteer
        sm_active_pan_list = search_event_plan(event_id, "Active", 1, app_db_web_location)
        sm_plan_id = 0
        for plan in sm_active_pan_list:
            sm_plan_id = plan[1]
            break

        # insert data to DSTAGE_SCORE
        save_fm_stage_scores(current_plan_id, sm_plan_id, current_pair_id, stage_scores, current_stage_agenda, current_stage_code,
                          current_room_code, current_user_id, app_db_web_location)

        # clear session for stage specific values
        #session.pop('current_stage_problems')
        session.pop('fm_reporter_problem')
        session.pop('current_stage_agenda')
        session.pop('fm_current_room_round_pairs')
        session.pop('current_codes')
        return redirect(url_for('main.fm_draw'))
    else:
        # Process valid GET
        # get up to date jurors on board
        current_stage_jurors = get_stage_jurors(current_plan_id, current_pair_id, current_stage_code, app_db_web_location)

    return render_template('main/fm_scoring.html', form=form, current_room_code=current_room_code, master_mrooms=master_mrooms,
                           sm_current_room_round_pairs=sm_current_room_round_pairs, master_mteams=master_mteams,
                           plan_id=current_plan_id, current_stage_code=current_stage_code, master_mjurors=master_mjurors,
                           current_stage_agenda=current_stage_agenda, fm_reporter_problem=fm_reporter_problem,
                           current_jury=current_stage_jurors)


@main_blueprint.route('/sm_problem', methods=['GET', 'POST'])
@roles_required('admin', 'super')  # Limits access to users with the 'admin' role and 'super' role
def sm_problem():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']

    current_user_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = EventPlanForm(request.form)
    flash_msg = None
    team_problems = list()
    sm_round_code = 0
    sm_room_code = 0
    selected_pair_codes = list()
    current_mpair_id = 0
    problem_guide = None

    # get plan from database
    plan_status = "Active"
    sm_plan_id = 0
    sm_plan_sub_status = 0
    active_sm_plan_list = search_event_plan(event_id, plan_status, 1, app_db_web_location)
    if active_sm_plan_list is not None and len(active_sm_plan_list) > 0:
        # plan has already been activated, changes to the plan are NOT allowed
        for plan in active_sm_plan_list:
            sm_plan_id = plan[1]
            sm_plan_sub_status = plan[4]  # 1-released 2-published
            break

        if sm_plan_sub_status > 0:
            if request.method == 'POST':
                current_mpair_id = int(request.form.get('current_mpair_id'))
                problem_guide = request.form.get('proble_guide')
                add_problem_guide(sm_plan_id, current_mpair_id, problem_guide, current_user_id, app_db_web_location)
                flash_msg = "Problem guide has been added successfully!"
                flash(flash_msg, 'success')

            sm_team_problems = get_all_reporter_problems(sm_plan_id, app_db_web_location)
            # (mteam_code, mteam_name, team_info, team_member_list)
            master_mteams = get_mteams(sm_plan_id, app_db_web_location)
            # re-arrange current_pair_team_problems
            if sm_team_problems is not None:
                for team in sm_team_problems:
                    tmp_problem_code_list = []
                    for i in range(10):
                        tmp_problem_code = i + 1
                        has_matched_problem = False
                        tmp_problme_list = []
                        for item in team[1]:
                            if item[0] == tmp_problem_code:
                                tmp_problme_list.append(item[1])
                                has_matched_problem = True
                        if has_matched_problem:
                            tmp_problem_code_list.append((tmp_problem_code, tmp_problme_list))
                        else:
                            tmp_problem_code_list.append((tmp_problem_code, None))
                    team_problems.append((team[0], tmp_problem_code_list))

            problem_label_codes = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")

            # get sm schedule
            sm_round_schedule = get_schedue_by_round_room(sm_plan_id, app_db_web_location)
            # (mroom_code, mroom_label, mroom_info)
            master_mrooms = get_mrooms(sm_plan_id, app_db_web_location)

            try:
                sm_round_code = int(request.args.get("sm_round"))
                sm_room_code = int(request.args.get("sm_room"))
                current_mpair_id = sm_round_schedule[sm_round_code-1][1][sm_room_code-1][3]
                problem_guide = sm_round_schedule[sm_round_code-1][1][sm_room_code-1][4]
                for team in sm_round_schedule[sm_round_code-1][1][sm_room_code-1][1]:
                    selected_pair_codes.append(team[4])
            except:
                selected_pair_codes = None
                sm_round_code = 0

            return render_template('main/sm_problem.html', form=form, sm_plan_id=sm_plan_id, plan_status=plan_status,
                                   team_problems=team_problems, problem_label_codes=problem_label_codes,
                                   master_mteams=master_mteams, master_mrooms=master_mrooms, sm_round_code=sm_round_code,
                                   round_schedule=sm_round_schedule, selected_pair_codes=selected_pair_codes,
                                   current_mpair_id=current_mpair_id, problem_guide=problem_guide, sm_room_code=sm_room_code)
        else:
            flash_msg = "Selective Plan is not released yet!"
    else:
        # plan has not been finalized, can view, re-plan or manual change the plan
        flash_msg = "Selective Plan is not activiated yet!"
    flash(flash_msg, 'error')
    return redirect(url_for('main.admin_mgmt'))


# validate score and calculate the total
@main_blueprint.route('/fm_validate', methods=['GET', 'POST'])
@roles_required('super')  # Limits access to users with the 'super' role
def fm_validate():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    current_user_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = EventStageForm(request.form)
    fm_current_pair_scores = None

    # Initialize parameters from request and session
    current_room_code = 0
    current_round_code = 6
    current_plan_id = 0
    current_plan_sub_status = 0
    sm_plan_id = 0
    fm_current_room_round_pairs = None
    current_pair_stage_status = 0
    master_mteams = None
    master_mrooms = None
    master_mjurors = None
    current_stage_code = 0
    stage_agenda = None
    current_pair_assigned_jurors = None
    current_pair_assigned_juror_codes = None
    current_pair_id = 0
    opponent_team_members_roles = None
    reporter_team_members_roles = None
    current_team_codes = None
    current_team_codes_SP = None
    current_stage_problems = None
    current_dstage_score_id = 0
    current_mpair_id = 0

    # initial parameters
    try:
        current_plan_id = int(request.args.get('fm_plan_id'))
        sm_plan_id = int(request.args.get('sm_plan_id'))
        current_plan_sub_status = int(request.args.get('plan_sub_status'))
    except:
        flash_msg = "Invalid access to validate final match score!"
        flash(flash_msg, 'error')
        return redirect(url_for('main.fm_draw'))

    try:
        # get master table from session
        master_mteams = session['master_mteams']
        master_mrooms = session['master_mrooms']
        master_mjurors = session['master_mjurors']
    except:
        # (mroom_code, mroom_label, mroom_info)
        master_mrooms = get_mrooms(sm_plan_id, app_db_web_location)
        # (mteam_code, mteam_name, team_info, team_member_list)
        master_mteams = get_mteams(sm_plan_id, app_db_web_location)
        # (mjuror_code, mjuror_name, mjuror_info, has_cois, juror_cois_list)
        master_mjurors = get_mjurors(sm_plan_id, app_db_web_location)
        # (mroom_code, mroom_label, room_volunteers)

    try:
        current_dstage_score_id = int(request.args.get('dss'))
    except:
        current_dstage_score_id = 0

    if request.method == 'POST':
        # Process valid POST
        # check if the scoresheet is confirmed
        scoresheet_validate = request.form.get('validate')
        if scoresheet_validate is not None:
            if scoresheet_validate == "correct":
                # get calculated values
                #2_opp_dstage_team_P 2_rep_dstage_team_P 2_opp_dstage_team_AP 2_opp_dstage_team_id 2_rep_dstage_team_AP 2_rep_dstage_team_id
                #1_opp_dstage_team_P 1_rep_dstage_team_P 1_opp_dstage_team_AP 1_opp_dstage_team_id 1_rep_dstage_team_AP 1_rep_dstage_team_id
                #ds_fw_mteam_code ds_fw_mteam_code_SP ds_fl_mteam_code ds_fl_mteam_code_SP
                try:
                    current_mpair_id = int(request.form.get('current_mpair_id'))

                    ds3_opp_dstage_team_P = float(request.form.get("3_opp_dstage_team_P"))
                    ds3_rep_dstage_team_P = float(request.form.get("3_rep_dstage_team_P"))
                    ds3_rev_dstage_team_P = float(request.form.get("3_rev_dstage_team_P"))
                    ds3_opp_dstage_team_AP = float(request.form.get("3_opp_dstage_team_AP"))
                    ds3_opp_dstage_team_id = int(request.form.get("3_opp_dstage_team_id"))
                    ds3_rep_dstage_team_AP = float(request.form.get("3_rep_dstage_team_AP"))
                    ds3_rep_dstage_team_id = int(request.form.get("3_rep_dstage_team_id"))
                    ds3_rev_dstage_team_AP = float(request.form.get("3_rev_dstage_team_AP"))
                    ds3_rev_dstage_team_id = int(request.form.get("3_rev_dstage_team_id"))

                    ds2_opp_dstage_team_P = float(request.form.get("2_opp_dstage_team_P"))
                    ds2_rep_dstage_team_P = float(request.form.get("2_rep_dstage_team_P"))
                    ds2_rev_dstage_team_P = float(request.form.get("2_rev_dstage_team_P"))
                    ds2_opp_dstage_team_AP = float(request.form.get("2_opp_dstage_team_AP"))
                    ds2_opp_dstage_team_id = int(request.form.get("2_opp_dstage_team_id"))
                    ds2_rep_dstage_team_AP = float(request.form.get("2_rep_dstage_team_AP"))
                    ds2_rep_dstage_team_id = int(request.form.get("2_rep_dstage_team_id"))
                    ds2_rev_dstage_team_AP = float(request.form.get("2_rev_dstage_team_AP"))
                    ds2_rev_dstage_team_id = int(request.form.get("2_rev_dstage_team_id"))

                    ds1_opp_dstage_team_P = float(request.form.get("1_opp_dstage_team_P"))
                    ds1_rep_dstage_team_P = float(request.form.get("1_rep_dstage_team_P"))
                    ds1_rev_dstage_team_P = float(request.form.get("1_rev_dstage_team_P"))
                    ds1_opp_dstage_team_AP = float(request.form.get("1_opp_dstage_team_AP"))
                    ds1_opp_dstage_team_id = int(request.form.get("1_opp_dstage_team_id"))
                    ds1_rep_dstage_team_AP = float(request.form.get("1_rep_dstage_team_AP"))
                    ds1_rep_dstage_team_id = int(request.form.get("1_rep_dstage_team_id"))
                    ds1_rev_dstage_team_AP = float(request.form.get("1_rev_dstage_team_AP"))
                    ds1_rev_dstage_team_id = int(request.form.get("1_rev_dstage_team_id"))

                    ds_f1_mteam_code = int(request.form.get("ds_f1_mteam_code"))
                    ds_f1_mteam_code_SP = float(request.form.get("ds_f1_mteam_code_SP"))
                    ds_f1_mteam_code_fw = int(request.form.get("ds_f1_mteam_code_fw"))
                    ds_f2_mteam_code = int(request.form.get("ds_f2_mteam_code"))
                    ds_f2_mteam_code_SP = float(request.form.get("ds_f2_mteam_code_SP"))
                    ds_f2_mteam_code_fw = int(request.form.get("ds_f2_mteam_code_fw"))
                    ds_f3_mteam_code = int(request.form.get("ds_f3_mteam_code"))
                    ds_f3_mteam_code_SP = float(request.form.get("ds_f3_mteam_code_SP"))
                    ds_f3_mteam_code_fw = int(request.form.get("ds_f3_mteam_code_fw"))

                    # update three mpair_teams of the current mpair_id: SP and FW=1 or 0
                    # winner is the ranking #1 including tie scenario
                    # use mteam_code and mpair_id to find mpair_team_id (PK)
                    mpair_team_records = [
                        (ds_f1_mteam_code, ds_f1_mteam_code_SP, ds_f1_mteam_code_fw),
                        (ds_f2_mteam_code, ds_f2_mteam_code_SP, ds_f2_mteam_code_fw),
                        (ds_f3_mteam_code, ds_f3_mteam_code_SP, ds_f3_mteam_code_fw)
                    ]
                    # update four dstage_teams of the current mpair_id: Average Point, Point (POINT_WITH_FACTOR)
                    # stage 1: rep and opp, stage 2: rep and opp
                    dstage_team_records = [
                        (ds1_rep_dstage_team_id, ds1_rep_dstage_team_AP, ds1_rep_dstage_team_P),
                        (ds1_opp_dstage_team_id, ds1_opp_dstage_team_AP, ds1_opp_dstage_team_P),
                        (ds1_rev_dstage_team_id, ds1_rev_dstage_team_AP, ds1_rev_dstage_team_P),
                        (ds2_rep_dstage_team_id, ds2_rep_dstage_team_AP, ds2_rep_dstage_team_P),
                        (ds2_opp_dstage_team_id, ds2_opp_dstage_team_AP, ds2_opp_dstage_team_P),
                        (ds2_rev_dstage_team_id, ds2_rev_dstage_team_AP, ds2_rev_dstage_team_P),
                        (ds3_rep_dstage_team_id, ds3_rep_dstage_team_AP, ds3_rep_dstage_team_P),
                        (ds3_opp_dstage_team_id, ds3_opp_dstage_team_AP, ds3_opp_dstage_team_P),
                        (ds3_rev_dstage_team_id, ds3_rev_dstage_team_AP, ds3_rev_dstage_team_P)
                    ]

                    validate_dstage_score(current_plan_id, current_mpair_id, mpair_team_records, dstage_team_records, current_user_id,
                                          app_db_web_location)

                    flash_msg = "Final match Scoresheet has been confirmed successfully!"
                    flash(flash_msg, 'success')
                    return redirect(url_for('main.admin_publish'))
                except:
                    flash_msg = "Scoresheet was not confirmed properly, please double check!"
                    flash(flash_msg, 'error')
                    return redirect(url_for('main.admin_publish'))
            else:
                flash_msg = "Scoresheet was not confirmed, please double check!"
                flash(flash_msg, 'error')
                return redirect(url_for('main.admin_publish'))
        else:
            try:
                dstage_score_id = int(request.form.get('ds_sc_id'))
                ds_sc_1 = float(request.form.get('ds_sc_1'))
                ds_sc_2 = float(request.form.get('ds_sc_2'))
                ds_sc_3 = float(request.form.get('ds_sc_3'))
                ds_sc_4 = float(request.form.get('ds_sc_4'))
                ds_sc_5 = float(request.form.get('ds_sc_5'))
                ds_sc_6 = float(request.form.get('ds_sc_6'))
                ds_sc_7 = float(request.form.get('ds_sc_7'))
            except:
                flash_msg = "Invalid access in post!"
                flash(flash_msg, 'error')
                return redirect(url_for('main.admin_publish'))

            # update dstage_score by dstage_score_id
            if dstage_score_id > 0:
                dstage_scores = (round(ds_sc_1 + ds_sc_2 + ds_sc_3 + ds_sc_4 + ds_sc_5 + ds_sc_6 + ds_sc_7, 1), ds_sc_1, ds_sc_2, ds_sc_3, ds_sc_4, ds_sc_5, ds_sc_6, ds_sc_7)
                update_dstage_score_by_id(current_plan_id, dstage_score_id, dstage_scores, current_user_id, app_db_web_location)
        current_dstage_score_id = 0
    else:
        # Process valid GET
        pass

    # get up to date mpair fight status
    fm_room_pairs = get_mpairs_by_room_round(current_plan_id, app_db_web_location)
    # (current_room_code, tmp_mroom_label, tmp_round_list)
    fm_current_room_round_pairs = fm_room_pairs[0][2][0]
    current_room_code = fm_room_pairs[0][0]
    current_mpair_id = fm_current_room_round_pairs[3]
    current_pair_stage_status = fm_current_room_round_pairs[2]
    current_team_codes = (fm_current_room_round_pairs[1][0][4], fm_current_room_round_pairs[1][1][4], fm_current_room_round_pairs[1][2][4])

    # get up to date mpair stage problem info
    current_stage_problems = get_mpair_problems_simmple(current_plan_id, current_mpair_id, app_db_web_location)
    # get up to date mpair stage score info
    print("****____current_mpair_id: ", current_mpair_id)
    validation_scores = get_fm_mpair_scores_4validate(current_plan_id, current_mpair_id, current_team_codes, app_db_web_location)
    current_team_codes_SP = validation_scores[1]
    fm_current_pair_scores = validation_scores[0]
    # compare who is the winner
    ranked_team_codes_SP = check_ranking3(current_team_codes_SP)

    return render_template('main/fm_validate.html', form=form, current_room_code=current_room_code, master_mrooms=master_mrooms,
                           current_round_code=current_round_code, master_mteams=master_mteams, current_plan_id=current_plan_id,
                           master_mjurors=master_mjurors, sm_current_pair_scores=fm_current_pair_scores, current_mpair_id=current_mpair_id,
                           current_team_codes_SP=current_team_codes_SP, current_team_codes=current_team_codes, ranked_team_codes_SP=ranked_team_codes_SP,
                           current_stage_problems=current_stage_problems, current_dstage_score_id=current_dstage_score_id,
                           plan_sub_status=current_plan_sub_status, fm_plan_id=current_plan_id, sm_plan_id=sm_plan_id)


# view FM scores
@main_blueprint.route('/fm_score_view', methods=['GET', 'POST'])
@roles_required('super')  # Limits access to users with the 'super' role
def fm_score_view():
    # Retrieve database settings from app.config
    app_db_web_location = current_app.config['SQLALCHEMY_DATABASE_URI_LOCAL']
    current_user_id = current_user.id
    event_id = current_app.config['CURRENT_EVENT']

    # Initialize form
    form = EventStageForm(request.form)
    fm_current_pair_scores = None

    # Initialize parameters from request and session
    current_room_code = 0
    current_round_code = 6
    current_plan_id = 0
    current_plan_sub_status = 0
    sm_plan_id = 0
    fm_current_room_round_pairs = None
    current_pair_stage_status = 0
    master_mteams = None
    master_mrooms = None
    master_mjurors = None
    current_stage_code = 0
    stage_agenda = None
    current_pair_assigned_jurors = None
    current_pair_assigned_juror_codes = None
    current_pair_id = 0
    opponent_team_members_roles = None
    reporter_team_members_roles = None
    current_team_codes = None
    current_team_codes_SP = None
    current_stage_problems = None
    current_dstage_score_id = 0
    current_mpair_id = 0

    # initial parameters
    try:
        current_plan_id = int(request.args.get('fm_plan_id'))
        sm_plan_id = int(request.args.get('sm_plan_id'))
        current_plan_sub_status = int(request.args.get('plan_sub_status'))
    except:
        flash_msg = "Invalid access to validate final match score!"
        flash(flash_msg, 'error')
        return redirect(url_for('main.fm_draw'))

    try:
        # get master table from session
        master_mteams = session['master_mteams']
        master_mrooms = session['master_mrooms']
        master_mjurors = session['master_mjurors']
    except:
        # (mroom_code, mroom_label, mroom_info)
        master_mrooms = get_mrooms(sm_plan_id, app_db_web_location)
        # (mteam_code, mteam_name, team_info, team_member_list)
        master_mteams = get_mteams(sm_plan_id, app_db_web_location)
        # (mjuror_code, mjuror_name, mjuror_info, has_cois, juror_cois_list)
        master_mjurors = get_mjurors(sm_plan_id, app_db_web_location)
        # (mroom_code, mroom_label, room_volunteers)

    # get up to date mpair fight status
    fm_room_pairs = get_mpairs_by_room_round(current_plan_id, app_db_web_location)
    # (current_room_code, tmp_mroom_label, tmp_round_list)
    fm_current_room_round_pairs = fm_room_pairs[0][2][0]
    current_pair_stage_status = fm_current_room_round_pairs[2]
    if current_pair_stage_status > 20:
        current_room_code = fm_room_pairs[0][0]
        current_mpair_id = fm_current_room_round_pairs[3]
        current_team_codes = (fm_current_room_round_pairs[1][0][4], fm_current_room_round_pairs[1][1][4], fm_current_room_round_pairs[1][2][4])

        # get up to date mpair stage problem info
        current_stage_problems = get_mpair_problems_simmple(current_plan_id, current_mpair_id, app_db_web_location)
        # get up to date mpair stage score info
        print("****____current_mpair_id: ", current_mpair_id)
        validation_scores = get_fm_mpair_scores_4validate(current_plan_id, current_mpair_id, current_team_codes, app_db_web_location)
        current_team_codes_SP = validation_scores[1]
        fm_current_pair_scores = validation_scores[0]
        # compare who is the winner
        ranked_team_codes_SP = check_ranking3(current_team_codes_SP)

        return render_template('main/fm_score_view.html', form=form, current_room_code=current_room_code, master_mrooms=master_mrooms,
                               current_round_code=current_round_code, master_mteams=master_mteams, current_plan_id=current_plan_id,
                               master_mjurors=master_mjurors, sm_current_pair_scores=fm_current_pair_scores, current_mpair_id=current_mpair_id,
                               current_team_codes_SP=current_team_codes_SP, current_team_codes=current_team_codes,
                               ranked_team_codes_SP=ranked_team_codes_SP, current_pair_stage_status=current_pair_stage_status,
                               current_stage_problems=current_stage_problems, current_dstage_score_id=current_dstage_score_id,
                               plan_sub_status=current_plan_sub_status, fm_plan_id=current_plan_id, sm_plan_id=sm_plan_id)
    else:
        flash_msg = "FM scores not ready yet!"
        flash(flash_msg, 'error')
        return redirect(url_for('main.admin_publish'))
