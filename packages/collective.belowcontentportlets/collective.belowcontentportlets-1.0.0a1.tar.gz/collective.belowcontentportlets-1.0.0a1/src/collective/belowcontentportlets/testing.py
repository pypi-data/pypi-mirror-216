from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import collective.belowcontentportlets


class CollectiveBelowContentPortletsLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.belowcontentportlets)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.belowcontentportlets:default")


COLLECTIVE_BELOW_CONTENT_PORTLETS_FIXTURE = CollectiveBelowContentPortletsLayer()


COLLECTIVE_BELOW_CONTENT_PORTLETS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_BELOW_CONTENT_PORTLETS_FIXTURE,),
    name="CollectiveBelowContentPortletsLayer:IntegrationTesting",
)


COLLECTIVE_BELOW_CONTENT_PORTLETS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_BELOW_CONTENT_PORTLETS_FIXTURE,),
    name="CollectiveBelowContentPortletsLayer:FunctionalTesting",
)
