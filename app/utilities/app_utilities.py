# untility functions
from random import shuffle
from datetime import datetime, date
import itertools
import secrets


def get_2days_timeslots():
    two_days_timeslots = {
        "1": "Day 1 (Saturday Feb 27th, 2021) 10am - 2pm",
        "2": "Day 1 (Saturday Feb 27th, 2021) 2pm - 6pm",
        "3": "Day 2 (Saturday Mar 6th, 2021) 10am - 3pm",
        "4": "Day 2 (Saturday Mar 6th, 2021) 3pm - 7pm"
    }
    return two_days_timeslots


def count_by_status(team_counts, team_status):
    count_result = 0
    for item in team_counts:
        if item[1].lower() == team_status.lower():
            count_result = item[0]
            break
    return count_result


def check_ranking2(team_score_list):
    i = 0
    refined_team_scores = list()
    min_score = min(team_score_list)
    max_score = max(team_score_list)
    if max_score == min_score:
        # all two are tier, all are ranking #1
        for i in range(2):
            tmp_dict = {
                "original_team_sequence": i + 1,
                "ranking": 1,
                "fw": 1,
                "score": max_score
            }
            refined_team_scores.append(tmp_dict)
    else:
        rank_1_index = team_score_list.index(max_score)
        rank_2_index = team_score_list.index(min_score)
        # add rank #1
        tmp_dict = {
            "original_team_sequence": rank_1_index + 1,
            "ranking": 1,
            "fw": 1,
            "score": max_score
        }
        refined_team_scores.append(tmp_dict)

        # add rank #2
        tmp_dict = {
            "original_team_sequence": rank_2_index + 1,
            "ranking": 2,
            "fw": 0,
            "score": min_score
        }
        refined_team_scores.append(tmp_dict)
    return refined_team_scores


def check_ranking3(team_score_list):
    i = 0
    refined_team_scores = list()
    min_score = min(team_score_list)
    mid_score = 0
    max_score = max(team_score_list)
    if max_score == min_score:
        # all three are tier, all are ranking #1
        for i in range(3):
            tmp_dict = {
                "original_team_sequence": i + 1,
                "ranking": 1,
                "fw": 1,
                "score": max_score
            }
            refined_team_scores.append(tmp_dict)
    else:
        rank_1_index = team_score_list.index(max_score)
        rank_3_index = team_score_list.index(min_score)
        rank_2_index = 0
        for i in range(3):
            if (i+1) != rank_1_index and (i+1) != rank_3_index:
                rank_2_index = i+1
                mid_score = team_score_list[rank_2_index]
                break
        # add rank #1
        tmp_dict = {
            "original_team_sequence": rank_1_index + 1,
            "ranking": 1,
            "fw": 1,
            "score": max_score
        }
        refined_team_scores.append(tmp_dict)

        if mid_score == min_score:
            for i in range(2):
                tmp_dict = {
                    "original_team_sequence": i + 2,
                    "ranking": 2,
                    "fw": 0,
                    "score": mid_score
                }
                refined_team_scores.append(tmp_dict)
        elif mid_score == max_score:
            # add rank #2 -> should be tie with rank #1
            tmp_dict = {
                "original_team_sequence": rank_2_index + 1,
                "ranking": 1,
                "fw": 1,
                "score": mid_score
            }
            refined_team_scores.append(tmp_dict)

            # add rank #3
            tmp_dict = {
                "original_team_sequence": rank_3_index + 1,
                "ranking": 3,
                "fw": 0,
                "score": min_score
            }
            refined_team_scores.append(tmp_dict)
        else:
            # add rank #2
            tmp_dict = {
                "original_team_sequence": rank_2_index + 1,
                "ranking": 2,
                "fw": 0,
                "score": mid_score
            }
            refined_team_scores.append(tmp_dict)

            # add rank #3
            tmp_dict = {
                "original_team_sequence": rank_3_index + 1,
                "ranking": 3,
                "fw": 0,
                "score": min_score
            }
            refined_team_scores.append(tmp_dict)
    return refined_team_scores


def get_sm_performance_order():
    sm_steps = [
        {
            "step_number": 1,
            "step_text": "The Opponent challenges the Reporter for the problem",
            "step_mins": 1,
            "reporter": "off",
            "opponent": "on"
        },
        {
            "step_number": 2,
            "step_text": "The Reporter accepts or rejects the challenge",
            "step_mins": 1,
            "reporter": "on",
            "opponent": "off"
        },
        {
            "step_number": 3,
            "step_text": "Preparation of the Reporter",
            "step_mins": 5,
            "reporter": "on",
            "opponent": "off"
        },
        {
            "step_number": 4,
            "step_text": "Presentation of the Reporter",
            "step_mins": 12,
            "reporter": "on",
            "opponent": "off"
        },
        {
            "step_number": 5,
            "step_text": "Questions of the Opponent to the Reporter and answers of the Reporter",
            "step_mins": 2,
            "reporter": "on",
            "opponent": "on"
        },
        {
            "step_number": 6,
            "step_text": "Preparation of the Opponent",
            "step_mins": 3,
            "reporter": "off",
            "opponent": "on"
        },
        {
            "step_number": 7,
            "step_text": "The Opponent takes the floor (maximum 4 min)",
            "step_mins": 4,
            "reporter": "off",
            "opponent": "on"
        },
        {
            "step_number": 8,
            "step_text": "Discussion between the Reporter and the Opponent",
            "step_mins": 14,
            "reporter": "on",
            "opponent": "on"
        },
        {
            "step_number": 9,
            "step_text": "The Opponent summarizes the discussion",
            "step_mins": 1,
            "reporter": "off",
            "opponent": "on"
        },
        {
            "step_number": 10,
            "step_text": "Concluding remarks of the Reporter",
            "step_mins": 2,
            "reporter": "on",
            "opponent": "off"
        },
        {
            "step_number": 11,
            "step_text": "Questions of the Jury",
            "step_mins": 5,
            "reporter": "on",
            "opponent": "on"
        }
    ]
    return sm_steps


