# -*- coding: utf-8 -*-
import werkzeug.datastructures

import ga4gh.dos.server
from ga4gh.dos.test.compliance import AbstractComplianceTest

# We set this so that `nose` doesn't try and run the abstract tests.
# (If that happens, all of the tests fail since :meth:`_make_request`
# raises a :exc:`NotImplementedError` for each of the test cases.
AbstractComplianceTest.__test__ = False


class TestCompliance(AbstractComplianceTest):
    """
    Runs the :class:`~ga4gh.dos.test.compliance.AbstractComplianceTest`
    against :mod:`ga4gh.dos.server`.
    """
    # See above - if we don't explicitly set :var:`__test__` here,
    # this test suite won't run as we adjust the value of the variable
    # in the superclass above.
    __test__ = True

    @classmethod
    def setUpClass(cls):
        # :mod:`ga4gh.dos.server` is built on top of :mod:`connexion`,
        # which is built on top of :mod:`flask`, which is built on top
        # of :mod:`werkzeug`, which means we can do some cool nice
        # things with testing.
        app = ga4gh.dos.server.configure_app().app
        cls.client = app.test_client()

        # Populate our new server with some test data objects and bundles
        for data_obj in cls.generate_data_objects(250):
            cls.dos_request('POST', '/dataobjects', body={'data_object': data_obj})
        for data_bdl in cls.generate_data_bundles(250):
            cls.dos_request('POST', '/databundles', body={'data_bundle': data_bdl})

    @classmethod
    def _make_request(cls, meth, path, headers=None, body=None):
        # For documentation on this function call, see
        # :class:`werkzeug.test.EnvironBuilder` and :meth:`werkzeug.test.Client.get`.
        headers = werkzeug.datastructures.Headers(headers)
        r = cls.client.open(method=meth, path='/ga4gh/dos/v1' + path,
                            data=body, headers=headers)
        return r.data, r.status_code
