


def load_settings_from_file(id: int):
    '''
    Загружает данные из файлов в переменные: crop_left, crop_right, crop_up, crop_down, confidence_threshold.
    Параметр id отвечает за то, для какого детектора грузятся данные [0,1,2,3].
    '''
    from src.manage_service_data import get_service_data_from_file
    return  int(get_service_data_from_file("crop_left", id)),\
            int(get_service_data_from_file("crop_right", id)),\
            int(get_service_data_from_file("crop_up", id)),\
            int(get_service_data_from_file("crop_down", id)),\
            int(get_service_data_from_file("confidence_threshold", id))



def save_settings_into_file(crop_left, crop_right, crop_up, crop_down, confidence_threshold, id: int = 0):
    '''
    Сохраняет данные в файлы из переменных.
    Параметр id отвечает за то, для какого детектора грузятся данные [0,1,2,3].
    '''        
    from src.manage_service_data import set_service_data_into_file
    set_service_data_into_file("crop_left", crop_left, id)
    set_service_data_into_file("crop_right", crop_right, id)
    set_service_data_into_file("crop_up", crop_up, id)
    set_service_data_into_file("crop_down", crop_down, id)
    set_service_data_into_file("confidence_threshold", confidence_threshold, id)