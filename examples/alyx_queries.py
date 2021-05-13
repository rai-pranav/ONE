"""
Examples of using ONE to query Alyx via Django REST queries.

Alyx queries require and internet connection and are slower than the local cache queries using
one.search, however it is much more powerful.  Searching for datasets or sessions based solely on
the fields in `one.search_terms` should be done using one.search.  This script demonstrates some
of the more complex queries that must be done remotely.
"""
from one.api import ONE, OneAlyx

one = ONE()
assert isinstance(one, OneAlyx)

# Full documentation of using Alyx REST interface can be found at
# https://openalyx.internationalbrainlab.org/docs

# List the available endpoints:
print(one.alyx.list_endpoints())

# query sessions that have histology available
ses = one.alyx.rest('sessions', 'list', histology=True)
# the generic way
ses = one.alyx.rest('sessions', 'list',
                    django="subject__actions_sessions__procedures__name,Histology")

# query sessions having specific channel locations (hierarchical, will fetch everything below)
ses = one.alyx.rest('sessions', 'list', atlas_id=500)
ses = one.alyx.rest('sessions', 'list', atlas_acronym="MO")
ses = one.alyx.rest('sessions', 'list', atlas_name="Somatomotor areas")


# query sessions that do not have matlab in the project name
ses = one.alyx.rest('sessions', 'list', django='~project__name__icontains,matlab')

# query sessions that do not contain a given dataset type
ses = one.alyx.rest('sessions', 'list',
                    django='~data_dataset_session_related__dataset_type__name__icontains,wheel')

# FIXME Use to_eid instead
def session_response_to_eids(ses):
    """A simple function to return a list of eids from a sessions list response"""
    return [x['url'][-36:] for x in ses]

# query probe insertions for a given task protocol
one.alyx.rest('insertions', 'list', django='session__task_protocol__icontains,choiceworld')

