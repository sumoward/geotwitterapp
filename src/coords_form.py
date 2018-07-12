from wtforms import Form, FloatField
from wtforms.validators import InputRequired, NumberRange


class CoordsForm(Form):
    latitude = FloatField(u'Latitude', default=-30, validators=[InputRequired(), NumberRange(-90, 90)],
                          description='48.182601')
    longitude = FloatField(u'Longitude', default=150,
                           validators=[InputRequired(), NumberRange(-180, 180)], description='11.304939')
