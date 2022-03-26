#!/usr/bin/env python
from __future__ import print_function

import os
import subprocess
import unittest


class MainTestCase(unittest.TestCase):
    def test_files(self):
        for filename in os.listdir('infiles'):
            if filename.endswith('.txt'):
                res = subprocess.run(
                    ['repx', '/$/a/', 'infiles/%s' % filename],
                    capture_output=True,
                    # text=True,
                )
                output = res.stdout
                expected_output = ''
                with open('outfiles/%s' % filename, 'rb') as f:
                    expected_output = f.read()
                self.assertEqual(output, expected_output)
