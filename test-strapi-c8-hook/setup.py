import argparse
import git
import logging
import os

from pynpm import NPMPackage


# Create logger
logger = logging.getLogger()

# Args Parser
parser = argparse.ArgumentParser()

# strapi-examples repo
STRAPI_EXAMPLES = "https://github.com/strapi/strapi-examples.git"

# Current working directory
CWD = os.getcwd()

# Cheesecake example path
FAMILY_EXAMPLE = CWD + "/test"

# package.json path
PACKAGE_JSON = FAMILY_EXAMPLE + "/package.json"


# Functions
# Set Logger config
def setLogger():

    logger.setLevel(logging.DEBUG)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
    ch.setFormatter(formatter)

    # Add Handlers
    logger.addHandler(ch)


def setParser():

    # Optional arguments
    parser.add_argument("-i", "--install", help="Install test suite for strapi C8\
                        hook", action="store_true")
    parser.add_argument("-t", "--test", help="Test C8 hook for strapi",
                        action="store_true")

    # Parse args
    return parser.parse_args()


# Driver
def setup():

    try:
        # Set logger
        setLogger()

        # Set Parser config
        args = setParser()

        # npm package manager
        npm = NPMPackage(PACKAGE_JSON)

        # If "install" flag is set
        if args.install:

            logger.info("Installing C8 hook test suite")

            # git clone strapi-example repo
            logger.debug("Cloning git repo: '%s'" % STRAPI_EXAMPLES)
            git.Git(CWD).clone(STRAPI_EXAMPLES)
            logger.debug("Cloned successfully")

            # ch cwd to examples repo
            os.chdir(FAMILY_EXAMPLE)

            # install npm packages
            logger.debug("Install npm packages")
            npm.install()
            npm.run_script('setup', '--plugins')
            logger.debug("Installed successfully")

        else:
            if os.path.isdir(FAMILY_EXAMPLE):
                # ch cwd to examples repo
                os.chdir(FAMILY_EXAMPLE)
            else:
                logger.error("Test suite not installed")
                logger.error("Execute: %s --install" % os.path.basename(__file__))
                return

        logger.info("Testing C8 hook for strapi")
        npm.start()

    except KeyboardInterrupt:
        return
    except Exception as e:
        logger.error("Error: '%s'" % e)
        return


def main():

    # Create strapi setup for C8 hook
    setup()

# Driver
main()
