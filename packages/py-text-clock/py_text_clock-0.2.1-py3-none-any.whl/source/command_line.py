from .clockFace import TimeGenerator
from .mylogger import logger
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--show','-s',is_flag=True, help="Show the current time")
@click.option('--matrix','-m',is_flag=True, help="Show time as matrix")
@click.option('--debug','-d',is_flag=True,help="Run in debug mode")
def main(show,matrix,debug):
    if debug:
        logger.setLevel('DEBUG')
    if show:
        
        if matrix:
            logger.debug('Getting current time as matrix')
            TimeGenerator('upper').print_time_matrix()
        else:
            logger.debug('Getting current time as sentence')
            TimeGenerator('upper').print_time()

if __name__ == '__main__':
    main()