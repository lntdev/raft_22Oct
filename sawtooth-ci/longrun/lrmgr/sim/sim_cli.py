import argparse

import sim.run

CMDS = {
    'run': sim.run
}

EPILOG = """
Tools for running test simulations against a managed network. See subcommands
for more information.
"""

def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('sim', parents=[parent_parser])
    parser.epilog = EPILOG

    sim_subparser = parser.add_subparsers(
        title='subcommands', dest='sim_command'
    )

    for cmd in CMDS:
        CMDS[cmd].add_parser(sim_subparser, parent_parser)


def do(args, on_invalid):
    if args.sim_command in CMDS:
        CMDS[args.sim_command].do(args)
    else:
        on_invalid()
