"""Setup tests for this package."""
from collective.belowcontentportlets.testing import (
    COLLECTIVE_BELOW_CONTENT_PORTLETS_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletManager
from zope.component import getSiteManager

import unittest


try:
    from plone.base.utils import get_installer
except ImportError:
    from Products.CMFPlone.utils import get_installer


class TestSetup(unittest.TestCase):
    """Test that collective.belowcontentportlets is properly installed."""

    layer = COLLECTIVE_BELOW_CONTENT_PORTLETS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.belowcontentportlets is installed."""
        self.assertTrue(
            self.installer.is_product_installed("collective.belowcontentportlets")
        )

    def test_browserlayer(self):
        """Test that ICollectiveBelowContentPortletsLayer is registered."""
        from collective.belowcontentportlets.interfaces import (
            ICollectiveBelowContentPortletsLayer,
        )
        from plone.browserlayer import utils

        self.assertIn(ICollectiveBelowContentPortletsLayer, utils.registered_layers())

    def test_portlet_manager_registered(self):
        sm = getSiteManager(self.portal)
        registrations = [
            r.name for r in sm.registeredUtilities() if IPortletManager == r.provided
        ]
        self.assertIn("collective.belowcontentportlets", registrations)


class TestUninstall(unittest.TestCase):
    layer = COLLECTIVE_BELOW_CONTENT_PORTLETS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("collective.belowcontentportlets")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.belowcontentportlets is cleanly uninstalled."""
        self.assertFalse(
            self.installer.is_product_installed("collective.belowcontentportlets")
        )

    def test_browserlayer_removed(self):
        """Test that ICollectiveBelowContentPortletsLayer is removed."""
        from collective.belowcontentportlets.interfaces import (
            ICollectiveBelowContentPortletsLayer,
        )
        from plone.browserlayer import utils

        self.assertNotIn(
            ICollectiveBelowContentPortletsLayer, utils.registered_layers()
        )

    def test_portlet_manager_removed(self):
        sm = getSiteManager(self.portal)
        registrations = [
            r.name for r in sm.registeredUtilities() if IPortletManager == r.provided
        ]
        self.assertNotIn("collective.belowcontentportlets", registrations)
