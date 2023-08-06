"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

import os
import unittest

from datetime import datetime

from stellanow_cli.code_generators import CsharpCodeGenerator
from stellanow_cli.api import StellaEventDetailed, StellaField, StellaEntity


class TestCsharpCodeGenerator(unittest.TestCase):
    def test_generate_class_handles_all_valueTypes(self):
        # Define an event with each valueType
        event = StellaEventDetailed(
            id="1",
            name="test_event",
            entities=[
                StellaEntity(id='', name="entity1"),
                StellaEntity(id='', name="entity2"),
            ],
            fields=[
                StellaField(id='', name="field1", valueType="Decimal"),
                StellaField(id='', name="field2", valueType="Integer"),
                StellaField(id='', name="field3", valueType="Boolean"),
                StellaField(id='', name="field4", valueType="String"),
                StellaField(id='', name="field5", valueType="Date"),
                StellaField(id='', name="field6", valueType="DateTime"),
            ],
            isActive=True,
            createdAt=datetime(2022, 1, 1).strftime("%Y-%m-%dT%H:%M:%S"),
            updatedAt=datetime(2022, 1, 2).strftime("%Y-%m-%dT%H:%M:%S"),
            description="Test event"
        )

        # Generate the class
        generated_class = CsharpCodeGenerator.generate_class(event)

        # Save to file during debug
        # file_path = os.path.join('output', 'test.cs')
        # with open(file_path, "w") as file:
        #     file.write(generated_class)

        # Check that each field is added with the correct conversion
        self.assertIn('AddField("field1", field1.ToString("F2", CultureInfo.InvariantCulture));', generated_class)
        self.assertIn('AddField("field2", field2.ToString());', generated_class)
        self.assertIn('AddField("field3", field3.ToString().ToLower());', generated_class)
        self.assertIn('AddField("field4", field4);', generated_class)
        self.assertIn('AddField("field5", field5.ToString("yyyy-MM-dd"));', generated_class)
        self.assertIn('AddField("field6", field6.ToString("yyyy-MM-ddTHH:mm:ssZ"));', generated_class)


if __name__ == "__main__":
    unittest.main()
