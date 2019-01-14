# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import pytest

# Project imports
from restible import RestEndpoint, RestResource, RawResponse


class FakeRes(RestResource):
    name = 'fake_res'


def test_treats_single_result_as_data_and_uses_give_default_status_code():
    endpoint = RestEndpoint(res_cls=FakeRes)
    fake_result = {'test': 'asdf'}

    output = endpoint.process_result(fake_result, 200)

    assert output.data == fake_result
    assert output.status == 200
    assert output.headers == {}


def test_if_result_is_tuple_of_2_it_means_status_and_data():
    endpoint = RestEndpoint(res_cls=FakeRes)
    fake_result = (400, {'test': 'asdf'})

    output = endpoint.process_result(fake_result, 200)

    assert output.status == 400
    assert output.data == {'test': 'asdf'}
    assert output.headers == {}


def test_if_result_is_tuple_of_3_it_means_status_data_and_headers():
    endpoint = RestEndpoint(res_cls=FakeRes)
    fake_result = (400, {'Authorization': 'hello'}, {'test': 'asdf'})

    output = endpoint.process_result(fake_result, 200)

    assert output.status == 400
    assert output.headers == {'Authorization': 'hello'}
    assert output.data == {'test': 'asdf'}


def test_raises_ValueError_if_results_tuple_has_more_than_3_elements():
    endpoint = RestEndpoint(res_cls=FakeRes)
    fake_result = (400, {'Authorization': 'hello'}, {'test': 'asdf'}, None)

    with pytest.raises(ValueError):
        endpoint.process_result(fake_result, 200)


def test_instances_of_RawResponse_are_passed_through():
    endpoint = RestEndpoint(res_cls=FakeRes)
    fake_result = RawResponse('my response')

    output = endpoint.process_result(fake_result, 200)
    assert isinstance(output, RawResponse)
    assert output.response == 'my response'
