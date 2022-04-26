How to setup and use git for IOTstack development.

1. First, create a
   [fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) of
   SensorsIot/IOTstack on github. And
   [setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
   your ssh-keys.
1. Clone your fork and setup your github username and email
   ``` console
   $ git clone git@github.com:<username>/IOTstack.git
   $ cd IOTstack
   $ git config user.name <username>
   $ git config user.email <1234>+<username>@users.noreply.github.com
   ```
1. Add up the SensorsIot/IOTstack upstream
   ``` console
   $ git remote add upstream https://github.com/SensorsIot/IOTstack.git
   ```
1. Configure for ease of operation
   ``` console
   $ git config fetch.prune true
   $ git config remote.pushDefault origin
   $ git config --add remote.origin.fetch "^refs/heads/gh-pages"
   $ git config --add remote.upstream.fetch "^refs/heads/gh-pages"
   $ git config branch.master.mergeoptions "--no-ff"
   $ git config fetch.parallel 0
   $ git fetch --all
   ```

## Make a pull-request

``` mermaid
flowchart LR
  upstream["upstream (SensorsIOT)"] -- "1. git fetch + git checkout -b"
    --> local[local branch]
  local -- "2. git commit" --> local
  local -- "3. git push" --> origin["origin (your fork)"]
  origin -- "3. create github pull-request" --> upstream
```

Please see [Contributing](index.md) for instructions on how to write commit
messages.

``` console
$ git fetch upstream
$ git checkout -b <your-descriptive-branch-name> upstream/master
...coding and testing...
$ git add <your new or changed file>
Check everything has been added:
$ git status
$ git commit
$ git push
```
When you execute git push, its output should have a link for creating the
pull-request to github.

## Common operations

### Show compact history with "git lg"

``` console
$ git config alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
```

### Remove branches of merged pull-requests.

When your pull-requests have been merged, their branches aren't needed anymore.
Remove them to reduce clutter and distractions. The master branch is never
deleted.

``` console
$ git fetch --all
$ git checkout master
$ git branch -r --merged upstream/master | \
    grep -v origin/master$ | grep origin | sed 's/origin\///' | \
    xargs -I 'B' git push --delete origin B
$ git branch --merged upstream/master | grep -v "  master$" | \
    xargs -I'B' git branch -d B
```

## Advanced topics

### Fetch all pull-requests as branches

This is handy for easily testing out other persons' suggested changes. The
branches are of course fetch-only, and you can't push your own commits to them.

``` console
$ git config --add remote.upstream.fetch +refs/pull/*/head:refs/remotes/upstream/pr-*
$ git fetch upstream
```

*Note:* Everything below requires this.

### Show up-to-date branches not merged

Branches that include the latest upstream/master, but are not merged to
your current branch, are potentially mergeable pull-requests. This is useful
for identifying which pull-requests you should be able to merge without
conflict.

``` console
$ git fetch upstream
$ git branch -r --contains upstream/master --no-merged upstream/master
```

### Check pull-requests on Github can be merged without conflicts

In git, the only way to know if a branch can be merged without a conflict, is
by actually doing the merge. An alias to (re-)create a branch named
`merge-test` and do merges into it:

``` console
$ git config alias.test-pull-request-merge $'!f() { : git merge && \
    OPENPULLS=$(curl -s \'https://api.github.com/repos/SensorsIot/IOTstack/pulls?base=master&per_page=100\' | \
        grep "^.....number" | sed -E \'s/.* ([0-9]+),/  upstream\\/pr-\\1/\') && \
    git fetch upstream && git checkout -B merge-test upstream/master && \
    git branch -r --contains upstream/master --no-merged upstream/master | \
    grep upstream/pr- | sort - <(echo "$OPENPULLS") | \
    { uniq -d; [[ "$1" ]] && echo "$1"; } | \
    xargs -I B sh -c "echo Merging B && \
        git merge --no-rerere-autoupdate --no-ff --quiet B || \
        { echo ***FAILED TO MERGE B && exit 255; };" ;}; f'
```

<!-- Old version using 'plain' commands
``` console
$ OPENPULLS=$(curl -s 'https://api.github.com/repos/SensorsIot/IOTstack/pulls?state=open&per_page=100' | \
    grep "^.....number" | sed -E 's/.* ([0-9]+),/  upstream\/pr-\1/')
$ git fetch upstream && git checkout -B merge-test upstream/master && \
    git branch -r --contains upstream/master --no-merged upstream/master | \
    grep upstream/pr- | sort - <(echo "$OPENPULLS") | uniq -d | \
    xargs -I B  sh -c "echo Merging B && \
        git merge --no-rerere-autoupdate --no-ff --quiet B || \
        ( echo ***FAILED TO MERGE B && exit 255 )"
```
-->


Then use this alias combined with `git checkout -`, returning your working copy
back to the original branch if all merges succeeded:

``` console
$ git test-pull-request-merge && git checkout -
```

This merges all branches that are: a) currently open pull requests and b)
up-to-date, i.e. contains upstream/master and c) not merged already and d) the
optional provided argument. Note: won't ignore draft pull-requests. If it
encounters a failure, it stops immediately to let you inspect the conflict.

!!! help "Failed merge?"

    *If* there was a merge-conflict, inspect it e.g. using `git diff`, but
    don't do any real work or conflict resolution in the merge-test branch.
    When you have understood the merge-conflict and want to leave the
    merge-test branch, abort the failed merge and switch to your actual branch:

    ``` console
    $ git diff
    $ git merge --abort
    $ git checkout <your-PR-branch-that-resulted-in-the-conflict>
    ```

### Check your branch doesn't conflict with any existing pull-request

When you intend to submit a pull-request you might want to check that it won't
conflict with any of the existing pull-requests.

1.  Commit all your changes into your pull request branch.
2.  Use the alias from the previous "Test all current pull-requests..."-topic
    to test merging your branch in addition to all current pull request:

    ``` console
    $ git test-pull-request-merge <your-pull-request-branch> && git checkout -
    ```

    If there is a merge-conflict, see "Failed merge?" above.
