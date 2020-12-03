# Flask-WTF v0.13 renamed Flask to FlaskForm
try:
    from flask_wtf import FlaskForm             # Try Flask-WTF v0.13+
except ImportError:
    from flask_wtf import Form as FlaskForm     # Fallback to Flask-WTF v0.12 or older

from wtforms import BooleanField, HiddenField, PasswordField, SubmitField, StringField, IntegerField, SelectField, \
    DateField, RadioField, FieldList, FormField
from wtforms import validators, ValidationError


# ***********
# ** Forms for the application **
# ***********

class CreateTeamForm(FlaskForm):
    school_id = SelectField('Team School', default=None)
    team_name = StringField('Team Name', validators=[validators.DataRequired('Team name is required')])
    school_name = StringField('School Name')
    address = StringField('Address')
    postal_code = StringField('Postal Code')
    city = StringField('City')
    province = SelectField('province',
        choices=[('AB', 'Alberta'), ('BC', 'British Columbia'), ('MB', 'Manitoba'), ('NB', 'New Brunswick'),
                 ('NL', 'Newfoundland and Labrador'), ('NS', 'Nova Scotia'), ('ON', 'Ontario'), ('NT', 'Northwest Territories'),
                 ('NU', 'Nunavut'), ('PE', 'Prince Edward Island'), ('QC', 'Quebec'), ('SK', 'Saskatchewan'), ('YT', 'Yukon')]
    )
    teleconferencing = RadioField('Are you teleconferencing?',
        choices=[('Yes', 'Yes'), ('No', 'No')], default='No'
    )
    submit = SubmitField('Save')

    def validate(self):
        #school_id = int(self.school_id.data)
        if self.school_id.data is None or len(self.school_id.data)<1:
            error_count = 0
            if self.school_name.data is None or len(self.school_name.data)<1:
                # school name is required
                self.school_name.errors = (" ")
                error_count = error_count + 1
            if self.address.data is None or len(self.address.data)<1:
                # school name is required
                self.address.errors = (" ")
                error_count = error_count + 1
            if self.city.data is None or len(self.city.data)<1:
                # school name is required
                self.city.errors = (" ")
                error_count = error_count + 1
            if self.province.data is None or len(self.province.data)<1:
                # school name is required
                self.province.errors = (" ")
                error_count = error_count + 1
            if self.postal_code.data is None or len(self.postal_code.data)<1:
                # school name is required
                self.postal_code.errors = (" ")
                error_count = error_count + 1

            if error_count > 0:
                return False
            else:
                return True
        else:
            return True


class SchoolForm(FlaskForm):
    school_id = IntegerField('School ID', default=None)
    school_name = StringField('School Name', validators=[validators.DataRequired('Team name is required')])
    address = StringField('Address', validators=[validators.DataRequired('Team name is required')])
    postal_code = StringField('Postal Code', validators=[validators.DataRequired('Team name is required')])
    city = StringField('City', validators=[validators.DataRequired('Team name is required')])
    province = SelectField('province',
        choices=[('AB', 'Alberta'), ('BC', 'British Columbia'), ('MB', 'Manitoba'), ('NB', 'New Brunswick'),
                 ('NL', 'Newfoundland and Labrador'), ('NS', 'Nova Scotia'), ('ON', 'Ontario'), ('NT', 'Northwest Territories'),
                 ('NU', 'Nunavut'), ('PE', 'Prince Edward Island'), ('QC', 'Quebec'), ('SK', 'Saskatchewan'), ('YT', 'Yukon')]
    )
    country = SelectField('Country', choices=[('CA', 'Canada')])
    school_status = SelectField('School Validation Status',
        choices=[('Pending', 'Waiting for Validation'), ('Valid', 'Valid'), ('Invalid', 'Invalid'), ('Unsure', 'Not Sure')]
    )
    submit = SubmitField('Save')

    def validate(self):
        error_count = 0
        #school_id = int(self.school_id.data)
        if self.school_id.data is None or self.school_id.data<1:
            # school name is required
            self.school_id.errors = (" ")
            error_count = error_count + 1
        if self.school_name.data is None or len(self.school_name.data)<1:
            # school name is required
            self.school_name.errors = (" ")
            error_count = error_count + 1
        if self.address.data is None or len(self.address.data)<1:
            # school name is required
            self.address.errors = (" ")
            error_count = error_count + 1
        if self.city.data is None or len(self.city.data)<1:
            # school name is required
            self.city.errors = (" ")
            error_count = error_count + 1
        if self.province.data is None or len(self.province.data)<1:
            # school name is required
            self.province.errors = (" ")
            error_count = error_count + 1
        if self.postal_code.data is None or len(self.postal_code.data)<1:
            # school name is required
            self.postal_code.errors = (" ")
            error_count = error_count + 1

        if error_count > 0:
            return False
        else:
            return True


