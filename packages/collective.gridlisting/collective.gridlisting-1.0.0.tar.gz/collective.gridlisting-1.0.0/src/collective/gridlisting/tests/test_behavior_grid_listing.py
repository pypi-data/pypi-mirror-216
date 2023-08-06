# -*- coding: utf-8 -*-
from collective.gridlisting.behaviors.grid_listing import IGridListingMarker
from collective.gridlisting.testing import (  # noqa
    COLLECTIVE_GRIDLISTING_INTEGRATION_TESTING,
)
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class GridListingIntegrationTest(unittest.TestCase):
    layer = COLLECTIVE_GRIDLISTING_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_behavior_grid_listing(self):
        behavior = getUtility(IBehavior, "collective.gridlisting.grid_listing")
        self.assertEqual(
            behavior.marker,
            IGridListingMarker,
        )
