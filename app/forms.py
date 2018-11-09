from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms import FloatField, DateField, FieldList, FormField, Form
from wtforms.validators import DataRequired, Length, NumberRange 

#TODO: clean up
class NPOwnerField(Form):
    natural_person_first_name = StringField('Osaniku eesnimi:')   
    natural_person_last_name = StringField('Osaniku eesnimi:')   
    natural_person_registry_id = IntegerField('Registrikood:')
    shares =  FloatField('Osaniku osa suurus [€]:',)   
    founder = BooleanField('Asutaja')    
class JPOwnerField(Form):
    juridical_person_name = StringField('Juriidilise isiku nimi:')   
    juridical_person_registry_id = IntegerField('Registrikood:')
    shares =  FloatField('Osaniku osa suurus [€]:')   
    founder = BooleanField('Asutaja')
class AddCompanyForm(FlaskForm):
    company_name = StringField('Osaühingu nimi:', 
        validators=[DataRequired(), Length(min=3,max=100, 
            message="3-100 tähemärki")])
    identificator = IntegerField('Registrikood:', 
        validators=[DataRequired(), NumberRange(min=1,max=9999999, 
            message="registrikood 7 tähemärki")])
    total_capital = FloatField('Kogukapitali suurus [€]:', 
        validators=[DataRequired(), 
        NumberRange(min=2500, message="min kogukapital 2500€")], default=2500)
    established_date = DateField('Asutamiskuupäev:',
        validators=[DataRequired()], format='%d.%m.%Y')
    natural_person_first_name = StringField('Osaniku eesnimi:', 
        validators=[DataRequired(), Length(min=3,
            max=100, message="3-100 tähemärki")])   
    natural_person_last_name = StringField('Osaniku eesnimi:', 
        validators=[DataRequired(), Length(min=3,
            max=100, message="3-100 tähemärki")])   
    natural_person_registry_id = IntegerField('Registrikood:', 
        validators=[DataRequired(), 
            NumberRange(min=30000000000,max=60000000000, 
            message="isikukood 11 numbrimärki")])
    shares =  FloatField('Osaniku osa suurus [€]:',
        validators=[DataRequired()])   
    founder = BooleanField('Asutaja')
    juridical_person_name = StringField('Juriidilise isiku nimi:', 
        validators=[DataRequired(), Length(min=3,
            max=100, message="3-100 tähemärki")])   
    juridical_person_registry_id = IntegerField('Registrikood:', 
        validators=[DataRequired(), NumberRange(min=1,max=9999999, 
            message="juriidilise isiku registrikood 7 nurmbimärki")])
    np_owners = FieldList(FormField(NPOwnerField), min_entries=0) 
    jp_owners = FieldList(FormField(JPOwnerField), min_entries=0) 
    