class ApproveRegistForm(FlaskForm):
    type = StringField('Registration Person Type')
    label = StringField('Person Status')

    submit = SubmitField('Submit')

    def validate(self):
        error_count = 0
        if self.type.data is None or len(self.type.data)<1:
            #self.type.errors = (" ")
            error_count = error_count + 1
        if self.label.data is None or int(self.label.data)<1:
            #self.label.errors = (" ")
            error_count = error_count + 1
        if error_count > 0:
            return False
        else:
            return True


class JoinTeamForm(FlaskForm):
    """create team form."""

    team_school_id = SelectField('Team School', default=None, validators=[validators.DataRequired('School must be selected')])

    team_id = IntegerField('Team ID', validators=[validators.DataRequired()])
    team_name = StringField('Team Name', validators=[validators.DataRequired('Team name is required')])

    team_member_id = IntegerField('Team Member ID', default=None)
    team_member_user_id = IntegerField('Team Member User ID', validators=[validators.DataRequired()])

    submit = SubmitField('Submit')

    def validate(self):
        error_count = 0
        if self.team_school_id.data is None or int(self.team_school_id.data)<1:
            self.team_school_id.errors = (" ")
            error_count = error_count + 1
        if self.team_id.data is None or int(self.team_id.data)<1:
            # school name is required
            self.team_id.errors = (" ")
            error_count = error_count + 1
        if error_count > 0:
            #print("*********2.1*** total errors: ", error_count)
            return False
        else:
            #print("*********2.2***: ", error_count)
            return True


class PpantForm(FlaskForm):
    ppant_id = IntegerField('Participant ID', validators=[validators.DataRequired()])
    role_type = StringField('Role Type')
    last_coi_count = IntegerField('Last COI Count')
    teleconferencing = RadioField('Are you teleconferencing?',
        choices=[('Yes', 'Yes'), ('No', 'No')], default='No'
    )
    juror_experience = RadioField('Have you had any experience as a CaYPT juror before?',
        choices=[('Yes', 'Yes'), ('No', 'No')], default='No'
    )
    is_chair = RadioField('Is Chair',
        choices=[('Yes', 'Yes'), ('No', 'No')], default='No'
    )
    time_slot1 = StringField('Day 1 (Saturday Feb 29th, 2020) 10am - 2pm ')
    time_slot2 = StringField('Day 1 (Saturday Feb 29th, 2020) 2pm - 6pm ')
    time_slot3 = StringField('Day 2 (Saturday Mar 7th, 2020) 10am - 3pm ')
    time_slot4 = StringField('Day 2 (Saturday Mar 7th, 2020) 3pm - 7pm ')
    submit = SubmitField('Save')


class IMForm(FlaskForm):
    protocol = SelectField(choices=[('aim', 'AIM'), ('msn', 'MSN')])
    username = StringField()


