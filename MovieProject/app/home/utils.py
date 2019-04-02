from datetime import datetime

def change_filename(filename):
    return datetime.now().strftime('%Y%m%d_%H%M%S')+'_'+filename