def get_fm_performance_order():
    fm_steps = [
        {
            "step_number": 1,
            "step_text": "The Opponent challenges the Reporter for the problem",
            "step_mins": 1,
            "reporter": "off",
            "opponent": "on",
            "reviewer": "off"
        },
        {
            "step_number": 2,
            "step_text": "The Reporter accepts or rejects the challenge",
            "step_mins": 1,
            "reporter": "on",
            "opponent": "off",
            "reviewer": "off"
        },
        {
            "step_number": 3,
            "step_text": "Preparation of the Reporter",
            "step_mins": 5,
            "reporter": "on",
            "opponent": "off",
            "reviewer": "off"
        },
        {
            "step_number": 4,
            "step_text": "Presentation of the Reporter",
            "step_mins": 12,
            "reporter": "on",
            "opponent": "off",
            "reviewer": "off"
        },
        {
            "step_number": 5,
            "step_text": "Questions of the Opponent to the Reporter and answers of the Reporter",
            "step_mins": 2,
            "reporter": "on",
            "opponent": "on",
            "reviewer": "off"
        },
        {
            "step_number": 6,
            "step_text": "Preparation of the Opponent",
            "step_mins": 3,
            "reporter": "off",
            "opponent": "on",
            "reviewer": "off"
        },
        {
            "step_number": 7,
            "step_text": "The Opponent takes the floor (maximum 4 min)",
            "step_mins": 4,
            "reporter": "off",
            "opponent": "on",
            "reviewer": "off"
        },
        {
            "step_number": 8,
            "step_text": "Discussion between the Reporter and the Opponent",
            "step_mins": 14,
            "reporter": "on",
            "opponent": "on",
            "reviewer": "off"
        },
        {
            "step_number": 9,
            "step_text": "The Opponent summarizes the discussion",
            "step_mins": 1,
            "reporter": "off",
            "opponent": "on",
            "reviewer": "off"
        },
        {
            "step_number": 10,
            "step_text": "Concluding remarks of the Reporter",
            "step_mins": 2,
            "reporter": "on",
            "opponent": "off",
            "reviewer": "off"
        },
        {
            "step_number": 11,
            "step_text": "Questions of the Reviewer to the Reporter and the Opponent and answers to the questions",
            "step_mins": 3,
            "reporter": "on",
            "opponent": "on",
            "reviewer": "on"
        },
        {
            "step_number": 12,
            "step_text": "Preparation of the Reviewer",
            "step_mins": 2,
            "reporter": "off",
            "opponent": "off",
            "reviewer": "on"
        },
        {
            "step_number": 13,
            "step_text": "The Reviewer takes the floor",
            "step_mins": 4,
            "reporter": "off",
            "opponent": "off",
            "reviewer": "on"
        },
        {
            "step_number": 14,
            "step_text": "Concluding remarks of the Reporter",
            "step_mins": 2,
            "reporter": "on",
            "opponent": "off",
            "reviewer": "off"
        },
        {
            "step_number": 15,
            "step_text": "Questions of the Jury",
            "step_mins": 5,
            "reporter": "on",
            "opponent": "on",
            "reviewer": "on"
        }
    ]
    return fm_steps


def convert_background_text(background_code):
    background_choices = [('10', 'Middle School'), ('12', 'High School'), ('20', 'Under Graduate or above')]
    background_text = None
    for item in background_choices:
        if item[0] == background_code:
            background_text = item[1]
            break
    return background_text


def calculate_age_from_datetime(dob_datetime):
    days_in_year = 365.25
    today = datetime.now()
    age = float((today - dob_datetime).days / days_in_year)
    return age


def calculate_age_from_string(dob_string):
    days_in_year = 365.25
    today = date.today()
    dob_date = datetime.strptime(dob_string, "%Y-%m-%d").date()
    age = float((today - dob_date).days / days_in_year)
    return age


"""
# this function is to randomly matching two teams for each round
# the rules are:
# - each team should not meet the same team more than once
# - each pair has two teams (this doesn't work for the final round)
# - each team has assigned team code from 1 to N (N=total number of teams)
# - after this team matching function, the system will assign real team to each team code randomly in another function
# the return type of this function is a list of team_matches
# each element in the team_matches is a dictionary initiated as following:
        {
            "team_code": index + 1,
            "opponents": [], # paired team for each round
            "team_name": 'unassigned',
            "team_id": 0,
            "school_id": 0,
            "school_name": '',
            "room_codes": [] # assigned room code for each round
        }
"""
def team_matching_2(team_count, round_count):
    # fixed number of teams in each pair
    num_in_each_pair = 2  # set the number of teams in each pair
    # initial team list
    team_list_original = []
    for i in range(team_count):
        team_list_original.append(i + 1)

    # initial team matches for each round
    team_matches = []
    for i in range(team_count):
        tmp_dict = {
            "team_code": i + 1,
            "opponents": [],
            "team_name": 'unassigned',
            "team_id": 0,
            "school_id": 0,
            "school_name": '',
            "room_codes": []
        }
        team_matches.append(tmp_dict)

    # start loop for all rounds
    warning_max_try = 3000 * team_count * round_count
    warning_try = 0
    secure_random = secrets.SystemRandom()  # creates a secure random object.
    accepted_pairs = []
    accepted_pairs_by_round = []
    for round in range(round_count):
        warning_try += 1
        if warning_try > warning_max_try:
            return None
        # initialize at the beginning of each round
        tmp_selected_pairs = []
        # initial team list for current round
        tmp_team_list = []
        for i in range(team_count):
            tmp_team_list.append(i + 1)
        # loop at current round
        while tmp_team_list is not None and len(tmp_team_list) > 0:
            warning_try += 1
            if warning_try > warning_max_try:
                return None
            # randomly select one pair
            tmp_random_pair = secure_random.sample(tmp_team_list, num_in_each_pair)
            tmp_random_pair_accepted = True
            # get all the possible combinations of the tmp_random_pair
            tmp_iter_result = itertools.permutations(tmp_random_pair)
            for each in tmp_iter_result:
                warning_try += 1
                if warning_try > warning_max_try:
                    return None
                if each in accepted_pairs or each in tmp_selected_pairs:
                    tmp_random_pair_accepted = False
                    break
                else:
                    tmp_selected_pairs.append(each)

            if tmp_random_pair_accepted:
                for item in tmp_random_pair:
                    # remove form tmp team list of the current round
                    tmp_team_list.remove(item)
            else:
                # initial team list
                tmp_team_list = []
                for i in range(team_count):
                    tmp_team_list.append(i + 1)
                tmp_selected_pairs = []

        # add current round selected pairs to accepted pairs
        accepted_pairs_by_round.append(tmp_selected_pairs)
        for pair in tmp_selected_pairs:
            accepted_pairs.append(pair)

        # add current round selected to team matches
        for pair in tmp_selected_pairs:
            team_matches[pair[0] - 1]["opponents"].append(pair[1])

    return team_matches


"""
# this function is to assign the team code to the real team randomly
# rules:
# - get all the teams for the event
# - if the total team number is bigger than the real total, then use vacancy to replace the remaining
# the return type of this function is a list of teams
# Each team in the list is initiated as following:
# tmp_tuple = (team[2], team[3], team[5], team[6]) # team_id, team_name, team_school_id, team_school_name
"""
def assign_team_code_randomly(current_event_teams, teams_total_number):
    # random generate team sequence
    current_event_teams_name = list()
    for team in current_event_teams:
        # team_name = team[3]
        tmp_tuple = (team[2], team[3], team[5], team[6])
        current_event_teams_name.append(tmp_tuple)
    current_event_teams_number = len(current_event_teams_name)
    if current_event_teams_number < teams_total_number:
        i = current_event_teams_number
        while i < teams_total_number:
            i = i+1
            tmp_tuple_vacancy = (0, "Vacancy", 0, "Unknown")
            current_event_teams_name.append(tmp_tuple_vacancy) # originally append "Vacancy"
    shuffle(current_event_teams_name)
    current_teams_number_assignment = list()
    i = 0
    for team in current_event_teams_name:
        i = i+1
        tmp_tuple_team = (i, team)
        current_teams_number_assignment.append(tmp_tuple_team)
    return current_teams_number_assignment


