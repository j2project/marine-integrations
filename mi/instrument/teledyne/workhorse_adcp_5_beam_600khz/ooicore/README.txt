Driver code for the VADCP instrument
====================================

See https://confluence.oceanobservatories.org/display/ENG/VADCP+Driver

Some development notes:

2012-06-18:
- overall review, some adjustment and clean-up, and more comments in the code.

2012-06-13:
- some code review, pyflakes fixes, documentation on confluence.
- all the tests at the moment:
    $ VADCP="mi/instrument/teledyne/workhorse_adcp_5_beam_600khz/ooicore/connection.yml" bin/nosetests -v mi/instrument/teledyne/workhorse_adcp_5_beam_600khz
    test_all_tests (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_client.Test) ... ok
    test_connect_disconnect (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_client.Test) ... ok
    test_execute_run_recorder_tests (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_client.Test) ... ok
    test_get_latest_sample (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_client.Test) ... ok
    test_get_metadata (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_client.Test) ... ok
    test_start_and_stop_autosample (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_client.Test) ... ok
    test_connect_disconnect (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver.Test) ... ok
    test_execute_get_latest_sample (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver.Test) ... ok
    test_execute_get_metadata (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver.Test) ... ok
    test_execute_run_all_tests (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver.Test) ... ok
    test_execute_run_recorder_tests (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver.Test) ... ok
    test_start_and_stop_autosample (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver.Test) ... ok
    test_connect_disconnect (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver0.Test) ... ok
    test_execute_get_latest_sample (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver0.Test) ... ok
    test_execute_get_metadata (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver0.Test) ... ok
    test_execute_run_all_tests (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver0.Test) ... ok
    test_execute_run_recorder_tests (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver0.Test) ... ok
    test_start_and_stop_autosample (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver0.Test) ... ok
    test_connect_disconnect (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver_proc.Test) ... ok
    test_execute_get_latest_sample (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver_proc.Test) ... ok
    test_execute_get_metadata (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver_proc.Test) ... ok
    test_execute_run_all_tests (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver_proc.Test) ... ok
    test_execute_run_recorder_tests (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver_proc.Test) ... ok
    test_start_and_stop_autosample (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver_proc.Test) ... ok
    test_pd0 (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_pd0.Test) ... ok
    test_partial_match_close (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_ts.Test) ... ok
    test_partial_match_open (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_ts.Test) ... ok
    test_all_tests (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_unit_client.Test) ... ok
    test_connect_disconnect (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_unit_client.Test) ... ok
    test_execute_run_recorder_tests (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_unit_client.Test) ... ok
    test_get_latest_sample (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_unit_client.Test) ... ok
    test_get_metadata (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_unit_client.Test) ... ok
    test_start_and_stop_autosample (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_unit_client.Test) ... ok

    ----------------------------------------------------------------------
    Ran 33 tests in 456.395s

    OK


2012-06-11:
- new UnitClient based on what VadcpClient had until now, which was specific
  to a particular unit. Now, VadcpClient has two UnitClient objects, which
  will be used to control and integrate responses from the two units.

  Two of the key command operations are "break" and "CS" (start pinging).
  Assuming other relevant master-slave configuration settings are in
  place, these operations basically consist of sending the corresponding
  command first to the slave unit (5th beam) and then to the master (4-beam).
  For the CS command in particular, this order is needed "to ensure exact
  timing between the Master and Slave systems."

2012-06-10:
- Incorporating concept of "VADCP unit" to refer to the particular unit, either
  the 4-beam unit or the 5th beam unit. Each unit has a raw connection and an
  OOI Digi connection.


2012-06-08:
- troubleshooting access to 5th beam with Dana enabling an OOI digi interface
  as with the 4-beam unit.
- adding get operations to PD0DataStructure to retrieve time-related
  information, which I'll be using to correlate ensembles from both units,
  probably in combination with the OOI Digi timestamping, but in general
  while a proper timestamping mechanism is implemented according to Bill.

2012-06-05:
- implement "break" command, which needs connection to the OOI digi.
- initial implementation of start_autosample and stop_autosample.

    $ VADCP="mi/instrument/teledyne/workhorse_adcp_5_beam_600khz/ooicore/connection.yml" \
      bin/nosetests -v mi/instrument/teledyne/workhorse_adcp_5_beam_600khz
    ...
    ----------------------------------------------------------------------
    Ran 27 tests in 261.790s

    OK

2012-06-04:
- added ad hoc connection.yml to indicate the various hosts/ports needed to
  interact with both the 4-beam system and the 5th beam system. In particular,
  additional functionality is to send "break" commands via the OOI Digi
  interface (10.180.80.178 port 2102). The environment variable VADCP can also
  be given the name of the connection.yml file, for ex:
    $ VADCP="mi/instrument/teledyne/workhorse_adcp_5_beam_600khz/ooicore/connection.yml" \
      bin/nosetests mi/instrument/teledyne/workhorse_adcp_5_beam_600khz/ooicore/test/test_client.py