class JoinAsJurorForm(FlaskForm):
    """create team form."""

    first_name = StringField('First name', validators=[validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[validators.DataRequired('Last name is required')])
    dob = DateField('Date of Birth', validators=[validators.DataRequired()])
    institution = StringField('Institution', validators=[validators.DataRequired()])

    coi_teams = None
    coi_members = None
    # im_accounts = FieldList(FormField(IMForm))
    choices = [(1, 'one'),
               (2, 'two'),
               (3, 'tree')]
    # resident = MultiCheckboxField('Label', choices=choices, coerce=int)

    participant_id = IntegerField('Participant ID')
    participant_user_id = IntegerField('Participant User ID', validators=[validators.DataRequired()])
    participant_role_type = StringField('Participant Role Type', default='Juror')
    # participant_has_coi = BooleanField('Has Conflict of Interest?', default='checked')
    # in html {{ render_field(form.participant_has_coi, tabindex=310, checked="checked") }}
    participant_has_coi = RadioField('Has Conflict of Interest?', choices=[('0', 'No'), ('1', 'Yes')], default=1)

    team_school_id = SelectField('Team School', default=None)
    team_school_name = StringField('Team School Name')
    team_school_address = StringField('Team School Address')
    team_school_country = SelectField('Team School Country', choices=[('CA', 'Canada')])
    team_school_province = SelectField('Team School Province',
        choices=[('AB', 'Alberta'), ('BC', 'British Columbia'), ('MB', 'Manitoba'), ('NB', 'New Brunswick'),
                 ('NL', 'Newfoundland and Labrador'), ('NS', 'Nova Scotia'), ('ON', 'Ontario'), ('NT', 'Northwest Territories'),
                 ('NU', 'Nunavut'), ('PE', 'Prince Edward Island'), ('QC', 'Quebec'), ('SK', 'Saskatchewan'), ('YT', 'Yukon')]
    )
    team_school_city = StringField('Team School City')
    team_school_zipcode = StringField('Team School Postal Code')

    team_id = IntegerField('Team ID', validators=[validators.DataRequired()])
    team_name = StringField('Team Name', validators=[validators.DataRequired('Team name is required')])

    team_member_id = IntegerField('Team Member ID', default=None)
    team_member_user_id = IntegerField('Team Member User ID', validators=[validators.DataRequired()])

    submit = SubmitField('Submit')

    def validate(self):
        # tmp_school_id = 0 #self.team_school_name
        if self.participant_user_id is None:
            #print(type("***********form, something wrong", self.participant_user_id))
            return False
        else:
            return True


class EventPlanForm(FlaskForm):
    """create team form."""

    teams_total_number = IntegerField('Total # of Teams ')
    teams_mini_number = IntegerField('Minimum # of Teams (must be 6 or more teams) ', validators=[validators.DataRequired()], default=6)
    pair_number_of_teams_per_pair = IntegerField('Number of Teams per Pair', validators=[validators.DataRequired()], default=2)
    rounds_total_number = IntegerField('Total # of Rounds for Selective Matches', validators=[validators.DataRequired()], default=5)
    rooms_for_each_round = IntegerField('Total # of Rooms for each round', validators=[validators.DataRequired()], default=4)
    max_re_do_times = IntegerField('Maximum Number of Tries', validators=[validators.DataRequired()], default=15)
    max_repeated_rooms = IntegerField('Ideally each team will not repeat the same room more than ? times', validators=[validators.DataRequired()], default=2)
    last_round_repeatable = RadioField('Allow last round repeatable?', choices=[('0', 'No'), ('1', 'Yes')], default=0)
    accept_proposal = RadioField('Do you want to save the proposal?', choices=[('0', 'No'), ('1', 'Yes')], default=0)

    submit = SubmitField('Generate Plan')
    accept = SubmitField('Save Plan')
    activate = SubmitField('Accept and Activate Plan')
    deactivate = SubmitField('De-Activate Plan (change status to proposed)')
    release = SubmitField('Release (freeze plan)')

    def validate(self):
        # tmp_school_id = 0 #self.team_school_name
        if self.teams_total_number is None:
            return False
        else:
            return True


class EventStageForm(FlaskForm):
    """create team form."""

    current_room_code = IntegerField('Room No.')
    current_round_code = IntegerField('Round No.')
    current_stage_code = IntegerField('Stage No.')
    current_plan_id = IntegerField('Plan Id')
    current_pair_id = IntegerField('Pair Id')
    reporter = StringField('Reporter Member ID--Name')
    opponent = StringField('Opponent Member ID--Name')
    reviewer = StringField('Reviewer Member ID--Name')
    team1 = IntegerField('Team No.1')
    team2 = IntegerField('Team No.2')
    team2 = IntegerField('Team No.3')
    submit = SubmitField('Submit')


class EventFinalPlanForm(FlaskForm):
    """create team form."""
    fm_room_code = IntegerField('FM Room No.')
    fm_round_code = IntegerField('FM Round No.')
    current_stage_code = IntegerField('Stage No.')
    fm_plan_id = IntegerField('FM Plan Id')
    activate = SubmitField('Accept and Activate Plan')
    deactivate = SubmitField('De-Activate Plan (change status to proposed)')
    release = SubmitField('Release (freeze plan)')