"""
# this function is to assign the team code to the real team randomly
# rules:
# - get all the teams for the event
# - if the total team number is bigger than the real total, then use vacancy to replace the remaining
# the return type of this function is a list of teams
# Each team in the list is initiated as following:
# tmp_tuple = (team[2], team[3], team[5], team[6]) # team_id, team_name, team_school_id, team_school_name
"""
def assign_team_code_inorder(current_event_teams, teams_total_number):
    # random generate team sequence
    current_event_teams_name = list()
    for team in current_event_teams:
        # team_name = team[3]
        tmp_tuple = (team[2], team[3], team[5], team[6])
        current_event_teams_name.append(tmp_tuple)
    current_event_teams_number = len(current_event_teams_name)
    if current_event_teams_number < teams_total_number:
        i = current_event_teams_number
        while i < teams_total_number:
            i = i+1
            tmp_tuple_vacancy = (0, "Vacancy", 0, "Unknown")
            current_event_teams_name.append(tmp_tuple_vacancy) # originally append "Vacancy"
    current_teams_number_assignment = list()
    i = 0
    for team in current_event_teams_name:
        i = i+1
        tmp_tuple_team = (i, team)
        current_teams_number_assignment.append(tmp_tuple_team)
    return current_teams_number_assignment


"""
# This function is to randomly assign juror to each room
# rules:
# - Each room has a room code from 1 to N (N = number of team pairs for each round + 1) ideally
# - the total number of rooms N should not be less than the total number of teams / 2
# - the jurors that are available for all the four timeslots will be assigned to each room AS BALANCED AS POSSIBLE
# - the jurors that are available for three timeslots will be assigned to each room evenly but without checking the exact timeslots
# - the jurors that are available for one or two timeslots will be assigned to each room randomly
# - the jurors that are not available at all should not be approved by the administrator
# the return type of this function is a list with two elements: [room_plan, juror_plan]
# - room_plan is a list of rooms, the element in the room is a dictionary that is initiated as the following:
            {
                "room_code": index + 1,
                "jurors": [], # a list of juror codes that assigned to the room
                "room_name": 'unassigned',
                "room_id": 0,
                "room_number": '',
                "room_cois": [], # a list of school ids that includes all the coi schools of all the jurors in the room
                "room_team_matches_codes": [] # a list that includes the pair of the teams for each round, again each team is represented by team_code
                "room_team_matches_school_ids": [],
                "room_telec": '',
                "room_type": '',
                "room_details": ''
            }
# - juror_plan is a list of jurors, the element in the juror is a dictionary that is initiated as the following:
            {
                "juror_code": index + 1,
                "juror_info": juror, # it is a list of juror attributes like ppant_id, cois, is_tl, etc.
                "room_code": 0,
                "room_id": 0,
                "room_number": ''
            }
"""
def assign_room_juror_code_randomly(juror_list, teams_total_number, rooms_for_each_round, rounds_total_number):
    # plan room and juror
    # room_juror_plan = assign_room_juror_code_randomly(juror_list, teams_total_number, rooms_for_each_round)
    juror_count = len(juror_list)
    pair_count_per_round = int(teams_total_number / 2)
    room_count = pair_count_per_round
    if rooms_for_each_round > room_count:
        room_count = rooms_for_each_round
    if juror_list is None or juror_count < room_count:
        return [None, 'A', juror_count]
    else:
        secure_random = secrets.SystemRandom()  # creates a secure random object.
        # initial juror code list
        juror_code_list_original = []
        for j in range(juror_count):
            juror_code_list_original.append(j + 1)
        # initial juror_plan
        juror_plan = []
        i = 0
        for juror in juror_list:
            tmp_dict = {
                "juror_code": i + 1,
                "juror_info": juror,
                "room_code": 0,
                "room_id": 0,
                "room_number": ''
            }
            juror_plan.append(tmp_dict)
            i += 1
        # initial room_plan for each room
        room_plan = []
        for i in range(room_count):
            tmp_dict = {
                "room_code": i + 1,
                "jurors": [],
                "room_name": 'unassigned',
                "room_id": 0,
                "room_number": '',
                "room_cois": [],
                "room_team_matches_codes": [],
                "room_team_matches_school_ids": [],
                "room_telec": '',
                "room_type": '',
                "room_details": ''
            }
            room_plan.append(tmp_dict)
        # split all the juror codes based on the availability
        jurors_available_4slots = list()
        jurors_available_3slots = list()
        jurors_available_2slots = list()
        jurors_available_1slots = list()
        i = 0
        for juror in juror_list:
            i += 1
            if juror[11] == "Yes" and juror[12] == "Yes" and juror[13] == "Yes" and juror[14] == "Yes":
                jurors_available_4slots.append(i)
            elif juror[11] == "Yes" and juror[12] == "Yes" and juror[13] == "Yes":
                jurors_available_3slots.append(i)
            elif juror[11] == "Yes" and juror[12] == "Yes" and juror[14] == "Yes":
                jurors_available_3slots.append(i)
            elif juror[11] == "Yes" and juror[13] == "Yes" and juror[14] == "Yes":
                jurors_available_3slots.append(i)
            elif juror[12] == "Yes" and juror[13] == "Yes" and juror[14] == "Yes":
                jurors_available_3slots.append(i)
            elif juror[11] == "Yes" and juror[12] == "Yes":
                jurors_available_2slots.append(i)
            elif juror[11] == "Yes" and juror[13] == "Yes":
                jurors_available_2slots.append(i)
            elif juror[11] == "Yes" and juror[14] == "Yes":
                jurors_available_2slots.append(i)
            elif juror[12] == "Yes" and juror[13] == "Yes":
                jurors_available_2slots.append(i)
            elif juror[12] == "Yes" and juror[14] == "Yes":
                jurors_available_2slots.append(i)
            elif juror[13] == "Yes" and juror[14] == "Yes":
                jurors_available_2slots.append(i)
            else:
                jurors_available_1slots.append(i)
        if len(jurors_available_4slots) < room_count:
            return [None, 'B', juror_count, len(jurors_available_4slots)]
        else:
            # add first juror to each room
            # randomly select from jurors_available_4slots
            tmp_random_jurors = secure_random.sample(jurors_available_4slots, room_count)
            i = 0
            for juror_code in tmp_random_jurors:
                room_plan[i]['jurors'].append(juror_code)
                i += 1
                jurors_available_4slots.remove(juror_code)
                juror_code_list_original.remove(juror_code)
            while len(jurors_available_4slots) >= room_count:
                # randomly select
                tmp_random_jurors = secure_random.sample(jurors_available_4slots, room_count)
                i = 0
                for juror_code in tmp_random_jurors:
                    room_plan[i]['jurors'].append(juror_code)
                    i += 1
                    jurors_available_4slots.remove(juror_code)
                    juror_code_list_original.remove(juror_code)
            # if jurors_available_4slots has left over
            if len(jurors_available_4slots) > 0:
                missed_4slots_juror_count = room_count - len(jurors_available_4slots)
                # get missed from jurors_available_3slots
                if len(jurors_available_3slots) > missed_4slots_juror_count:
                    # randomly select from jurors_available_3slots
                    tmp_random_jurors = secure_random.sample(jurors_available_3slots, missed_4slots_juror_count)
                    for juror_code in tmp_random_jurors:
                        jurors_available_4slots.append(juror_code)
                        jurors_available_3slots.remove(juror_code)
                    # randomly select from jurors_available_4slots
                    tmp_random_jurors = secure_random.sample(jurors_available_4slots, room_count)
                    i = 0
                    for juror_code in tmp_random_jurors:
                        room_plan[i]['jurors'].append(juror_code)
                        i += 1
                        jurors_available_4slots.remove(juror_code)
                        juror_code_list_original.remove(juror_code)
                else:
                    # give the jurors_available_4slots to jurors_available_3slots
                    for juror_code in jurors_available_4slots:
                        jurors_available_3slots.append(juror_code)

            while len(jurors_available_3slots) >= room_count:
                # randomly select
                tmp_random_jurors = secure_random.sample(jurors_available_3slots, room_count)
                i = 0
                for juror_code in tmp_random_jurors:
                    room_plan[i]['jurors'].append(juror_code)
                    i += 1
                    jurors_available_3slots.remove(juror_code)
                    juror_code_list_original.remove(juror_code)
            # if jurors_available_3slots has left over
            if len(jurors_available_3slots) > 0:
                missed_3slots_juror_count = room_count - len(jurors_available_3slots)
                # get missed from jurors_available_2slots
                if len(jurors_available_2slots) > missed_3slots_juror_count:
                    # randomly select from jurors_available_2slots
                    tmp_random_jurors = secure_random.sample(jurors_available_2slots, missed_3slots_juror_count)
                    for juror_code in tmp_random_jurors:
                        jurors_available_3slots.append(juror_code)
                        jurors_available_2slots.remove(juror_code)
                    # randomly select from jurors_available_3slots
                    tmp_random_jurors = secure_random.sample(jurors_available_3slots, room_count)
                    i = 0
                    for juror_code in tmp_random_jurors:
                        room_plan[i]['jurors'].append(juror_code)
                        i += 1
                        jurors_available_3slots.remove(juror_code)
                        juror_code_list_original.remove(juror_code)
                else:
                    # give the jurors_available_3slots to jurors_available_2slots
                    for juror_code in jurors_available_3slots:
                        jurors_available_2slots.append(juror_code)
            # deal with the rest of the juror codes
            while len(juror_code_list_original) >= room_count:
                # randomly select
                tmp_random_jurors = secure_random.sample(juror_code_list_original, room_count)
                i = 0
                for juror_code in tmp_random_jurors:
                    room_plan[i]['jurors'].append(juror_code)
                    i += 1
                    juror_code_list_original.remove(juror_code)
            # if juror_code_list_original has left over
            if len(juror_code_list_original) > 0:
                while len(juror_code_list_original) < room_count:
                    juror_code_list_original.append(0)
                # randomly select
                tmp_random_jurors = secure_random.sample(juror_code_list_original, room_count)
                i = 0
                for juror_code in tmp_random_jurors:
                    if juror_code > 0:
                        room_plan[i]['jurors'].append(juror_code)
                        juror_code_list_original.remove(juror_code)
                    i += 1

        # end of assigning jurors to rooms
        for room in room_plan:
            # update juror_plan
            for juror_code in room['jurors']:
                juror_plan[juror_code - 1]['room_code'] = room['room_code']
                for coi_school in juror_plan[juror_code -1]['juror_info'][3]:
                    room['room_cois'].append(coi_school[1])
        return [room_plan, juror_plan]

