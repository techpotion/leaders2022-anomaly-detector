import dill

def get_combined_model(config) -> None:
    path = config.pickles_path + '/comb_model.pickle'

    with open(path, 'rb') as handle:
        comb_model = dill.load(handle)
    handle.close()

    return comb_model

