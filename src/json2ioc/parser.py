import argcomplete, argparse


def parser():
    """
    Substitutions file creator parser details
    """

    main_parser = argparse.ArgumentParser(
        prog="substitutions creator",
        description="From a set of json configuration files create substitutions and the start commands files for an IOC",
        epilog="For any problem write an e-mail to giovanni.savarese@lnl.infn.it",
    )

    # INPUTS
    main_parser.add_argument(
        "-w",
        "--workspace",
        type=str,
        default=".",
        help="Specify workspace. By default it is the folder where the command is executed",
    )
    main_parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="Path to the configuration folder containing one or multiple configuration files and the template one. By default the app searches into the *App/config/ folder. Configuration files must be a .json file. When receiving a folder it will read only .json files",
    )
    main_parser.add_argument(
        "-t",
        "--subs-template",
        type=str,
        default="template.substitutions",
        help="Name of a specific template file to use as reference when generating the new substitutions files.",
    )
    main_parser.add_argument(
        "-s",
        "--st-cmd-template",
        type=str,
        help="Path to the specific st.cmd file to use as template with respect to the specified workspace dir. By default the app search for the iocBoot/ioc*/st.cmd file.",
    )

    # OUTPUTS
    main_parser.add_argument(
        "-o",
        "--subs-out",
        type=str,
        help="Path to the folder where to create the substitutions files with respect to the specified workspace dir. By default the app writes the output files in the *App/Db/ folder.",
    )
    main_parser.add_argument(
        "-m",
        "--make",
        action="store_true",
        help="Flag to compile project after file creation",
    )

    # Start argcomplete
    argcomplete.autocomplete(main_parser)

    return main_parser.parse_args()
