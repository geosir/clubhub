Club Hub
========
A Digital Event System for Schools (Version 4.1.2)

> *Club Hub is now a hosted service! Visit [clubhub.live](https://clubhub.live) for more info.*

> *For a working example of what Club Hub can do, check out* [example.clubhub.live](https://example.clubhub.live "Club Hub") *and*
[example.clubhub.live/present](https://example.clubhub.live/present "Club Hub LIVE").

**See what's next in one glance: Club Hub is a webservice that automatically displays events and posters neatly and intuitively.**
It is designed for schools and other organizations with large amounts of communications about events and activities.

The service comes in three main parts:

1. **A central online event listing.** This event listing is automatically generated from event data.
Past events are hidden and upcoming events are listed chronologically. This listing is searchable and scrollable,
and also features links that generate Google Calendar events.

2. **A live-updated poster slideshow.** This slideshow is generated automatically like the event listing, and can
be shown on web-enabled digital displays (Chromecasts, Smart TVs, etc.).
By default, it displays all posters, but it can also be set to display a subset of posters in a specific "Display Group."

3. **An intuitive administration interface.** Events are easily edited and approved as objects in Django's beautiful online
database manager. It is also simple to add additional accounts for approving events and regularly submitting and editing events.

Club Hub is a Dockerized Django application, which means that it's easy to deploy on your own server for your organization's needs!
Read on for more info. It is also a hosted cloud service&mdash;visit [clubhub.live](https://clubhub.live) for more details.

Getting Club Hub
----------------

Club Hub is a hosted cloud service operated by George Moe.
Visit [clubhub.live](https://clubhub.live) to learn more about its features and pricing,
and to sign up for a deployment for your organization.

The Club Hub source code is also available for non-commercial use.
Contact George Moe at [george@george.moe](mailto:george@george.moe) for a distribution of the
latest version of Club Hub.

The Club Hub Source Code
========================

Below are some instructions regarding deploying Club Hub from source.

Club Hub is meant to be deployed as a Dockerized application. However,
these instructions can be modified to deploy it as a standalone service.
More can be learned about the deployment process by reading the `Dockerfile` and
`runclubhub*.sh` scripts.

Organization
----------------

The Club Hub source code directory contains the following:

1. Scripts to help setup Club Hub's application and database containers.
2. A `Dockerfile` used by the scripts to spawn the Club Hub container.
3. `clubhub.conf`, an Apache configuration file used by the Dockerfile.
4. The Club Hub source code needed to build the site.

Install
----------------

Installing the backend:

1. Begin by configuring `clubhub/clubhub/settings.py` to suit your needs.
    1. Generate a new `SECRET_KEY`.
    2. Change `ALLOWED_HOSTS` to your domain name(s).
    3. Update your `DATABASES` information to suit your application.
    4. Specify the appropriate `TIME_ZONE`.
    5. Finally, update the `EMAIL_*` parameters to point to your mailserver and account.
2. Update the information in `runclubhubdb.sh` to match the database user, name, and password you specified in `settings.py`.
3. Run `runclubhubdb.sh` AND THEN run `runclubhub.sh`. Let them work their magic :)
4. You need to run some first-time setup to begin administering Club Hub.
This involves creating a Django superuser account and running some inital database imports.
    1. Do `docker exec -it clubhub /bin/bash`. Once you're in the container shell, run `one_time_setup.sh`.

Club Hub is now up and running!
All you need to do now is to make Club Hub accessible from the web.
You can do this by pointing your webserver to Club Hub's Docker IP (which can be seen with `docker inspect clubhub | grep IPAddress`).

Once Club Hub is online, be sure to edit the Settings in the admin panel to suit your needs.
In particular, you should set the `CLUBHUB_CONTACT_EMAIL` setting.
More guidance on settings can be found in the **Settings** section of this README.

You can customize Club Hub by editing the templates in `clubhub/main/templates`.
In particular,
 * `main` contains the templates for the main event listing,
 * `present` contains the templates for the poster slideshow,
 * `submit` contains the templates for the Event Registration Form,
 * `mail` contains the templates for Club Hub's automatic email notifications, and
 * `registration` contains the templates for Club Hub's account management routes.

If you need to make customizations to the Club Hub site, make sure you run `runclubhub.sh` to update you docker deployment.

You'll also see several new folders around: `backup` and `media`.
These folders allow you to save vital clubhub assets.
You can backup the Club Hub database from the Docker into `backup`
by running the `backupclubhubdb.sh` script.
All posters uploaded to Club Hub will be stored in `media`.

Using and Administering Club Hub
----------------

*To see a working deployment of Club Hub, check out* [example.clubhub.live](https://example.clubhub.live).

Now that Club Hub is set up, you can navigate its pages on the web!
The homepage is a summary of upcoming events, featuring the event date, poster, event name, event host, description, time, and location.
This list is searchable via the search bar at the top of the page. Entries can also be collasped by clicking on their header bar.
Each entry also features a Google Calendar button that generates a calendar event when clicked.

Club Hub users submit new posters at the `/submit` page.
This is accessible directly, as well as through the "Register an Event" button at the bottom of the page.
Submitting an event is as easy as completing the online form and uploading a poster.
These submissions are aggregated in the adminstration panel, Club Hub Central.

Club Hub Central can be accessed at the `/admin` URL.
You can log in with the superuser credentials you created during installation; after logging in, you can create more users with different passwords and privileges.

Administering events is easy. First, enter the event view by clicking on the "Events" link in the administration panel. Then, simply select the events you want to approve for display and choose "Approve selected events" in the Actions dropdown and hit "Go". You can also modify individual events by clicking on their name.

You can enlist other users to help you with administration.
There are three kinds of users:
* **Superusers** are the technical administrators of Club Hub.
They can change Club Hub's settings, as well as define the available Locations and Display Groups.
Superusers can also create and manage user accounts.
* **Approvers** are Club Hub's main event administrators.
They have full access over all events in the Club Hub database,
and can create, modify, and delete them as needed. Their main role is
to review new events and approve them for display on the Club Hub's public pages.
* **Editors** are privileged event submitters.
They can create and edit events directly in the Club Hub database without needing to use
the submission form.
However, they can only see events which they have created and which have not yet been approved.
They can also delete events which they can see (those they own and have not yet been approved).
This role is meant to be given to frequent users that consistently submit valid events.

Users can be designated to these roles by adding them to the appropriate Group.
Superusers can be created by checking the Superuser option on the User's profile.

To deploy Club Hub on digital displays, you can direct the displays to show the `/present` page. This will display all events by default. To display specific subsets of posters, assign them to a Display Group and use the `/present?group=<display group name>` endpoint instead.

Settings
--------

The Settings model control in the admin panel is a nice way to manage Club Hub's dynamic variables.
You can change these settings at any time and Club Hub will immedately change to reflect them
without needing a reboot via `runclubhub.sh`.

Setting keys and their appropriate values are explained below:


| Key                     	| Expected Value                                                                                                                    	|
|-------------------------	|-----------------------------------------------------------------------------------------------------------------------------------	|
| `CLUBHUB_CONTACT_EMAIL` 	| A single email address managed by the Club Hub Administrator. This key may only be used once.                                                                    	|
| `ALLOWED_EMAIL_SUFFIX`  	| An email suffix (e.g. `@example.com`) which users are permitted to use to sign up.  This key can be used as many times as needed. 	|

Attribution
----------------

The original idea and framework was formulated, designed, tested, and coded by [George Moe](https://george.moe "George's Website") since 2014. Attribution would be very much appreciated.

This work is distributed under an MIT license. See `LICENSE.md` for more details.

Contact and Support
----------------

If you have any questions or comments, or if you would like a flavor of Club Hub custom-built for your use case, you can contact George Moe at [george@george.moe](mailto:george@george.moe "Email George Moe").
