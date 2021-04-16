import argcomplete, argparse


def parser():
    """
    Substitutions file creator parser details
    """

    main_parser = argparse.ArgumentParser(
        prog="substitutions creator",
        description="""From one or more given configurations and 
            a template of the desired .substitutions file, 
            create the corresponding .substitutions file""",
        epilog="For any problem write an e-mail to giovanni.savarese@lnl.infn.it",
    )

    main_parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="""Path to the configuration folder containing
            one or multiple configuration files and the template one.
            By default the app searches into the *App/config/ folder.
            Configuration files must be a .json file.
            When receiving a folder it will read only .json files""",
    )
    main_parser.add_argument(
        "-t",
        "--template",
        type=str,
        default="template.substitutions",
        help="""Name of a specific template file to use as reference 
            when generating the new substitutions files.""",
    )
    main_parser.add_argument(
        "-o",
        "--out",
        type=str,
        help="""Path to the folder where to create the substitutions files.
            If not given it is the same of the template file.
            By default the app writes the output files in the *App/Db/ folder.""",
    )
    main_parser.add_argument(
        "-s",
        "--st-cmd",
        type=str,
        help="""Path to the specific st.cmd file to use as template.
            By default the app search for the iocBoot/ioc*/st.cmd file.""",
    )

    main_parser.add_argument(
        "-y",
        "--make",
        action="store_true",
        help="Flag to compile project after file creation",
    )
    # Start argcomplete
    argcomplete.autocomplete(main_parser)

    return main_parser.parse_args()