# holds jurors[]: juror_code only, volunteers[]: volunteer_code only, room_sids: all the teams' school id from all rounds
def assign_chair_room(chair_list, rooms_for_each_round):
    # initial room_plan for each room
    room_plan = []
    for i in range(rooms_for_each_round):
        tmp_dict = {
            "room_code": i + 1,
            "jurors": [],
            "room_name": 'unassigned',
            "room_id": 0,
            "room_number": '',
            "room_cois": [],
            "room_team_matches_codes": [],
            "room_team_matches_school_ids": [],
            "room_telec": '',
            "room_type": '',
            "room_details": '',
            "room_sids": [],
            "volunteers": [],
            "is_chair": 'Yes'
        }
        room_plan.append(tmp_dict)

    chair_room_assignment = list()
    for chair in chair_list:
        temp = {
            "juror_code": 0,
            "is_chair": "Yes",
            "juror_info": chair,
            "juror_cois": [],
            "room_code": 0,
            "room_id": 0,
            "room_number": ''
        }

        for coi_school in chair[3]:
            temp['juror_cois'].append(coi_school[1])
        chair_room_assignment.append(temp)
    secure_random = secrets.SystemRandom()  # creates a secure random object.
    temp_chair_room_assignment = secure_random.sample(chair_room_assignment, rooms_for_each_round)
    juror_plan = list()
    i = 0
    for chair in temp_chair_room_assignment:
        i = i + 1
        chair['juror_code'] = i
        chair['room_code'] = i
        # add chair to juror_plan
        juror_plan.append(chair)
        # add juror_code to the assigned room
        room_plan[i - 1]['jurors'].append(i)
        # add juror's cois to the assigned room
        for coi_school in chair['juror_info'][3]:
            room_plan[i - 1]['room_cois'].append(coi_school[1])

    return [juror_plan, room_plan]


