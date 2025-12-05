import pytest


@pytest.fixture
def fixture_noparams(request):
    print(f'{request = }')
    # print(f'{request.param = }')


def test_fixture_no_param(fixture_noparams):
    pass


@pytest.fixture
def fixture_oneparam(request):
    print(f'{request = }')
    print(f'{request.param = }')
    # yield request.param



@pytest.mark.parametrize(
    'fixture_oneparam',
    ['hi'],
    indirect=True
)
def test_fixture_one_param(fixture_oneparam):
    # print(f'{fixture_oneparam = }')
    pass


@pytest.fixture
def fixture_twoparams(request):
    print(f'{request = }')
    print(f'{request.param = }')
    yield request.param


@pytest.mark.parametrize(
    'fixture_twoparams',
    [('hi', 'there')],
    indirect=True
)
def test_fixture_two_params(fixture_twoparams):
    print(f'{fixture_twoparams = }')