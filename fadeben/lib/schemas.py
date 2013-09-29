import formencode

class BaseSchema(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

class LoginSchema(BaseSchema):
    username = formencode.validators.String(not_empty=True)
    password = formencode.validators.String(not_empty=True)
    remember_me = formencode.validators.StringBool(if_missing=False)

class ChangePasswordSchema(BaseSchema):
    old_password = formencode.validators.String(not_empty=True)
    new_password1 = formencode.validators.String(not_empty=True)
    new_password2 = formencode.validators.String(not_empty=True)

    chained_validators = [
        formencode.validators.FieldsMatch(
            'new_password1',
            'new_password2')
        ]

class ResetPasswordSchema(BaseSchema):
    email = formencode.validators.Email(not_empty=True)

class GameSchema(BaseSchema):
    season = formencode.validators.Int(not_empty=True)
    week = formencode.validators.Int(not_empty=True)
    home_team_id = formencode.validators.Int(not_empty=True)
    away_team_id = formencode.validators.Int(not_empty=True)
    home_score = formencode.validators.Int()
    away_score = formencode.validators.Int()
    spread = formencode.validators.Number()
    game_date = formencode.validators.DateConverter(not_empty=True)
    game_time = formencode.validators.TimeConverter(not_empty=True)
    

class UpdateGameSchema(BaseSchema):
    home_score = formencode.validators.Int(if_empty=None)
    away_score = formencode.validators.Int(if_empty=None)
    spread = formencode.validators.Number(if_empty=None)
   
class PredictionSchema(BaseSchema):
    prediction = formencode.validators.StringBool(not_empty=True)