"""
# This function is to randomly assign each team pair at each round to each room
# rules:
# - There must not have conflict of interest for each room for each team pair at each round
# - There might be one team assigned to the same room at different round, but this function tried best to
#   minimize the likelyhood, but still can't avoid 100%
# - it is allowed and encourage to have more rooms than the total number of team pairs at each round, which helps to meet the above requirements
# the return type of this function is a list with two elements: [round_plan, room_plan]
# - room_plan is also the input parameter and was initiated in function:
# - round_plan is a list of rounds, the element in the round is a dictionary that is initiated as the following:
        {
            "round_code": index + 1,
            "round_team_matches_code": [], # a list of team pair codes for each round
            "round_team_matches_school_ids": [], # a list of school ids of the team pair for each round
            "round_team_matches_room_codes": [], # a list of room codes for each round
        }
"""
def assign_room_to_team(rounds_total_number, team_plan, teams_total_number , rooms_for_each_round, room_plan):
    # plan round
    # initial each round
    round_plan = []
    for i in range(rounds_total_number):
        tmp_dict = {
            "round_code": i + 1,
            "round_team_matches_code": [],
            "round_team_matches_school_ids": [],
            "round_team_matches_room_codes": []
        }
        round_plan.append(tmp_dict)
    # add team to each round
    for round in round_plan:
        tmp_current_round_code = round['round_code']
        for team in team_plan:
            tmp_team_a = team['team_code']
            tmp_team_b = team['opponents'][tmp_current_round_code - 1]
            tmp_random_pair = [tmp_team_a, tmp_team_b]

            # get all the possible combinations of the team a and team b
            tmp_iter_result = itertools.permutations(tmp_random_pair)
            tmp_random_pair_accepted = False
            for each in tmp_iter_result:
                if each in round['round_team_matches_code']:
                    tmp_random_pair_accepted = False
                    break
                else:
                    tmp_random_pair_accepted = True
            if tmp_random_pair_accepted:
                round['round_team_matches_code'].append((tmp_team_a, tmp_team_b))
                tmp_cois = [team_plan[tmp_team_a - 1]['school_id'], team_plan[tmp_team_b - 1]['school_id']]
                round['round_team_matches_school_ids'].append(tmp_cois)

    # assign room_code to each team_matches of each round in round_plan
    secure_random = secrets.SystemRandom()  # creates a secure random object.
    give_up = False
    retry_round_times = 0
    max_retry_round_times = 10
    show_stopper = False
    max_try_times = 100 * teams_total_number * rooms_for_each_round
    for round in round_plan:
        tmp_try_times = 0
        tmp_random_room_code = 0
        matched_rooms_available = False
        current_round_room_code_assignment = []
        while tmp_try_times < max_try_times:
            tmp_round_team_matches_room_code = []
            tmp_random_room_code = 0
            tmp_try_times += 1
            # initial current_round_room_assignment
            current_round_room_code_assignment = []
            i = 0
            for school_ids_at_team_pair in round['round_team_matches_school_ids']:
                # reset all the original room_codes to matched_rooms
                matched_rooms = []
                for r in range(rooms_for_each_round):
                    if r + 1 not in current_round_room_code_assignment:
                        matched_rooms.append(r + 1)
                # check if there are room(s) fits current team_pair (two school ids)
                matched_rooms_available = False
                for team_school_id in school_ids_at_team_pair:
                    for room in room_plan:
                        if room['room_code'] not in current_round_room_code_assignment:
                            if team_school_id in room['room_cois']:
                                if len(matched_rooms) > 0:
                                    if room['room_code'] in matched_rooms:
                                        matched_rooms.remove(room['room_code'])
                                else:
                                    # no matched room for current team pair
                                    show_stopper = True
                                    break
                    if show_stopper:
                        break
                i += 1
                if not show_stopper and len(matched_rooms) > 0:
                    tmp_random_room_code = secure_random.sample(matched_rooms, 1)
                    selected_room_codes_for_current_pair = []
                    if round['round_code'] > 1:
                        try:
                            for round_done in range(round['round_code'] - 1):
                                tmp_round_done_room_code = round_plan[round_done]['round_team_matches_room_codes'][
                                    i - 1]
                                selected_room_codes_for_current_pair.append(tmp_round_done_room_code)
                            tmp_rooms_for_selection = []
                            for room_code in matched_rooms:
                                if room_code not in selected_room_codes_for_current_pair:
                                    tmp_rooms_for_selection.append(room_code)
                            if len(tmp_rooms_for_selection) > 0:
                                tmp_random_room_code = secure_random.sample(tmp_rooms_for_selection, 1)
                            else:
                                if tmp_try_times == max_try_times:
                                    tmp_random_room_code = secure_random.sample(matched_rooms, 1)
                                else:
                                    show_stopper = True
                                    break
                        except:
                            if tmp_try_times == max_try_times:
                                tmp_random_room_code = secure_random.sample(matched_rooms, 1)
                            else:
                                show_stopper = True
                                break
                    # tmp_round_team_matches_room_code.append(tmp_random_room_code)
                    current_round_room_code_assignment.append(tmp_random_room_code[0])
                else:
                    # can't find matched room for current team_pair
                    # re-do
                    break
            if not show_stopper and len(current_round_room_code_assignment) > 0:
                break
            else:
                current_round_room_code_assignment = []
                if tmp_try_times < max_try_times:
                    show_stopper = False
        if not show_stopper and len(current_round_room_code_assignment) > 0:
            for room_code in current_round_room_code_assignment:
                round['round_team_matches_room_codes'].append(room_code)
        else:
            break
    return [round_plan, room_plan]