2012-05-30:
- some reorganization of the code
- implemented a workaround to be able to run the unit tests involving the
  client's receiver object (which by defatult uses threading.Thread) within
  the regular bin/nosetests execution. The workaround is simply to use a
  Greenlet instead of Thread only in such cases. Now I can do a single call to
  run all available tests:

    $ VADCP="10.180.80.178:2101" bin/nosetests mi/instrument/teledyne/workhorse_adcp_5_beam_600khz
    ...
    Ran 23 tests in 165.632s

    OK

2012-05-29:
- Renamed "600khz_workhorse_adcp_5_beam" to "workhorse_adcp_5_beam_600khz"
  in the path (leading digit would cause syntax error).
- Migrated code to new mi repo. Did all needed adjustments to paths and
  imports.

- All tests passing:
    $ VADCP="10.180.80.178:2101" bin/nosetests -sv mi/instrument/teledyne/workhorse_adcp_5_beam_600khz
    ...
    Ran 22 tests in 76.248s

    OK (SKIP=14)

- The 14 tests skipped above can also be forced to run via defining the "run_it"
  environment variable and excluding extern/pyon in bin/nosetests (to avoid
  issues related with gevent monkey-patching):

    $ run_it= VADCP="10.180.80.178:2101"  bin/nosetests -sv mi/instrument/teledyne/workhorse_adcp_5_beam_600khz/ooicore/test/test_client.py
    test_all_tests (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_client.ClientTest) ... ok
    test_connect_disconnect (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_client.ClientTest) ... ok
    test_get_latest_sample (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_client.ClientTest) ... ok
    test_get_metadata (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_client.ClientTest) ... ok

    ----------------------------------------------------------------------
    Ran 4 tests in 28.914s

    OK

    $ run_it= VADCP="10.180.80.178:2101"  bin/nosetests -sv mi/instrument/teledyne/workhorse_adcp_5_beam_600khz/ooicore/test/test_driver.py
    test_connect_disconnect (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver.DriverTest) ... ok
    test_execute_get_latest_sample (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver.DriverTest) ... ok
    test_execute_get_metadata (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver.DriverTest) ... ok
    test_execute_run_all_tests (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver.DriverTest) ... ok
    test_execute_run_recorder_tests (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver.DriverTest) ... ok

    ----------------------------------------------------------------------
    Ran 5 tests in 29.354s

    OK

    $ run_it= VADCP="10.180.80.178:2101"  bin/nosetests -sv mi/instrument/teledyne/workhorse_adcp_5_beam_600khz/ooicore/test/test_driver0.py
    test_connect_disconnect (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver0.DriverTest) ... ok
    test_execute_get_latest_sample (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver0.DriverTest) ... ok
    test_execute_get_metadata (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver0.DriverTest) ... ok
    test_execute_run_all_tests (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver0.DriverTest) ... ok
    test_execute_run_recorder_tests (mi.instrument.teledyne.workhorse_adcp_5_beam_600khz.ooicore.test.test_driver0.DriverTest) ... ok

    ----------------------------------------------------------------------
    Ran 5 tests in 30.941s

    OK



2012-05-28:
- instrument_driver.py: refactor construction of LoggerClient via a
  _build_connection method that subclasses can overwrite as needed. In the
  case of the VADCP, this is a Client object instead of LoggerClient.
- driver.py is now based on the general framework scheme including FSMs.
- The preliminary INT tests go as follows:
    $ VADCP="10.180.80.178:2101" bin/nosetests -sv ion/services/mi/drivers/vadcp/test/test_driver_proc.py
    test_connect_disconnect (ion.services.mi.drivers.vadcp.test.test_driver_proc.DriverTest) ... ok
    test_execute_get_latest_sample (ion.services.mi.drivers.vadcp.test.test_driver_proc.DriverTest) ... ok
    test_execute_get_metadata (ion.services.mi.drivers.vadcp.test.test_driver_proc.DriverTest) ... ok
    test_execute_run_all_tests (ion.services.mi.drivers.vadcp.test.test_driver_proc.DriverTest) ... ok
    test_execute_run_recorder_tests (ion.services.mi.drivers.vadcp.test.test_driver_proc.DriverTest) ... ok

    ----------------------------------------------------------------------
    Ran 5 tests in 76.442s

    OK

- driver0.py and test_driver0.py now contain the simpler version that directly
  uses the Client class and no protocol nor FSMs.

2012-05-24:
- more preparations while reviewing the workhorse documentation, in particular,
  "Workhorse Commands and Output Format" and "Workhorse 5 Beam ADCP."
- preliminary tests and supporting code.
- preparing to move code to the new mi repo, whose buildout is working better.

2012-05-21:
- Improved algorithms for parsing of incoming stream and reorg code now using
  coroutines in a more clear and reusable way.
- Validating extraction of PD0 ensembles by checking that values make sense
  and also comparing with output from an ad hoc program in java using SIAM.

2012-05-18:
- Along with PD0 binary ensembles, also parsing incoming stream for timestamps,
  see direct.py. Strategy implemented based on generators.
  TODO refactor this functionality for easier integration with driver framework.

2012-05-16:
- started coding supporting stuff. SIAM code being a very good reference.
- vadcp/pd0.py: PD0DataStructure to capture a PD0 ensemble.
- vadcp/test/pd0_sample.bin contains an ensemble captured with the
  vadcp/test/direct.py program
- unit tests for the PD0DataStructure class.
