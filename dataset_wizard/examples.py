from settings import load_initial_200_ECGs
from dataset_wizard.query_specific_ECGS import Query
from dataset_wizard.create_custom_dataset import get_ecgs_by_query, save_new_dataset_by_ids
from dataset_wizard.dataset_to_html import draw_ecgs_from_json_to_html_by_ids
from settings import PATH_TO_DATASETS_FOLDER

def example_scenario_1():
    ########################----- Load dataset ---################
    json_data = load_initial_200_ECGs()

    ########################----- Make a Query ---################
    diags = {}
    substrs = []
    HR_l=65
    HR_r=75
    unwanted_substrs = []
    query = Query(diagnosys_names=diags,
                  substrs=substrs,
                  unwanted_substrs=unwanted_substrs,
                  HR_from=HR_l,
                  HR_to=HR_r
                  )
    ecgs_ids = get_ecgs_by_query(json_data, query)

    ################ Visualise result of the Query ################
    message = "Query result for " + str(query.diagnosys_names)
    name = "some"
    folder = "test"
    draw_ecgs_from_json_to_html_by_ids(json_data,
                                       ecgs_ids,
                                       name_html=name + ".html",
                                       folder=folder,
                                       message=message)
    ################ ---Save new dataset ---------##################
    save_new_dataset_by_ids(old_json=json_data,
                            ecg_ids_to_save=ecgs_ids,
                            name_new_dataset=name + ".json")

    ################# ------- Some log ------#######################
    print("Found: " + str(len(ecgs_ids)) + "ecgs;")
    print("Html: folder" + str(folder) + ", file " + name + ".html")




def example_scenario_2():
    ########################----- Load dataset ---################
    json_data = load_initial_200_ECGs()

    ########################----- List ids ---################
    ecgs_ids = []

    ################ Visualise   ################
    message = "Selected ECGs were: " + str(ecgs_ids)
    name = "some"
    folder = PATH_TO_DATASETS_FOLDER
    draw_ecgs_from_json_to_html_by_ids(json_data,
                                       ecgs_ids,
                                       name_html=name + ".html",
                                       folder=folder,
                                       message=message)
    ################ ---Save new dataset ---------##################
    save_new_dataset_by_ids(old_json=json_data,
                            ecg_ids_to_save=ecgs_ids,
                            name_new_dataset=name + ".json")

    ################# ------- Some log ------#######################
    print("Found: " + str(len(ecgs_ids)) + "ecgs;")
    print("Html: folder" + str(folder) + ", file " + name + ".html")


if __name__ == "__main__":
    example_scenario_1()