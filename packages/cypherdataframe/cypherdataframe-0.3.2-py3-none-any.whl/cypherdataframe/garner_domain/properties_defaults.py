from datetime import datetime

from cypherdataframe.model.Property import Property


ID_PROP = Property(label='id', datatype=str, postfix="_id")
NUMBER_PROP = Property(label='number', datatype=str, postfix="_n")
ID_PROP_COLLECT = Property(label='id', datatype=list[str], postfix="_id")
ID_BRANCH_PROP = Property(label='id', datatype=str, postfix="_id")
CODE_PROP = Property(label='code', datatype=str, postfix="_c")
VALUE_PROP = Property(label='value', datatype=str, postfix="_v")
OCCURSON_PROP = Property(label='occursOn', datatype=datetime, postfix="_o")
OCCURSON_BRANCH_PROP = Property(label='occursOn', datatype=list[datetime], postfix="_o")
CREATEDON_PROP = Property(label='createdOn', datatype=datetime, postfix="_cr")
CREATEDON_BRANCH_PROP = Property(label='createdOn', datatype=list[datetime], postfix="_cr")

PROPERTY_KEY = "props"
ID_KEY = "id"

MATERIAL_RETURN_ID = "m"
MATERIAL_LABEL = "Material"

TRANSFER_RETURN_ID = "t"
TRANSFER_LABEL = "Transfer"
TRANSFER_RELATIONSHIP = "COMPRISES"

FORECASTED_RELATIONSHIP = "FORECASTED"
FORECASTED_RETURN_POSTFIX = "F"

MEASURE_RELATIONSHIP = "MEASURED_AS"
MEASURE_RETURN_POSTFIX = "ME"

ARCHIVED_FORECASTED_RELATIONSHIP = "ARCHIVED_FORECASTED"
ARCHIVED_FORECASTED_RETURN_POSTFIX = "AF"

ATTAINED_RELATIONSHIP = "ATTAINED"
ATTAINED_RETURN_POSTFIX = "A"

ARCHIVED_ATTAINED_RELATIONSHIP = "ARCHIVED_ATTAINED"
ARCHIVED_ATTAINED_RETURN_POSTFIX = "AA"

REFERENCED_RELATIONSHIP = "REFERENCED_AS"
REFERENCED_RETURN_POSTFIX = "R"


PROP_TAGS = {
    "Status": {
        "VALUE": [OCCURSON_PROP]
        , "WITH_ID": [ID_PROP, OCCURSON_PROP]
        , "WITH_ID_CREATED": [
            ID_PROP
            , OCCURSON_PROP
            , CREATEDON_PROP
        ]
    },
    "StatusWithIDCreated": {
        "VALUE":  [
            ID_PROP
            , OCCURSON_PROP
            , CREATEDON_PROP
        ]
    },
    "StatusBranch": {
        "VALUE": [OCCURSON_BRANCH_PROP]
        , "WITH_ID": [ID_BRANCH_PROP, OCCURSON_BRANCH_PROP]
        , "WITH_ID_CREATED": [
            ID_BRANCH_PROP
            , OCCURSON_BRANCH_PROP
            , CREATEDON_BRANCH_PROP
        ]
    },
    "Reference": {
        "VALUE": [VALUE_PROP]
        , "WITH_ID": [ID_PROP, VALUE_PROP]
        , "WITH_ID_CREATED": [
            ID_PROP
            , VALUE_PROP
            , CREATEDON_PROP
        ]
    },
    "Transfer": {
        "VALUE": [ID_PROP]
    },
}
