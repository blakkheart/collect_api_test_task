from django.core.exceptions import ValidationError


def validate_file_size(value):
    '''Валидатор проверки размера загружаемой картинки.'''
    filesize = value.size

    if filesize > 4*1024*1024:
        raise ValidationError(
            "The maximum file size that can be uploaded is 4MB")
    else:
        return value