"""
# This function is to randomly assign each team pair at each round to each room with chair already assigned
# rules:
# - There must not have conflict of interest for each room for each team pair at each round, including chair
# - There might be one team assigned to the same room at different round, but this function tried best to
#   minimize the likelyhood, but still can't avoid 100%
# - it is not allowed to have more rooms than the total number of team pairs at each round
# the return type of this function is a list with two elements: [round_plan, room_plan]
# - room_plan is also the input parameter and was initiated in function: assign_chair_room
# - round_plan is a list of rounds, the element in the round is a dictionary that is initiated as the following:
        {
            "round_code": index + 1,
            "round_team_matches_code": [], # a list of team pair codes for each round
            "round_team_matches_school_ids": [], # a list of school ids of the team pair for each round
            "round_team_matches_room_codes": [], # a list of room codes for each round
        }
"""
def assign_room_to_team_wt_chair(rounds_total_number, team_plan, teams_total_number, rooms_for_each_round, chairs_room_assignment, max_repeated_rooms, open_last_round):
    juror_plan = chairs_room_assignment[0]
    room_plan = chairs_room_assignment[1]
    # plan round
    # initial each round
    round_plan = []
    for i in range(rounds_total_number):
        tmp_dict = {
            "round_code": i + 1,
            "round_team_matches_code": [],
            "round_team_matches_school_ids": [],
            "round_team_matches_room_codes": []
        }
        round_plan.append(tmp_dict)
    # add team to each round => round_plan
    for round in round_plan:
        tmp_current_round_code = round['round_code']
        for team in team_plan:
            tmp_team_a = team['team_code']
            tmp_team_b = team['opponents'][tmp_current_round_code - 1]
            tmp_random_pair = [tmp_team_a, tmp_team_b]

            # get all the possible combinations of the team a and team b
            tmp_iter_result = itertools.permutations(tmp_random_pair)
            tmp_random_pair_accepted = False
            for each in tmp_iter_result:
                if each in round['round_team_matches_code']:
                    tmp_random_pair_accepted = False
                    break
                else:
                    tmp_random_pair_accepted = True
            if tmp_random_pair_accepted:
                round['round_team_matches_code'].append((tmp_team_a, tmp_team_b))
                tmp_cois = [team_plan[tmp_team_a - 1]['school_id'], team_plan[tmp_team_b - 1]['school_id']]
                round['round_team_matches_school_ids'].append(tmp_cois)

    # assign room_code to each team_matches of each round in round_plan
    secure_random = secrets.SystemRandom()  # creates a secure random object.
    finding_room_tried_times = 0
    finding_room_max_try_times = 10 * teams_total_number * rooms_for_each_round
    finding_room = False
    team_round_room_codes = []
    while finding_room_tried_times < finding_room_max_try_times:
        finding_room_tried_times += 1
        # start of one while loop here
        team_round_room_codes = []
        for team in team_plan:
            tmp_item = [team['team_code'], []]
            team_round_room_codes.append(tmp_item)
        # reset room_code in round_plan to 0
        for round in round_plan:
            round['round_team_matches_room_codes'] = []
        # start to loop in the round_plan
        for round in round_plan:
            current_round_code = round['round_code']
            current_round_tried_times = 0
            current_round_max_try_times = 10
            team_current_round_room_code = []
            for team in team_plan:
                tmp_item2 = [team['team_code'], 0]
                team_current_round_room_code.append(tmp_item2)
            finding_room = False
            while current_round_tried_times < current_round_max_try_times:
                current_round_tried_times += 1
                # find room for current round - start one loop
                current_round_assigned_room_codes = []
                pair_index = -1
                for pair in round['round_team_matches_code']:
                    pair_index += 1
                    # find room for current pair
                    tmp_available_room_codes = []
                    for i in range(rooms_for_each_round):
                        tmp_available_room_codes.append(i + 1)
                    # remove the room has been assigned to other teams at current round
                    for room_code in current_round_assigned_room_codes:
                        tmp_available_room_codes.remove(room_code)
                    current_pair_school_ids = round['round_team_matches_school_ids'][pair_index]
                    # check if there is a room that has not conflict wiht current chair
                    tmp_ok_room_for_current_pair = []
                    for room_code in tmp_available_room_codes:
                        if (current_pair_school_ids[0] not in room_plan[room_code-1]['room_cois']) and (current_pair_school_ids[1] not in room_plan[room_code-1]['room_cois']):
                            # this room is ok for current pair so far, continue to look at next room
                            tmp_ok_room_for_current_pair.append(room_code)
                            #tmp_available_room_codes.remove(room['room_code'])
                        else:
                            # has conflict with the room, look for next available room
                            pass
                    # check current pair finding room results
                    if len(tmp_ok_room_for_current_pair) > 0:
                        # there are room(s) at current round is not conflict with current pair
                        # continue to check if the teams in the current pair have been the ok room(s) in previous round, if yes, remove it
                        if current_round_code > (rounds_total_number - max_repeated_rooms) or pair_index > (teams_total_number/2 -open_last_round):
                            # too hard to find not-repeated room, give up
                            pass
                        else:
                            # check current pair - 1st team's previous assigned rooms
                            for room_code in team_round_room_codes[pair[0]-1][1]:  #team_round_room_codes[i][1]
                                if room_code in tmp_ok_room_for_current_pair:
                                    tmp_ok_room_for_current_pair.remove(room_code)
                            for room_code in team_round_room_codes[pair[1]-1][1]:
                                if room_code in tmp_ok_room_for_current_pair:
                                    tmp_ok_room_for_current_pair.remove(room_code)
                        # end of check, select one of room for current pair current round if success otherwise re-do this round
                        if len(tmp_ok_room_for_current_pair) > 0:
                            # final good ending for current pair
                            #current_round_tried_times += 1
                            finding_room = True
                            # found room for current pair, randomly select one to the the current pair
                            tmp_random_pair_room_code = secure_random.sample(tmp_ok_room_for_current_pair, 1)
                            current_pair_room_code = 0
                            for item in tmp_random_pair_room_code:
                                current_pair_room_code = item
                                current_round_assigned_room_codes.append(current_pair_room_code)
                                team_current_round_room_code[pair[0]-1][1]=current_pair_room_code
                                team_current_round_room_code[pair[1]-1][1]=current_pair_room_code
                                break
                        else:
                            # can't find room for current pair, this round is failed, re-do this round
                            finding_room = False
                            break
                    else:
                        # there is NOT room at current round is not conflict with current pair
                        # current round failed, should re-do this round
                        finding_room = False
                        break
                # find room for current round - end one loop
                if finding_room:
                    # final good ending for the current round
                    # add curent round's room assignment to round plan
                    round['round_team_matches_room_codes'] = current_round_assigned_room_codes
                    i = -1
                    for team in team_current_round_room_code:
                        i += 1
                        team_round_room_codes[i][1].append(team[1])
                    break
                else:
                    #current_round_tried_times += 1
                    # failed in this round, continue to try
                    finding_room = False

            if finding_room:
                # continue next round
                pass
            else:
                # current round is failed, stop the this while loop, try another while loop
                break
        # end of one while loop here
        if finding_room:
            break
        else:
            finding_room_tried_times += 1
    return [round_plan, room_plan, finding_room, team_round_room_codes]


"""
# This function is to do final cleanup for the planning
# rules:
# - fill the team pair codes to room_plan
# --- use the team pair codes in the round_plan
# --- the sequence of the team_pair_codes are the number of the teams at each round
# --- use the team_code - 1 as the team index to find the according team record in the team_plan
# --- use append to add data, replace function will cause the mess up
# - fill the room code to each team at each round in the team_plan
# --- the same as above
# - assign real room number to room_code in room_plan
# --- get the list of active PM rooms and randomly select the required number of rooms
# --- if available active PM room is less than required rooms, then add vacancy as placeholder
# --- else: randomly select the required number of active PM rooms
# --- shuffle the selected room list and assign to room_code
"""
def tournament_plan_cleanup(round_plan, room_plan, team_plan, current_event_rooms_usage1):
    # clean the data
    for round in round_plan:
        for i in range(len(round['round_team_matches_code'])):
            tmp_team_pair_codes_me = round['round_team_matches_code'][i]
            tmp_team_pair_school_ids = round['round_team_matches_school_ids'][i]
            tmp_team_pair_room_code = round['round_team_matches_room_codes'][i]
            room_plan[tmp_team_pair_room_code - 1]['room_team_matches_codes'].append(tmp_team_pair_codes_me)
            room_plan[tmp_team_pair_room_code - 1]['room_team_matches_school_ids'].append(tmp_team_pair_school_ids)
            # fill room_sids
            if tmp_team_pair_school_ids[0] not in room_plan[tmp_team_pair_room_code - 1]['room_sids']:
                room_plan[tmp_team_pair_room_code - 1]['room_sids'].append(tmp_team_pair_school_ids[0])
            if tmp_team_pair_school_ids[1] not in room_plan[tmp_team_pair_room_code - 1]['room_sids']:
                room_plan[tmp_team_pair_room_code - 1]['room_sids'].append(tmp_team_pair_school_ids[1])
        # add None to remaining room for the current round
        for room in room_plan:
            if len(room['room_team_matches_codes']) < round['round_code']:
                room['room_team_matches_codes'].append(None)
                room['room_team_matches_school_ids'].append(None)
    for round in round_plan:
        round_code = round['round_code']
        round_index = round_code - 1
        team_pair_index = -1
        for team_pair in round['round_team_matches_code']:
            team_pair_index += 1
            current_room_code = round['round_team_matches_room_codes'][team_pair_index]
            if team_pair is not None:
                current_team_a_code = team_pair[0]
                current_team_b_code = team_pair[1]
                team_plan[current_team_a_code-1]['room_codes'].append(current_room_code)
                team_plan[current_team_b_code - 1]['room_codes'].append(current_room_code)

    # initial event_room_list
    current_event_room_list = []
    secure_random = secrets.SystemRandom()  # creates a secure random object.
    for room in current_event_rooms_usage1:
        current_event_room_list.append(room)

    current_event_rooms_total = len(current_event_room_list)
    current_event_rooms_required = len(room_plan)
    current_event_room_list_usg1 = []
    if current_event_rooms_total < current_event_rooms_required:
        i = current_event_rooms_total
        while i < current_event_rooms_required:
            i = i+1
            current_event_room_list.append(None)
        current_event_room_list_usg1 = current_event_room_list
    else:
        tmp_random_rooms = secure_random.sample(current_event_room_list, current_event_rooms_required)
        for room in tmp_random_rooms:
            current_event_room_list_usg1.append(room)

    shuffle(current_event_room_list_usg1)
    for room in room_plan:
        room_index = room['room_code'] - 1
        if current_event_room_list_usg1[room_index] is not None:
            room['room_number'] = current_event_room_list_usg1[room_index][2]
            room['room_id'] = current_event_room_list_usg1[room_index][0]
            room['room_telec'] = current_event_room_list_usg1[room_index][6]
            room['room_type'] = current_event_room_list_usg1[room_index][8]
            room['room_details'] = current_event_room_list_usg1[room_index][9]
    return [round_plan, room_plan, team_plan]


