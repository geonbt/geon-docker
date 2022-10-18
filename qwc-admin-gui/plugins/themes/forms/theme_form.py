from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, SelectField, BooleanField, \
        SelectMultipleField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional, Regexp


class BackgroundLayerForm(FlaskForm):
    """Subform for backgroundlayers"""

    layerName = SelectField(coerce=str, validators=[DataRequired()])
    printLayer = StringField(validators=[Optional()])
    visibility = BooleanField(validators=[Optional()])


class ThemeForm(FlaskForm):
    """Main form for Theme GUI"""

    url = SelectField("Projekt", validators=[DataRequired()])
    title = StringField(
        "Title",
        description="Customized theme title.",
        validators=[Optional()]
    )
    attribution = StringField(
        "Atrribution",
        description=("Theme attribution, is displayed in the bottom right corner of the map."),
        validators=[Optional()]
    )
    thumbnail = SelectField(
        "Thumbnail",
        description=("Filename of the theme thumbnail. "
                     "By default, autogenerated via WMS GetMap."),
        validators=[Optional()]
    )
    format = SelectField(
        "Format",
        description=("Image format requested from the WMS Service. Default is 'image/png'."),
        validators=[Optional()]
    )
    mapCrs = SelectField(
        "CRS",
        description="The map projection.",
        default=("EPSG:3857"),
        validators=[Optional()]
    )
    additionalMouseCrs = SelectMultipleField(
        "Add. CRS",
        description=("Additional CRS for the mouse coordinate display."),
        validators=[Optional()]
    )
    searchProviders = StringField(
        "Search providers",
        description="List of available search providers.",
        default=("coordinates"),
        validators=[Regexp(r'^(\w+)(,\s*\w+)*$',
                    message="Please enter a comma separted list of names.")]
    )
    scales = StringField(
        "Scales",
        description="List of available map scales.",
        default=(""),
        validators=[Optional(), Regexp(r'^(\d+)(,\s*\d+)*$',
                    message="Please enter a comma separted list of numbers.")]
    )
    printScales = StringField(
        "Print scales",
        description="List of available print scales.",
        default=(""),
        validators=[Optional(), Regexp(r'^(\d+)(,\s*\d+)*$',
                    message="Please enter a comma separted list of numbers.")]
    )
    printResolutions = StringField(
        "Print resolutions",
        description="List of available print resolutions.",
        default=(""),
        validators=[Optional(), Regexp(r'^(\d+)(,\s*\d+)*$',
                    message="Please enter a comma separted list of numbers.")]
    )
    printLabelBlacklist = StringField(
        "Print label blacklist",
        description="Optional, list of composer label ids to not expose in the print dialog.",
        validators=[Optional(), Regexp(r'^(\w+)(,\s*\w+)*$',
                    message="Please enter a comma separted list of names.")]
    )
    collapseLayerGroupsBelowLevel = IntegerField(
        "collapse layer groups below level",
        description="Optional, layer tree level below which to initially collapse groups. By default the tree is completely expanded.",
        validators=[Optional()]
    )
    default = BooleanField(
        "default",
        description="Whether to use this theme as initial theme.",
        validators=[Optional()]
    )
    skipEmptyFeatureAttributes = BooleanField(
        "Skip empty feature attributes",
        description="Optional, whether to skip empty attributes in the identify results. Default is false.",
        validators=[Optional()]
    )

    backgroundLayers = FieldList(FormField(BackgroundLayerForm))

    submit = SubmitField("Save")
