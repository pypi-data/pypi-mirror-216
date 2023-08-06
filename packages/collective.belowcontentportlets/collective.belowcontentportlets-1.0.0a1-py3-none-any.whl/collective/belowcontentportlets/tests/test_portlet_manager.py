from collective.belowcontentportlets.testing import (
    COLLECTIVE_BELOW_CONTENT_PORTLETS_INTEGRATION_TESTING,
)
from plone.app.portlets.portlets import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletType
from zope.component import getUtility

import unittest


class TestPortletManager(unittest.TestCase):
    layer = COLLECTIVE_BELOW_CONTENT_PORTLETS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Site Administrator"])

    def test_portlet_manager_position(self):
        html = self.portal()

        # The portlet manager is on the page.
        manager_pos = html.find('id="belowcontentportlets"')
        self.assertTrue(manager_pos != -1)

        # First id content, then portlet manager.
        content_pos = html.find('id="content"')
        self.assertLess(content_pos, manager_pos)

        # First viewlet manager, then portlet manager.
        viewlet_manager_pos = html.find('id="viewlet-below-content"')
        self.assertLess(viewlet_manager_pos, manager_pos)

        # First portlet manager, then the footer.
        footer_pos = html.find('id="portal-footer-wrapper"')
        self.assertLess(manager_pos, footer_pos)

    def test_portlet_manager_link(self):
        link = "@@topbar-manage-portlets/collective.belowcontentportlets"
        html = self.portal()
        self.assertIn(link, html)
        # We cannot traverse all the way, we need to use two steps.
        manage_portlets = self.portal.restrictedTraverse("@@topbar-manage-portlets")
        page = manage_portlets.publishTraverse(
            self.request, "collective.belowcontentportlets"
        )
        html = page()
        self.assertIn("Add portlet", html)

    def test_with_actual_portlet(self):
        # Adapted from login portlet tests.
        portlet = getUtility(IPortletType, name="portlets.Login")
        mapping = self.portal.restrictedTraverse(
            "++contextportlets++collective.belowcontentportlets"
        )
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse("+/" + portlet.addview)
        # This is a NullAddForm - calling it does the work
        addview()
        self.assertEqual(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0], login.Assignment))

        # Logout and check that the portlet shows up where we expect it.
        logout()

        # The portlet manager is on the page.
        html = self.portal()
        manager_pos = html.find('id="belowcontentportlets"')
        self.assertTrue(manager_pos != -1)

        # First portlet manager, then input.
        input_pos = html.find('name="__ac_name"')
        self.assertLess(manager_pos, input_pos)

        # First input, then the footer.
        footer_pos = html.find('id="portal-footer-wrapper"')
        self.assertLess(input_pos, footer_pos)
