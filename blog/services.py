

def file_rename(instance, filename):
    return "photos/{}_{}".format(instance.pk, filename)