def assign_volunteer(data_entrier_options, volunteer_list, room_plan):
    # randomly select qualified volunteer and assign to each room for data entry
    room_count = len(room_plan)
    secure_random = secrets.SystemRandom()  # creates a secure random object.
    data_entrier_options_list = list()
    for row in data_entrier_options:
        data_entrier_options_list.append(row)
    tmp_random_data_entriers = secure_random.sample(data_entrier_options_list, room_count)
    volunteer_plan = list()
    volunteer_selected_ppant_id_list = list()
    i = 0
    for data_entrier in tmp_random_data_entriers:
        tmp_dict = {
            "mvolunteer_code": i + 1,
            "cois": [],
            "volunteer_name": data_entrier[5] + " " + data_entrier[6],
            "ppant_id": data_entrier[1],
            "ppant_subtype": 9,
            "timeslots": data_entrier[9] + " " + data_entrier[10] + " " + data_entrier[11] + " " + data_entrier[12],
            "mroom_code": i + 1,
            "data_entry": 'Yes'
        }
        i += 1
        volunteer_selected_ppant_id_list.append(data_entrier[1])
        volunteer_plan.append(tmp_dict)

    # assign the rest of the volunteers to the room that without conflict of interests
    tmp_available_mroom_codes = list()
    current_mvolunteer_code = len(volunteer_plan)
    for volunteer in volunteer_list:
        current_ppant_id = volunteer[0]
        if current_ppant_id not in volunteer_selected_ppant_id_list:
            current_mvolunteer_code += 1
            current_timeslots = volunteer[11] + volunteer[12] + volunteer[13] + volunteer[14]
            current_volunteer_name = volunteer[5]
            current_cois = list()
            if volunteer[1] == 1:
                # add cois
                for coi_school in volunteer[3]:
                    tmp_coi_school_id = coi_school[1]
                    current_cois.append(tmp_coi_school_id)

            # generate the mroom codes for selection
            if tmp_available_mroom_codes is None or len(tmp_available_mroom_codes) < 1:
                tmp_available_mroom_codes = list()
                for i in range(room_count):
                    tmp_available_mroom_codes.append(i + 1)

            # find mroom for current volunteer
            current_mroom_code = 0
            if current_cois is not None and len(current_cois)>0:
                # has cois
                tmp_coi_mroom_codes = list()
                # find the mrooms that has conflict
                for coi_school_id in current_cois:
                    # check the mroom that without conflict of interest with current volunteer
                    for room in room_plan:
                        if coi_school_id in room['room_cois']:
                            tmp_coi_mroom_codes.append(coi_school_id)
                # filter the mrooms that has conflict
                filter_result = itertools.filterfalse(lambda x: x in tmp_coi_mroom_codes, tmp_available_mroom_codes)
                if filter_result is not None:
                    tmp_filter_result_list = list()
                    for row in filter_result:
                        tmp_filter_result_list.append(row)
                    # has room available, randomly select on mroom for current volunteer
                    tmp_random_mroom_codes = secure_random.sample(tmp_filter_result_list, 1)
                    for item in tmp_random_mroom_codes:
                        current_mroom_code = item
                        tmp_available_mroom_codes.remove(current_mroom_code)
                        break
                else:
                    # no room available, leave it 0 and assign mroom later
                    current_mroom_code = 0
            else:
                # this volunteer has no coi, can random select one room from available mroom codes
                tmp_random_mroom_codes = secure_random.sample(tmp_available_mroom_codes, 1)
                for item in tmp_random_mroom_codes:
                    current_mroom_code = item
                    tmp_available_mroom_codes.remove(current_mroom_code)
                    break

            # assemble the current mvolunteer
            tmp_dict2 = {
                "mvolunteer_code": current_mvolunteer_code,
                "cois": current_cois,
                "volunteer_name": current_volunteer_name,
                "ppant_id": current_ppant_id,
                "ppant_subtype": 8,
                "timeslots": current_timeslots,
                "mroom_code": current_mroom_code,
                "data_entry": 'No'
            }
            # add current volunteer to volunteer plan
            volunteer_plan.append(tmp_dict2)
        else:
            # no need to add this volunteer
            pass

    # assign mroom to those didn't get assigned in the previous loop
    for volunteer in volunteer_plan:
        if volunteer['mroom_code'] == 0:
            # assign whatever room number that fits this volunteer
            # generate the mroom codes for selection
            if tmp_available_mroom_codes is None or len(tmp_available_mroom_codes) < 1:
                tmp_available_mroom_codes = list()
                for i in range(room_count):
                    tmp_available_mroom_codes.append(i + 1)
            # find the mrooms that has conflict
            tmp_mroom_codes_has_conflict = list()
            for coi_school_id in volunteer['cois']:
                for room in room_plan:
                    if coi_school_id in room['room_cois']:
                        tmp_mroom_codes_has_conflict.append(room['room_code'])
                        break
            # filter the mrooms with conflict
            filter_result = itertools.filterfalse(lambda x: x in tmp_mroom_codes_has_conflict, tmp_available_mroom_codes)
            tmp_filter_result_list = list()
            for row in filter_result:
                tmp_filter_result_list.append(row)

            # randomly select one mroom to the current volunteer
            tmp_random_mroom_codes = secure_random.sample(tmp_filter_result_list, 1)
            for item in tmp_random_mroom_codes:
                # assigne the mroom code to the current volunteer
                volunteer['mroom_code'] = item
                break
    return volunteer_plan


