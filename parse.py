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
        "config",
        type=str,
        help="""Path to a specific configuration file or path to 
            a folder containing one or multiple configuration files.
            It must be a .json file. 
            When receiving a folder it will read only .json files""",
    )
    main_parser.add_argument(
        "template",
        type=str,
        help="""Path to a specific template file to use as reference 
            when generating the new substitutions files.""",
    )
    main_parser.add_argument(
        "-o",
        "--out",
        type=str,
        help="""Path to the folder where to create the substitutions files.
            If not given it is the same of the template file.""",
    )

    # Start argcomplete
    argcomplete.autocomplete(main_parser)

    return main_parser.parse_args()
