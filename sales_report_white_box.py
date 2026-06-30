"""
White-Box Test Suite — Odoo Sales Report Controller
=====================================================
Techniques:
  - Path Coverage (Basis Path): CFG + V(G) + 7 basis paths
  - Decision/Condition Coverage: Table with all T/F combinations

User Stories:
  RHU02: Search in Sales Report Flow Analysis
  RHU03: Advanced Record Filtering
  RHU04: Save Favorite Searches
  RHU06: Data Export to Excel (XLSX)
"""
import unittest
from typing import Any, Optional

# ---------------------------------------------------------------------------
# 1. PSEUDO-CONTROLLER — Simulates Odoo sale.report backend logic
# ---------------------------------------------------------------------------

VALID_METRICS = {'total', 'average', 'count'}


def query_database(search_text: str, metric: str) -> list[dict]:
    """Simulates DB query — returns mock records."""
    if search_text:
        return [{'name': f'Result for {search_text}', 'value': 100, 'metric': metric}]
    return [
        {'name': 'All Sales Q1', 'value': 500, 'metric': metric},
        {'name': 'All Sales Q2', 'value': 700, 'metric': metric},
    ]


def apply_filters(results: list[dict], filters: dict) -> list[dict]:
    """Simulates filter application — returns filtered subset."""
    if not results:
        return []
    active = [k for k, v in filters.items() if v]
    if not active:
        return results
    # Simulate filtering: keep only first record
    return [results[0]]


def persist_favorite(name: str, state: dict) -> bool:
    """Simulates saving a favorite search."""
    return bool(name and state)


def generate_xlsx(results: list[dict]) -> str:
    """Simulates XLSX generation — returns file URL."""
    if results:
        return '/exports/report.xlsx'
    return ''


def generate_csv(results: list[dict]) -> str:
    """Simulates CSV generation — returns file URL."""
    if results:
        return '/exports/report.csv'
    return ''


def process_sales_report_action(
    search_text: str,
    metric: str,
    filters: Optional[dict] = None,
    favorite_name: str = '',
    export_format: str = '',
) -> dict[str, Any]:
    """
    Core controller logic for Sales Report actions.
    Each if/elif is a predicate node in the CFG.
    """
    # ---- D0: Input validation ----
    if not isinstance(search_text, str) or metric not in VALID_METRICS:
        return {'error': 'Invalid input', 'results': [], 'saved': False, 'file_url': None}

    results: list[dict] = []
    saved = False
    file_url: Optional[str] = None
    current_state: dict[str, Any] = {}
    filters = filters or {}

    # ---- D1: Search logic (RHU02) ----
    if search_text and metric:                          # Predicate 1 (compound)
        results = query_database(search_text, metric)
        current_state['search'] = search_text
        current_state['metric'] = metric
    else:
        results = query_database('', 'total')
        current_state['search'] = ''
        current_state['metric'] = 'total'

    # ---- D2: Advanced filtering (RHU03) ----
    if filters and any(v for v in filters.values()):   # Predicate 2 (compound)
        results = apply_filters(results, filters)
        current_state['filters'] = filters
    else:
        current_state['filters'] = {}

    # ---- D3: Save favorite (RHU04) ----
    if favorite_name and not export_format:             # Predicate 3 (compound)
        saved = persist_favorite(favorite_name, current_state)

    # ---- D4 / D5: Export logic (RHU06) ----
    if export_format == 'xlsx':                         # Predicate 4
        file_url = generate_xlsx(results)
    elif export_format == 'csv':                        # Predicate 5
        file_url = generate_csv(results)

    return {
        'results': results,
        'saved': saved,
        'file_url': file_url,
        'state': current_state,
    }


