import os

# Home directory path
HOME = os.path.expanduser('~')

# Root directory of the project (dirname).
ROOT_FOLDER = os.path.join(os.path.dirname(__file__), '../..')

GBS_ROOT_PATH = os.path.join(HOME, 'GBS-ROOT')

GBS_ARCH_PATH = os.path.join(GBS_ROOT_PATH, 'local/BUILD-ROOTS/scratch.armv7l.0')

GBS_IOTJS_PATH = os.path.join(GBS_ARCH_PATH, 'home/abuild/rpmbuild/BUILD/iotjs-1.0.0')

GBS_IOTJS_BUILD_PATH = os.path.join(GBS_IOTJS_PATH, 'build/noarch-tizen')
