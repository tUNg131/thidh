from django import template
from django.template.loader import get_template

register = template.Library()

class IncludeOptionNode(template.Node):
    def __init__(self, template_name, field_context_name, nodelist):
        self.field = template.Variable(field_context_name)
        self.template = get_template(template_name)
        self.nodelist = nodelist

    def render(self, context):
        try:
            field = self.field.resolve(context)
            label = self.nodelist.render(context)
            return self.template.render({"field": field, "label": label})
        except template.VariableDoesNotExist:
            return ''

@register.tag("include_option")
def do_option(parser, token):
    nodelist = parser.parse(('end_include', ))
    parser.delete_first_token()

    try:
        tag_name, template_name, option_context_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires exactly two arguments" % token.contents.split()[0]
        )
    if not (template_name[0] == template_name[-1] and template_name[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )
    return IncludeOptionNode(template_name[1:-1], option_context_name, nodelist)