# ==============================================================
# CFG: CONTROL FLOW GRAPH ANALYSIS
# ==============================================================
#                   ┌─────────────┐
#                   │    START    │
#                   └──────┬──────┘
#                          │
#                   ┌──────▼──────┐     T
#              ┌────│  D0: valid  │──────────► return error
#              │    └──────┬──────┘
#              │           │ F
#              │    ┌──────▼──────┐
#              │    │  D1: search │◄──── compound: search_text AND metric
#              │    │  & metric   │
#              │    └──┬───┬──────┘
#              │       │T  │F
#              │       ▼   ▼
#              │    ┌──────┐ ┌──────────┐
#              │    │query │ │query all │
#              │    └──┬───┘ └────┬─────┘
#              │       │         │
#              │       ▼         ▼
#              │    ┌──────────────────┐
#              │    │  D2: filters AND │◄──── compound: filters AND any active
#              │    │  any active      │
#              │    └──┬───┬───────────┘
#              │       │T  │F
#              │       ▼   ▼
#              │    ┌────────┐ ┌───────────┐
#              │    │apply   │ │keep       │
#              │    │filters │ │results    │
#              │    └──┬─────┘ └─────┬─────┘
#              │       │            │
#              │       ▼            ▼
#              │    ┌──────────────────────────┐
#              │    │ D3: favorite AND NOT     │◄──── compound
#              │    │ export_format            │
#              │    └──┬───┬───────────────────┘
#              │       │T  │F
#              │       ▼   ▼
#              │    ┌────────┐ ┌─────────┐
#              │    │ save   │ │ skip    │
#              │    │favorite│ │         │
#              │    └──┬─────┘ └────┬────┘
#              │       │            │
#              │       ▼            ▼
#              │    ┌──────────────────────┐
#              │    │ D4: export == xlsx   │
#              │    └──┬───┬───────────────┘
#              │       │T  │F
#              │       ▼   ▼
#              │    ┌────────┐ ┌──────────────────┐
#              │    │ generate│ │ D5: export == csv│
#              │    │ xlsx   │ └──┬───┬───────────┘
#              │    └──┬─────┘    │T  │F
#              │       │         ▼   ▼
#              │       │      ┌──────┐ ┌─────────┐
#              │       │      │csv   │ │ no      │
#              │       │      │export│ │ export  │
#              │       │      └──┬───┘ └────┬────┘
#              │       │         │          │
#              │       ▼         ▼          ▼
#              │    ┌───────────────────────────┐
#              │    │          RETURN           │
#              │    └───────────────────────────┘
#              │
#              └──── All paths converge at RETURN
#
# ==============================================================
# CYCLOMATIC COMPLEXITY V(G)
# ==============================================================
#   V(G) = Number of predicate nodes + 1
#   Predicate nodes: D0, D1, D2, D3, D4, D5  =  6
#   V(G) = 6 + 1 = 7
#
#   Also: V(G) = E - N + 2P
#   E = 17 edges, N = 12 nodes, P = 1 connected component
#   V(G) = 17 - 12 + 2 = 7  ✅
#
# ==============================================================
# 7 BASIS PATHS (INDEPENDENT PATHS)
# ==============================================================
#
# Path 1: D0-F → D1-F → D2-F → D3-F → D4-F → D5-F → RETURN
#   (No search, no filters, no favorite, no export)
#
# Path 2: D0-F → D1-T → D2-F → D3-F → D4-F → D5-F → RETURN
#   (Search only, no filters, no favorite, no export)
#
# Path 3: D0-F → D1-T → D2-T → D3-F → D4-F → D5-F → RETURN
#   (Search + filters, no favorite, no export)
#
# Path 4: D0-F → D1-T → D2-T → D3-T → D4-F → D5-F → RETURN
#   (Search + filters + save favorite, no export)
#
# Path 5: D0-F → D1-T → D2-T → D3-F → D4-T → RETURN
#   (Search + filters + XLSX export)
#
# Path 6: D0-F → D1-T → D2-T → D3-F → D4-F → D5-T → RETURN
#   (Search + filters + CSV export)
#
# Path 7: D0-T → RETURN (early exit on invalid input)
#
# ==============================================================
# DECISION / CONDITION COVERAGE
# ==============================================================
# Simple conditions to evaluate:
#   C1: isinstance(search_text, str)
#   C2: metric in VALID_METRICS
#   C3: search_text (truthy)
#   C4: metric (truthy)
#   C5: filters (truthy)
#   C6: any(v for v in filters.values())
#   C7: favorite_name (truthy)
#   C8: not export_format (truthy)
#   C9: export_format == 'xlsx'
#   C10: export_format == 'csv'
#
# Compound decisions (each needs T/F at least once):
#   D0: C1 AND C2
#   D1: C3 AND C4
#   D2: C5 AND C6
#   D3: C7 AND C8
#   D4: C9
#   D5: C10
# ==============================================================


# ---------------------------------------------------------------------------
# 2. UNIT TEST SUITE — 7 test methods from basis paths
# ---------------------------------------------------------------------------

