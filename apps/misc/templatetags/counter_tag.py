from django import template

register = template.Library()

class IncrementNode(template.Node):
    def __init__(self, var_name="counter"):
        self.var_name = var_name
        
    def get_context(self, top_context):
        for context in top_context.dicts:
            if self.var_name in context:
                return context
        return top_context
    def render(self, context):
        try:
            resolved_var = template.resolve_variable(self.var_name,
                                                     context)
                
            self.get_context(context)[self.var_name] = resolved_var+1
        except template.VariableDoesNotExist:
            self.get_context(context)[self.var_name] = 0
        return ''

@register.tag
def increment_count(parser, token):
    args = token.split_contents()
    return IncrementNode()
    

