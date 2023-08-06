# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.gridlisting


class CollectiveGridlistingLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.gridlisting)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.gridlisting:default")


COLLECTIVE_GRIDLISTING_FIXTURE = CollectiveGridlistingLayer()


COLLECTIVE_GRIDLISTING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_GRIDLISTING_FIXTURE,),
    name="CollectiveGridlistingLayer:IntegrationTesting",
)


COLLECTIVE_GRIDLISTING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_GRIDLISTING_FIXTURE,),
    name="CollectiveGridlistingLayer:FunctionalTesting",
)


COLLECTIVE_GRIDLISTING_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_GRIDLISTING_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CollectiveGridlistingLayer:AcceptanceTesting",
)
