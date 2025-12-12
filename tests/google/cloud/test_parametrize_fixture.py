import pytest
from google.cloud.util import setup_logger

logger = setup_logger(__name__)


@pytest.fixture
def getpath(request, param_fixture):
    # path = request.param
    logger.info(f'{request = }')
    # logger.info(f'{request.param = }')
    # logger.info(f'{path = }')
    logger.info(f'{param_fixture = }')
    # return path


def test_getpath(getpath):
    logger.info(f'{getpath = }')



@pytest.fixture(params=['hello'])
def param_fixture(request):
    '''sets default param to hello'''
    path = request.param
    logger.info(f'{path = }')
    return path


@pytest.mark.parametrize( 'param_fixture', ['hi'], indirect=True )
def test_fixture_one_param(param_fixture):
    '''prints hi'''
    logger.info(f'{param_fixture = }')


def test_fixture_default_param(param_fixture):
    '''prints hello '''
    logger.info(f'{param_fixture = }')

