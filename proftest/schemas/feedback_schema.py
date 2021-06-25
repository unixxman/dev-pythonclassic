from marshmallow import Schema, fields


class FeedbackSchema(Schema):
    score = fields.Integer()
    proficiency = fields.Method('get_proficiency')
    state = fields.Method('get_state')

    def get_proficiency(self, obj):
        return obj.proficiency.name

    def get_state(self, obj):
        return obj.state.name
