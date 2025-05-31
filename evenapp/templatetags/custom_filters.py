from django import template # type: ignore

register = template.Library()

dias_semana = {
    'Monday': 'Segunda',
    'Tuesday': 'Terça',
    'Wednesday': 'Quarta',
    'Thursday': 'Quinta',
    'Friday': 'Sexta',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

meses = {
    'Jan': 'Jan',
    'Feb': 'Fev',
    'Mar': 'Mar',
    'Apr': 'Abr',
    'May': 'Mai',
    'Jun': 'Jun',
    'Jul': 'Jul',
    'Aug': 'Ago',
    'Sep': 'Set',
    'Oct': 'Out',
    'Nov': 'Nov',
    'Dec': 'Dez'
}

@register.filter
def format_date(value):
    if not value:
        return ''
    
    dia_semana = dias_semana[value.strftime('%A')]
    dia = value.strftime('%d')
    mes = meses[value.strftime('%b')]
    ano = value.strftime('%Y')
    hora = value.strftime('%H:%M')

    return f'{dia_semana}, {dia} de {mes} de {ano} às {hora}'
