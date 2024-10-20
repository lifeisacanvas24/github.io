+++
    title = "Comprehensive GitHub Workflow Guide"
    description = "A detailed guide covering essential GitHub workflows, including repository setup, SSH access, and best practices."
    date = "2024-10-20"
    author = "[Lifeisacanvas24]"
    draft = false
    updated = "2024-10-20T13:03:29.033161"
    reading_time = "N/A"
    social_image = ""
    tags = ["GitHub", "workflow", "Git", "version control", "repository"]
    categories = ["technology", "None"]
    
    [extra]
    og_title = "Comprehensive GitHub Workflow Guide"
    og_description = "A detailed guide covering essential GitHub workflows, including repository setup, SSH access, and best practices."
    og_image = ""
    og_url = "http://lifeisacanvas24.github.io/blog/technology//comprehensive-github-workflow-guide/"
    og_type = "article"

    [json_ld]
    type = "BlogPosting"
    context = "https://schema.org"
    itemprop = [
        { name = "Comprehensive GitHub Workflow Guide" },
        { description = "A detailed guide covering essential GitHub workflows, including repository setup, SSH access, and best practices." },
        { url = "http://lifeisacanvas24.github.io/blog/technology//comprehensive-github-workflow-guide/" },
        { author = "Lifeisacanvas24" },
        { datePublished = "2024-10-20" }
    ]
    +++
    
# Comprehensive GitHub Workflow Guide

