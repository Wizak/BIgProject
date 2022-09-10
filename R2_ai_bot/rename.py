import os


def rename_file(dir):
    list_dir = os.listdir(dir)
    count_file = range(len(list_dir))

    for filename, i in zip(list_dir, count_file):
        new_name = f'{dir}/mob_{i}.png'
        old_name = f'{dir}/{filename}'
        os.rename(old_name, new_name)


if __name__ == '__main__':
    dirs = ['mobs/train/images', 'mobs/validation/images']
    [rename_file(dir) for dir in dirs]