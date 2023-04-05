# Contributing

We welcome pull-requests.

For larger contributions, please open an issue describing your idea. It
may provide valuable discussion and feedback. It also prevents the unfortunate
case of two persons working on the same thing. There's no need to wait for any
approval.

!!! check "Development guidelines"
    * It-just-works - use good defaults that will work well for a first time user
    * Keep-it-simple - try to keep stuff beginner-friendly and don't go too
      deep into advanced topics

## Writing documentation

!!! tip inline end
    For simple changes you can straight-up just use the edit link available on
    every documentation page. It's the pen-icon to the right of the top
    heading. Write your changes, check the preview-tab everything looks as
    expected and submit as proposed changes.

Documentation is is written as markdown, processed using mkdocs ([docs](https://www.mkdocs.org/user-guide/writing-your-docs/#writing-your-docs)) and the Material theme ([docs](https://squidfunk.github.io/mkdocs-material/reference/)). The Material theme is not just styling, but provides additional syntax extensions.

To test your local changes while writing them and before making a pull-request,
start a local mkdocs server:
``` console
$ ~/IOTstack/scripts/development/mkdocs-serve.sh
```
And then open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in a browser.

## Creating a new service

In this section you can find information on how to contribute a service to IOTstack. We are generally very accepting of new services where they are useful. Keep in mind that if it is not IOTstack, selfhosted, or automation related we may not approve the PR.

Services will grow over time, we may split up the buildstack menu into subsections or create filters to make organising all the services we provide easier to find.

## Checks
* `service.yml` file is correct
* `build.py` file is correct
* Service allows for changing external WUI port from Build Stack's options menu if service uses a HTTP/S port
* Use a default password, or allow the user to generate a random password for the service for initial installation. If the service asks to setup an account this can be ignored.
* Ensure [Default Configs](../Basic_setup/Default-Configs.md) is updated as required. A helper script (default_ports_md_generator.sh) exists to simplify this. 
* Must detect port conflicts with other services on [BuildStack](Menu-System.md) Menu.
* `Pre` and `Post` hooks work with no errors. 
* Does not require user to edit config files in order to get the service running.
* Ensure that your service can be backed up and restored without errors or data loss.
* Any configs that are required before getting the service running should be configured in the service's options menu (and a BuildStack menu Issue should be displayed if not).
* Fork the repo and push the changes to your fork. Create a cross repo PR for the mods to review. We may request additional changes from you.

## Commit message

```
service_name: Add/Fix/Change feature or bug summary

Optional longer description of the commit. What is changed and why it
is changed. Wrap at 72 characters.

* You can use markdown formating as this will automatically be the
  description of your pull-request.
* End by adding any issues this commit fixes, one per line:

Fixes #1234
Fixes #4567
```

1.  The first line is a short description. Keep it short, aim for 50
    characters. This is like the subject of an email. It shouldn't try to fully
    or uniquely describe what the commit does. More importantly it should aim
    to inform *why* this commit was made.

    `service_name` - service or project-part being changed, e.g. influxdb,
    grafana, docs. Documentation changes should use the the name of the
    service. Use `docs` if it's changes to general documentation. If all else
    fails, use the folder-name of the file you are changing. Use lowercase.

    `Add/Fix/Change` - what type of an change this commit is. Capitalized.

    `feature or bug summary` - free very short text giving an idea of why/what.

2. Empty line.

3.  A longer description of what and why. Wrapped to 72 characters.

    Use [github issue linking](
    https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue)
    to automatically close issues when the pull-request of this commit is
    merged.

For tips on how to use git, see [Git Setup](Git-Setup.md).

## Follow up
If your new service is approved and merged then congratulations! Please watch the Issues page on github over the next few days and weeks to see if any users have questions or issues with your new service.

Links:

* [Default configs](../Basic_setup/Default-Configs.md)
* [Password configuration for Services](BuildStack-RandomPassword.md)
* [Build Stack Menu System](Menu-System.md)
* [Coding a new service](BuildStack-Services.md)
* [IOTstack issues](https://github.com/SensorsIot/IOTstack/issues)
