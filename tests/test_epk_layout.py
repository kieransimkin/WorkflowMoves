import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('epk_layout', Path(__file__).parents[1]/'tools/audit_epk_layout.py')
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)


def observation(width):
    return dict(width=width, height=900, measured_width=width, measured_height=900,
                client_width=width, scroll_width=width, overflow=False, ready_state='complete', evidence_kind='emulated',
                content_overflow=[], text_overflow=[], clipped_text=[], scrolling_descendants=[], offscreen_focus_links=[], visible_images=[],
                alignments=[dict(selector='.art', matches=1, container_matches=1, expected='center',
                                 target=dict(left=30, right=width-30), container=dict(left=14, right=width-14))],
                screenshot=dict(path=f'fixture-{width}.jpg', width=width, height=900, reviewed=True), below_fold_reviewed=True)


def widths():
    return [observation(width) for width in module.REQUIRED_WIDTHS]


class LayoutTests(unittest.TestCase):
    def test_complete_matrix_and_extra_breakpoint_pass(self):
        self.assertEqual(module.audit_widths(widths()+[observation(421)]), [])

    def test_old_single_phone_matrix_cannot_pass(self):
        self.assertTrue(module.audit_widths([observation(w) for w in (390,900,1440)]))

    def test_hidden_overflow_with_no_document_scroll_fails(self):
        rows=widths(); row=next(r for r in rows if r['width']==430)
        row['content_overflow']=[dict(selector='h1',right=463)]
        self.assertFalse(row['overflow'])
        self.assertTrue(module.audit_widths(rows))

    def test_clipped_text_and_identifiers_fail(self):
        for field in ('clipped_text','text_overflow'):
            rows=widths(); rows[0][field]=[dict(selector='p')]
            self.assertTrue(module.audit_widths(rows))

    def test_asymmetric_artwork_gutters_fail(self):
        rows=widths(); row=next(r for r in rows if r['width']==390)
        row['alignments'][0]['target']=dict(left=14,right=340)
        self.assertTrue(module.audit_widths(rows))

    def test_unapplied_phone_viewport_fails(self):
        rows=widths(); rows[0]['measured_width']=1280
        self.assertTrue(module.audit_widths(rows))

    def test_miniature_screenshot_on_wrong_canvas_fails(self):
        rows=widths(); rows[4]['screenshot']['height']=242
        self.assertTrue(module.audit_widths(rows))

    def test_browser_pixel_rounding_is_bounded(self):
        rows=widths(); rows[1]['screenshot']['height']=899
        self.assertEqual(module.audit_widths(rows),[])
        rows[1]['screenshot']['height']=898
        self.assertTrue(module.audit_widths(rows))

    def test_missing_measurements_are_not_zero(self):
        for field in ('content_overflow','text_overflow','clipped_text','alignments','visible_images','measured_width'):
            rows=widths(); del rows[0][field]
            self.assertTrue(module.audit_widths(rows))

    def test_unreviewed_capture_and_below_fold_fail(self):
        for field in ('reviewed','below_fold_reviewed'):
            rows=widths()
            if field=='reviewed': rows[0]['screenshot'][field]=False
            else: rows[0][field]=False
            self.assertTrue(module.audit_widths(rows))

    def test_intentional_scroller_needs_review(self):
        rows=widths(); rows[0]['scrolling_descendants']=[dict(container='nav')]
        self.assertTrue(module.audit_widths(rows))
        rows[0]['scrolling_containers_reviewed']=True
        self.assertEqual(module.audit_widths(rows), [])

    def test_skip_link_needs_focus_review(self):
        rows=widths(); rows[0]['offscreen_focus_links']=[dict(selector='.skip')]
        self.assertTrue(module.audit_widths(rows))
        rows[0]['focus_links_reviewed']=True
        self.assertEqual(module.audit_widths(rows), [])

    def test_incomplete_image_and_document_fail(self):
        rows=widths(); rows[0]['visible_images']=[dict(complete=True,natural_width=0)]
        self.assertTrue(module.audit_widths(rows))
        rows=widths(); rows[0]['ready_state']='loading'
        self.assertTrue(module.audit_widths(rows))

    def test_duplicate_boolean_nonfinite_and_invalid_alignment_fail(self):
        self.assertTrue(module.audit_widths(widths()+[copy.deepcopy(widths()[0])]))
        for value in (True,float('nan'),float('inf')):
            rows=widths(); rows[0]['measured_width']=value
            self.assertTrue(module.audit_widths(rows))
        rows=widths(); rows[0]['alignments'][0]['tolerance']=500
        self.assertTrue(module.audit_widths(rows))


if __name__=='__main__': unittest.main()
