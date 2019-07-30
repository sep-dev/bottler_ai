from django import template
 
register = template.Library()
 
@register.filter
def multi(value, coefficient):
    return round(value * coefficient, 2)
