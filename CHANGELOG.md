CLUB HUB 4.1.0 CHANGELOG
========================
2017-10-15

This update to Club Hub introduces user accounts and campus-internal events.

**Changes to the Club Hub Framework:**

* Support for "campus-internal" events, which are only visible
to logged-in users.
* Support for user creation, email confirmation, email-suffix
limiting, and password reset.
* New custom SendGrid Django Email Backend to support django's
native email features and uses.
* Views to support Hub Group Pages.
* Small changes to model names (DisplayGroup -> HubGroup) and
help text.

**Changes to the Club Hub Website:**

* New Hub Group Pages, which show events specific to that Hub
Group.
* A new 'parties' Hub Group page with a dark-neon CSS style.
* Style updates, including nicer message pages and better
automatic return-to-home countdowns.


4.1.4
-----
2019-10-30

* Update Django version to 1.11.23 to fix security vulnerabilities.
* Migrate from Bower to use Yarn, as recommended.

4.1.3
-----
2019-08-13

* Froze proper module versions in requirements.txt.
* Update to use Ubuntu 18.04 LTS in container.
* Update to use python sendgrid 6.0 (API v3)
* Updated README with more detailed documentation.
* Small style fixes.
* Bugfixes.

4.1.2
-----

* Added working migration survival.
* Removed parties link from frontpage; the organization can add one
easily themselves.
* Cleaned up code.

4.1.1
-----

* Improved search function.
* Improved menu layout.
* Made events linkable via ID.
* Small style updates:
    * Added info on loggin in.
    * Updated Read More link to a Skeleton CSS button.
    * Added a "HAPPENING NOW" highlight for ongoing events.





CLUB HUB 4.0.0 CHANGELOG
==============================
2017-09-30

This major update to Club Hub reworks the event display interface
and offers significant new features in event management
and registration.

**Changes to the Club Hub Framework:**

* Created Approver and Editor roles for more flexible control
 over the event registration process.
* Enabled Display Groups to allow for subsets of posters to
 be displayed on Club Hub LIVE.
* Created models for Locations and Display Groups so that
 they can be edited on-the-fly.
* Changed email system to use SMTP instead of SendGrid.
 Updated email styles and formatting.

**Changes to the Club Hub Website:**

* Major overhaul of the main event listing. Events are now
 displayed as a scrollable chronological list.
* Added a search function to the main event listing. This
 replaces the sorting and filtering functions of previous
 versions.
* Added an event preview on the Club Hub Event Registration
 form.
* Style updates and unifications across public pages.

4.0.1
-----

* Updated Google Analytics to gtag.js.
* Added Google Analytics event tracking capabilities.
* Fixed bug where quotation marks and apostrophes from the
registration form were over-sanitized.
* Style updates to layout: slicker sticky header behavior,
and moved buttons to top of page.
* Added validation to ensure that an event's End Date/Time
is not earlier than its Start Date/Time.
* Gave each event an ID so that they are linkable.


CLUB HUB 3.1.0 CHANGELOG
==============================
2016-10-28

This update features improvements to time entries in the database.

**Changes to the Club Hub Framework:**

* Moved away from django-easy-timezones (timezone over
 GeoIP), instead implementing an option for users to
 select their correct time zone at first visit.
* Events now have a Start and End time, allowing for posters
 to be shown after start time but before the event ends.

**Changes to the Club Hub Website:**

* Date/Time entry on the submission form is now in an intuitive
 12-hour time format, instead of the weird dd/MM/YY HH:mm
 it was before.
* Added a select box for the user to choose their timezone.
* Added a modal dialog and a Cookie to alert users to
 pick their timezone upon first visit.

CLUB HUB 3.0.0 CHANGELOG
==============================
2016-08-21

This version of Club Hub features a migration to Django,
along with major UX updates.

**Changes to the Club Hub Framework:**

* Migrated to Django. Moved from a Google App Script storage
 and submisson system to Django's database system.

**Changes to the Club Hub Website:**

* Improved UX around the site
* Added an adminstration panel for ease of management

CLUB HUB 2.5.0 CHANGELOG
==============================
2016-04-08

This is the first version that is ready for use at IMSA.

**Changes to the Club Hub Framework:**

* Fixed some broken links to george.moe after it was reorganized.
* Cleaned up code.

**Changes to the Club Hub Website:**

* Fixed stability and memory issues with SUD Cast on Chromecasts.
* Optimized Club Hub Present and the Synchronized Universal Display to use
 an in-house lightweight jQuery slideshow solution.
* Cleaned up code.

CLUB HUB 2.2.0 CHANGELOG
==============================

**Changes to the Club Hub Framework:**

* Now packaged and reorganized on Github so that other organizations can download and install it.
* Added comments to the entire codebase.

**Changes to the Club Hub Website:**

* New Synchronized Universal Display page
* SUD now can create slideshows based on groups entered into CHER through use of the ?group= querystring.
* SUD can now create slides for fullscreen posters.
* SUD can now respect posters which have requested not to be included in the slideshow.
* SUD now has an offline mode that prevents it from refreshing (and therefore stopping) when there is no internet.
	It waits until there is internet before it refreshes its content.
* IMSA website moved to https://clubhub.studco.org
* george.moe/clubhub replaced with a project description page with download links.

**Changes to the Club Hub Event Registrator:**

* New fields for entry of email contact, group tags, and poster display options.


CLUB HUB 2.0.0 CHANGELOG
==============================

**Changes to the Club Hub website:**

* Now under the george.moe domain.
* Entirely revamped layout, featuring a table of event details.
* New CSS focusing on a minimalistic style.
* New large and attractive button that opens the event registration page.
* Now able to display events without requiring a poster. The poster is displayed alongside event details and is enlargeable by clicking on it.
* Sorting allows the table to be organized by different properties.
* Filtering allows parts of the table to be hidden in order to bring focus to selected properties.
* Significantly cleaned up the code.
* Fixed a bug that caused high resource consumption.

**Changes to the Club Hub Event Registrator:**

* Poster is no longer required.
* New CSS to match the main website's aesthetic.
* New time, location, and general location inputs for added event details.
* More efficient administration backend.
* Increased storage efficiency by detecting whether an image has been uploaded.

**Changes to the Club Hub RemindMe! Service:**

* New CSS to match the main website's aesthetic.
* Improved email format.
* Fixed a bug where non-existent images in the email would appear as broken links.
* Fixed a bug where IDs were being stored as numbers rather than strings.
