"""Test introduce errors methods from TableGenerator package."""

from opentablebench.TableGenerator import TableGenerator

import pytest


@pytest.fixture
def rows():
    """Load header fixture."""
    return [{'label': 'Adobe Systems', 'type': 'abstract entity'},
            {'label or name': 'Kult', 'label': 'Kult (role-playing game)', 'type': 'activity', 'comment': 'Kult is a contemporary horror role-playing game originally designed by Gunilla Jonsson and Michael Petersén, first published in Sweden by Äventyrsspel (later Target Games) in 1991. The first English edition was published in 1993 by Metropolis Ltd.. The game will get a new edition in December 2016 after a successful Kickstarter crowdfunding campaign by current licensor Helmgast: Kult: Divinity Lost. Kult is notable for its philosophical and religious depth as well as for its mature and controversial content.'},
            {'label': '1._FC_Slovácko__Michal_Danek__1', 'member': 'Michal Daněk', 'numeral': '25'},
            {'label': '221', 'type': 'time period', 'label': '221'},
            {'label': 'TM6SF2__2__1TM6SF2__2__1', 'character': 'MouseGeneLocationMouseGeneLocation', 'gene': '70080061', 'location': '70072892'}]


def test_introduce_errors_row(rows):
    """Test introduce_errors_row method."""
    table_gen = TableGenerator()
    for row in rows:
        print(table_gen.introduce_errors_row(row))
