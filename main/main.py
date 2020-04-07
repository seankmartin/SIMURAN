import os
from copy import copy


from tqdm import tqdm
import simuran.batch_setup
import simuran.recording
import simuran.analysis.analysis_handler
import simuran.param_handler


def main(
        location, functions, attributes_to_save,
        args_fn=None, do_batch_setup=False, friendly_names=None,
        sort_container_fn=None, reverse_sort=False,
        param_name="simuran_params.py", batch_name="simuran_batch_params.py",
        verbose_batch_params=False, load_all=False):

    # Do batch setup if requested.
    if do_batch_setup:
        if not os.path.isdir(location):
            raise ValueError(
                "Please provide a directory, entered {}".format(location))
        batch_setup = simuran.batch_setup.BatchSetup(
            location, fname=batch_name)
        print("Running batch setup {}".format(batch_setup))
        param_handler = simuran.param_handler.ParamHandler(
            in_loc=os.path.join(location, batch_name), name="params")
        if param_handler["overwrite"] and (not param_handler["only_check"]):
            batch_setup.clear_params(location, to_remove=param_name)
        dirs = batch_setup.write_batch_params(
            verbose_params=verbose_batch_params)
        if param_handler["only_check"]:
            print("Was only checking params so exiting.")
            exit(-1)

    # Setup the recording_container
    recording_container = simuran.recording.RecordingContainer()
    if os.path.isdir(location):
        recording_container.auto_setup(
            location, param_name=param_name, recursive=True)
    elif os.path.isfile(location):
        recording_container.auto_setup(
            os.path.dirname(location), param_name=param_name,
            recursive=False)
    else:
        raise ValueError(
            "Please provide a valid location, entered {}".format(location))
    if sort_container_fn is not None:
        recording_container.sort(sort_container_fn, reverse=reverse_sort)

    analysis_handler = simuran.analysis.analysis_handler.AnalysisHandler()
    pbar = tqdm(range(len(recording_container)))
    for i in pbar:
        if args_fn is not None:
            function_args = args_fn(recording_container[i])
        disp_name = recording_container[i].source_file[
            len(recording_container.base_dir + os.sep):]
        pbar.set_description(
            "Running {} on {} with arguments {}".format(
                [fn.__name__ for fn in functions], disp_name, function_args))
        if load_all:
            recording = recording_container.get(i)
        else:
            recording = recording_container[i]
        for fn in functions:
            fn_args = function_args.get(fn.__name__, [])
            analysis_handler.add_fn(fn, recording, *fn_args)
        analysis_handler.run_all_fns()
        recording.results = copy(analysis_handler.results)
        analysis_handler.reset()
    out_loc = os.path.join(recording_container.base_dir,
                           "sim_results", "results.csv")
    recording_container.save_summary_data(
        out_loc, attr_list=attributes_to_save, friendly_names=friendly_names)


if __name__ == "__main__":
    in_dir = r"D:\SubRet_recordings_imaging\muscimol_data\CanCSR7_muscimol\2_03082018"

    # Example sorting
    def sort_fn(x):
        comp = x.source_file[len(in_dir + os.sep) + 1:]
        order = int(comp.split("_")[0])
        return order

    from examples.function_args import run
    from examples.function_list import functions as list_of_functions
    from examples.attrs_to_save import save_list
    main(
        in_dir, list_of_functions, save_list,
        args_fn=run, do_batch_setup=True, sort_container_fn=sort_fn,
        verbose_batch_params=True, load_all=True)
