# Steps in using GIT

# Git standards

## Branch Names

1. Always start with the reason for creations

   - bugfix
   - feature
   - refactor

2. Examples
   - feature/create-forum
   - feature/detection
   - bugfix/detection-fps
   - refactor/detection
   - refactor/create-forum

## Commit messages

Prefix must follow the following according to the code

```
build | ci | docs | feat | fix | perf | refactor | style | test | chore | revert | bump
```

Examples

```
feat: added fps counter to detection
```

```
fix: fps counter incorrect measurement time
```

```
docs: adjusted read.me
```

```
refactor: change naming of sending email function
```

# Creating new feature

1. `git clone <repo>` - clone repo if needed
2. `git checkout -b <feature/amazing-new-feature>`
3. Make changes
4. `git add -A`
5. `git commit -a`
6. `git push` - git push upstream may be needed
7. Once everything is ready to be updated on the repo
8. `git fetch` - get the latest repo info
9. `git checkout develop` - go into develop in case someone else has made a change
10. `git pull` - get the latest changes
11. `git merge develop` - always merge develop first
12. `git add -A`
13. `git commit -a`
14. `git push`

# Commonly used git commands

```git
git clone <repo name>               : Clone a repo
git fetch                           : Fetch information about any new branches
git pull                            : Pull the latest update from branch
git add -a                          : Add new files to git
git commit -A                       : Commit message
git switch <branch name>            : Switch to an existing branch
git checkout -b <new branch name>   : Create a new branch based on current branch
git merge <branch name>             : Merge current branch with another
```
