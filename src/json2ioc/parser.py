import argcomplete, argparse


def parser(args):
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
        help="Path to the configuration folder containing one or multiple configuration files or path to a specific configuration. By default the app searches into the json_config folder in the workspace. Configuration files must be .json files or a folder. When receiving a folder it will read all and only .json files",
    )
    main_parser.add_argument(
        "-t",
        "--subs-template",
        type=str,
        help="Name of a specific template file to use as reference when generating the new substitutions files.",
    )
    main_parser.add_argument(
        "-T",
        "--st-cmd-template",
        type=str,
        help="Path to the specific start command file to use as template. By default the app search for the iocBoot/ioc*/st.cmd file.",
    )

    # OUTPUTS
    main_parser.add_argument(
        "-o",
        "--subs-out",
        type=str,
        help="Path to the folder where to create the substitutions files. By default the app writes the output files in the *App/Db folder.",
    )
    main_parser.add_argument(
        "-m",
        "--make",
        action="store_true",
        help="Compile project after file creation",
    )
    main_parser.add_argument(
        "-O",
        "--st-cmd-out",
        type=str,
        help="Path to the folder where to create the start command files. By default the app writes the output files in the iocBoot/ioc* folder.",
    )

    # Start argcomplete
    argcomplete.autocomplete(main_parser)

    return main_parser.parse_args(args)
