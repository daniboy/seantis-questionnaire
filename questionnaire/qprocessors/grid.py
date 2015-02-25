from collections import OrderedDict
from json import dumps
from questionnaire import question_proc, answer_proc, add_type


@question_proc('grid')
def question_grid(request, question):
    choices = []
    counter = 0
    cd = question.getcheckdict()
    for choice in question.choices():
        counter += 1
        key = "question_%s_multiple_%d" % (question.number, choice.sortid)
        if key in request.POST:
            selected_col_key = request.POST[key].split('__', 1)[0]
            choices.append( (choice, key, True, selected_col_key,) )
        else:
            choices.append( (choice, key, False, None) )
    columns = [column.split(',', 1) for column in question.extra.split(';')]
    return {
        "choices": choices,
        "columns": columns,
        "template"  : "questionnaire/grid.html",
        "required" : False,
    }

@answer_proc('grid')
def process_grid(question, answer):
    multiple = OrderedDict()

    items = filter(lambda item: item[0].startswith('multiple_'), answer.items())
    items = sorted(items, key=lambda item: int(item[0].split('_')[1]))
    for k, v in items:
        if v:
            col_key, value = v.split('__', 1)
            multiple[value] = col_key
    return dumps(multiple)
add_type('grid', 'Grid [radios]')