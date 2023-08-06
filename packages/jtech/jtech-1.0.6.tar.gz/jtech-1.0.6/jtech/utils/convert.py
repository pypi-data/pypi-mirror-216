import glob


def generate_tpl_constants():
    tpl_files = glob.glob('../resources/tpl/*.tpl')

    constants = []
    for tpl_file in tpl_files:
        tpl_name = tpl_file.split('/')[-1].split('.')[0]
        tpl_constant = f"{tpl_name.upper()}='{tpl_name}'"
        constants.append(tpl_constant)

    with open('tpl_constants.py', 'w') as file:
        file.write('\n'.join(constants))


if __name__ == '__main__':
    generate_tpl_constants()
