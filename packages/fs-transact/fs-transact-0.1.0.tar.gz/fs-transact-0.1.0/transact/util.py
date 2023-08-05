def prompt_bool(prompt, default=False):
    if default is True:
        options = '[Y/n] '
    elif default is False:
        options = '[y/N] '
    elif default is None:
        options = '[y/n] '
    else:
        raise ValueError()

    while True:
        response = input(prompt + " " + options)
        if response.lower() not in ['y', 'n', '']:
            continue

        if response == '' and default is None:
            continue

        if response == 'y':
            return True

        if response == 'n':
            return False

        return default