## Table of Contents
1. [Setting up a repository on GitHub](#1-setting-up-a-repository-on-github)
2. [Setting up SSH access](#2-setting-up-ssh-access)
3. [Cloning and setting up the local repository](#3-cloning-and-setting-up-the-local-repository)
4. [Working with branches](#4-working-with-branches)
5. [Managing Pull Requests](#5-managing-pull-requests)
6. [Managing conflicts and diffs](#6-managing-conflicts-and-diffs)
7. [Keeping branches up to date](#7-keeping-branches-up-to-date)
8. [Removing and resyncing a branch](#8-removing-and-resyncing-a-branch)
9. [Best Practices and Advanced Techniques](#9-best-practices-and-advanced-techniques)
10. [Deep Dive: Git Stash and Git Rebase](#10-deep-dive-git-stash-and-git-rebase)
11. [Committing from an Existing Folder to GitHub](#11-committing-from-an-existing-folder-to-github)

## 1. Setting up a repository on GitHub

1. Log in to your GitHub account
2. Click the "+" icon in the top right corner and select "New repository"
3. Fill in the repository name and description
4. Choose public or private
5. Select "Initialize this repository with a README"
6. Click "Create repository"

## 2. Setting up SSH access

1. Check for existing SSH keys:
   ```bash
   ls -al ~/.ssh
   ```

2. Generate a new SSH key (if needed):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
   or for custom keyname you could use
   ```bash
   ssh-keygen -t ed25519 -C "agriyain2k@gmail.com" -f ~/.ssh/<keyname>
   ```

3. Start the SSH agent:
   ```bash
   eval "$(ssh-agent -s)"
   ```

4. Add your SSH key to the agent:
   ```bash
   ssh-add ~/.ssh/id_ed25519
   ```
   or for custom keyname you could use
   ```bash
   ssh-add ~/.ssh/<keyname>
   ```

5. Copy the SSH public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   or for custom keyname you could use
   ```bash
   cat ~/.ssh/<keyname>.pub
   ```

6. Add the SSH key to your GitHub account:
   - Go to GitHub Settings > SSH and GPG keys > New SSH key
   - Paste your key and save

7. Test your SSH connection:
   ```bash
   ssh -T git@github.com
   ```

## 3. Cloning and setting up the local repository

1. Clone the repository:
   ```bash
   git clone git@github.com:username/repository.git
   cd repository
   ```

2. Create multiple branches:
   ```bash
   git branch staging
   git branch dev
   ```

## 4. Working with branches

1. Switch to a branch:
   ```bash
   git checkout dev
   ```

2. Make changes and commit:
   ```bash
   # Make your changes
   git add .
   git commit -m "Your commit message"
   ```

3. Push changes to a specific branch:
   ```bash
   git push origin dev
   ```

## 5. Managing Pull Requests

1. Create a pull request:
   - Go to your repository on GitHub
   - Click "Pull requests" tab > "New pull request"
   - Select the base and compare branches
   - Add a title and description
   - Click "Create pull request"

2. Merge a pull request:
   - Review the changes
   - Click "Merge pull request" if everything looks good
   - Click "Confirm merge"

## 6. Managing conflicts and diffs

1. Resolve conflicts:
   - If GitHub indicates conflicts, click "Resolve conflicts"
   - Edit the file(s) to resolve conflicts manually
   - Mark the conflicts as resolved
   - Commit the changes

2. View diffs:
   - In a pull request, go to the "Files changed" tab
   - Or locally:
     ```bash
     git diff branch1..branch2
     ```

## 7. Keeping branches up to date

1. Update local master:
   ```bash
   git checkout master
   git pull origin master
   ```

2. Update feature branch:
   ```bash
   git checkout dev
   git merge master
   ```

## 8. Removing and resyncing a branch

1. Delete a branch locally:
   ```bash
   git branch -d branch-name
   ```

2. Delete a branch on GitHub:
   ```bash
   git push origin --delete branch-name
   ```

3. Resync a branch from scratch:
   ```bash
   git checkout master
   git pull origin master
   git checkout -b branch-name
   git push -u origin branch-name
   ```

## 9. Best Practices and Advanced Techniques

### 9.1 Always pull the latest changes before starting work

```bash
git checkout master
git pull origin master
git checkout your-feature-branch
git merge master
```

### 9.2 Create feature branches for new work

```bash
git checkout -b feature/new-feature-name
```

### 9.3 Keep commits atomic and write meaningful commit messages

```bash
git commit -m "Add user authentication feature

- Implement login functionality
- Add password hashing
- Create user session management"
```

### 9.4 Regularly merge master into your feature branch

```bash
git checkout master
git pull origin master
git checkout feature/your-feature
git merge master
```

### 9.5 Use pull requests for code review

1. Push your feature branch:
   ```bash
   git push -u origin feature/your-feature
   ```
2. Create a pull request on GitHub
3. Request reviews from team members
4. Address feedback and make necessary changes
5. Merge the pull request when approved

### 9.6 Delete feature branches after merging

Locally:
```bash
git branch -d feature/your-feature
```

On GitHub:
```bash
git push origin --delete feature/your-feature
```

### 9.7 Use meaningful branch names

```bash
git checkout -b feature/add-user-authentication
git checkout -b bugfix/fix-login-issue
git checkout -b refactor/optimize-database-queries
```

### 9.8 Commit often, perfect later, publish once

```bash
git add file1.js file2.js
git commit -m "Add initial structure for user profile"
git add file3.js
git commit -m "Implement profile picture upload"
```

### 9.9 Use git stash for temporary changes

```bash
git stash save "WIP: Experimenting with new feature"
git stash list
git stash apply stash@{0}
git stash drop stash@{0}
```

### 9.10 Use git rebase for a cleaner history

```bash
git checkout feature/your-feature
git rebase master
```

### 9.11 Skip certain files from being committed

1. Create or edit `.gitignore` file in your repository root:
   ```bash
   touch .gitignore
   ```

2. Add patterns to ignore:
   ```
   # Ignore all .log files
   *.log

   # Ignore the build directory
   /build/

   # Ignore a specific file
   config.ini

   # Ignore all files in a directory
   temp/*

   # But don't ignore this specific file
   !temp/important.txt
   ```

3. Commit the `.gitignore` file:
   ```bash
   git add .gitignore
   git commit -m "Add .gitignore file"
   ```

4. If you've already committed files that you now want to ignore:
   ```bash
   git rm --cached filename
   ```
   Then commit this change.

### 9.12 Use git aliases for common commands

Add to your `~/.gitconfig`:
```
[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    unstage = reset HEAD --
    last = log -1 HEAD
```

### 9.13 Use interactive rebase to clean up commits before pushing

```bash
git rebase -i HEAD~3  # Rebase the last 3 commits
```

### 9.14 Use git hooks for automated checks

1. Create a pre-commit hook:
   ```bash
   touch .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit
   ```

2. Edit the pre-commit hook to run tests or linters:
   ```bash
   #!/bin/sh
   npm run lint
   npm test
   ```

### 9.15 Use git blame to understand code history

```bash
git blame filename
```

### 9.16 Use git bisect to find bugs

```bash
git bisect start
git bisect bad  # Current version is bad
git bisect good <commit-hash>  # Last known good version
# Git will checkout different commits
# Test and mark as good or bad until the first bad commit is found
git bisect good
git bisect bad
# When done
git bisect reset
```

## 10. Deep Dive: Git Stash and Git Rebase

### 10.1 Git Stash

Git stash is a powerful feature that allows you to temporarily store modified, tracked files in order to clean your working directory without committing incomplete work.

#### Use Cases for Git Stash:

1. When you need to quickly switch branches but aren't ready to commit your current work.
2. When you want to apply a stash to multiple branches.
3. When you need to put aside some experimental changes.

#### Common Git Stash Commands:

1. Stash your changes:
   ```bash
   git stash save "Your stash message"
   ```

2. List all stashes:
   ```bash
   git stash list
   ```

3. Apply the most recent stash and remove it from the stash list:
   ```bash
   git stash pop
   ```

4. Apply a specific stash without removing it:
   ```bash
   git stash apply stash@{n}
   ```

5. Create a new branch from a stash:
   ```bash
   git stash branch new-branch-name stash@{n}
   ```

6. Remove a specific stash:
   ```bash
   git stash drop stash@{n}
   ```

7. Clear all stashes:
   ```bash
   git stash clear
   ```

#### Example Workflow:

```bash
# You're working on a feature
git checkout feature-branch
# Make some changes...

# Suddenly, you need to fix a bug on master
git stash save "WIP: Feature XYZ"
git checkout master

# Fix the bug
git commit -am "Fix critical bug"

# Go back to your feature
git checkout feature-branch
git stash pop

# Continue working on your feature
```

### 10.2 Git Rebase

Git rebase is a way to integrate changes from one branch into another. It's an alternative to merging that can result in a cleaner, more linear project history.

#### Use Cases for Git Rebase:

1. Keeping a feature branch up-to-date with the latest changes from the main branch.
2. Cleaning up your local commit history before pushing to a shared repository.
3. Maintaining a linear project history.

#### Common Git Rebase Commands:

1. Basic rebase:
   ```bash
   git checkout feature-branch
   git rebase master
   ```

2. Interactive rebase (for editing, squashing, or reordering commits):
   ```bash
   git rebase -i HEAD~n  # n is the number of commits to go back
   ```

3. Continue a rebase after resolving conflicts:
   ```bash
   git rebase --continue
   ```

4. Abort a rebase:
   ```bash
   git rebase --abort
   ```

#### Example Workflow:

```bash
# Start a new feature
git checkout -b feature-branch
# Make some commits...

# Meanwhile, master has progressed
git checkout master
git pull

# Update your feature branch
git checkout feature-branch
git rebase master

# If there are conflicts, resolve them and then:
git add .
git rebase --continue

# Push your updated feature branch
git push --force-with-lease origin feature-branch
```

#### Interactive Rebase Example:

```bash
git rebase -i HEAD~3

# In the interactive editor, you'll see something like:
# pick f7f3f6d Change A
# pick 310154e Change B
# pick a5f4a0d Change C

# You can reorder these lines to reorder commits
# Change 'pick' to:
# 'r' or 'reword' to change the commit message
# 's' or 'squash' to combine the commit with the previous one
# 'f' or 'fixup' to combine the commit with the previous one and discard this commit's message
# 'd' or 'drop' to remove the commit
```

### Important Notes:

1. Rebasing rewrites commit history. Never rebase commits that have been pushed to a public repository unless you're absolutely sure no one has based work on them.

2. When using `git push --force-with-lease`, be cautious as it can overwrite remote changes. It's safer than `git push --force` as it checks if the remote branch has been updated.

3. Stashing is local to your machine. Stashes are not transferred to the remote repository when you push.

4. Always communicate with your team about your Git workflow, especially when using advanced features like rebase.

## 11. Committing from an Existing Folder to GitHub

If you have an existing folder with files that you want to commit to a new or existing GitHub repository, follow these steps:

### 11.1 Initialize a New Repository

1. Navigate to your existing folder:
   ```bash
   cd /path/to/your/folder
   ```

2. Initialize a new Git repository:
   ```bash
   git init
   ```

3. Add the files to the staging area:
   ```bash
   git add .
   ```

4. Commit your changes:
   ```bash
   git commit -m "Initial commit of existing folder"
   ```

### 11.2 Linking to a Remote Repository

1. Add the remote repository (replace `<username>` and `<repository>` with your actual GitHub username and repository name):
   ```bash
   git remote add origin git@github.com:<username>/<repository>.git
   ```

2. Push your changes to GitHub:
   ```bash
   git push -u origin master
   ```

### 11.3 If the Repository Already Exists on GitHub

If you have an existing GitHub repository and want to commit files from your local folder:

1. Clone the repository to a local folder (optional, if you don't want to work directly in the existing folder):
   ```bash
   git clone git@github.com:<username>/<repository>.git
   cd repository
   ```

2. Copy or move your existing files into this cloned repository folder.

3. Add, commit, and push your changes as shown above:
   ```bash
   git add .
   git commit -m "Add files from existing folder"
   git push origin master
   ```

### 11.4 Managing Future Changes

After committing from an existing folder, manage future changes by:

1. Creating a branch for new features:
   ```bash
   git checkout -b feature/new-feature
   ```

2. Making changes, adding, and committing:
   ```bash
   git add .
   git commit -m "Implement new feature"
   ```

3. Pushing to GitHub:
   ```bash
   git push origin feature/new-feature
   ```

4. Creating a pull request on GitHub to merge your changes into the main branch.

## Conclusion

This guide provides a comprehensive overview of GitHub workflows, including essential commands, best practices, and advanced techniques. Regularly updating your knowledge of Git and GitHub will enhance your development workflow, enabling effective collaboration and version control.

Feel free to refer back to this guide as needed, and happy coding!
