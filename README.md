# Bike2Work @ CERN

Sync Bike2Work rides from Strava to CERN Sharepoint.

## Configuration

Create the configuration file `~/.config/bike2cern/sync.cfg` with the
following contents (adjusted):

    [strava]
    client_id = 12345
    secret = deadbeef0123456789

    [cern]
    username = johndoe
    list_id = dead-beef-01234-56789

Client ID and secret can be obtained on
[Strava](https://www.strava.com/settings/api), the `list_id` identifies
which calendar to use for the CERN Sharepoint.

Save the CERN password in the system keyring:

    keyring set bike2cern cern

Upon first usage, `bike2cern` will request a Strava access token.

## Usage

Use with a start and end date (rides on the day of the end date will not be
synced), e.g., for the first half of the year:

    bike2cern --dry-run 2017-01-01 2017-07-01

Remove `--dry-run` to actually do the sync.  **Use at your own risk, syncing
too much will require manual deletion!**
