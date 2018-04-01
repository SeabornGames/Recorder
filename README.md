# SeabornRecorder
SeabornRecorder will proxy an object and record all
    all getattr, setattr, method calls, and instantiations

## Example:
SeabornTable = get_recorder(SeabornTable)
table = SeabornTable(data)
table.deliminator = '/'
print(str(table))
...
SeabornTable.access_log would have three AttributeRecorders
    1. init SeabornTable
    2. set attribute value
    3. method call to str

# TestRecorder
TestRecorder subclasses SeabornRecorder, with the added capability
to monitor the test being run and then record a duplicate test
based on only the object calls.

This is useful for when class "A" is used in a third party test, and
you want to create a test for class "A" without the third party software.


