import os


IGNORE_LIST = ["docs", "tests", "devtools", "__pycache__", "code_review", "test_suite", "utils"]

# this function is used to create the entire directory structure
# of our source docs, as well as writing out each individual rst file.


def generate_docs(directory, top, packages, project_name="openmdao"):
    """
    generate_docs

    Can supply a project name other than `openmdao` to use this function
    with other projects.
    """
    index_top = """:orphan:

.. _source_documentation:

********************
Source Docs
********************

.. toctree::
   :titlesonly:
   :maxdepth: 1

"""
    package_top = """
.. toctree::
    :maxdepth: 1

"""

    ref_sheet_bottom = """
   :members:
   :undoc-members:
   :special-members: __init__, __contains__, __iter__, __setitem__, __getitem__
   :exclude-members: __init__, compute, add_constraint, add_design_var, add_input, add_objective, add_output, add_recorder, add_response, check_config, cleanup, compute_jacvec_product, compute_partials, declare_partials, distributed, get_constraints, get_design_vars, get_linear_vectors, get_nonlinear_vectors, get_objectives, get_responses, initialize, is_active, jacobian_context, linear_solver, list_inputs, list_outputs, ln_solver, metadata, nl_solver, nonlinear_solver, reconfigure, record_iteration, resetup, run_apply_linear, run_apply_nonlinear, run_linearize, run_solve_linear, run_solve_nonlinear, set_check_partial_options, set_initial_values, setup, system_iter, add, add_subsystem, approx_totals, compute_sys_group, configure, connect, set_order, apply_linear, apply_nonlinear, guess_nonlinear, linearize, solve_linear, solve_nonlinear, compute_sys_graph
   :show-inheritance:
   :inherited-members:

.. toctree::
   :maxdepth: 1
"""

    docs_dir = os.path.dirname(directory)

    doc_dir = os.path.join(docs_dir, "_srcdocs")
    if os.path.isdir(doc_dir):
        import shutil

        shutil.rmtree(doc_dir)

    if not os.path.isdir(doc_dir):
        os.mkdir(doc_dir)

    packages_dir = os.path.join(doc_dir, "packages")
    if not os.path.isdir(packages_dir):
        os.mkdir(packages_dir)

    # look for directories in the top level, one up from docs
    # those directories will be the packages that
    # auto-generate at the top-level index.rst file for _srcdocs, based on
    # the packages that are passed in, which are set in conf.py.

    # to improve the order in which the user sees the source docs,
    # order the packages in this list explicitly. Any new ones that
    # are detected will show up at the end of the list.

    # everything in openmdao directory that isn't discarded is appended as a source package.
    for listing in os.listdir(os.path.join(top)):
        if os.path.isdir(os.path.join("..", listing)):
            if listing not in IGNORE_LIST and listing not in packages:
                packages.append(listing)

    # begin writing the '_srcdocs/index.rst' file at mid  level.
    index_filename = os.path.join(doc_dir, "index.rst")
    index = open(index_filename, "w")
    index.write(index_top)

    # auto-generate package header files (e.g. 'openmdao.core.rst')
    for package in packages:
        # a package is e.g. openmdao.core, that contains source files
        # a sub_package, is a src file, e.g. openmdao.core.component
        sub_packages = []
        package_filename = os.path.join(packages_dir, project_name + "." + package + ".rst")
        package_name = project_name + "." + package

        # the sub_listing is going into each package directory and listing what's in it
        for sub_listing in sorted(os.listdir(os.path.join(directory, package.replace(".", "/")))):
            # don't want to catalog files twice, nor use init files nor test directory
            if (os.path.isdir(sub_listing) and sub_listing != "tests") or (
                sub_listing.endswith(".py") and not sub_listing.startswith("_")
            ):
                # just want the name of e.g. dataxfer not dataxfer.py
                sub_packages.append(sub_listing.rsplit(".")[0])

        if len(sub_packages) > 0:
            # continue to write in the top-level index file.
            # only document non-empty packages -- to avoid errors
            # (e.g. at time of writing, doegenerators, drivers, are empty dirs)

            # specifically don't use os.path.join here.  Even windows wants the
            # stuff in the file to have fwd slashes.
            index.write("   packages/" + project_name + "." + package + "\n")

            # make subpkg directory (e.g. _srcdocs/packages/core) for ref sheets
            package_dir = os.path.join(packages_dir, package)
            os.mkdir(package_dir)

            # create/write a package index file: (e.g. "_srcdocs/packages/openmdao.core.rst")
            package_file = open(package_filename, "w")
            package_file.write(package_name + "\n")
            package_file.write("-" * len(package_name) + "\n")
            package_file.write(package_top)

            for sub_package in sub_packages:
                SKIP_SUBPACKAGES = ["__pycache__"]
                # this line writes subpackage name e.g. "core/component.py"
                # into the corresponding package index file (e.g. "openmdao.core.rst")
                if sub_package not in SKIP_SUBPACKAGES:
                    # specifically don't use os.path.join here.  Even windows wants the
                    # stuff in the file to have fwd slashes.
                    package_file.write("    " + package + "/" + sub_package + "\n")

                    # creates and writes out one reference sheet (e.g. core/component.rst)
                    ref_sheet_filename = os.path.join(package_dir, sub_package + ".rst")
                    ref_sheet = open(ref_sheet_filename, "w")

                    # get the meat of the ref sheet code done
                    filename = sub_package + ".py"
                    ref_sheet.write(".. index:: " + filename + "\n\n")
                    ref_sheet.write(".. _" + package_name + "." + filename + ":\n\n")
                    ref_sheet.write(filename + "\n")
                    ref_sheet.write("-" * len(filename) + "\n\n")
                    ref_sheet.write(".. automodule:: " + package_name + "." + sub_package)

                    # finish and close each reference sheet.
                    ref_sheet.write(ref_sheet_bottom)
                    ref_sheet.close()

            # finish and close each package file
            package_file.close()

    # finish and close top-level index file
    index.close()