class TestSalesReportController(unittest.TestCase):
    """7 test methods = 7 basis paths from the CFG (V(G) = 7)."""

    # ---- Path 1: No search, no filters, no favorite, no export -----------
    def test_path1_no_actions_default_flow(self) -> None:
        """Basis Path 1: All F-F-F-F — default state, no export."""
        result = process_sales_report_action(
            search_text='',
            metric='total',
            filters={},
            favorite_name='',
            export_format='',
        )
        self.assertNotIn('error', result)
        self.assertEqual(len(result['results']), 2)
        self.assertFalse(result['saved'])
        self.assertIsNone(result['file_url'])
        self.assertEqual(result['state']['search'], '')
        self.assertEqual(result['state']['metric'], 'total')
        self.assertEqual(result['state']['filters'], {})

    # ---- Path 2: Search only, no filters, no favorite, no export ---------
    def test_path2_search_only(self) -> None:
        """Basis Path 2: T search — query executes, no filter/fav/export."""
        result = process_sales_report_action(
            search_text='Laptops',
            metric='total',
            filters={},
            favorite_name='',
            export_format='',
        )
        self.assertNotIn('error', result)
        self.assertEqual(len(result['results']), 1)
        self.assertIn('Laptops', result['results'][0]['name'])
        self.assertFalse(result['saved'])
        self.assertIsNone(result['file_url'])

    # ---- Path 3: Search + filters, no favorite, no export ---------------
    def test_path3_search_and_filter(self) -> None:
        """Basis Path 3: T-T — search then apply filters."""
        result = process_sales_report_action(
            search_text='Laptops',
            metric='count',
            filters={'date_2026': True, 'team_sales': False},
            favorite_name='',
            export_format='',
        )
        self.assertNotIn('error', result)
        self.assertEqual(len(result['results']), 1)
        self.assertTrue(result['state']['filters']['date_2026'])
        self.assertFalse(result['saved'])
        self.assertIsNone(result['file_url'])

    # ---- Path 4: Search + filters + save favorite, no export ------------
    def test_path4_full_with_favorite(self) -> None:
        """Basis Path 4: T-T-T — search, filter AND save favorite."""
        result = process_sales_report_action(
            search_text='Laptops',
            metric='average',
            filters={'date_2026': True},
            favorite_name='My Laptop Report',
            export_format='',
        )
        self.assertNotIn('error', result)
        self.assertEqual(len(result['results']), 1)
        self.assertTrue(result['saved'])
        self.assertIsNone(result['file_url'])

    # ---- Path 5: Search + filters + XLSX export -------------------------
    def test_path5_xlsx_export(self) -> None:
        """Basis Path 5: T-T + D4-T — search, filter, export to XLSX."""
        result = process_sales_report_action(
            search_text='Laptops',
            metric='total',
            filters={'date_2026': True},
            favorite_name='',
            export_format='xlsx',
        )
        self.assertNotIn('error', result)
        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['file_url'], '/exports/report.xlsx')
        self.assertFalse(result['saved'])

    # ---- Path 6: Search + filters + CSV export --------------------------
    def test_path6_csv_export(self) -> None:
        """Basis Path 6: T-T + D4-F/D5-T — search, filter, export to CSV."""
        result = process_sales_report_action(
            search_text='Laptops',
            metric='total',
            filters={'date_2026': True},
            favorite_name='',
            export_format='csv',
        )
        self.assertNotIn('error', result)
        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['file_url'], '/exports/report.csv')
        self.assertFalse(result['saved'])

    # ---- Path 7: Invalid input → early return ---------------------------
    def test_path7_invalid_input_validation_error(self) -> None:
        """Basis Path 7: D0-T — invalid input triggers early error return."""
        result = process_sales_report_action(
            search_text=12345,       # not a string
            metric='total',
            filters={},
            favorite_name='',
            export_format='',
        )
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Invalid input')

        result = process_sales_report_action(
            search_text='Laptops',
            metric='invalid_metric',  # not in VALID_METRICS
        )
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Invalid input')


# ---------------------------------------------------------------------------
# 2.b DECISION / CONDITION COVERAGE — Supplementary tests
# ---------------------------------------------------------------------------

class TestDecisionConditionCoverage(unittest.TestCase):
    """Ensures every simple condition takes both T and F at least once."""

    def test_d0_validation_conditions(self) -> None:
        """C1=F: non-string search → error / C2=F: invalid metric → error."""
        r1 = process_sales_report_action(search_text=42, metric='total')
        self.assertIn('error', r1)

        r2 = process_sales_report_action(search_text='ok', metric='bogus')
        self.assertIn('error', r2)

    def test_d1_search_conditions(self) -> None:
        """C3=F: empty search → all results / C4 is always T (validated)."""
        r = process_sales_report_action(search_text='', metric='total')
        self.assertEqual(len(r['results']), 2)

        r2 = process_sales_report_action(search_text='X', metric='total')
        self.assertEqual(len(r2['results']), 1)

    def test_d2_filter_conditions(self) -> None:
        """C5=F: None filters → no filter applied / C6=F: all inactive."""
        r1 = process_sales_report_action(
            search_text='X', metric='total', filters=None,
        )
        self.assertNotIn('error', r1)

        r2 = process_sales_report_action(
            search_text='X', metric='total',
            filters={'a': False, 'b': False},
        )
        self.assertNotIn('error', r2)

    def test_d3_favorite_conditions(self) -> None:
        """C7=F: empty name → no save / C8=F: export active → no save."""
        r1 = process_sales_report_action(
            search_text='X', metric='total',
            favorite_name='', export_format='',
        )
        self.assertFalse(r1['saved'])

        r2 = process_sales_report_action(
            search_text='X', metric='total',
            favorite_name='My Fav', export_format='xlsx',
        )
        self.assertFalse(r2['saved'])

    def test_d4_d5_export_conditions(self) -> None:
        """C9=T: xlsx / C10=T: csv / Both F: no export."""
        r1 = process_sales_report_action(search_text='X', metric='total', export_format='xlsx')
        self.assertEqual(r1['file_url'], '/exports/report.xlsx')

        r2 = process_sales_report_action(search_text='X', metric='total', export_format='csv')
        self.assertEqual(r2['file_url'], '/exports/report.csv')

        r3 = process_sales_report_action(search_text='X', metric='total', export_format='')
        self.assertIsNone(r3['file_url'])


# ---------------------------------------------------------------------------
# 3. RUNNER — coverage measurement entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