# this is new
def assign_volunteers(data_entrier_options, volunteer_list, room_plan):
    # randomly select qualified volunteer and assign to each room for data entry
    room_count = len(room_plan)
    secure_random = secrets.SystemRandom()  # creates a secure random object.
    data_entrier_options_list = list()
    for row in data_entrier_options:
        data_entrier_options_list.append(row)
    tmp_random_data_entriers = secure_random.sample(data_entrier_options_list, room_count)
    volunteer_plan = list()
    volunteer_selected_ppant_id_list = list()
    i = 0
    for data_entrier in tmp_random_data_entriers:
        tmp_dict = {
            "mvolunteer_code": i + 1,
            "cois": [],
            "volunteer_name": data_entrier[5] + " " + data_entrier[6],
            "ppant_id": data_entrier[1],
            "ppant_subtype": 9,
            "timeslots": data_entrier[9] + " " + data_entrier[10] + " " + data_entrier[11] + " " + data_entrier[12],
            "mroom_code": i + 1,
            "data_entry": 'Yes'
        }
        i += 1
        volunteer_selected_ppant_id_list.append(data_entrier[1])
        volunteer_plan.append(tmp_dict)

    # assign the rest of the volunteers to each room
    tried_times = 0
    max_try_times = len(volunteer_list)*room_count*len(volunteer_list)
    while tried_times <= max_try_times:
        for i in range(room_count):
            room_code = i + 1
            # get a volunteer who has not conflict with current room
            for volunteer in volunteer_list:
                tried_times += 1
                current_ppant_id = volunteer[0]
                current_mvolunteer_code = len(volunteer_plan) + 1
                current_cois = []
                current_volunteer_name =volunteer[5]
                current_timeslots = volunteer[11] + volunteer[12] + volunteer[13] + volunteer[14]
                current_mroom_code = room_code
                if current_ppant_id not in volunteer_selected_ppant_id_list:
                    # check cois
                    if volunteer[1] == 1:
                        # has cois
                        for coi_school in volunteer[3]:
                            tmp_coi_school_id = coi_school[1]
                            current_cois.append(tmp_coi_school_id)

                        # check if fit this room
                        current_volunteer_fit_current_room = True
                        for school_id in room_plan[room_code-1]['room_sids']:
                            if school_id in current_cois:
                                # not fit
                                current_volunteer_fit_current_room = False
                                break
                        if current_volunteer_fit_current_room:
                            # fit this room
                            # assemble the current mvolunteer
                            tmp_dict2 = {
                                "mvolunteer_code": current_mvolunteer_code,
                                "cois": current_cois,
                                "volunteer_name": current_volunteer_name,
                                "ppant_id": current_ppant_id,
                                "ppant_subtype": 8,
                                "timeslots": current_timeslots,
                                "mroom_code": current_mroom_code,
                                "data_entry": 'No'
                            }
                            # add current volunteer to volunteer plan
                            volunteer_plan.append(tmp_dict2)
                            volunteer_selected_ppant_id_list.append(current_ppant_id)
                            break
                    else:
                        # no cois - assign this volunteer to this room,
                        # assemble the current mvolunteer
                        tmp_dict2 = {
                            "mvolunteer_code": current_mvolunteer_code,
                            "cois": current_cois,
                            "volunteer_name": current_volunteer_name,
                            "ppant_id": current_ppant_id,
                            "ppant_subtype": 8,
                            "timeslots": current_timeslots,
                            "mroom_code": current_mroom_code,
                            "data_entry": 'No'
                        }
                        # add current volunteer to volunteer plan
                        volunteer_plan.append(tmp_dict2)
                        volunteer_selected_ppant_id_list.append(current_ppant_id)
                        break
        if len(volunteer_plan) == len(volunteer_list):
            break

    not_assigned_volunteers = []
    if len(volunteer_selected_ppant_id_list) < len(volunteer_list):
        for volunteer in volunteer_list:
            if volunteer[0] in volunteer_selected_ppant_id_list:
                pass
            else:
                tmp_n_volunteer = (volunteer[0], volunteer[5], volunteer[3])
                not_assigned_volunteers.append(tmp_n_volunteer)

    return (volunteer_plan, not_assigned_volunteers)


def assign_moved_jurors(moved_juror_list, round_plan, rooms_for_each_round):
    # initial moved_juror_plan
    moved_juror_room_assignment = list()
    juror_code_index = rooms_for_each_round - 1
    for juror in moved_juror_list:
        juror_code_index += 1
        tmp = {
            "juror_code": juror_code_index + 1,
            "is_chair": "No",
            "juror_info": juror,
            "juror_cois": [],
            "round_room_codes": [],
            "room_id": 0,
            "room_number": ''
        }
        for i in range(len(round_plan)):
            tmp['round_room_codes'].append(0)
        for coi_school in juror[3]:
            tmp['juror_cois'].append(coi_school[1])
        moved_juror_room_assignment.append(tmp)

    moved_juror_plan = []
    for round in round_plan:
        current_round_code = round['round_code']

        current_round_assigned_juror_codes = []
        while True:
            pair_index = -1
            for room_code in round['round_team_matches_room_codes']:
                pair_index += 1
                # found one moved juror for current round and current room
                current_round_room_sids = round['round_team_matches_school_ids'][pair_index]
                for juror in moved_juror_room_assignment:
                    # each round: each available juror only can be assgined once
                    if juror['juror_code'] not in current_round_assigned_juror_codes:
                        # check if this guy is available for current round index 11 - round 1, 12 - round 2&3, 13 - round 4&5, 14 - final round
                        juror_available = False
                        if current_round_code == 1:
                            if juror['juror_info'][11] == "Yes":
                                juror_available = True
                        elif current_round_code == 2 or current_round_code == 3:
                            if juror['juror_info'][12] == "Yes":
                                juror_available = True
                        elif current_round_code == 4 or current_round_code == 5:
                            if juror['juror_info'][13] == "Yes":
                                juror_available = True

                        if juror_available:
                            if juror['juror_code'] not in current_round_assigned_juror_codes:
                                if (current_round_room_sids[0] not in juror['juror_cois']) and (current_round_room_sids[1] not in juror['juror_cois']):
                                    # this juror is ok to stay at this room,
                                    tmp_tuple = (current_round_code, room_code, juror['juror_code'])
                                    moved_juror_plan.append(tmp_tuple)
                                    current_round_assigned_juror_codes.append(juror['juror_code'])
                                    break
                                else:
                                    pass
                        else:
                            current_round_assigned_juror_codes.append(juror['juror_code'])

            if len(current_round_assigned_juror_codes) >= len(moved_juror_list):
                break

        # finished the assignment to the moved jurors, now to fill the plan
        for item in moved_juror_plan:
            round_code = item[0]
            room_code = item[1]
            juror_code = item[2]
            moved_juror_room_assignment[juror_code-1-rooms_for_each_round]['round_room_codes'][round_code-1] = room_code
    return moved_juror_room_assignment
