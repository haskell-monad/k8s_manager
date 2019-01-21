#!/bin/sh

#git filter-branch -f --commit-filter '
#        if [ "$GIT_AUTHOR_EMAIL" = "mengyu.li@ikang.com" ];
#        then
#                GIT_AUTHOR_NAME="limengyu1990";
#                GIT_AUTHOR_EMAIL="limengyu1990@163.com";
#                git commit-tree "$@";
#        else
#                git commit-tree "$@";
#        fi' HEAD


git filter-branch -f --commit-filter '
        if [ "$GIT_COMMITTER_EMAIL" = "mengyu.li@ikang.com" ];
        then
                GIT_COMMITTER_NAME="limengyu1990";
                GIT_COMMITTER_EMAIL="limengyu1990@163.com";
                git commit-tree "$@";
        else
                git commit-tree "$@";
        fi' HEAD

#git filter-branch --commit-filter '
#OLD_EMAIL="mengyu.li@ikang.com"
#CORRECT_NAME="limengyu1990"
#CORRECT_EMAIL="limengyu1990@163.com"
#if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
#then
#    export GIT_COMMITTER_NAME="$CORRECT_NAME"
#    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
#fi' ref..HEAD

