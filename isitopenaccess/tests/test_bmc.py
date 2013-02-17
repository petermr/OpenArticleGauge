from unittest import TestCase

from isitopenaccess.plugins import bmc
from isitopenaccess import config

keys_in_license = ['provenance', 'description', 'type', 'title', 'url',
    'jurisdiction', 'open_access', 'BY', 'NC', 'SA', 'ND']

keys_in_provenance = ['date', 'agent', 'source', 'category', 'description']

class TestWorkflow(TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_01_bmc_standard_OA_license_from_doi(self):
        record = {}
        record['bibjson'] = {}
        record['provider'] = {}
        record['provider']['url'] = 'http://www.biomedcentral.com/1471-2164/13/425'

        bmc.page_license(record)

        # check if all the important keys were created
        assert record['bibjson'].has_key('license')

        # NB: some examples may fail the 'url' test since the Open Definition
        # data we're using as the basis for our licenses dictionary does not
        # have 'url' for all licenses. Fix by modifying licenses.py - add the data.
        assert all (key in record['bibjson']['license'] for key in keys_in_license)

        assert all (key in record['bibjson']['license']['provenance'] for key in keys_in_provenance)

        # some content checks now
        assert record['bibjson']['license']['type'] == 'cc-by'
        assert record['bibjson']['license']['version'] == '2.0'
        assert 'id' not in record['bibjson']['license'] # should not have "id" - due to bibserver
        assert not record['bibjson']['license']['jurisdiction']
        assert record['bibjson']['license']['open_access']
        assert record['bibjson']['license']['BY']
        assert not record['bibjson']['license']['NC']
        assert not record['bibjson']['license']['SA']
        assert not record['bibjson']['license']['ND']

        assert record['bibjson']['license']['provenance']['agent'] == config.agent
        assert record['bibjson']['license']['provenance']['source'] == record['provider']['url']
        assert record['bibjson']['license']['provenance']['date']
        assert record['bibjson']['license']['provenance']['category'] == 'page_scrape'
        assert record['bibjson']['license']['provenance']['description'] == 'License decided by scraping the resource at http://www.biomedcentral.com/1471-2164/13/425 and looking for the following license statement: "This is an Open Access article distributed under the terms of the Creative Commons Attribution License (<a href=\'http://creativecommons.org/licenses/by/2.0\'>http://creativecommons.org/licenses/by/2.0</a>), which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited.".'