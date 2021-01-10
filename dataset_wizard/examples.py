from settings import load_json_dset_with_delin
from dataset_wizard.query_specific_ECGS import Query
from dataset_wizard.create_custom_dataset import get_ecgs_by_query, save_new_dataset_by_ids
from dataset_wizard.dataset_to_html import draw_ecgs_from_json_to_html_by_ids
from settings import PATH_TO_METADATASETS_FOLDER

def example_scenario_1():
    ########################----- Load dataset ---################
    json_data = load_json_dset_with_delin()

    ########################----- Make a Query ---################
    diags = {'electric_axis_normal':False}
    substrs = ["стимул"]
    HR_l=0
    HR_r=200
    unwanted_substrs = []
    query = Query(diagnosys_names=diags,
                  substrs=substrs,
                  unwanted_substrs=unwanted_substrs,
                  HR_from=HR_l,
                  HR_to=HR_r
                  )
    ecgs_ids = get_ecgs_by_query(json_data, query)
    ecgs_ids = ecgs_ids[:10]
    ################ Visualise result of the Query ################
    message = "Query result for " + str(query.diagnosys_names)
    name = "unnormal_axis10"
    folder = PATH_TO_METADATASETS_FOLDER
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
    json_data = load_json_dset_with_delin()

    ########################----- List ids ---################
    ecgs_ids = ['50488354']

    ################ Visualise   ################
    message = "Selected ECGs were: " + str(ecgs_ids)
    name = "stimulator1"
    folder = PATH_TO_METADATASETS_FOLDER
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
    example_scenario_2()